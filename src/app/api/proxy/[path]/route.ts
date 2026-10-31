import { catalog, legacyDetails, readDeck, searchCards, saveV2Deck } from "@/server/cards-v2";
import { NextRequest, NextResponse } from "next/server";

const API_BASE_URL = process.env.API_BASE_URL as string;
const API_PUBLIC_KEY = process.env.API_PUBLIC_KEY as string;
const API_SECRET_KEY = process.env.API_SECRET_KEY as string;

export async function GET(req: NextRequest, { params }: { params: Promise<{ path: string }> }) {
  const searchParams = req.nextUrl.searchParams.toString();
  const path = (await params).path;
  try {
    const q = req.nextUrl.searchParams;
    if (path === "deck") return NextResponse.json({data:{rows:await readDeck(q.get('deck_code') || '')}});
    if (path === 'card_detail' && q.get('version') !== '2') return NextResponse.json({data:{rows:await legacyDetails((q.get('ids') || '').split(','))}});
    if (q.get('version') === '2') {
      if (path === 'character_options') {
        const unique = new Map<string, {feature_value: string; character_name: string}>();
        for (const card of await catalog()) {
          if (card.feature_value && card.character_name?.trim()) {
            unique.set(`${card.feature_value}:${card.character_name}`, {feature_value: card.feature_value, character_name: card.character_name});
          }
        }
        return NextResponse.json({data:{rows:[...unique.values()].sort((a,b) => a.character_name.localeCompare(b.character_name, 'ja'))}});
      }
      if (path === 'search' || path === 'search_count') return NextResponse.json({data:{rows:await searchCards(q, path === 'search_count')}});
      if (path === 'card_detail') {
        const ids = new Set((q.get('ids') || '').split(','));
        return NextResponse.json({data:{rows:(await catalog()).filter(c => ids.has(c.id))}});
      }
    }
  } catch { return NextResponse.json({error:'Unable to load cards or deck'}, {status:503}); }


  const response = await fetch(`${API_BASE_URL}/${path}?${searchParams}`, {
    method: "GET",
    headers: {
      Authorization: `Basic ${Buffer.from(`${API_PUBLIC_KEY}:${API_SECRET_KEY}`).toString("base64")}`,
    },
  });

  if (!response.ok) {
    return NextResponse.json({ error: "Failed to fetch data" }, { status: response.status });
  }

  const data = await response.json();
  return NextResponse.json(data);
}

export async function POST(req: NextRequest, { params }: { params: Promise<{ path: string }> }) {
  const body = await req.json();
  const path = (await params).path;
  if (path === 'new_deck') {
    try { return NextResponse.json({data:{rows:await saveV2Deck(body)}}); }
    catch { return NextResponse.json({error:'Deck could not be saved'}, {status:400}); }
  }


  const response = await fetch(`${API_BASE_URL}/${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Basic ${Buffer.from(`${API_PUBLIC_KEY}:${API_SECRET_KEY}`).toString("base64")}`,
    },
    body: JSON.stringify(body),
  });

  if (!response.ok) {
    return NextResponse.json({ error: "Failed to post data" }, { status: response.status });
  }

  const data = await response.json();
  return NextResponse.json(data);
}
