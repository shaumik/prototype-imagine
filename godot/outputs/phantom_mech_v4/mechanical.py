import bpy, bmesh, math, random
from mathutils import Vector
COL=None
def group(name):
    global COL
    COL=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(COL);return COL
def add(o,name,material=None):
    o.name=name
    for c in list(o.users_collection):c.objects.unlink(o)
    COL.objects.link(o)
    if material:o.data.materials.append(material)
    return o
def rgb(h):
    v=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(x/12.92 if x<.04045 else ((x+.055)/1.055)**2.4 for x in v)
def material(name,h,metal=.7,rough=.36,glow=0,glass=0,wear=False):
    m=bpy.data.materials.new(name);m.use_nodes=True;m.diffuse_color=(*rgb(h),1)
    ns=m.node_tree.nodes;lk=m.node_tree.links;p=ns.get('Principled BSDF')
    p.inputs['Base Color'].default_value=(*rgb(h),1);p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    p.inputs['Emission Color'].default_value=(*rgb(h),1);p.inputs['Emission Strength'].default_value=glow
    p.inputs['Transmission Weight'].default_value=glass;p.inputs['IOR'].default_value=1.46
    if wear:
        geo=ns.new('ShaderNodeNewGeometry');noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=155;noise.inputs['Detail'].default_value=2
        ramp=ns.new('ShaderNodeValToRGB');ramp.color_ramp.elements[0].position=.515;ramp.color_ramp.elements[1].position=.555
        lk.new(geo.outputs['Pointiness'],ramp.inputs[0])
        mult=ns.new('ShaderNodeMath');mult.operation='MULTIPLY';lk.new(ramp.outputs['Color'],mult.inputs[0]);lk.new(noise.outputs['Fac'],mult.inputs[1])
        mix=ns.new('ShaderNodeMixRGB');mix.inputs[1].default_value=(*rgb(h),1);mix.inputs[2].default_value=(*rgb('8B969A'),1)
        lk.new(mult.outputs[0],mix.inputs[0]);lk.new(mix.outputs[0],p.inputs['Base Color'])
        bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.13;bump.inputs['Distance'].default_value=.0018
        lk.new(noise.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs['Normal'],p.inputs['Normal'])
    return m
def bevel(o,width=.025):
    b=o.modifiers.new('Machined edge breaks','BEVEL');b.width=width;b.segments=3
    n=o.modifiers.new('Weighted planar highlights','WEIGHTED_NORMAL');n.keep_sharp=True;n.weight=50
    return o
def mesh(name,vs,fs,mat,edge=.015):
    me=bpy.data.meshes.new(name);me.from_pydata(vs,[],fs);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    o=bpy.data.objects.new(name,me);COL.objects.link(o);me.materials.append(mat)
    if edge:bevel(o,edge)
    return o
def box(name,p,d,mat,edge=.025,q=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=p);o=add(bpy.context.object,name,mat);o.scale=d
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if q:o.rotation_euler=q.to_euler()
    if edge:bevel(o,edge)
    return o
def cyl(name,a,b,r,mat,r2=None,n=48,edge=.006):
    a,b=Vector(a),Vector(b);v=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=n,radius1=r,radius2=r if r2 is None else r2,depth=v.length,location=(a+b)/2)
    o=add(bpy.context.object,name,mat);o.rotation_euler=v.to_track_quat('Z','Y').to_euler()
    for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
    if edge:bevel(o,edge)
    return o
def ring(name,p,r,t,mat,axis=(0,-1,0)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=t,major_segments=48,minor_segments=10,location=p)
    o=add(bpy.context.object,name,mat);o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    for f in o.data.polygons:f.use_smooth=True
    return o
def line(name,pts,mat,r=.007):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=2
    sp=c.splines.new('POLY');sp.points.add(len(pts)-1)
    for p,v in zip(sp.points,pts):p.co=(*v,1)
    o=bpy.data.objects.new(name,c);COL.objects.link(o);c.materials.append(mat);return o
def bolt(name,p,r=.023,axis=(0,-1,0)):
    p=Vector(p);v=Vector(axis);cyl(name,p,p+v*.012,r,steel,n=8)
    cyl(name+' socket',p+v*.012,p+v*.014,r*.45,black,n=12,edge=0)
def plate(name,points,y,depth,mat,edge=.018,ridge=0):
    n=len(points);cx=sum(p[0] for p in points)/n
    vs=[(x,y-ridge*(1-min(1,abs(x-cx)/max(abs(p[0]-cx) for p in points))),z) for x,z in points]
    vs += [(x,y+depth,z) for x,z in points]
    fs=[tuple(range(n)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name,vs,fs,mat,edge)
def spl(name,s,points,y,depth,mat,edge=.018):return plate(name,[(s*x,z) for x,z in points],y,depth,mat,edge)
def prism(name,a,b,w,h,mat,chamfer=.18,sections=None,edge=.015):
    a,b=Vector(a),Vector(b);length=(b-a).length
    if sections is None:sections=[(0,1),(.04,1),(.96,1),(1,1)]
    r=[(-.5+chamfer,-.5),(.5-chamfer,-.5),(.5,-.5+chamfer),(.5,.5-chamfer),(.5-chamfer,.5),(-.5+chamfer,.5),(-.5,.5-chamfer),(-.5,-.5+chamfer)]
    vs=[(x*w*k,y*h*k,(t-.5)*length) for t,k in sections for x,y in r];fs=[tuple(range(8))]
    for j in range(len(sections)-1):
        for i in range(8):fs.append((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i))
    fs.append(tuple(range((len(sections)-1)*8,len(sections)*8)))
    o=mesh(name,vs,fs,mat,edge);o.location=(a+b)/2;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler();return o
def tube(name,a,b,outer,inner,mat,n=48):
    a,b=Vector(a),Vector(b);q=(b-a).to_track_quat('Z','Y');vs=[]
    for p,r in [(a,outer),(b,outer),(b,inner),(a,inner)]:
        for i in range(n):vs.append(p+q@Vector((r*math.cos(math.tau*i/n),r*math.sin(math.tau*i/n),0)))
    fs=[]
    for j in range(4):
        for i in range(n):fs.append((j*n+i,j*n+(i+1)%n,((j+1)%4)*n+(i+1)%n,((j+1)%4)*n+i))
    o=mesh(name,vs,fs,mat,.004)
    for f in o.data.polygons:f.use_smooth=f.index//n in [0,2]
    return o
def cut(target,cutter):
    bpy.context.view_layer.objects.active=target
    for existing in list(target.modifiers):bpy.ops.object.modifier_apply(modifier=existing.name)
    b=target.modifiers.new('Machined recess','BOOLEAN');b.operation='DIFFERENCE';b.solver='EXACT';b.object=cutter
    bpy.ops.object.modifier_apply(modifier=b.name);bpy.data.objects.remove(cutter,do_unlink=True)
def label(text,p,size=.045,rot=(math.pi/2,0,0)):
    c=bpy.data.curves.new('Stencil','FONT');c.body=text;c.size=size;c.align_x='CENTER';c.space_character=1.05
    o=bpy.data.objects.new('Stencil / '+text,c);COL.objects.link(o);o.location=p;o.rotation_euler=rot;c.materials.append(mark);return o
def lens(name,p,r,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=p);o=add(bpy.context.object,name,mat);o.scale=(r,r*.46,r)
    return o
def pivot(name,p,width,r,axis=(1,0,0)):
    p=Vector(p);v=Vector(axis).normalized()
    cyl(name+' rubber seal',p-v*(width*.58),p+v*(width*.58),r*.87,black)
    cyl(name+' outer bearing',p-v*width*.45,p+v*width*.45,r,steel)
    for s in [-1,1]:
        ring(name+' retaining lip',p+v*(s*width*.46),r*.85,r*.10,bronze,v)
        cyl(name+' recessed cap',p+v*(s*width*.54),p+v*(s*width*.56),r*.58,frame)
        bolt(name+' center',p+v*(s*width*.57),r*.26,v*s)

teal=material('V4 / chipped petrol armor','3B5861',.73,.39,wear=True)
teal2=material('V4 / edge armor','476A73',.74,.37,wear=True)
gold=material('V4 / brushed bronze trim','B39663',.76,.34,wear=True)
bronze=material('V4 / dark bronze mechanics','72624E',.78,.33)
frame=material('V4 / machined graphite','42464C',.78,.34,wear=True)
steel=material('V4 / exposed alloy','869196',.86,.29,wear=True)
black=material('V4 / recessed black','111A23',.56,.37)
mouth=material('V4 / mask satin titanium','5D706E',.61,.42,wear=True)
blueglass=material('V4 / optical blue glass','286AB0',.25,.10,.12,.66)
eye=material('V4 / ice optics','69BEEA',.25,.15,.65,.28)
amber=material('V4 / amber optical emitter','EBB640',.36,.25,1.6)
cyan=material('V4 / cyan status emitter','50DADD',.3,.3,1.7)
mark=material('V4 / micro stencil','A4AFB0',.12,.5)
