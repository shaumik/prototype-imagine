import bpy, os, sys, json, time
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__));scene=bpy.context.scene
if 'V3 • Blade inspection' not in bpy.data.objects:
    data=bpy.data.cameras.new('V3 • Blade inspection')
    camera=bpy.data.objects.new('V3 • Blade inspection',data);scene.collection.objects.link(camera)
    camera.location=(7.1,-12,7.0)
    camera.rotation_euler=(Vector((3.70,-.03,4.99))-camera.location).to_track_quat('-Z','Y').to_euler()
    data.type='ORTHO';data.ortho_scale=5.90;data.passepartout_alpha=.95
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU';scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.075
scene.cycles.max_bounces=7;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=3;scene.cycles.transmission_bounces=5
ground=bpy.data.objects.get('Seamless studio floor')
if ground:ground.location.z=-.05
jobs=[('01 • Hero','phantom_v3_hero.png',1600,2000,48),
      ('V3 • Face inspection','phantom_v3_face.png',1100,1100,48),
      ('V3 • Hand inspection','phantom_v3_hand.png',1100,1100,48),
      ('V3 • Cannon inspection','phantom_v3_cannon.png',1100,800,32),
      ('V3 • Blade inspection','phantom_v3_blade.png',1100,1400,40)]
all_jobs=jobs[:]
if '--hero-only' in sys.argv:jobs=jobs[:1]
if '--blade-only' in sys.argv:jobs=jobs[-1:]
start=time.time()
for camera,file,w,h,samples in jobs:
    scene.camera=bpy.data.objects[camera];scene.cycles.samples=samples
    scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.resolution_percentage=100
    scene.render.filepath=os.path.join(OUT,file)
    print('RENDER_START',file,flush=True);bpy.ops.render.render(write_still=True);print('RENDER_DONE',file,round(time.time()-start),flush=True)
scene.camera=bpy.data.objects['01 • Hero'];scene.cycles.samples=48
scene.render.resolution_x=1600;scene.render.resolution_y=2000;scene.render.filepath=os.path.join(OUT,'phantom_v3_hero.png')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha_v3.blend'))
with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump({'revision':3,'files':[j[1] for j in all_jobs if os.path.exists(os.path.join(OUT,j[1]))],'last_render_seconds':round(time.time()-start),'mesh_objects':sum(o.type=='MESH' for o in scene.objects),'packed_references':[i.name for i in bpy.data.images if i.packed_file]},f,indent=2)
print('FINAL_COMPLETE',flush=True)
