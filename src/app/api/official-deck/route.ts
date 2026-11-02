import { NextRequest, NextResponse } from 'next/server';
import { importOfficialDeck, OfficialDeckError } from '@/server/official-deck';
export const runtime = 'nodejs';
export async function POST(req: NextRequest) {
  try {
    const body = await req.json();
    if (typeof body?.code !== 'string' || body.code.length > 1000) return NextResponse.json({errorKey:'official.error.input'}, {status:400});
    return NextResponse.json(await importOfficialDeck(body.code));
  } catch (error) {
    if (error instanceof OfficialDeckError) return NextResponse.json({errorKey:error.message}, {status:error.status});
    return NextResponse.json({errorKey:'official.error.generic'}, {status:502});
  }
}
