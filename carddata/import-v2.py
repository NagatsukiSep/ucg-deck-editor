#!/usr/bin/env python3
"""Import the cached official catalog without legacy identity matching."""
import argparse
import importlib.util
import json
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('catalog', ROOT / 'gen-sql.py')
catalog = importlib.util.module_from_spec(spec)
spec.loader.exec_module(catalog)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--offline', action='store_true')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    client = catalog.Client(ROOT / '.cache', offline=args.offline)
    cards = client.listing()['cards']
    rows = []
    for index, card in enumerate(cards, 1):
        detail = client.detail(card)
        rows.append((card, detail))
        if index % 50 == 0:
            print(f'Validated {index}/{len(cards)}', flush=True)
    sql = ['CREATE TABLE IF NOT EXISTS cards_v2 (id BIGINT PRIMARY KEY, management_number VARCHAR(100) NOT NULL, code VARCHAR(100) NOT NULL, name VARCHAR(255) NOT NULL, listing JSON NOT NULL, detail JSON NOT NULL);', 'START TRANSACTION;']
    for card, detail in rows:
        values = [card['id'], card['managementNumber'], card['code'], detail['name'], json.dumps(card, ensure_ascii=False), json.dumps(detail, ensure_ascii=False)]
        sql.append('INSERT INTO cards_v2 (id,management_number,code,name,listing,detail) VALUES (' + ','.join(catalog.sql(v) for v in values) + ') ON DUPLICATE KEY UPDATE management_number=VALUES(management_number),code=VALUES(code),name=VALUES(name),listing=VALUES(listing),detail=VALUES(detail);')
    sql.extend(['COMMIT;', 'SELECT COUNT(*) AS cards_v2_count FROM cards_v2;'])
    output = ROOT / '.cache' / 'cards-v2.sql'
    output.write_text('\n'.join(sql), encoding='utf-8')
    print(f'Prepared {len(rows)} artworks; API calls: {client.calls}', flush=True)
    if args.apply:
        subprocess.run(['bash', '-c', '''set -euo pipefail
set -a
source .env.local
set +a
export MYSQL_PWD="$TIDB_PASSWORD"
exec mysql --host "$TIDB_HOST" --port "$TIDB_PORT" --user "$TIDB_USER" --ssl-ca "${TIDB_SSL_CA:-/etc/ssl/certs/ca-certificates.crt}" --ssl-mode VERIFY_IDENTITY --default-character-set=utf8mb4 "$TIDB_DATABASE"
'''], cwd=ROOT.parent, input=output.read_bytes(), check=True)

if __name__ == '__main__':
    main()
