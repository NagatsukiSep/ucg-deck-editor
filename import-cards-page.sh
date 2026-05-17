#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF'
Usage:
  ./import-cards-page.sh <page> [--promo]
  ./import-cards-page.sh <page> [y|n]

Arguments:
  <page>  Positive integer page number for carddata/gen-sql.py
  [--promo]  Optional flag. Imports promo cards when present.
  [y|n]      Legacy optional promo flag. "y" imports promo cards, "n" imports normal cards.

Environment:
  Reads TiDB connection settings from .env.local in the repository root.
EOF
}

SCRIPT_DIR=$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)
REPO_ROOT="$SCRIPT_DIR"
ENV_FILE="${ENV_FILE:-$REPO_ROOT/.env.local}"

PAGE="${1:-}"
PROMO="n"

if [[ "$PAGE" == "-h" || "$PAGE" == "--help" ]]; then
  usage
  exit 0
fi

if [[ -z "$PAGE" || ! "$PAGE" =~ ^[0-9]+$ || "$PAGE" -lt 1 ]]; then
  echo "page must be a positive integer" >&2
  usage
  exit 1
fi

if [[ $# -ge 2 ]]; then
  case "${2:-}" in
    --promo)
      PROMO="y"
      ;;
    y|n)
      PROMO="$2"
      ;;
    *)
      echo "promo flag must be --promo, y, or n" >&2
      usage
      exit 1
      ;;
  esac
fi

if [[ ! -f "$ENV_FILE" ]]; then
  echo "env file not found: $ENV_FILE" >&2
  exit 1
fi

set -a
source "$ENV_FILE"
set +a

required_vars=(
  TIDB_HOST
  TIDB_PORT
  TIDB_USER
  TIDB_PASSWORD
  TIDB_DATABASE
)

for var_name in "${required_vars[@]}"; do
  if [[ -z "${!var_name:-}" ]]; then
    echo "missing required env var: $var_name" >&2
    exit 1
  fi
done

TIDB_SSL_CA="${TIDB_SSL_CA:-/etc/ssl/certs/ca-certificates.crt}"
TIDB_SSL_MODE="${TIDB_SSL_MODE:-VERIFY_IDENTITY}"
GEN_SQL_MAX_RETRIES="${GEN_SQL_MAX_RETRIES:-3}"
GEN_SQL_RETRY_DELAY="${GEN_SQL_RETRY_DELAY:-2}"

mysql_base_cmd=(
  mysql
  --host "$TIDB_HOST"
  --port "$TIDB_PORT"
  --user "$TIDB_USER"
  --ssl-ca "$TIDB_SSL_CA"
  --ssl-mode "$TIDB_SSL_MODE"
  --default-character-set=utf8mb4
  "$TIDB_DATABASE"
)

run_count_query() {
  MYSQL_PWD="$TIDB_PASSWORD" "${mysql_base_cmd[@]}" -Nse "SELECT COUNT(*) FROM cards;"
}

before_count=$(run_count_query)

tmp_dir=$(mktemp -d)
trap 'rm -rf "$tmp_dir"' EXIT

echo "Generating SQL for page=$PAGE promo=$PROMO"
gen_sql_cmd=(
  python3
  "$REPO_ROOT/carddata/gen-sql.py"
  --page "$PAGE"
  --output-dir "$tmp_dir/output"
  --chunk-size 100
  --retries "$GEN_SQL_MAX_RETRIES"
  --retry-delay "$GEN_SQL_RETRY_DELAY"
)

if [[ "$PROMO" == "y" ]]; then
  gen_sql_cmd+=(--promo)
fi

if ! "${gen_sql_cmd[@]}"; then
  echo "SQL generation failed" >&2
  exit 1
fi

shopt -s nullglob
sql_files=("$tmp_dir"/output/insert_cards_part_*.sql)
shopt -u nullglob

if [[ "${#sql_files[@]}" -eq 0 ]]; then
  echo "no generated SQL files found in $tmp_dir/output" >&2
  exit 1
fi

for sql_file in "${sql_files[@]}"; do
  echo "Importing $(basename "$sql_file")"
  MYSQL_PWD="$TIDB_PASSWORD" "${mysql_base_cmd[@]}" < "$sql_file"
done

after_count=$(run_count_query)
inserted_count=$((after_count - before_count))

echo "Done"
echo "cards before:   $before_count"
echo "cards after:    $after_count"
echo "cards inserted: $inserted_count"
