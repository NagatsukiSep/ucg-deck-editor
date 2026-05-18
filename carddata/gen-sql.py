import argparse
import json
import os
import re
import sys
import time
import requests


# # JSONデータの読み込み
# with open("carddata/data.json", "r", encoding="utf-8") as f:
#     data_json = f.read()

# # JSONデータをPythonの辞書に変換
# data = json.loads(data_json)

def parse_args():
    parser = argparse.ArgumentParser(description="Generate SQL files for UCG cards.")
    parser.add_argument("--page", type=int, required=True, help="Positive integer page number.")
    parser.add_argument(
        "--promo",
        action="store_true",
        help="Fetch promo cards only.",
    )
    parser.add_argument(
        "--output-dir",
        default="output",
        help="Directory to write generated SQL files into.",
    )
    parser.add_argument(
        "--chunk-size",
        type=int,
        default=100,
        help="Number of INSERT statements per output file.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Number of retries for the remote card API.",
    )
    parser.add_argument(
        "--retry-delay",
        type=float,
        default=2.0,
        help="Seconds to wait between retries.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="HTTP timeout in seconds for the remote card API.",
    )
    args = parser.parse_args()
    if args.page < 1:
        raise ValueError("page must be a positive integer.")
    return args


def fetch_cards(page, promo_only, retries, retry_delay, timeout):
    promo_query = "&card_bundle_id=1" if promo_only else ""
    url = f"https://api.ultraman-cardgame.com/api/v1/jp/cards?page={page}&per_page=100{promo_query}"

    last_error = None
    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, timeout=timeout)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as exc:
            last_error = exc
            if attempt == retries:
                break
            print(
                f"Request failed on attempt {attempt}/{retries}. Retrying in {retry_delay} seconds..."
            )
            time.sleep(retry_delay)

    raise RuntimeError(f"Failed to fetch cards after {retries} attempts: {last_error}")


BASE_CARD_NUMBER_PATTERN = re.compile(r"[A-Z]+\d{2}-[A-Z]?\d{3}|PR-\d{3}")


def extract_base_card_key(number):
    raw_number = (number or "").strip()
    if not raw_number:
        return ""

    matches = BASE_CARD_NUMBER_PATTERN.findall(raw_number)
    if matches:
        return matches[-1]

    return raw_number


# 特殊文字をエスケープする関数
def escape_sql(value):
    if value is None:
        return "NULL"
    return "'" + str(value).replace("'", "''") + "'"


# INSERT文を生成する関数
def generate_sql(data):
    inserts = []

    for card in data["data"]:
        # 安全に取得する関数
        def get_value(obj, key, default="NULL"):
            return escape_sql(obj[key]) if obj and obj.get(key) is not None else default

        # メインテーブル(cards)のINSERT文
        inserts.append(
            f"""
        INSERT IGNORE INTO cards (
            id, section, bundle_version, serial, branch, number, base_card_key,
            rarity_value, rarity_description, round, level, 
            type_value, type_description, feature_value, feature_description, 
            battle_power_1, battle_power_2, battle_power_3, battle_power_ex, 
            publication_year, display_card_bundle_names, detail_id,
            product_language_value, product_language_description, detail_name, 
            ruby, character_name, effect, flavor_text, participating_works, 
            participating_works_url, type_name, illustrator_name, 
            image_url, thumbnail_image_url
        ) VALUES (
            {card['id']},
            {escape_sql(card['section'])},
            {escape_sql(card['bundle_version'])},
            {escape_sql(card['serial'])},
            {escape_sql(card['branch'])},
            {escape_sql(card['number'])},
            {escape_sql(extract_base_card_key(card['number']))},
            {escape_sql(card['rarity']['value'])},
            {escape_sql(card['rarity']['description'])},
            {card['round'] if card['round'] is not None else "NULL"},
            {escape_sql(card['level']) if card['level'] else "NULL"},
            {get_value(card.get('type'), 'value')},
            {get_value(card.get('type'), 'description')},
            {escape_sql(card['feature']['value'])},
            {escape_sql(card['feature']['description'])},
            {card['battle_power_1'] if card['battle_power_1'] is not None else "NULL"},
            {card['battle_power_2'] if card['battle_power_2'] is not None else "NULL"},
            {card['battle_power_3'] if card['battle_power_3'] is not None else "NULL"},
            {card['battle_power_ex'] if card['battle_power_ex'] is not None else "NULL"},
            {card['publication_year'] if card['publication_year'] is not None else "NULL"},
            {escape_sql(json.dumps(card['display_card_bundle_names']))},
            {card['detail']['id']},
            {escape_sql(card['detail']['product_language']['value'])},
            {escape_sql(card['detail']['product_language']['description'])},
            {escape_sql(card['detail']['name'])},
            {escape_sql(card['detail']['ruby'])},
            {escape_sql(card['detail']['character_name'])},
            {escape_sql(card['detail']['effect'])},
            {escape_sql(card['detail']['flavor_text'])},
            {escape_sql(card['detail']['participating_works'])},
            {escape_sql(card['detail']['participating_works_url']) if card['detail']['participating_works_url'] else "NULL"},
            {escape_sql(card['detail']['type_name']) if card['detail']['type_name'] else "NULL"},
            {escape_sql(card['detail']['illustrator_name'])},
            {escape_sql(card['detail']['image_url'])},
            {escape_sql(card['detail']['thumbnail_image_url'])}
        );
        """
        )

    return inserts


# SQL分割してファイル出力
def split_and_save_sql(inserts, chunk_size=100, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(0, len(inserts), chunk_size):
        part_number = i // chunk_size + 1
        chunk = inserts[i : i + chunk_size]
        file_name = os.path.join(output_dir, f"insert_cards_part_{part_number}.sql")

        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk))

        print(f"File {file_name} created with {len(chunk)} statements.")


def main():
    args = parse_args()
    data = fetch_cards(
        page=args.page,
        promo_only=args.promo,
        retries=args.retries,
        retry_delay=args.retry_delay,
        timeout=args.timeout,
    )
    inserts = generate_sql(data)
    split_and_save_sql(inserts, chunk_size=args.chunk_size, output_dir=args.output_dir)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        raise SystemExit(1)
