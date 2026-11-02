# カード差分取り込み（新公式アプリAPI）

## 基本方針

- DBは読み取り、生成したSQLを確認してから適用する。生成処理はDBを書き換えない。
- 一覧は100件ずつ全ページ取得する。既存カードが途中に現れても終了しない。
- 一覧の全件数・重複IDを検証し、新規と確定したカードだけ詳細GETする。
- 詳細は成功ごとに保存する。再実行やSQL再生成では取得済み詳細を使う。
- 再実行は一覧も再利用する。新着確認のときだけ --refresh-list を指定する。
- --offline は通信を一切しない。 --plan-only は詳細を一切取得しない。
- --allow-unresolved は未判定の絵柄を保留し、確認済みの既存対応と新規カードだけを出力する。
- APIのタイムアウトを自動再試行しない（サーバーに届いていた可能性があるため）。再実行時は成功済みキャッシュを使う。
- 同じキャッシュでの同時実行をロックする。異常終了後は実行中プロセスがないことを確認してから .cache/import.lock を取り除く。

## 初回移行

旧DBの id と新APIの id は別物。例えば BP01-001 は旧DB id=16、新API id=99。
カード番号だけで判定すると絵違いを取りこぼすため、新APIのIDを source_app_card_id に保存する。
既存DBのIDは変えず、新規行は読み取った最大DB IDの次から採番する。新APIのID順に採番し、INTの上限を超える場合は中断する。
元APIにない detail_id は NULL。古いSQLと新しいSQLは混在適用しない。

1. bash import-cards-page.sh --plan-only

.env.local の TiDB 設定で現在のDBを読み取る。結果は carddata/output/app/plan.json。
既存 source_app_card_id、管理番号の完全一致、画像URLの完全一致で判定する。
同じカード番号があって絵柄が判別できないものは unresolved とし、詳細GET前に中断する。
DBにないカード番号は新規。途中の再録番号も検索対象として照合する。

2. 初回の絵柄対応表を作る（任意、Pillow が必要）。

    python3 -m pip install Pillow
    python3 carddata/bootstrap-identities.py \
      --existing-cards carddata/.cache/existing-cards.jsonl \
      --output carddata/identity-map.json

この処理は画像配信先の画像だけ取得し、app-admin のAPIは呼ばない。
画像は全画素・サイズが完全一致し、対応先が一意の場合のみ対応付ける。
似ている画像の推定はしない。判定失敗を新規とみなさない。画像のハッシュは保存して再利用する。

残る unresolved は plan.json の新旧画像を確認して対応表に追加する。
対応表は JSON オブジェクトで、新API ID（キー）→既存DB ID（数値）。
明確に未登録の絵柄だけ null にする。null は詳細GETが必要という意味で、未確認という意味ではない。
例: {"99": 16, "16266": null}。不存在ID・カード番号不整合・二重対応はエラー。

3. bash import-cards-page.sh --identity-map carddata/identity-map.json

通常は未解決が1件でもあれば詳細GETせず終了する。全件解決すると新規カードだけ取得しSQLを生成する。
確定分を先に取り込む場合は --allow-unresolved を付ける。未解決分は新規扱いにせず、plan.json に残す。
実行途中で失敗しても詳細キャッシュは残り、再実行時は未完了分だけを取得する。

4. DB管理ツールで以下を順に適用する。

- carddata/migrations/001-app-card-source.sql（初回1回だけ）
- carddata/output/app/manifest.json の files に列挙されたSQLのみ

古いSQLが残る可能性があるため、ワイルドカードで全SQLを適用しない。
失敗・計画のみ実行では古い manifest.json を削除し、適用可能な結果と誤認させない。
ALTER は自動適用しない。既に追加済みの環境では列とインデックスを確認する。
SQLは再適用可能。INSERT IGNORE で型・ID衝突を黙って無視しない。
文字列は UTF-8 の16進リテラルで出力し、MySQLのバックスラッシュ設定に依存しない。

## 通常の新着確認

    bash import-cards-page.sh --refresh-list --identity-map carddata/identity-map.json

毎回DBを読み直す。一度 source_app_card_id を保存した既存カードの詳細GETは0回。
一覧Pページ、新規N枚、取得済み新規詳細C枚なら app-admin へのリクエストは P + (N-C) 回。
新規の同番号別絵柄が判定できない場合は、再び対応表で null または既存IDを指定する。
旧データへの確実な対応がない場合は自動で新規扱いしない。
一覧取得中のカタログ変更は件数不一致・ID重複で検出するが、APIにスナップショット機能がないため、
件数を変えない同時入れ替えまでは保証できない。結果の fetched_at は plan.json に記録する。

DBのスナップショットを手元で用意する場合:

    python3 carddata/gen-sql.py --existing-cards existing.json --plan-only
    python3 carddata/gen-sql.py --existing-cards existing.json --offline --identity-map carddata/identity-map.json

入力はJSON配列または1行1オブジェクトのJSONL。id（整数）、number（文字列）が必須。
branch、base_card_key、image_url、thumbnail_image_url、source_app_card_id を含める。
空DBは [] と明示する。空ファイルは取りこぼし防止のためエラー。
キャッシュと出力には取得データが含まれ、gitignore 対象。identity-map.json は次回も使うため保存する。

## 保存する項目

- 既存のフラットな cards カラムに新APIの詳細を変換する。
- QUADは battle_power_4、元の新API IDは source_app_card_id。
- source_app_management_number に管理番号、source_app_detail に一覧・詳細の原文JSONを保存する。
- 新しい特徴・タイプ等は旧enum値に推測変換せず app_ 接頭辞の値と日本語説明を保存する。
  画面の検索候補などの対応は別途必要。
- 元APIにない項目は NULL。別項目から効果や名称を推測して補完しない。

新画像のAlibaba OSSホストは src/app/api/card-image/route.ts の許可リストに追加済み。
管理画面の取り込みAPIは旧API方式のままで、この新しい差分SQLワークフローとは別。
旧管理画面から新方式の取り込みを実行しないこと。

## 検証

    python3 carddata/test_gen_sql.py

判定の曖昧さ、絵違い、ID衝突、キャッシュ再利用、途中再開、ページング、SQL文字列を通信なしで検証する。

## メタデータ照合（DB更新なし）

`match-metadata.py` は保存済み詳細を使い、同じcode内でレアリティ・作者・フレーバー・商品を比較する。
作者・フレーバーの `-`、`（無し）`、`なし` 等は空欄として扱い、フレーバー内のダッシュ記号・連続数の差を揃える。
日本語の長音 `ー` やレアリティ、カード番号は変更しない。空欄の一致は肯定的根拠として数えず、別分類にする。
同じ旧IDに複数の新API IDが一致したものは候補の確定対象から除く。
既定の `--fetch-limit 0` ではAPI通信せず、照合結果と候補一覧だけを `carddata/output/` に出力する。

### Independent V2 catalog

`python3 carddata/import-v2.py --apply` reuses the cached listing and each
validated detail, fetching only missing details. Successful responses are saved
immediately. After all details validate, it writes `.cache/cards-v2.sql` and
upserts `cards_v2` over a TLS connection with certificate identity verification.
`--offline` disallows API calls; omit `--apply` to prepare SQL without DB writes.
Legacy cards and decks are never modified by this importer. The official id is
the artwork primary key; code is stored separately and is not unique. Full raw
listing and detail JSON preserve optional and future API fields.

Application routing and deck version migration must be implemented before
switching new deck creation to this table. Existing deck storage currently has
no version column; `decks` has historical rows while `deck` is empty.

V2 application support uses `mysql2` on the Next.js server with the existing
`TIDB_*` environment variables and verified TLS. Apply migration 003 once before
running the updated application. It defaults every historical deck to V1; new
saves explicitly write V2. The proxy reads deck metadata from `decks`, reads V1 card details from the preserved legacy `cards` table, and serves V2 search,
card details and saves directly from TiDB. Deployments need these environment
variables available to the server. No deployment has been performed locally.

Artwork ids stay independent. Copy limits aggregate by official code, or by name
for scene cards. Official listing limits (including zero, eight and fifty) are
checked both when editing and saving. V1 decks support viewing and image output
but cannot be copied into the V2 editor. Boost cards have their own search tab.

### Import published official decks

The home page and empty editor accept a published official deck code or the
`getPublishDetail?code=...` URL. `POST /api/official-deck` signs requests on the
server and joins official artwork ids against `cards_v2`. It never saves a deck
automatically. All five official card lists, including boost cards, are imported.
Missing local card ids reject the import rather than silently omitting cards.
Successful responses are cached for five minutes in `.cache/official-decks`;
concurrent requests for the same code share one upstream request.

Deployments may configure `UCG_API_SIGNING_KEY` as a server-only secret. Local
development can reuse `.cache/signing-key.txt`. If neither exists, the server
reads the signing constants from the official web application, following the
card importer, and caches the result. Concurrent discovery is deduplicated;
failed discovery waits one minute before retrying. Read-only filesystems use
the in-memory cache. An official application format change may require updating
the extractor or configuring the environment variable. Neither the key nor API signing
headers are returned to the browser. The official API host is fixed; pasted URLs
are used only to extract and validate the code.

### Verified character-name translations

`character-name-sources.json` records official regional card references for all
81 kaiju names currently in the Japanese catalog (checked 2026-11-01). English
labels come from the US card catalog (tenant 2, `en_US`); Korean labels come from
the Korean catalog (tenant 7, `ko_KR`). Cards are matched by their common card
number and labels use the regional detail's `characterName`, preserving spelling,
spacing and capitalization. This avoids relying on franchise names or inferred
transliterations that differ from the card game's own terminology. Raw responses
are cached under `.cache/regional` and are not committed. Translation tests check
that the dictionaries match the recorded official names.

English names were verified for all 81 entries. Korean names were verified for
78 entries; Emi, Gigantron and Destroyer remain Japanese in the official Korean
regional responses. These three are marked `untranslated_in_official_data` and
the original API labels are preserved in the source record. As of 2026-11-02,
the UI uses `에미` for Emi, verified in Bandai Namco Korea's official product
listing. For Gigantron and Destroyer it uses the user-approved transliterations
`자이간트론` and `디스트로이어`. These display overrides are explicitly recorded
as external-source verification or transliteration, not official card-game names.
