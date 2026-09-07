import bpy,os,json,math
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'Phantom_Revision6.blend'))
s=bpy.context.scene
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.cycles.use_denoising=True;s.cycles.samples=32;s.cycles.adaptive_threshold=.075
col=bpy.data.collections.get('STUDIO • Cameras and lighting')
def cam(name,loc,target,scale):
    data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);col.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=scale;return o
head=cam('R6 camera • head detail',(-1.8,-10,7.15),(0,-.12,6.78),1.90)
head_side=cam('R6 camera • head side',(-10,-.1,6.8),(0,-.1,6.8),1.75)
wrist=cam('R6 camera • wrist detail',(10,-13,6.1),(2.26,-.12,4.12),2.04)
clay=bpy.data.materials.new('R6 neutral clay');clay.use_nodes=True;p=clay.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(.37,.41,.43,1);p.inputs['Roughness'].default_value=.68
cameras={'side':bpy.data.objects['CAM • Side traced alignment'],'front':bpy.data.objects['CAM • Front traced alignment'],'hero':bpy.data.objects['CAM • Three quarter geometry'],'head':head,'head_side':head_side,'wrist':wrist,'rear':bpy.data.objects['CAM • Rear traced alignment'],'side_clay':bpy.data.objects['CAM • Side traced alignment'],'hero_clay':bpy.data.objects['CAM • Three quarter geometry']}
for view in ['head','head_side','side','front','hero','wrist','rear','side_clay','hero_clay']:
    camera=cameras[view]
    s.camera=camera;s.view_layers[0].material_override=clay if 'clay' in view else None
    bpy.data.objects['Ground'].hide_render=view not in ['hero','hero_clay']
    detail=view in ['head','head_side','wrist'];s.render.resolution_x=1100 if detail or view not in ['side','side_clay','rear'] else 850;s.render.resolution_y=1100 if detail else 1400
    s.render.resolution_percentage=100;s.cycles.samples=40 if detail else 32;s.render.filepath=os.path.join(OUT,'blender_'+view+'.png')
    bpy.ops.render.render(write_still=True);print('COMPLETE',view,flush=True)
s.view_layers[0].material_override=None;s.camera=cameras['hero'];bpy.data.objects['Ground'].hide_render=False
s.render.resolution_x=1100;s.render.resolution_y=1400;s.render.filepath=os.path.join(OUT,'blender_hero.png')
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            sp=area.spaces.active;sp.shading.type='SOLID';sp.shading.color_type='MATERIAL';sp.shading.show_cavity=True;sp.overlay.show_overlays=False;sp.region_3d.view_perspective='CAMERA'
manifest={'native_scene':'Phantom_Revision6.blend','mesh_objects':len([o for o in bpy.data.objects if o.type=='MESH']),'packed_reference_images':len([im for im in bpy.data.images if im.packed_file]),'actual_blender_renders':['blender_'+v+'.png' for v in cameras],'ai_design_reference':'construction_guide.png','image_generation_method':'built-in image generation tool','image_prompt':'construction_prompt.txt','calf_main_shell_max_depth':.64,'blade_width_max':.245,'blade_length':2.36}
with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump(manifest,f,indent=2)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Revision6.blend'))
