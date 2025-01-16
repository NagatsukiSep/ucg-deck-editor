import json
import os


# JSONデータの読み込み
with open("carddata/data.json", "r", encoding="utf-8") as f:
    data_json = f.read()

# JSONデータをPythonの辞書に変換
data = json.loads(data_json)


# 特殊文字をエスケープする関数
def escape_sql(value):
    if value is None:
        return "NULL"
    return f"'{str(value).replace('\'', '\'\'')}'"  # シングルクォートを2つに置換


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
        INSERT INTO cards (
            id, section, bundle_version, serial, branch, number, 
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
def split_and_save_sql(inserts, chunk_size=50, output_dir="output"):
    os.makedirs(output_dir, exist_ok=True)

    for i in range(0, len(inserts), chunk_size):
        part_number = i // chunk_size + 1
        chunk = inserts[i : i + chunk_size]
        file_name = os.path.join(output_dir, f"insert_cards_part_{part_number}.sql")

        with open(file_name, "w", encoding="utf-8") as f:
            f.write("\n".join(chunk))

        print(f"File {file_name} created with {len(chunk)} statements.")


# メイン処理
inserts = generate_sql(data)
split_and_save_sql(inserts, chunk_size=50)
