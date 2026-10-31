const { test } = require('node:test');
const assert = require('node:assert/strict');
const fs = require('node:fs');
const path = require('node:path');
const ts = require('typescript');
const compiled = ts.transpileModule(fs.readFileSync(path.join(__dirname, '../src/server/official-signing-key.ts'), 'utf8'), {compilerOptions:{module:ts.ModuleKind.CommonJS,target:ts.ScriptTarget.ES2017,esModuleInterop:true}}).outputText;
function load({env={},local='',script='var u={a:1,n:"test-value"};',failFetch=false}={}) {
  let calls=0;
  const exports={};
  const mockedFs={readFile:async()=>{if(local)return local;throw Error('missing')},mkdir:async()=>{},writeFile:async()=>{throw Error('read-only')}};
  new Function('exports','require','process','fetch',compiled)(exports, id=>id==='node:fs/promises'?mockedFs:require(id), {env,cwd:()=>'/test'}, async()=>{calls++;if(failFetch)throw Error('network');return {ok:true,text:async()=>script}});
  return {...exports,calls:()=>calls};
}
test('fresh read-only deployment discovers once for concurrent requests and reuses memory',async()=>{
 const m=load(); const values=await Promise.all([m.officialSigningKey(),m.officialSigningKey()]);assert.deepEqual(values,['test-value','test-value']);await m.officialSigningKey();assert.equal(m.calls(),1);
});
test('environment setting and existing cache avoid upstream requests',async()=>{
 for(const options of [{env:{UCG_API_SIGNING_KEY:' configured '},local:'local'},{local:'configured'}]){const m=load(options);assert.equal(await m.officialSigningKey(),'configured');assert.equal(m.calls(),0)}
});
test('invalid official script fails closed and repeated failure is throttled',async()=>{
 const m=load({script:'changed format'});await assert.rejects(m.officialSigningKey());await assert.rejects(m.officialSigningKey());assert.equal(m.calls(),1);
});
test('extractor supports escaped strings and rejects missing or empty constants',()=>{
 const m=load();assert.equal(m.parseOfficialSigningKey('var u={a:1,n:"a\\\"b"};'),'a"b');assert.throws(()=>m.parseOfficialSigningKey('var u={n:""};'));assert.throws(()=>m.parseOfficialSigningKey('other'));
});
