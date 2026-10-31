import { NextRequest, NextResponse } from 'next/server';
import { cardImage, cardThumbnail } from '@/server/card-images';
export const runtime = 'nodejs';
export async function GET(req: NextRequest) {
  const src = req.nextUrl.searchParams.get('src');
  const width = req.nextUrl.searchParams.get('width');
  if (!src || (width !== null && !['240','360'].includes(width))) return NextResponse.json({error:'Invalid image request'}, {status:400});
  try {
    const body = width ? await cardThumbnail(src, Number(width)) : await cardImage(src);
    const contentType = width ? 'image/webp' : body[0] === 0x89 ? 'image/png' : body[0] === 0xff ? 'image/jpeg' : body.toString('ascii',8,12) === 'WEBP' ? 'image/webp' : 'application/octet-stream';
    return new NextResponse(new Uint8Array(body), {headers:{'Content-Type':contentType, 'Cache-Control':'public, max-age=604800', 'X-Content-Type-Options':'nosniff'}});
  } catch { return NextResponse.json({error:'Unable to load image'}, {status:502}); }
}
