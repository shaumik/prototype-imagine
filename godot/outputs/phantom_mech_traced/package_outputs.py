import json,zipfile,pathlib,struct
out=pathlib.Path(__file__).resolve().parent
names=['Phantom_Traced.blend','README.md','manifest.json','hero.png','front.png','side.png','rear.png','clay.png','face.png','hand.png']
for name in names:
    p=out/name
    if not p.is_file() or p.stat().st_size==0:raise RuntimeError('Missing output: '+name)
    if p.suffix=='.png':
        head=p.read_bytes()[:24]
        if head[:8]!=b'\x89PNG\r\n\x1a\n':raise RuntimeError('Invalid PNG: '+name)
        print(name,struct.unpack('>II',head[16:24]))
archive=out/'Phantom_Traced_Package.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in names:z.write(out/name,'Phantom_Traced/'+name)
with zipfile.ZipFile(archive) as z:
    if z.testzip() is not None:raise RuntimeError('Archive validation failed')
print(archive,archive.stat().st_size)
