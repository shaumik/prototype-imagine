import bpy, os, sys, json, time
OUT=os.path.dirname(os.path.abspath(__file__))
scene=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU';scene.cycles.use_denoising=True
scene.cycles.max_bounces=6;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=3
jobs=[('01 • Hero','phantom_v2_hero.png',1600,2000,64),('03 • Face','phantom_v2_face.png',1000,1000,48)]
if '--face-only' in sys.argv:jobs=jobs[1:]
if '--hero-only' in sys.argv:jobs=jobs[:1]
start=time.time()
for cam,file,w,h,samples in jobs:
    scene.camera=bpy.data.objects[cam];scene.cycles.samples=samples;scene.cycles.adaptive_threshold=.06
    scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100
    scene.render.filepath=os.path.join(OUT,file)
    print('RENDER_START',file,flush=True);bpy.ops.render.render(write_still=True);print('RENDER_DONE',file,round(time.time()-start),flush=True)
scene.camera=bpy.data.objects['01 • Hero'];scene.render.resolution_x=1600;scene.render.resolution_y=2000;scene.cycles.samples=64
scene.render.filepath=os.path.join(OUT,'phantom_v2_hero.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha_v2.blend'))
with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump({'revision':2,'renders':[j[1] for j in jobs],'render_seconds':round(time.time()-start),'packed_reference':any(i.packed_file for i in bpy.data.images),'mesh_objects':sum(o.type=='MESH' for o in scene.objects)},f,indent=2)
print('FINAL_COMPLETE',flush=True)
