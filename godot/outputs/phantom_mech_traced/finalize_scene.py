import bpy,os,math,json
OUT=os.path.dirname(os.path.abspath(__file__))
bpy.ops.wm.open_mainfile(filepath=os.path.join(OUT,'Phantom_Traced.blend'))
s=bpy.context.scene
s.camera=bpy.data.objects.get('CAM • Three quarter geometry')
s.render.resolution_x=1100;s.render.resolution_y=1300;s.render.resolution_percentage=100
s.render.filepath=os.path.join(OUT,'hero.png');s.view_layers[0].material_override=None
bpy.data.objects['Ground'].hide_render=False
for screen in bpy.data.screens:
    for area in screen.areas:
        if area.type=='VIEW_3D':
            sp=area.spaces.active;sp.shading.type='SOLID';sp.shading.color_type='MATERIAL';sp.shading.show_cavity=True;sp.shading.cavity_type='BOTH'
            sp.overlay.show_overlays=False;sp.region_3d.view_perspective='CAMERA'
for mat in list(bpy.data.materials):
    if mat.users==0:bpy.data.materials.remove(mat)
for im in bpy.data.images:
    if im.source=='FILE' and not im.packed_file:im.pack()
meshes=[o for o in bpy.data.objects if o.type=='MESH']
assert all(math.isfinite(v) for o in meshes for p in o.data.vertices for v in p.co)
manifest={'scene':'Phantom_Traced.blend','mesh_objects':len(meshes),'mesh_vertices':sum(len(o.data.vertices) for o in meshes),'reference_images_packed':sum(bool(i.packed_file) for i in bpy.data.images),'render_views':['front','side','rear','hero','clay','face','hand'],'image_projection_enabled':False,'paired_wrist_blades':True}
with open(os.path.join(OUT,'manifest.json'),'w') as f:json.dump(manifest,f,indent=2)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Traced.blend'))
print(json.dumps(manifest),flush=True)
