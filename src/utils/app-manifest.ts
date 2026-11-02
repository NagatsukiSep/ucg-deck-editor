import type { MetadataRoute } from 'next';
import { Locale, translations } from '@/i18n';
export function appManifest(locale: Locale): MetadataRoute.Manifest {
  return {id:'/', name:'Ultra Deck Builder', short_name:'UDB', description:translations[locale]['meta.pwaDescription'], start_url:'/', scope:'/', display:'standalone', background_color:'#111827', theme_color:'#111827', lang:locale, icons:[{src:'/icon_origin.png',sizes:'512x512',type:'image/png'}]};
}
