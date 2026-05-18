import { NextRequest, NextResponse } from "next/server";
import { queryTiDB } from "@/lib/tidb";
import { CardDetail } from "@/types/deckCard";
import { withBaseCardKey } from "@/utils/deckCardIdentity";

type CardVariantRow = {
  id: string;
  base_card_key: string | null;
  branch: string | null;
  number: string | null;
  rarity_description: string | null;
  detail_name: string;
  image_url: string;
  thumbnail_image_url: string | null;
  level: number | null;
  character_name: string | null;
  feature_value: string | null;
  type_value: "ultra_hero" | "kaiju" | "ultra_mech" | "scene" | null;
};

export async function GET(req: NextRequest) {
  const baseCardKey = req.nextUrl.searchParams.get("base_card_key")?.trim();
  if (!baseCardKey) {
    return NextResponse.json(
      { error: "base_card_key is required" },
      { status: 400 }
    );
  }

  try {
    const rows = await queryTiDB<CardVariantRow[]>(
      `
        SELECT
          CAST(id AS CHAR) AS id,
          base_card_key,
          branch,
          number,
          rarity_description,
          detail_name,
          image_url,
          thumbnail_image_url,
          CAST(level AS SIGNED) AS level,
          character_name,
          feature_value,
          type_value
        FROM cards
        WHERE base_card_key = ?
        ORDER BY
          CASE WHEN branch IS NULL OR TRIM(branch) = '' THEN 0 ELSE 1 END,
          number ASC,
          id ASC
      `,
      [baseCardKey]
    );

    const variants: CardDetail[] = rows.map((row) =>
      withBaseCardKey({
        id: row.id,
        base_card_key: row.base_card_key ?? undefined,
        branch: row.branch,
        number: row.number ?? undefined,
        rarity_description: row.rarity_description ?? undefined,
        detail_name: row.detail_name,
        image_url: row.image_url,
        thumbnail_image_url: row.thumbnail_image_url ?? undefined,
        level: row.level ?? undefined,
        character_name: row.character_name ?? undefined,
        feature_value: row.feature_value ?? undefined,
        type_value: row.type_value ?? undefined,
      })
    );

    return NextResponse.json(variants);
  } catch (error) {
    console.error("Failed to fetch card variants:", error);
    return NextResponse.json(
      { error: "Failed to fetch card variants" },
      { status: 500 }
    );
  }
}
