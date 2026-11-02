import { requestLocale } from '@/server/locale';
import { appManifest } from '@/utils/app-manifest';
export default async function manifest() { return appManifest(await requestLocale()); }
