import { NextRequest, NextResponse } from 'next/server';
import { importOfficialDeck, OfficialDeckError } from '@/server/official-deck';
export const runtime = 'nodejs';
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    if (typeof body?.code !== 'string' || body.code.length > 1000) return NextResponse.json({error:'公式デッキコードを入力してください。'}, {status:400});
    return NextResponse.json(await importOfficialDeck(body.code));
  } catch (error) {
    if (error instanceof OfficialDeckError) return NextResponse.json({error:error.message}, {status:error.status});
    return NextResponse.json({error:'デッキを展開できませんでした。時間をおいて再試行してください。'}, {status:502});
  }
}
