#!/usr/bin/env bash
set -euo pipefail

# SQL preparation only. This script never executes INSERT/UPDATE/ALTER statements.
SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
ENV_FILE="${ENV_FILE:-$SCRIPT_DIR/.env.local}"
if [[ "${1:-}" == "--help" || "${1:-}" == "-h" ]]; then
  cat <<'EOF'
Usage: ./import-cards-page.sh [gen-sql.py options]

Reads the current DB into carddata/.cache/existing-cards.jsonl, then generates SQL.
No DB writes. On the first run, use --plan-only to inspect artwork matches.
Cached listing/details are reused; --refresh-list explicitly checks for new cards.
Examples:
  ./import-cards-page.sh --plan-only
  ./import-cards-page.sh --identity-map carddata/identity-map.json
  ./import-cards-page.sh --refresh-list --identity-map carddata/identity-map.json

The old page/promo positional arguments are no longer supported: checking every
listing page avoids missing new artwork added between already-imported cards.
See carddata/README.md for migration/application steps.
EOF
  exit 0
fi
if [[ ! -f "$ENV_FILE" ]]; then
  echo "env file not found: $ENV_FILE" >&2
  exit 1
fi
set -a
source "$ENV_FILE"
set +a
for var_name in TIDB_HOST TIDB_PORT TIDB_USER TIDB_PASSWORD TIDB_DATABASE; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "missing required env var: $var_name" >&2
    exit 1
  fi
done
cache_dir="$SCRIPT_DIR/carddata/.cache"
mkdir -p "$cache_dir"
snapshot=$(mktemp "$cache_dir/existing-cards.XXXXXX")
trap 'rm -f -- "$snapshot"' EXIT
mysql_base_cmd=(mysql --host "$TIDB_HOST" --port "$TIDB_PORT" --user "$TIDB_USER"
  --ssl-ca "${TIDB_SSL_CA:-/etc/ssl/certs/ca-certificates.crt}"
  --ssl-mode "${TIDB_SSL_MODE:-VERIFY_IDENTITY}" --default-character-set=utf8mb4
  --batch --raw --skip-column-names "$TIDB_DATABASE")
# Schema check works both before and after the one-time migration.
has_source=$(MYSQL_PWD="$TIDB_PASSWORD" "${mysql_base_cmd[@]}" -e "
SELECT COUNT(*) FROM information_schema.columns
WHERE table_schema=DATABASE() AND table_name='cards' AND column_name='source_app_card_id';")
source_column="NULL"
if [[ "$has_source" == "1" ]]; then source_column="source_app_card_id"; fi
MYSQL_PWD="$TIDB_PASSWORD" "${mysql_base_cmd[@]}" -e "
SELECT JSON_OBJECT('id',id,'number',number,'branch',branch,'base_card_key',base_card_key,
 'image_url',image_url,'thumbnail_image_url',thumbnail_image_url,
 'source_app_card_id',$source_column) FROM cards;" > "$snapshot"
if [[ ! -s "$snapshot" ]]; then printf '[]\n' > "$snapshot"; fi
mv -- "$snapshot" "$cache_dir/existing-cards.jsonl"
python3 "$SCRIPT_DIR/carddata/gen-sql.py" --existing-cards "$cache_dir/existing-cards.jsonl" "$@"
