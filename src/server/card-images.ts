import axios from 'axios';
import { createHash } from 'node:crypto';
import { mkdir, readFile, writeFile, rename, stat } from 'node:fs/promises';
import path from 'node:path';
import sharp from 'sharp';

const hosts = new Set(['api.ultraman-cardgame.com', 'img.ultraman-cardgame.com', 'tsuburaya-hk-prod.oss-accelerate.aliyuncs.com']);
const directory = path.join(process.cwd(), '.next/cache/card-images');
const ttl = 7 * 24 * 60 * 60 * 1000;
const pending = new Map<string, Promise<Buffer>>();
const memory = new Map<string, Buffer>();
let memorySize = 0;
function remember(key: string, data: Buffer) {
  if (memory.has(key)) memorySize -= memory.get(key)!.length;
  memory.delete(key); memory.set(key, data); memorySize += data.length;
  while (memorySize > 64 * 1024 * 1024 && memory.size) {
    const oldest = memory.keys().next().value!;
    memorySize -= memory.get(oldest)!.length; memory.delete(oldest);
  }
}
async function cached(key: string, create: () => Promise<Buffer>): Promise<Buffer> {
  const inMemory = memory.get(key);
  if (inMemory) { memory.delete(key); memory.set(key, inMemory); return inMemory; }
  const running = pending.get(key);
  if (running) return running;
  const operation = (async () => {
    const filename = path.join(directory, createHash('sha256').update(key).digest('hex'));
    try { if (Date.now() - (await stat(filename)).mtimeMs < ttl) { const data = await readFile(filename); remember(key, data); return data; } } catch { /* Cache miss. */ }
    const data = await create();
    // Read-only deployment filesystems must not prevent image delivery.
    try { await mkdir(directory, {recursive:true}); const temp = `${filename}.${process.pid}.tmp`; await writeFile(temp, data); await rename(temp, filename); } catch { /* Memory caching remains available. */ }
    remember(key, data); return data;
  })();
  pending.set(key, operation);
  try { return await operation; } finally { pending.delete(key); }
}
export function cardImage(url: string): Promise<Buffer> {
  const parsed = new URL(url);
  if (parsed.protocol !== 'https:' || !hosts.has(parsed.hostname) || parsed.port || parsed.username || parsed.password) throw new Error('Unsupported image URL');
  return cached(`original:${url}`, async () => {
    const response = await axios.get(url, {responseType:'arraybuffer', timeout:15000, maxContentLength:12 * 1024 * 1024, maxRedirects:0});
    const data = Buffer.from(response.data);
    const metadata = await sharp(data, {limitInputPixels:25000000}).metadata();
    if (!metadata.width || !metadata.height) throw new Error('Invalid image');
    return data;
  });
}
export function cardThumbnail(url: string, width: number) {
  return cached(`thumb-v1:${width}:${url}`, async () => sharp(await cardImage(url), {limitInputPixels:25000000}).resize({width, withoutEnlargement:true}).webp({quality:78}).toBuffer());
}
