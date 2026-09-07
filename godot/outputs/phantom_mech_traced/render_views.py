import bpy,os
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'Phantom_Traced.blend'))
s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.10
views={'hero':'CAM • Three quarter geometry','face':'CAM • Face inspection','hand':'CAM • Hand and blade inspection','front':'CAM • Front traced alignment','side':'CAM • Side traced alignment','rear':'CAM • Rear traced alignment','clay':'CAM • Three quarter geometry'}
clay=bpy.data.materials.get('Inspection clay')
if not clay:
    clay=bpy.data.materials.new('Inspection clay');clay.use_nodes=True
    sh=clay.node_tree.nodes.get('Principled BSDF');sh.inputs['Base Color'].default_value=(.38,.42,.44,1);sh.inputs['Roughness'].default_value=.65
for view,camera_name in views.items():
    s.camera=bpy.data.objects[camera_name]
    if view=='hand':
        s.camera.data.ortho_scale=2.1;s.camera.location=(8,-10,6)
        s.camera.rotation_euler=(Vector((2.1,-.25,3.8))-s.camera.location).to_track_quat('-Z','Y').to_euler()
    s.view_layers[0].material_override=clay if view=='clay' else None
    bpy.data.objects['Ground'].hide_render=view in ['front','side','rear']
    s.cycles.samples=32 if view in ['face','hand'] else 24
    s.render.resolution_x=1000 if view in ['face','hand'] else (850 if view in ['side','rear'] else 1100)
    s.render.resolution_y=1000 if view in ['face','hand'] else 1300
    s.render.resolution_percentage=100;s.render.filepath=os.path.join(OUT,view+'.png')
    bpy.ops.render.render(write_still=True)
    print('COMPLETE',view,flush=True)
