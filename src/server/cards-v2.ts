import mysql, { RowDataPacket } from 'mysql2/promise';
import { randomBytes } from 'node:crypto';
import { CardDetail } from '@/types/deckCard';

const pool = mysql.createPool({ host: process.env.TIDB_HOST, port: Number(process.env.TIDB_PORT || 4000), user: process.env.TIDB_USER, password: process.env.TIDB_PASSWORD, database: process.env.TIDB_DATABASE, ssl: { rejectUnauthorized: true }, connectionLimit: 4 });
const features: Record<string, string> = { '1': 'ultra_hero', '2': 'kaiju', '3': 'scene', '4': 'ultra_mech', '5': 'boost' };
const types: Record<string, string> = { '1': 'basic', '2': 'power', '3': 'speed', '4': 'armed', '6': 'invasion', '7': 'disaster', '10': 'devastation', '11': 'meteo' };
const parse = (v: unknown) => typeof v === 'string' ? JSON.parse(v) : v;
export async function catalog(): Promise<CardDetail[]> {
  const [rows] = await pool.query<RowDataPacket[]>('SELECT id, code, name, listing, detail FROM cards_v2');
  const cards: CardDetail[] = rows.map(row => {
    const d = parse(row.detail), l = parse(row.listing);
    return { id: String(row.id), rarity: d.rarityText, management_number: l.managementNumber, detail_name: d.name, image_url: d.cdnImageUrl || d.imageUrl, thumbnail_image_url: d.imageUrl, level: d.level == null ? undefined : Number(d.level), character_name: d.characterName, feature_value: features[String(d.feature)], code: row.code, group_key: d.feature === '3' ? `scene:${d.name}` : `code:${row.code}`, limit_count: Number(l.limitCount ?? 4), card_data_version: 2, type_value: types[String(d.type)], effect: d.effect || '' };
  });
  const counts = new Map<string, number>();
  for (const card of cards) counts.set(card.group_key!, (counts.get(card.group_key!) || 0) + 1);
  return cards.map(card => ({...card, artwork_count: counts.get(card.group_key!)}));
}
export async function readDeck(code: string) {
  const [rows] = await pool.execute<RowDataPacket[]>('SELECT deck_cards, card_data_version FROM decks WHERE deck_code=?', [code]);
  return rows.map(r => ({ ...r, deck_cards: typeof r.deck_cards === 'string' ? r.deck_cards : JSON.stringify(r.deck_cards) }));
}
export async function searchCards(q: URLSearchParams, count: boolean) {
  let cards = await catalog();
  const filters = [['feature_value','feature_value'], ['character_name','character_name'], ['level','level'], ['round','level'], ['type','type_value']] as const;
  for (const [param, key] of filters) {
    const value = q.get(param);
    if (value && value !== 'none') cards = cards.filter(c => String(c[key]) === value);
  }
  const keyword = (q.get('keyword') || '').toLocaleLowerCase();
  cards = cards.filter(c => `${c.detail_name} ${c.code} ${c.effect}`.toLocaleLowerCase().includes(keyword));
  cards.sort((a,b) => (a.code || '').localeCompare(b.code || '') || Number(a.id)-Number(b.id));
  const groups = new Map<string, CardDetail[]>();
  for (const card of cards) {
    const key = card.group_key || card.id;
    const group = groups.get(key) || [];
    group.push(card);
    groups.set(key, group);
  }
  if (q.get('group') === '0') {
    const expanded = cards.map(c => ({...c, artworks: groups.get(c.group_key || c.id)}));
    if (count) return [{total_count: expanded.length}];
    const offset = Math.max(0, Number(q.get('offset')) || 0);
    return expanded.slice(offset, offset + Math.min(100, Math.max(1, Number(q.get('per_page')) || 20)));
  }
  const grouped = [...groups.values()].map(artworks => ({ ...artworks[0], artworks }));
  if (count) return [{ total_count: grouped.length }];
  const offset = Math.max(0, Number(q.get('offset')) || 0), limit = Math.min(100, Math.max(1, Number(q.get('per_page')) || 20));
  return grouped.slice(offset, offset + limit);
}
export async function saveV2Deck(body: { deck_cards?: string; card_data_version?: number }) {
  if (body.card_data_version !== 2) throw new Error('V2 required');
  const input = JSON.parse(body.deck_cards || 'null');
  if (!Array.isArray(input) || input.length > 50) throw new Error('Invalid deck');
  const all = new Map((await catalog()).map(c => [c.id, c]));
  const seen = new Set<string>(), groups = new Map<string, {count:number; limit:number}>();
  let total = 0;
  const cards = input.map((v: {id: unknown; count: number}) => {
    const id = String(v.id), card = all.get(id);
    if (!card || seen.has(id) || !Number.isInteger(v.count) || v.count < 1 || v.count > 50) throw new Error('Invalid card');
    seen.add(id); total += v.count;
    const key = card.group_key!, prev = groups.get(key);
    groups.set(key, {count: (prev?.count || 0) + v.count, limit: Math.min(prev?.limit ?? 50, card.limit_count ?? 4)});
    return {id, count:v.count};
  });
  if (total !== 50 || [...groups.values()].some(g => g.count > g.limit)) throw new Error('Invalid deck limits');
  const code = randomBytes(8).toString('hex');
  await pool.execute('INSERT INTO decks (deck_code,deck_cards,card_data_version) VALUES (?,?,2)', [code,JSON.stringify(cards)]);
  return [{deck_code:code}];
}

export async function legacyDetails(ids: string[]) {
  if (!ids.length || ids.length > 100 || ids.some(id => !/^\d+$/.test(id))) return [];
  const [rows] = await pool.execute<RowDataPacket[]>(`SELECT id, detail_name, image_url, thumbnail_image_url, level, character_name, feature_value, type_value FROM cards WHERE id IN (${ids.map(() => '?').join(',')})`, ids);
  return rows.map(r => ({ ...r, id: String(r.id) }));
}
