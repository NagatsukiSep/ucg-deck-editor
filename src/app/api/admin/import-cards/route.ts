import { NextRequest, NextResponse } from "next/server";
import { hasValidOrigin } from "@/lib/admin-csrf";

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

const API_BASE_URL = process.env.API_BASE_URL as string;
const API_PUBLIC_KEY = process.env.API_PUBLIC_KEY as string;
const API_SECRET_KEY = process.env.API_SECRET_KEY as string;

function createAuthHeader() {
  return `Basic ${Buffer.from(`${API_PUBLIC_KEY}:${API_SECRET_KEY}`).toString("base64")}`;
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
  const response = await fetch(`${API_BASE_URL}/cards_count`, {
    method: "GET",
    headers: {
      Authorization: createAuthHeader(),
    },
    cache: "no-store",
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`cards_count failed with status ${response.status}: ${body}`);
  }

  const json = (await response.json()) as
    | { data?: { rows?: Array<Record<string, unknown>> } }
    | Array<Record<string, unknown>>
    | Record<string, unknown>;

  const candidates: unknown[] = [];

  if (Array.isArray(json)) {
    candidates.push(json[0]);
  } else {
    candidates.push(json);
    const data =
      "data" in json && json.data && typeof json.data === "object"
        ? json.data
        : undefined;
    const rows = data && "rows" in data ? data.rows : undefined;
    if (Array.isArray(rows)) {
      candidates.push(rows[0]);
    }
  }

  for (const candidate of candidates) {
    if (!candidate || typeof candidate !== "object") {
      continue;
    }

    for (const key of ["count", "cards_count", "total_count", "COUNT(*)"]) {
      const value = (candidate as Record<string, unknown>)[key];
      if (typeof value === "number") {
        return value;
      }
      if (typeof value === "string" && value.trim() !== "" && !Number.isNaN(Number(value))) {
        return Number(value);
      }
    }
  }

  throw new Error("cards_count returned an unexpected response shape");
}

function buildInsertPayload(card: CardApiCard) {
  return {
    id: card.id,
    section: card.section,
    bundle_version: card.bundle_version,
    serial: card.serial,
    branch: card.branch,
    number: card.number,
    rarity_value: card.rarity.value,
    rarity_description: card.rarity.description,
    round: card.round,
    level: card.level,
    type_value: card.type?.value ?? null,
    type_description: card.type?.description ?? null,
    feature_value: card.feature.value,
    feature_description: card.feature.description,
    battle_power_1: card.battle_power_1,
    battle_power_2: card.battle_power_2,
    battle_power_3: card.battle_power_3,
    battle_power_ex: card.battle_power_ex,
    publication_year: card.publication_year,
    display_card_bundle_names: JSON.stringify(card.display_card_bundle_names),
    detail_id: card.detail.id,
    product_language_value: card.detail.product_language.value,
    product_language_description: card.detail.product_language.description,
    detail_name: card.detail.name,
    ruby: card.detail.ruby,
    character_name: card.detail.character_name,
    effect: card.detail.effect,
    flavor_text: card.detail.flavor_text,
    participating_works: card.detail.participating_works,
    participating_works_url: card.detail.participating_works_url,
    type_name: card.detail.type_name,
    illustrator_name: card.detail.illustrator_name,
    image_url: card.detail.image_url,
    thumbnail_image_url: card.detail.thumbnail_image_url,
  };
}

async function insertCard(card: CardApiCard) {
  const response = await fetch(`${API_BASE_URL}/insert_card`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: createAuthHeader(),
    },
    body: JSON.stringify(buildInsertPayload(card)),
    cache: "no-store",
  });

  if (!response.ok) {
    const body = await response.text();
    throw new Error(`insert_card failed with status ${response.status}: ${body}`);
  }
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
