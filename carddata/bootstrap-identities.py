"""Build a first-import identity map using exact decoded image equality only.

Optional Pillow dependency. Never contacts app-admin.ultraman-cardgame.com.
Different/failed images remain unresolved; no perceptual guessing or 'new' inference.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import io
import json
from pathlib import Path
import sys
from urllib.parse import urlparse
from urllib.request import urlopen

# Allow the one-off verification environment to provide Pillow without project installs.
import os
if os.environ.get("UCG_PILLOW_PATH"):
    sys.path.insert(0, os.environ["UCG_PILLOW_PATH"])
from PIL import Image
from importlib.util import spec_from_file_location, module_from_spec
spec = spec_from_file_location("card_import", Path(__file__).with_name("gen-sql.py"))
importer = module_from_spec(spec)
spec.loader.exec_module(importer)
ALLOWED_HOSTS = {"api.ultraman-cardgame.com", "img.ultraman-cardgame.com", "tsuburaya-hk-prod.oss-accelerate.aliyuncs.com"}


def fingerprint(url, cache_dir):
    parsed = urlparse(url)
    if parsed.scheme != "https" or parsed.hostname not in ALLOWED_HOSTS:
        raise ValueError("Unsupported image host")
    cache_file = cache_dir / (hashlib.sha256(url.encode()).hexdigest() + ".json")
    if cache_file.exists():
        return importer.read_json(cache_file)["fingerprint"]
    with urlopen(url, timeout=20) as response:
        if urlparse(response.url).hostname not in ALLOWED_HOSTS:
            raise ValueError("Unsupported redirect")
        image = Image.open(io.BytesIO(response.read())).convert("RGBA")
    # A complete pixel hash, including dimensions. Compression/metadata differences
    # are ignored, while different artwork/printing is never merged approximately.
    digest = hashlib.sha256(str(image.size).encode() + image.tobytes()).hexdigest()
    importer.write_json(cache_file, {"url": url, "fingerprint": digest})
    return digest


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--existing-cards", required=True)
    parser.add_argument("--cache-dir", default=str(Path(__file__).parent / ".cache"))
    parser.add_argument("--identity-map", help="Existing verified map to extend")
    parser.add_argument("--output", required=True)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    if not 1 <= args.workers <= 8:
        parser.error("workers must be 1..8")
    cache_dir = Path(args.cache_dir)
    existing = importer.load_existing(args.existing_cards)
    cards = importer.read_json(cache_dir / "listing.json")["cards"]
    overrides = importer.read_json(args.identity_map) if args.identity_map else {}
    plan = importer.build_plan(cards, existing, overrides)
    urls = set()
    for item in plan["unresolved"]:
        urls.add(item["card"].get("cdnImageUrl") or item["card"]["imageUrl"])
        urls.update(row["image_url"] for row in item["candidates"] if row.get("image_url"))
    hashes, errors = {}, {}
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        pending = {pool.submit(fingerprint, url, cache_dir / "image-fingerprints"): url for url in sorted(urls)}
        for done, future in enumerate(as_completed(pending), 1):
            url = pending[future]
            try:
                hashes[url] = future.result()
            except Exception as error:
                errors[url] = str(error)
            if done % 100 == 0:
                print("Image checks: {}/{}".format(done, len(urls)), flush=True)
    proposed = {}
    for item in plan["unresolved"]:
        card = item["card"]
        digest = hashes.get(card.get("cdnImageUrl") or card["imageUrl"])
        matches = [row["id"] for row in item["candidates"] if digest is not None and hashes.get(row.get("image_url")) == digest]
        if len(matches) == 1:
            proposed[str(card["id"])] = matches[0]
    # Refuse to conflate two app entries with one old row, even for identical images.
    used = {entry["db_id"] for entry in plan["existing"]}
    repeated = {target for target in proposed.values() if list(proposed.values()).count(target) > 1}
    accepted = {key: target for key, target in proposed.items() if target not in used and target not in repeated}
    overrides.update(accepted)
    importer.build_plan(cards, existing, overrides)  # Validate map before saving.
    importer.write_json(args.output, overrides)
    importer.write_json(cache_dir / "identity-match-report.json", {"exact_image_matches": len(accepted), "errors": errors})
    print("Verified exact image matches: {}; failed images: {}".format(len(accepted), len(errors)))


if __name__ == "__main__":
    main()
