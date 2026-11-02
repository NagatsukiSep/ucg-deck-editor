'use client';
import { useI18n } from '@/i18n/I18nProvider';
import { translations, TranslationKey } from '@/i18n';
import { useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAppContext } from '@/context/AppContext';
import { CardDetail } from '@/types/deckCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
export function OfficialDeckImport({onImport}:{onImport?:(cards:CardDetail[])=>void}) {
  const {t} = useI18n();
  const [code,setCode] = useState(''), [busy,setBusy] = useState(false), [error,setError] = useState('');
  const locked = useRef(false);
  const {setOriginalDeckCards} = useAppContext();
  const router = useRouter();
  return <form className="space-y-3" onSubmit={async event=>{
    event.preventDefault(); if (locked.current) return;
    locked.current=true; setBusy(true);setError('');
    try {
      const response=await fetch('/api/official-deck',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code}),signal:AbortSignal.timeout(35000)});
      const result=await response.json();
      if (!response.ok) { setError(result.errorKey && Object.prototype.hasOwnProperty.call(translations.ja,result.errorKey) ? t(result.errorKey as TranslationKey) : t('official.error.generic')); return; }
      if (onImport) onImport(result.cards); else {setOriginalDeckCards(result.cards);router.push('/new');}
    } catch(e) {setError(e instanceof Error && e.name==='TimeoutError' ? t("official.timeout") : t("official.error.generic"));}
    finally {locked.current=false;setBusy(false);}
  }}>
    <Label htmlFor="official-deck-code">{t("official.code")}</Label>
    <Input id="official-deck-code" value={code} onChange={e=>setCode(e.target.value)} placeholder={t("official.placeholder")} disabled={busy} autoCapitalize="none" autoCorrect="off" spellCheck={false} required className="text-base md:text-sm" />
    <Button type="submit" disabled={busy || !code.trim()} className="w-full">{busy ? t("official.loading") : t("official.create")}</Button>
    {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
  </form>;
}
