"""Generate reviewable SQL from the ULTRA LEAGUE API, fetching only proven new details.

See carddata/README.md. No database writes are performed by this program.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import sys
import time
from urllib.request import Request, urlopen

BASE_URL = "https://app-admin.ultraman-cardgame.com"
CACHE_VERSION = 1
CODE_RE = re.compile(r"[A-Z]+[0-9]*-(?:[A-Z]?[0-9]{3}|SEC)")
RARITIES = dict(zip(
    ["C", "U", "R", "RR", "RRR", "RRRR", "ExP", "AP", "SP", "SSSP", "UR"],
    ["900_c", "800_u", "600_r", "500_rr", "400_rrr", "390_rrrr", "370_exp", "350_ap", "300_sp", "200_sssp", "100_ur"]))
FEATURES = {"ウルトラヒーロー": "ultra_hero", "ウルトラメカ": "ultra_mech", "ウルトラ怪獣": "kaiju", "シーン": "scene"}
TYPES = {"基本": "basic", "剛力": "power", "武装": "armed", "敏速": "speed", "災禍": "disaster", "壊滅": "devastation", "侵略": "invasion", "メテオ": "meteo"}


def compact(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def canonical(params):
    def stringify(value):
        if isinstance(value, (dict, list)):
            return compact(value)
        if value is None:
            return "null"
        if isinstance(value, bool):
            return "true" if value else "false"
        return str(value)
    return compact({key: stringify(params[key]) for key in sorted(params)})


def signature(params, nonce, timestamp, key):
    message = canonical(params) + str(nonce) + str(timestamp) + key
    # Flutter's cpE/cpC keeps only the low byte of each UTF-16 code unit.
    units = message.encode("utf-16-le", errors="surrogatepass")
    return hashlib.md5(units[::2]).hexdigest()


def read_json(file):
    return json.loads(Path(file).read_text(encoding="utf-8-sig"))


def write_json(file, value):
    file = Path(file)
    file.parent.mkdir(parents=True, exist_ok=True)
    temporary = file.with_suffix(file.suffix + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    temporary.replace(file)


def load_existing(file):
    text = Path(file).read_text(encoding="utf-8-sig").strip()
    if not text:
        raise ValueError("Empty DB snapshot. Use [] explicitly for an empty database.")
    value = json.loads(text) if text.startswith("[") else [json.loads(line) for line in text.splitlines() if line.strip()]
    if not isinstance(value, list):
        raise ValueError("DB snapshot must be a JSON array or JSONL rows")
    ids = set()
    for row in value:
        if not isinstance(row.get("id"), int) or not isinstance(row.get("number"), str):
            raise ValueError("Each DB row requires integer id and string number")
        if row["id"] in ids:
            raise ValueError("Duplicate DB id")
        ids.add(row["id"])
    return value


class Client:
    def __init__(self, cache_dir, offline=False, timeout=30, interval=0.25):
        self.cache_dir = Path(cache_dir)
        self.offline = offline
        self.timeout = timeout
        self.interval = interval
        self.calls = {"query": 0, "get": 0}
        self.last_request = 0
        self.key = None

    def signing_key(self):
        if self.key is not None:
            return self.key
        key_file = self.cache_dir / "signing-key.txt"
        self.key = os.environ.get("UCG_API_SIGNING_KEY")
        if not self.key and key_file.exists():
            self.key = key_file.read_text(encoding="utf-8").strip()
        if not self.key:
            if self.offline:
                raise ValueError("Signing key unavailable in offline mode")
            with urlopen("https://app.ultraman-cardgame.com/main.dart.js", timeout=self.timeout) as response:
                script = response.read().decode("utf-8")
            start = script.find("u={")
            constants = script[start:script.find(";", start)]
            match = re.search(r'(?:^|,)n:("(?:\\.|[^"\\])*")', constants)
            if start < 0 or not match:
                raise ValueError("App signing format changed. Set UCG_API_SIGNING_KEY after review.")
            self.key = json.loads(match.group(1))
            key_file.parent.mkdir(parents=True, exist_ok=True)
            key_file.write_text(self.key, encoding="utf-8")
        return self.key

    def request(self, method, endpoint, params):
        if self.offline:
            raise ValueError("Network disabled (--offline); cache is incomplete")
        from urllib.parse import urlencode
        key = self.signing_key()
        time.sleep(max(0, self.interval - (time.monotonic() - self.last_request)))
        timestamp = str(int(time.time() * 1000))
        nonce = str(secrets.randbelow(1000000))
        headers = {"content-type": "application/json;Charset=UTF-8", "api-access-token": "", "l": "ja_JP", "tid": "1", "v": "1.1", "timestamp": timestamp, "nonce": nonce, "signature": signature(params, nonce, timestamp, key)}
        url = BASE_URL + endpoint
        data = None
        if method == "POST":
            data = compact(params).encode("utf-8")
        else:
            url += "?" + urlencode(params)
        self.calls["query" if endpoint.endswith("/query") else "get"] += 1
        self.last_request = time.monotonic()
        # No automatic retries: a timeout might have reached the server already.
        with urlopen(Request(url, data=data, headers=headers, method=method), timeout=self.timeout) as response:
            result = json.load(response)
        if result.get("code") != 0 or result.get("data") is None:
            raise ValueError("Card API error: {} {}".format(result.get("code"), result.get("message")))
        return result["data"]

    def listing(self, refresh=False):
        file = self.cache_dir / "listing.json"
        if file.exists() and not refresh:
            snapshot = read_json(file)
            validate_listing(snapshot["cards"], snapshot["total"])
            return snapshot
        if self.offline:
            raise ValueError("Listing cache missing; --offline cannot refresh")
        cards = []
        page = 1
        total = None
        while True:
            result = self.request("POST", "/toc-api/v1/app/card/query", {
                "pageNum": page, "pageSize": 100, "keyword": "", "code": "",
                "commodityIdList": [], "feature": "", "type": "", "rarity": ""})
            if result.get("pageNum") != page or result.get("pageSize") != 100:
                raise ValueError("Unexpected API pagination")
            if total is not None and total != result.get("total"):
                raise ValueError("Catalog changed while paging. No details fetched; refresh again.")
            total = result.get("total")
            batch = result.get("list")
            if not isinstance(batch, list):
                raise ValueError("Unexpected listing response")
            cards.extend(batch)
            if not result.get("hasNextPage"):
                break
            if not batch:
                raise ValueError("Empty intermediate page")
            page += 1
        validate_listing(cards, total)
        snapshot = {"version": CACHE_VERSION, "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "total": total, "cards": cards}
        write_json(file, snapshot)
        return snapshot

    def detail(self, card):
        file = self.cache_dir / "details" / (str(card["id"]) + ".json")
        if file.exists():
            value = read_json(file)
        else:
            value = self.request("GET", "/toc-api/v1/app/card/get", {"id": card["id"]})
            validate_detail(card, value)
            write_json(file, value)  # Save immediately, even if a later card fails.
        validate_detail(card, value)
        return value


def validate_listing(cards, total):
    if not isinstance(cards, list) or len(cards) != total:
        raise ValueError("Incomplete listing cache")
    ids = set()
    for card in cards:
        if not isinstance(card.get("id"), int) or not card.get("code") or not card.get("managementNumber"):
            raise ValueError("Listing requires id, code and managementNumber")
        if card["id"] in ids:
            raise ValueError("Duplicate listing ID; catalog may have moved while paging")
        ids.add(card["id"])


def validate_detail(card, detail):
    if detail.get("id") != card["id"] or detail.get("code") != card["code"] or not detail.get("name"):
        raise ValueError("Detail/cache identity mismatch for {}".format(card["id"]))


def legacy_keys(row):
    # Only literal management-number equality is used automatically.
    # Historic parallel/promo numbering is resolved by image equality or a reviewed map.
    return {row["number"]}


def build_plan(cards, existing, overrides):
    by_id = {row["id"]: row for row in existing}
    sources = {}
    keys = {}
    codes = {}
    images = {}
    for row in existing:
        if row.get("source_app_card_id") is not None:
            source_id = int(row["source_app_card_id"])
            if source_id in sources:
                raise ValueError("Duplicate source_app_card_id in DB snapshot")
            sources[source_id] = row
        for key in legacy_keys(row):
            keys.setdefault(key, []).append(row)
        for code in CODE_RE.findall(row["number"]) + ([row["base_card_key"]] if row.get("base_card_key") else []):
            codes.setdefault(code, {})[row["id"]] = row
        for field in ["image_url", "thumbnail_image_url"]:
            if row.get(field):
                images.setdefault(row[field], {})[row["id"]] = row
    result = {"existing": [], "new": [], "unresolved": []}
    used = set()
    for card in cards:
        source_id = card["id"]
        mapped = sources.get(source_id)
        explicit = str(source_id) in overrides
        if explicit:
            target = overrides[str(source_id)]
            if target is not None and (isinstance(target, bool) or not isinstance(target, int) or target not in by_id):
                raise ValueError("Identity map references a nonexistent DB id: {}".format(source_id))
            if mapped and target != mapped["id"]:
                raise ValueError("Identity map conflicts with saved source id")
            mapped = by_id.get(target)
        if mapped is None and not explicit:
            candidates = {r["id"]: r for r in keys.get(card["managementNumber"], [])}
            for field in ["imageUrl", "cdnImageUrl"]:
                candidates.update(images.get(card.get(field), {}))
            if len(candidates) == 1:
                mapped = next(iter(candidates.values()))
            elif len(candidates) > 1:
                result["unresolved"].append({"card": card, "candidates": list(candidates.values()), "reason": "multiple exact matches"})
                continue
        if mapped is not None:
            target_codes = CODE_RE.findall(mapped["number"])
            if card["code"] not in target_codes and card["code"] != mapped.get("base_card_key"):
                raise ValueError("Identity map card code does not match DB row")
            if mapped["id"] in used:
                raise ValueError("Two app cards map to the same DB row; resolve the identity map")
            if mapped.get("source_app_card_id") is not None and int(mapped["source_app_card_id"]) != source_id:
                raise ValueError("DB row already belongs to a different app card")
            used.add(mapped["id"])
            result["existing"].append({"card": card, "db_id": mapped["id"]})
        elif explicit or card["code"] not in codes:
            result["new"].append(card)
        else:
            result["unresolved"].append({"card": card, "candidates": list(codes[card["code"]].values()), "reason": "same card code; artwork identity unknown"})
    unknown = set(overrides) - {str(c["id"]) for c in cards}
    if unknown:
        raise ValueError("Identity map contains IDs absent from this catalog: " + ", ".join(sorted(unknown)))
    result["next_db_id"] = max(by_id, default=0) + 1
    if result["next_db_id"] + len(result["new"]) - 1 > 2147483647:
        raise ValueError("New DB ids exceed INT")
    return result


def sql(value):
    if value is None:
        return "NULL"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return str(value)
    # Hex literals are safe under both MySQL backslash escaping modes (including NUL/newlines).
    return "CONVERT(X'{}' USING utf8mb4)".format(str(value).encode("utf-8").hex())


def number_or_none(value):
    return int(value) if value is not None and re.fullmatch(r"[0-9]+", str(value)) else None


def build_row(card, detail, db_id):
    validate_detail(card, detail)
    code = card["code"]
    match = re.fullmatch(r"([A-Z]+)([0-9]*)-([A-Z]?[0-9]+|SEC)", code)
    if not match:
        raise ValueError("Unsupported card code: " + code)
    feature_text = detail.get("featureText")
    type_text = detail.get("typeText")
    rarity = detail.get("rarityText")
    if not feature_text or not rarity:
        raise ValueError("Missing feature/rarity description for {}".format(card["id"]))
    # Preserve new enum values without pretending that they use the old code system.
    feature = FEATURES.get(feature_text, "app_" + str(detail.get("feature")))
    image = detail.get("cdnImageUrl") or detail.get("imageUrl")
    if not image:
        raise ValueError("Missing card image")
    management = card["managementNumber"]
    number = code if management == code else "({}){}".format(management, code)
    if len(number) > 50 or len(management) > 100:
        raise ValueError("Card number exceeds schema length")
    row = dict(
        id=db_id, section=match[1], bundle_version=match[2], serial=match[3],
        branch=None if management == code else management, number=number, base_card_key=code,
        rarity_value=RARITIES.get(rarity, "app_" + str(detail.get("rarity"))), rarity_description=rarity,
        round=number_or_none(detail.get("level")) if feature == "scene" else None,
        level=None if feature == "scene" else detail.get("level"),
        type_value=TYPES.get(type_text, "app_" + str(detail.get("type"))) if type_text else None,
        type_description=type_text, feature_value=feature, feature_description=feature_text,
        battle_power_1=detail.get("singleVal"), battle_power_2=detail.get("doubleVal"),
        battle_power_3=detail.get("tripleVal"), battle_power_4=detail.get("quattroVal"),
        battle_power_ex=detail.get("extraVal"), publication_year=number_or_none(detail.get("yearOfBirth")),
        display_card_bundle_names=compact([p["name"] for p in detail.get("commodityList", [])]),
        detail_id=None, product_language_value="ja", product_language_description="日本語",
        detail_name=detail["name"], ruby=detail.get("pronounce"), character_name=detail.get("characterName"),
        effect=detail.get("effect"), flavor_text=detail.get("other"), participating_works=detail.get("filmography"),
        participating_works_url=None, type_name=detail.get("subtitle"), illustrator_name=detail.get("illustratorName"),
        image_url=image, thumbnail_image_url=image, source_app_card_id=card["id"],
        source_app_management_number=management, source_app_detail=compact({"listing": card, "detail": detail}))
    if row["branch"] and len(row["branch"]) > 30:
        raise ValueError("Management number exceeds branch column length")
    return row


def insert_sql(row):
    columns = ", ".join("\x60" + key + "\x60" for key in row)
    values = ", ".join(sql(value) for value in row.values())
    # Reapplying a generated file is harmless. Unexpected ID/unique collisions are errors.
    return "INSERT INTO cards ({}) SELECT {} FROM DUAL WHERE NOT EXISTS (SELECT 1 FROM cards WHERE source_app_card_id = {});".format(columns, values, row["source_app_card_id"])


def generate_sql(plan, client):
    statements = []
    for match in plan["existing"]:
        card = match["card"]
        statements.append("UPDATE cards SET source_app_card_id = {}, source_app_management_number = {} WHERE id = {} AND (source_app_card_id IS NULL OR source_app_card_id = {});".format(card["id"], sql(card["managementNumber"]), match["db_id"], card["id"]))
    for index, card in enumerate(sorted(plan["new"], key=lambda entry: entry["id"])):
        statements.append(insert_sql(build_row(card, client.detail(card), plan["next_db_id"] + index)))
    return statements


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--existing-cards", required=True, help="Fresh DB JSON/JSONL snapshot")
    parser.add_argument("--identity-map", help='JSON object: app id -> existing DB id, or null for verified new artwork')
    parser.add_argument("--cache-dir", default=str(Path(__file__).parent / ".cache"))
    parser.add_argument("--output-dir", default=str(Path(__file__).parent / "output" / "app"))
    parser.add_argument("--refresh-list", action="store_true", help="Explicitly fetch all listing pages again")
    parser.add_argument("--offline", action="store_true", help="Never use the network")
    parser.add_argument("--plan-only", action="store_true", help="Classify without fetching any details")
    parser.add_argument("--allow-unresolved", action="store_true", help="Import only confirmed cards; leave unresolved artwork untouched")
    parser.add_argument("--chunk-size", type=int, default=100)
    parser.add_argument("--timeout", type=float, default=30)
    parser.add_argument("--interval", type=float, default=0.25)
    args = parser.parse_args()
    if args.chunk_size < 1 or args.timeout <= 0 or args.interval < 0:
        parser.error("chunk-size/timeout must be positive and interval must be nonnegative")
    if args.offline and args.refresh_list:
        parser.error("--offline and --refresh-list are mutually exclusive")
    return args


def prepare(args):
    output = Path(args.output_dir)
    output.mkdir(parents=True, exist_ok=True)
    # Never leave an old ready-to-apply manifest behind after a failed generation.
    manifest = output / "manifest.json"
    if manifest.exists():
        manifest.unlink()
    existing = load_existing(args.existing_cards)
    overrides = read_json(args.identity_map) if args.identity_map else {}
    if not isinstance(overrides, dict):
        raise ValueError("identity-map must be a JSON object")
    client = Client(args.cache_dir, args.offline, args.timeout, args.interval)
    snapshot = client.listing(args.refresh_list)
    plan = build_plan(snapshot["cards"], existing, overrides)
    report = dict(plan, listing_fetched_at=snapshot.get("fetched_at"), total=snapshot["total"],
                  counts={key: len(plan[key]) for key in ["existing", "new", "unresolved"]}, requests=client.calls)
    write_json(output / "plan.json", report)
    print("Catalog: {}; existing: {}; new: {}; unresolved: {}".format(snapshot["total"], len(plan["existing"]), len(plan["new"]), len(plan["unresolved"])))
    if args.plan_only:
        return
    if plan["unresolved"] and not args.allow_unresolved:
        raise ValueError("Resolve plan.json using --identity-map first. No detail GETs were made.")
    statements = generate_sql(plan, client)
    prepared_rows = [build_row(card, client.detail(card), plan["next_db_id"] + index)
                     for index, card in enumerate(sorted(plan["new"], key=lambda entry: entry["id"]))]
    write_json(output / "prepared-rows.json", prepared_rows)
    names = []
    for start in range(0, len(statements), args.chunk_size):
        name = "insert_cards_part_{}.sql".format(start // args.chunk_size + 1)
        (output / name).write_text("SET NAMES utf8mb4;\n" + "\n".join(statements[start:start + args.chunk_size]) + "\n", encoding="utf-8")
        names.append(name)
    report["requests"] = client.calls
    write_json(output / "plan.json", report)
    write_json(manifest, {"files": names, "counts": report["counts"], "requests": client.calls,
                          "migration": "carddata/migrations/001-app-card-source.sql"})
    print("SQL ready: {}; requests: {}".format(output, client.calls))


def main():
    args = parse_args()
    lock = Path(args.cache_dir) / "import.lock"
    lock.parent.mkdir(parents=True, exist_ok=True)
    try:
        handle = lock.open("x")
    except FileExistsError:
        raise ValueError("Another import may be running. Check before removing import.lock.")
    try:
        with handle:
            handle.write(str(os.getpid()))
        prepare(args)
    finally:
        lock.unlink()


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        print("Error: {}".format(error), file=sys.stderr)
        sys.exit(1)
