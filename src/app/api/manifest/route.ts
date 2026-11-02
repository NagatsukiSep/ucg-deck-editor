import { NextRequest, NextResponse } from 'next/server';
import { isLocale } from '@/i18n';
import { requestLocale } from '@/server/locale';
import { appManifest } from '@/utils/app-manifest';
export async function GET(req: NextRequest) {
  const requested = req.nextUrl.searchParams.get('lang');
  const locale = isLocale(requested) ? requested : await requestLocale();
  return NextResponse.json(appManifest(locale), {headers:{'Content-Type':'application/manifest+json','Cache-Control':'private, no-store'}});
}
