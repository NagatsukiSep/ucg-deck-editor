'use client';
import { useRef, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useAppContext } from '@/context/AppContext';
import { CardDetail } from '@/types/deckCard';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Label } from '@/components/ui/label';
export function OfficialDeckImport({onImport}:{onImport?:(cards:CardDetail[])=>void}) {
  const [code,setCode] = useState(''), [busy,setBusy] = useState(false), [error,setError] = useState('');
  const locked = useRef(false);
  const {setOriginalDeckCards} = useAppContext();
  const router = useRouter();
  return <form className="space-y-3" onSubmit={async event=>{
    event.preventDefault(); if (locked.current) return;
    locked.current=true; setBusy(true);setError('');
    try {
      const response=await fetch('/api/official-deck',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({code}),signal:AbortSignal.timeout(20000)});
      const result=await response.json();
      if (!response.ok) throw new Error(result.error || 'デッキを展開できませんでした。');
      if (onImport) onImport(result.cards); else {setOriginalDeckCards(result.cards);router.push('/new');}
    } catch(e) {setError(e instanceof Error && e.name!=='TimeoutError' ? e.message : '取得に時間がかかっています。再試行してください。');}
    finally {locked.current=false;setBusy(false);}
  }}>
    <Label htmlFor="official-deck-code">公式デッキコード</Label>
    <Input id="official-deck-code" value={code} onChange={e=>setCode(e.target.value)} placeholder="公式コード、または公式デッキ取得URL" disabled={busy} autoCapitalize="none" autoCorrect="off" spellCheck={false} required className="text-base md:text-sm" />
    <Button type="submit" disabled={busy || !code.trim()} className="w-full">{busy ? '取得中…' : '公式デッキコードから作成'}</Button>
    {error && <p role="alert" className="text-sm text-red-700">{error}</p>}
  </form>;
}
