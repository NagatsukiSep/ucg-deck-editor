import { readFile, mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const keyFile = path.join(process.cwd(), 'carddata/.cache/signing-key.txt');
let cachedKey: string | undefined;
let loading: Promise<string> | undefined;
let retryAfter = 0;

export function parseOfficialSigningKey(script: string): string {
  // The same constants table used by the offline card importer.
  const start = script.indexOf('u={');
  const end = script.indexOf(';', start);
  if (start < 0 || end < 0) throw new Error('Official signing format unavailable');
  const match = /(?:^|,)n:("(?:\\.|[^"\\])*")/.exec(script.slice(start, end));
  if (!match) throw new Error('Official signing format unavailable');
  const value: unknown = JSON.parse(match[1]);
  if (typeof value !== 'string' || !value.trim()) throw new Error('Official signing format unavailable');
  return value;
}

export async function officialSigningKey(): Promise<string> {
  const configured = process.env.UCG_API_SIGNING_KEY?.trim();
  if (configured) return configured;
  if (cachedKey) return cachedKey;
  if (loading) return loading;
  if (Date.now() < retryAfter) throw new Error('Official signing information temporarily unavailable');
  loading = (async () => {
    try {
      const local = (await readFile(keyFile, 'utf8')).trim();
      if (local) return local;
    } catch { /* New deployments have no local cache. */ }
    const response = await fetch('https://app.ultraman-cardgame.com/main.dart.js', {
      signal: AbortSignal.timeout(10000), cache: 'no-store'
    });
    if (!response.ok) throw new Error('Official signing information temporarily unavailable');
    const key = parseOfficialSigningKey(await response.text());
    try { await mkdir(path.dirname(keyFile), {recursive:true}); await writeFile(keyFile, key, {mode:0o600}); } catch { /* A read-only deployment can use the in-memory cache. */ }
    return key;
  })();
  try { cachedKey = await loading; return cachedKey; }
  catch { retryAfter = Date.now() + 60000; throw new Error('Official signing information temporarily unavailable'); }
  finally { loading = undefined; }
}
