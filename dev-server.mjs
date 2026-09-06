import http from 'node:http';
import {readFile} from 'node:fs/promises';
import path from 'node:path';
const root=path.resolve('dist'),types={'.html':'text/html','.js':'text/javascript','.css':'text/css','.png':'image/png','.jpg':'image/jpeg','.mp4':'video/mp4'};
const portIndex=process.argv.indexOf('--port');
http.createServer(async(req,res)=>{try{const name=decodeURIComponent(new URL(req.url,'http://local').pathname),special={'/animation-review.html':'tests/animation-review.html','/qa-tools.js':'tests/qa-tools.js'},file=special[name]?path.resolve(special[name]):path.resolve(root,'.'+(name==='/'||name==='/qa'?'/index.html':name));if(!special[name]&&!file.startsWith(root+path.sep))throw Error();let data=await readFile(file);if(name==='/qa')data=Buffer.from(data.toString().replace('</body>','<script type="module" src="/qa-tools.js"></script></body>'));res.writeHead(200,{'Content-Type':types[path.extname(file)]||'application/octet-stream','Cache-Control':'no-store'});res.end(data);}catch{res.writeHead(404);res.end('Not found');}}).listen(portIndex>=0?Number(process.argv[portIndex+1]):4173,'0.0.0.0');
