import { NextRequest, NextResponse } from "next/server";
import { hasValidOrigin } from "@/lib/admin-csrf";
import { executeTiDB, queryTiDB } from "@/lib/tidb";
import { extractBaseCardKey } from "@/utils/deckCardIdentity";

type NullableString = string | null;
type NullableNumber = number | null;

interface CardApiCard {
  id: number;
  section: string;
  bundle_version: string;
  serial: string;
  branch: string;
  number: string;
  rarity: {
    value: string;
    description: string;
  };
  round: NullableNumber;
  level: NullableString;
  type: {
    value: string;
    description: string;
  } | null;
  feature: {
    value: string;
    description: string;
  };
  battle_power_1: NullableNumber;
  battle_power_2: NullableNumber;
  battle_power_3: NullableNumber;
  battle_power_ex: NullableNumber;
  publication_year: NullableNumber;
  display_card_bundle_names: unknown;
  detail: {
    id: number;
    product_language: {
      value: string;
      description: string;
    };
    name: string;
    ruby: string;
    character_name: string;
    effect: string;
    flavor_text: string;
    participating_works: string;
    participating_works_url: NullableString;
    type_name: NullableString;
    illustrator_name: string;
    image_url: string;
    thumbnail_image_url: string;
  };
}

interface CardsApiResponse {
  data: CardApiCard[];
}

async function fetchCards(page: number, promoOnly: boolean): Promise<CardApiCard[]> {
  const searchParams = new URLSearchParams({
    page: String(page),
    per_page: "100",
  });

  if (promoOnly) {
    searchParams.set("card_bundle_id", "1");
  }

  const response = await fetch(
    `https://api.ultraman-cardgame.com/api/v1/jp/cards?${searchParams.toString()}`,
    { cache: "no-store" }
  );

  if (!response.ok) {
    throw new Error(`Card API request failed with status ${response.status}`);
  }

  const json = (await response.json()) as CardsApiResponse;
  return json.data;
}

async function fetchCardsCount(): Promise<number> {
  const rows = await queryTiDB<Array<{ count: number | string }>>(
    "SELECT COUNT(*) AS count FROM cards"
  );
  const count = rows[0]?.count;
  return typeof count === "string" ? Number(count) : (count ?? 0);
}

const INSERT_CARD_SQL = `
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
    ?, ?, ?, ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?, ?, ?,
    ?, ?, ?,
    ?, ?, ?,
    ?, ?, ?, ?, ?,
    ?, ?, ?,
    ?, ?
  )
`;

function buildInsertParams(card: CardApiCard) {
  return [
    card.id,
    card.section,
    card.bundle_version,
    card.serial,
    card.branch,
    card.number,
    extractBaseCardKey(card.number),
    card.rarity.value,
    card.rarity.description,
    card.round,
    card.level,
    card.type?.value ?? null,
    card.type?.description ?? null,
    card.feature.value,
    card.feature.description,
    card.battle_power_1,
    card.battle_power_2,
    card.battle_power_3,
    card.battle_power_ex,
    card.publication_year,
    JSON.stringify(card.display_card_bundle_names),
    card.detail.id,
    card.detail.product_language.value,
    card.detail.product_language.description,
    card.detail.name,
    card.detail.ruby,
    card.detail.character_name,
    card.detail.effect,
    card.detail.flavor_text,
    card.detail.participating_works,
    card.detail.participating_works_url,
    card.detail.type_name,
    card.detail.illustrator_name,
    card.detail.image_url,
    card.detail.thumbnail_image_url,
  ];
}

async function insertCard(card: CardApiCard) {
  await executeTiDB(INSERT_CARD_SQL, buildInsertParams(card));
}

export async function POST(req: NextRequest) {
  try {
    if (!hasValidOrigin(req)) {
      return NextResponse.json({ error: "Invalid origin" }, { status: 403 });
    }

    const body = (await req.json().catch(() => ({}))) as { page?: number; promo?: boolean };
    const page = body.page;
    const promoOnly = body.promo === true;

    if (!Number.isInteger(page) || (page as number) < 1) {
      return NextResponse.json({ error: "page must be a positive integer" }, { status: 400 });
    }

    const cards = await fetchCards(page as number, promoOnly);
    const beforeCount = await fetchCardsCount();

    for (const card of cards) {
      await insertCard(card);
    }

    const afterCount = await fetchCardsCount();

    return NextResponse.json({
      ok: true,
      page,
      promoOnly,
      fetched: cards.length,
      attemptedInserts: cards.length,
      beforeCount,
      afterCount,
    });
  } catch (error) {
    const message = error instanceof Error ? error.message : "Unknown error";
    console.error("Failed to import cards:", error);
    return NextResponse.json({ error: message }, { status: 500 });
  }
}
