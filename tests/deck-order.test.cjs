const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ts = require('typescript');
const compiled = ts.transpileModule(fs.readFileSync(path.join(__dirname, '../src/utils/deckOrder.ts'), 'utf8'), { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2017 } }).outputText;
const exportsForTest = {};
new Function('exports', compiled)(exportsForTest);
const { autoSortDeck } = exportsForTest;
const card = (id, group, count, extra = {}) => ({ id, group_key: group, count, detail_name: id, image_url: '/test.png', character_name: 'ヒーロー', feature_value: 'ultra_hero', level: 1, ...extra });
const analysis = { 'ヒーロー': { '1': 20, '3': 1 } };
test('groups alternate artwork by total count, then sorts artworks by count', () => {
  const cards = [card('a1', 'A', 1), card('b', 'B', 3), card('a2', 'A', 3)];
  const before = JSON.stringify(cards);
  assert.deepEqual(autoSortDeck(cards, analysis).map(c => c.id), ['a2', 'a1', 'b']);
  assert.equal(JSON.stringify(cards), before);
});
test('equal totals preserve group order and equal artwork counts preserve artwork order', () => {
  const cards = [card('a1', 'A', 2), card('b', 'B', 4), card('a2', 'A', 2)];
  assert.deepEqual(autoSortDeck(cards, analysis).map(c => c.id), ['a1', 'a2', 'b']);
});
test('level order precedes group totals and cards without a group remain independent', () => {
  const cards = [card('single', undefined, 3), card('a1', 'A', 1), card('high', 'H', 1, {level: 3}), card('a2', 'A', 1)];
  assert.deepEqual(autoSortDeck(cards, analysis).map(c => c.id), ['high', 'single', 'a1', 'a2']);
});
test('scene groups stay together before boost groups', () => {
  const cards = [card('s1', 'scene:scene', 1, {feature_value:'scene'}), card('boost1', 'boost', 1, {feature_value:'boost'}), card('hero', 'hero', 1), card('s2', 'scene:scene', 2, {feature_value:'scene'}), card('boost2', 'boost', 3, {feature_value:'boost'})];
  assert.deepEqual(autoSortDeck(cards, analysis).map(c => c.id), ['hero', 's2', 's1', 'boost2', 'boost1']);
});
