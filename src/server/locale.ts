import { cookies, headers } from 'next/headers';
import { isLocale, Locale } from '@/i18n';
export async function requestLocale(): Promise<Locale> {
  const selected = (await cookies()).get('udb-locale')?.value;
  if (isLocale(selected)) return selected;
  const language = (await headers()).get('accept-language')?.split(',')[0].toLowerCase() || 'ja';
  return language.startsWith('ko') ? 'ko' : language.startsWith('ja') ? 'ja' : 'en';
}
