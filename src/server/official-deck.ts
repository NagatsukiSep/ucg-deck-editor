import { createHash, randomInt } from 'node:crypto';
import { readFile, mkdir, writeFile, rename, stat } from 'node:fs/promises';
import path from 'node:path';
import { catalog } from './cards-v2';
import { officialSigningKey } from './official-signing-key';
const root = path.join(process.cwd(), 'carddata/.cache');
const inflight = new Map<string, Promise<unknown>>();
export class OfficialDeckError extends Error {
  constructor(message: string, public status = 502) { super(message); }
}
export function officialCode(input: string): string {
  let code = input.trim();
  if (code.startsWith('https://')) {
    const url = new URL(code);
    if (url.hostname !== 'app-admin.ultraman-cardgame.com' || url.pathname !== '/toc-api/v1/app/cardGroup/getPublishDetail') throw new OfficialDeckError('公式デッキコード、または公式デッキ取得URLを入力してください。', 400);
    code = url.searchParams.get('code') || '';
  }
  if (!/^[A-Za-z0-9_-]{8,100}$/.test(code)) throw new OfficialDeckError('公式デッキコードを確認してください。', 400);
  return code;
}
async function fetchDetail(code: string): Promise<unknown> {
  const cache = path.join(root, 'official-decks', `${code}.json`);
  try { if (Date.now() - (await stat(cache)).mtimeMs < 5 * 60 * 1000) return JSON.parse(await readFile(cache, 'utf8')); } catch { /* Cache miss. */ }
  let key: string;
  try { key = await officialSigningKey(); }
  catch { throw new OfficialDeckError('公式サービスの接続情報を取得できませんでした。時間をおいて再試行してください。', 503); }
  const timestamp = String(Date.now()), nonce = String(randomInt(1000000));
  // Match the official client's low-byte UTF-16 signature encoding.
  const utf16 = Buffer.from(JSON.stringify({code}) + nonce + timestamp + key, 'utf16le');
  const bytes = Buffer.alloc(utf16.length / 2);
  for (let i = 0; i < bytes.length; i++) bytes[i] = utf16[i * 2];
  const signature = createHash('md5').update(bytes).digest('hex');
  let response: Response;
  try {
    response = await fetch(`https://app-admin.ultraman-cardgame.com/toc-api/v1/app/cardGroup/getPublishDetail?${new URLSearchParams({code})}`, {
      headers:{'api-access-token':'', l:'ja_JP', tid:'1', v:'1.1', timestamp, nonce, signature}, signal:AbortSignal.timeout(15000), cache:'no-store'
    });
  } catch { throw new OfficialDeckError('公式サービスに接続できませんでした。時間をおいて再試行してください。'); }
  if (!response.ok) throw new OfficialDeckError('公式サービスからデッキを取得できませんでした。');
  const result = await response.json();
  if (result.code !== 0 || !result.data) throw new OfficialDeckError('デッキが存在しないか、非公開・削除済みです。コードを確認してください。',404);
  try { await mkdir(path.dirname(cache), {recursive:true}); const temp = `${cache}.${process.pid}.tmp`; await writeFile(temp, JSON.stringify(result.data)); await rename(temp,cache); } catch { /* Cache is optional. */ }
  return result.data;
}
export async function importOfficialDeck(input: string) {
  const code = officialCode(input);
  let pending = inflight.get(code);
  if (!pending) { pending = fetchDetail(code); inflight.set(code,pending); }
  let raw: unknown;
  try { raw = await pending; } finally { if (inflight.get(code) === pending) inflight.delete(code); }
  if (!raw || typeof raw !== 'object') throw new OfficialDeckError('公式デッキの形式を確認できませんでした。');
  const detail = raw as Record<string, unknown>;
  const quantities = new Map<string,number>();
  for (const key of ['superHeroList','superMonsterList','sceneList','superMachineList','speedUpCardList']) {
    const list = detail[key];
    if (list == null) continue;
    if (!Array.isArray(list)) throw new OfficialDeckError('公式デッキの形式を確認できませんでした。');
    for (const card of list) {
      if (!card || !Number.isSafeInteger(card.id) || !Number.isInteger(card.count) || card.count < 1 || card.count > 50) throw new OfficialDeckError('公式デッキのカード情報が不正です。');
      const id = String(card.id); quantities.set(id, (quantities.get(id) || 0) + card.count);
    }
  }
  const total = [...quantities.values()].reduce((a,b)=>a+b,0);
  if (total < 1 || total > 50) throw new OfficialDeckError('公式デッキのカード枚数を確認してください。',422);
  const all = new Map((await catalog()).map(card=>[card.id,card]));
  const missing = [...quantities.keys()].filter(id=>!all.has(id));
  if (missing.length) throw new OfficialDeckError('このデッキには未登録のカードが含まれています。カードデータの更新が必要です。',422);
  return {code, name:typeof detail.name === 'string' ? detail.name : '', cards:[...quantities].map(([id,count])=>({...all.get(id)!,count})), total};
}
