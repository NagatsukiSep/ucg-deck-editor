"""Read-only metadata matching for unresolved old/new artwork identities."""
import argparse
from collections import Counter
import importlib.util
from pathlib import Path
import re
import unicodedata

spec = importlib.util.spec_from_file_location("card_import", Path(__file__).with_name("gen-sql.py"))
imp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(imp)


def norm(value):
    return re.sub(r"\s+", "", unicodedata.normalize("NFKC", str(value or "")))


def text_key(value, field):
    """Normalize descriptive metadata only; codes and rarity keep their own rules."""
    value = norm(value)
    if value in {"", "-", "—", "―", "–", "─", "(無し)", "無し", "(なし)", "なし"}:
        return ""
    if field == "flavor":
        # Printing/export differences in dash glyphs and repeat lengths.
        # Preserve Japanese prolonged-sound marks (ー), ASCII hyphens and other punctuation.
        value = re.sub(r"[—―─–]+", "—", value)
    return value


def repair_product(value):
    return re.sub(r"\\?u([0-9a-fA-F]{4})", lambda m: chr(int(m[1], 16)), str(value))


def product_key(value):
    value = norm(repair_product(value))
    value = re.sub(r"【[^】]*】|\[[^\]]*\]", "", value)
    value = re.sub(r"^(?:ブースターパック|スターターデッキ|エクストラデッキ|エクストラブースター|パック)[0-9]*", "", value)
    return value


def products_equal(old, new):
    old_names = old.get("display_card_bundle_names") or []
    if isinstance(old_names, str):
        import json
        try:
            old_names = json.loads(old_names)
        except ValueError:
            return False
    if not isinstance(old_names, list):
        return False
    a = {product_key(name) for name in old_names} - {""}
    b = {product_key(item.get("name")) for item in new.get("commodityList", [])} - {""}
    # Require full set equality; extra/missing reprint products remain a separate category.
    return bool(a) and a == b


def compare(old, new):
    values = [
        ("rarity", old.get("rarity_description"), new.get("rarityText")),
        ("illustrator", old.get("illustrator_name"), new.get("illustratorName")),
        ("flavor", old.get("flavor_text"), new.get("other")),
    ]
    result = {}
    for key, a, b in values:
        normalize = norm if key == "rarity" else lambda value: text_key(value, key)
        a, b = normalize(a), normalize(b)
        result[key] = bool(a) and bool(b) and a == b
    result["products"] = products_equal(old, new)
    return result


def compatible_with_empty_fields(old, new):
    checks = compare(old, new)
    if not checks["rarity"] or not checks["products"]:
        return False
    return all(text_key(a, field) == text_key(b, field) for field, a, b in [
        ("illustrator", old.get("illustrator_name"), new.get("illustratorName")),
        ("flavor", old.get("flavor_text"), new.get("other")),
    ])


def analyze(plan, rows, client, fetch_limit=0):
    by_id = {row["id"]: row for row in rows}
    fetched = 0
    results = []
    for item in plan["unresolved"]:
        card = item["card"]
        candidates = [by_id[row["id"]] for row in item["candidates"] if by_id[row["id"]].get("source_app_card_id") is None]
        if not candidates:
            results.append({"card": card, "status": "no_unmapped_old_candidate", "candidates": []})
            continue
        file = client.cache_dir / "details" / (str(card["id"]) + ".json")
        if not file.exists() and fetched >= fetch_limit:
            results.append({"card": card, "status": "detail_not_fetched", "candidates": candidates})
            continue
        was_cached = file.exists()
        detail = client.detail(card)
        if not was_cached:
            fetched += 1
            if fetched % 25 == 0:
                print("New detail GETs: {}".format(fetched), flush=True)
        checks = [{"db_id": old["id"], "number": old["number"], "checks": compare(old, detail),
                   "rarity": old.get("rarity_description"), "illustrator": old.get("illustrator_name"),
                   "flavor": old.get("flavor_text"), "products": old.get("display_card_bundle_names"), "compatible_including_empty": compatible_with_empty_fields(old, detail)} for old in candidates]
        four = [match for match in checks if all(match["checks"].values())]
        three = [match for match in checks if all(match["checks"][key] for key in ["rarity", "illustrator", "flavor"])]
        compatible = [match for match in checks if match["compatible_including_empty"]]
        status = "four_fields_unique" if len(four) == 1 else "four_fields_multiple" if four else "three_fields_unique" if len(three) == 1 else "three_fields_multiple" if three else "no_three_field_match"
        if status == "no_three_field_match" and compatible:
            status = "empty_fields_unique" if len(compatible) == 1 else "empty_fields_multiple"
        result = {"card": card, "detail": detail, "status": status, "candidates": checks}
        if status == "empty_fields_unique":
            result["empty_compatible_db_id"] = compatible[0]["db_id"]
        if len(four) == 1:
            result["proposed_db_id"] = four[0]["db_id"]
        elif len(three) == 1:
            result["three_field_db_id"] = three[0]["db_id"]
        results.append(result)
    targets = Counter(row.get("proposed_db_id", row.get("empty_compatible_db_id")) for row in results if "proposed_db_id" in row or "empty_compatible_db_id" in row)
    for row in results:
        target = row.get("proposed_db_id", row.get("empty_compatible_db_id"))
        if target is not None and targets[target] > 1:
            row["status"] = "four_fields_target_conflict" if "proposed_db_id" in row else "empty_fields_target_conflict"
    return {"counts": dict(Counter(row["status"] for row in results)), "new_detail_gets": fetched,
            "results": results, "note": "Candidates only. No identity map or DB changes applied."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--existing-cards", required=True)
    parser.add_argument("--identity-map", required=True)
    parser.add_argument("--cache-dir", default=str(Path(__file__).parent / ".cache"))
    parser.add_argument("--fetch-limit", type=int, default=0, help="Maximum new detail GETs; default is cache-only")
    parser.add_argument("--output", default=str(Path(__file__).parent / "output/metadata-match.json"))
    args = parser.parse_args()
    if args.fetch_limit < 0:
        parser.error("fetch-limit must be nonnegative")
    rows = imp.load_existing(args.existing_cards)
    client = imp.Client(args.cache_dir, offline=args.fetch_limit == 0, interval=0.5)
    snapshot = client.listing()
    plan = imp.build_plan(snapshot["cards"], rows, imp.read_json(args.identity_map))
    report = analyze(plan, rows, client, args.fetch_limit)
    report["normalization"] = {"missing_text": ["-", "（無し）", "無し", "なし", "null", "empty"], "flavor_dashes": "—/―/─/– runs normalized to —", "rarity_and_codes": "unchanged"}
    report["requests"] = client.calls
    imp.write_json(args.output, report)
    candidates = []
    for row in report["results"]:
        if row["status"] not in {"four_fields_unique", "empty_fields_unique", "three_fields_unique"}:
            continue
        target = row.get("proposed_db_id", row.get("empty_compatible_db_id", row.get("three_field_db_id")))
        old = next(item for item in row["candidates"] if item["db_id"] == target)
        candidates.append({"status": row["status"], "source_id": row["card"]["id"],
                           "management_number": row["card"]["managementNumber"],
                           "code": row["card"]["code"], "name": row["detail"]["name"],
                           "db_id": target, "old_number": old["number"], "checks": old["checks"]})
    imp.write_json(Path(args.output).with_name("metadata-identity-candidates.json"),
                   {"counts": report["counts"], "candidates": candidates,
                    "note": "Review only; conflicting targets excluded; DB and identity map unchanged."})
    print(report["counts"], flush=True)
    print("Requests: {}".format(client.calls), flush=True)


if __name__ == "__main__":
    main()
