import bpy, os, sys, json, time
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__));scene=bpy.context.scene
hero=bpy.data.objects['V4 • Hero'];hero.location=(8,-30,11.8)
hero.rotation_euler=(Vector((0,-.20,6.14))-hero.location).to_track_quat('-Z','Y').to_euler()
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU';scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.075
scene.cycles.max_bounces=7;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=3;scene.cycles.transmission_bounces=3
jobs=[('V4 • Hero','phantom_v4_hero.png',1600,2100,48),
      ('V4 • Front proportion check','phantom_v4_front.png',1200,1600,40),
      ('V4 • Helmet and neck','phantom_v4_head.png',1100,1100,48),
      ('V4 • Hand construction','phantom_v4_hand.png',1100,1100,40),
      ('V4 • Blade and wrist clearance','phantom_v4_blade.png',1000,1400,40),
      ('V4 • Cannon construction','phantom_v4_cannon.png',1200,850,40)]
all_jobs=jobs[:]
if '--details-only' in sys.argv:jobs=jobs[2:]
if '--hero-only' in sys.argv:jobs=jobs[:1]
start=time.time()
for camera,file,w,h,samples in jobs:
    scene.camera=bpy.data.objects[camera];scene.cycles.samples=samples
    scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100
    scene.render.filepath=os.path.join(OUT,file)
    print('RENDER_START',file,flush=True);bpy.ops.render.render(write_still=True);print('RENDER_DONE',file,round(time.time()-start),flush=True)
scene.camera=bpy.data.objects['V4 • Hero'];scene.cycles.samples=48
scene.render.resolution_x=1600;scene.render.resolution_y=2100;scene.render.filepath=os.path.join(OUT,'phantom_v4_hero.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha_v4.blend'))
with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump({'revision':4,'renders':[j[1] for j in all_jobs if os.path.exists(os.path.join(OUT,j[1]))],'last_render_seconds':round(time.time()-start),'mesh_objects':sum(o.type=='MESH' for o in scene.objects),'packed_references':[i.name for i in bpy.data.images if i.packed_file]},f,indent=2)
print('FINAL_COMPLETE',flush=True)
