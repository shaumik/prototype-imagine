import {readFile,readdir,access} from 'node:fs/promises';
import {spawnSync} from 'node:child_process';
import path from 'node:path';
const files=(await readdir('dist')).filter(f=>f.endsWith('.js'));
const html=await readFile('dist/index.html','utf8');
const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
for(const file of files){
 const name=path.join('dist',file),text=await readFile(name,'utf8');
 const result=spawnSync(process.execPath,['--check',name],{encoding:'utf8'});if(result.status!==0)throw Error(result.stderr);
 for(const [,ref] of text.matchAll(/from\s+['"](\.\/?[^'"]+)['"]/g))await access(path.resolve('dist',ref));
 for(const [,id] of text.matchAll(/\$\('([^']+)'\)/g))if(!ids.has(id))throw Error(`${file}: missing UI element ${id}`);
}
for(const asset of ['panorama','sprites','car-frame','combat','run-v2','jump-v2','blade-v2','modules','harbor'])await access(`dist/assets/${asset}.png`);
await access('dist/assets/backseat.jpg');await access('dist/style.css');
const manifest=JSON.parse(await readFile('.openai/hosting.json','utf8'));
if(manifest.static?.directory!=='dist'||!manifest.project_id)throw Error('Static hosting metadata is incomplete');
console.log(`Static build ready: ${files.length} modules, all image assets and UI bindings verified.`);
