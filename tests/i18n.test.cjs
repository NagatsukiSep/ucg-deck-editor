const {test}=require('node:test');
const assert=require('node:assert/strict');
const fs=require('node:fs');
const path=require('node:path');
const dictionaries=Object.fromEntries(['ja','en','ko'].map(lang=>[lang,JSON.parse(fs.readFileSync(path.join(__dirname,`../src/i18n/translations/${lang}.json`),'utf8'))]));
test('all supported languages have identical keys and interpolation variables',()=>{
 for(const lang of ['en','ko']){
  assert.deepEqual(Object.keys(dictionaries[lang]).sort(),Object.keys(dictionaries.ja).sort());
  for(const [key,reference] of Object.entries(dictionaries.ja)){
   assert.equal(typeof dictionaries[lang][key],'string',`${lang}: ${key}`);
   assert(dictionaries[lang][key].trim(),`${lang}: empty ${key}`);
   const placeholders=text=>[...new Set([...text.matchAll(/\{(\w+)\}/g)].map(m=>m[1]))].sort();
   assert.deepEqual(placeholders(dictionaries[lang][key]),placeholders(reference),`${lang}: placeholders for ${key}`);
  }
 }
});
test('official deck API error keys have translations',()=>{
 for(const file of ['src/server/official-deck.ts','src/app/api/official-deck/route.ts']){
  const source=fs.readFileSync(path.join(__dirname,'..',file),'utf8');
  for(const [key] of source.matchAll(/official\.error\.[A-Za-z]+/g)) assert(Object.hasOwn(dictionaries.ja,key),`Missing API error translation: ${key}`);
 }
});
test('kaiju translations match regional sources or explicitly documented overrides',()=>{
 const source=JSON.parse(fs.readFileSync(path.join(__dirname,'../carddata/character-name-sources.json'),'utf8'));
 const options=fs.readFileSync(path.join(__dirname,'../src/types/cardElement.ts'),'utf8');
 const keys=[...options.matchAll(/labelKey: "(character\.kaiju\.[^"]+)"/g)].map(m=>m[1]);
 assert.equal(new Set(source.characters.map(c=>c.translation_key)).size,keys.length);
 for(const character of source.characters){
  assert(keys.includes(character.translation_key));
  assert.equal(dictionaries.ja[character.translation_key],character.japanese);
  for(const lang of ['en','ko']){
   const entry = character[lang];
   if (entry.displayName) {
    assert.equal(entry.status,'untranslated_in_official_data');
    assert(['verified_external','transliteration'].includes(entry.displayNameStatus));
    if (entry.displayNameStatus === 'verified_external') assert(entry.displayNameSource);
    else assert(entry.displayNameNote);
   }
   assert.equal(dictionaries[lang][character.translation_key],entry.displayName || entry.characterName);
   assert(character[lang].id && character[lang].code && character[lang].endpoint);
  }
 }
});
