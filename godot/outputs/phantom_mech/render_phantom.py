import bpy, os, sys, json, time
OUT=os.path.dirname(os.path.abspath(__file__))
scene=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences
prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU'
scene.cycles.use_denoising=True
if not scene.get('floor_contact_adjusted',False):
    for collection in bpy.data.collections:
        if collection.name[:2] in ['01','02','03','04','05','06','07']:
            for obj in collection.objects:obj.location.z-=.07
    scene['floor_contact_adjusted']=True
scene.view_settings.exposure=.15
for name,power in [('Key • large neutral softbox',1900),('Top • overhead',1150),('Rim • warm left',1900),('Rim • cold edge',2400)]:
    bpy.data.lights[name].energy=power
bpy.data.materials['CORE • emerald lens'].node_tree.nodes.get('Principled BSDF').inputs['Emission Strength'].default_value=.35
bpy.data.materials['TRIM • anodized warm gold'].node_tree.nodes.get('Principled BSDF').inputs['Metallic'].default_value=.62
bpy.data.materials['TRIM • anodized warm gold'].node_tree.nodes.get('Principled BSDF').inputs['Roughness'].default_value=.34
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.overlay.show_overlays=False
            a.spaces.active.region_3d.view_perspective='CAMERA'
            a.spaces.active.region_3d.view_camera_zoom=-3
scene.cycles.samples=128
scene.cycles.adaptive_threshold=.025
scene.render.resolution_percentage=100
scene.render.image_settings.color_mode='RGB'
scene.render.image_settings.color_depth='8'
jobs=[('CAM 01 • Hero','phantom_hero.png',2000,2250),
      ('CAM 03 • Rear','phantom_rear.png',1600,1800),
      ('CAM 04 • Helmet and torso','phantom_detail.png',1800,1600),
      ('CAM 02 • Front','phantom_front.png',1600,1800)]
if '--hero-only' in sys.argv:jobs=jobs[:1]
if '--extras-only' in sys.argv:jobs=jobs[1:]
if '--quick' in sys.argv:
    scene.cycles.samples=24;scene.cycles.adaptive_threshold=.07
    jobs=[('CAM 01 • Hero','preview.png',768,864),('CAM 03 • Rear','preview_rear.png',640,720),('CAM 04 • Helmet and torso','preview_detail.png',800,700)]
start=time.time()
for cam,file,w,h in jobs:
    scene.camera=bpy.data.objects[cam]
    scene.render.resolution_x=w;scene.render.resolution_y=h
    scene.render.filepath=os.path.join(OUT,file)
    print('START_RENDER',file,flush=True)
    bpy.ops.render.render(write_still=True)
    print('FINISH_RENDER',file,'elapsed',round(time.time()-start),flush=True)
scene.camera=bpy.data.objects['CAM 01 • Hero']
scene.render.resolution_x=2000;scene.render.resolution_y=2250
scene.render.filepath=os.path.join(OUT,'phantom_hero.png')
if '--quick' not in sys.argv:
    bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha.blend'))
stats={'mesh_objects':sum(o.type=='MESH' for o in scene.objects),'materials':len(bpy.data.materials),'cameras':sum(o.type=='CAMERA' for o in scene.objects),'render_seconds':round(time.time()-start),'renders':[j[1] for j in jobs]}
with open(os.path.join(OUT,'render_manifest.json'),'w') as f:json.dump(stats,f,indent=2)
print('ALL_RENDERS_COMPLETE',stats,flush=True)
