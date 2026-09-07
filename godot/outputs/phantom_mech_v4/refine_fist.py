import bpy, os, sys, math
from mathutils import Vector, Matrix
OUT=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,OUT)
import mechanical as M
from mechanical import *
scene=bpy.context.scene
for k,n in {'teal':'petrol ceramic coating','teal2':'blue teal panel coating','gold':'muted bronze trim','bronze':'recessed bronze mechanism','frame':'black phosphate chassis','steel':'machined bearing steel','black':'internal graphite'}.items():
    mat=bpy.data.materials['V4 / '+n];globals()[k]=mat;setattr(M,k,mat)
for col in list(bpy.data.collections):
    if col.name.startswith('05B •'):
        for ob in list(col.objects):bpy.data.objects.remove(ob,do_unlink=True)
        bpy.data.collections.remove(col)
for ob in list(scene.objects):
    if ob.name.startswith('Finger articulation split'):bpy.data.objects.remove(ob,do_unlink=True)
with open(os.path.join(OUT,'rebuild.py')) as f:source=f.read()
exec(source[source.index('def phalange('):source.index('# Weapons are fully replaced')])
scene.camera=bpy.data.objects['V4 • Hero'];bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha_v4.blend'))
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU';scene.cycles.samples=16;scene.cycles.adaptive_threshold=.13
for camera,file,w,h in [('V4 • Hand construction','preview_hand.png',760,760),('V4 • Front proportion check','preview_front.png',750,1000)]:
    scene.camera=bpy.data.objects[camera];scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100
    scene.render.filepath=os.path.join(OUT,file)
    print('PREVIEW_START',file,flush=True);bpy.ops.render.render(write_still=True);print('PREVIEW_DONE',file,flush=True)
