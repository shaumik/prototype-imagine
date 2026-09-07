from pathlib import Path
import json,zipfile,struct
out=Path(__file__).resolve().parent
meta=json.loads((out/'manifest.json').read_text())
names=['Phantom_Revision6.blend','construction_guide.png','construction_prompt.txt','README.md','manifest.json']+meta['actual_blender_renders']
for name in names:
    p=out/name
    assert p.is_file() and p.stat().st_size>0,name
    if p.suffix=='.png':
        h=p.read_bytes()[:24];assert h[:8]==b'\x89PNG\r\n\x1a\n',name
        print(name,struct.unpack('>II',h[16:24]))
archive=out/'Phantom_Revision6_Package.zip'
with zipfile.ZipFile(archive,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
    for name in names:z.write(out/name,'Phantom_Revision6/'+name)
with zipfile.ZipFile(archive) as z:assert z.testzip() is None
print('VALIDATED',archive,archive.stat().st_size)
