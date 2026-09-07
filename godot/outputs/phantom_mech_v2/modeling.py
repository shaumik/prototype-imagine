import bpy, math, os
from mathutils import Vector

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for c in list(bpy.data.collections): bpy.data.collections.remove(c)
COL=None
def group(name):
    global COL
    COL=bpy.data.collections.new(name);bpy.context.scene.collection.children.link(COL)
    return COL
group('01 • Structural frame')
def link(o,name,mat=None):
    o.name=name
    for c in list(o.users_collection):c.objects.unlink(o)
    COL.objects.link(o)
    if mat:o.data.materials.append(mat)
    return o
def rgb(h):
    a=[int(h[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(x/12.92 if x<.04045 else ((x+.055)/1.055)**2.4 for x in a)
def mat(name,h,metal=.65,rough=.34,emit=0,grain=False):
    m=bpy.data.materials.new(name);m.diffuse_color=(*rgb(h),1);m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF');p.inputs['Base Color'].default_value=(*rgb(h),1)
    p.inputs['Metallic'].default_value=metal;p.inputs['Roughness'].default_value=rough
    p.inputs['Emission Color'].default_value=(*rgb(h),1);p.inputs['Emission Strength'].default_value=emit
    if grain:
        n=m.node_tree.nodes.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=420;n.inputs['Detail'].default_value=2
        b=m.node_tree.nodes.new('ShaderNodeBump');b.inputs['Strength'].default_value=.07;b.inputs['Distance'].default_value=.002
        m.node_tree.links.new(n.outputs['Fac'],b.inputs['Height']);m.node_tree.links.new(b.outputs['Normal'],p.inputs['Normal'])
    return m
teal=mat('Armor / muted petrol','31545B',.72,.43,grain=True)
teal2=mat('Armor / blue steel','3F6770',.7,.40,grain=True)
tealdark=mat('Armor / deep teal recess','203A42',.68,.37)
gold=mat('Trim / aged champagne bronze','AC865D',.73,.39,grain=True)
bronze=mat('Mechanism / dark bronze','685444',.76,.34)
frame=mat('Frame / graphite titanium','383C42',.74,.43,grain=True)
steel=mat('Mechanism / brushed gunmetal','68767E',.78,.35,grain=True)
silver=mat('Face and edges / satin alloy','9BAAB0',.8,.3)
black=mat('Recess / blackened steel','111A21',.5,.39)
rubber=mat('Joint / flexible boot','171C23',.15,.55)
red=mat('Signal / dark vermilion','B14F3E',.54,.35)
optic=mat('Optics / pale ice','BBDADD',.25,.3,1.6)
cyan=mat('Emitter / ion blue','50CFEA',.32,.28,2.8)
core=mat('Reactor / emerald crystal','244E38',.55,.2,.18)
blade=mat('Blade / brushed alloy','9FB7C0',.82,.26,grain=True)
edge=mat('Blade / honed edge','BBDCE2',.85,.21,.18)
stencil=mat('Markings / subdued grey','869699',.1,.6)

def mesh(name,vs,fs,material,smooth=True,bevel=0):
    m=bpy.data.meshes.new(name);m.from_pydata(vs,[],fs);m.update();o=bpy.data.objects.new(name,m);COL.objects.link(o);m.materials.append(material)
    for p in m.polygons:p.use_smooth=smooth
    if bevel:
        b=o.modifiers.new('Small edge radius','BEVEL');b.width=bevel;b.segments=3
        n=o.modifiers.new('Stable face normals','WEIGHTED_NORMAL');n.keep_sharp=True
    return o
def box(name,loc,dims,material,radius=.04,rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1,location=loc);o=link(bpy.context.object,name,material);o.scale=dims
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if rot:o.rotation_euler=rot
    b=o.modifiers.new('Rounded machining','BEVEL');b.width=radius;b.segments=4
    n=o.modifiers.new('Normals','WEIGHTED_NORMAL');n.keep_sharp=True
    return o
def cyl(name,a,b,r,material,r2=None,verts=40):
    a,b=Vector(a),Vector(b);d=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=r,radius2=r if r2 is None else r2,depth=d.length,location=(a+b)/2)
    o=link(bpy.context.object,name,material);o.rotation_euler=d.to_track_quat('Z','Y').to_euler()
    m=o.modifiers.new('Machined lip','BEVEL');m.width=.012;m.segments=3
    for p in o.data.polygons:p.use_smooth=len(p.vertices)==4
    return o
def sphere(name,loc,dims,material):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=32,ring_count=20,location=loc);o=link(bpy.context.object,name,material);o.scale=dims
    for p in o.data.polygons:p.use_smooth=True
    return o
def ring(name,loc,r,thick,material,axis=(0,0,1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=r,minor_radius=thick,major_segments=48,minor_segments=12,location=loc)
    o=link(bpy.context.object,name,material);o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    for p in o.data.polygons:p.use_smooth=True
    return o
def line(name,pts,material,r=.012):
    c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';c.bevel_depth=r;c.bevel_resolution=3
    s=c.splines.new('POLY');s.points.add(len(pts)-1)
    for p,v in zip(s.points,pts):p.co=(*v,1)
    o=bpy.data.objects.new(name,c);COL.objects.link(o);c.materials.append(material);return o
def bolt(name,p,r=.026,axis=(0,-1,0)):
    p=Vector(p);v=Vector(axis);cyl(name,p,p+v*.014,r,steel,verts=8);cyl(name+' socket',p+v*.014,p+v*.019,r*.43,black,verts=12)
def label(text,loc,size=.05,rot=(math.pi/2,0,0)):
    c=bpy.data.curves.new('Service marking','FONT');c.body=text;c.size=size;c.align_x='CENTER'
    o=bpy.data.objects.new('Marking • '+text,c);COL.objects.link(o);c.materials.append(stencil);o.location=loc;o.rotation_euler=rot;return o

def pod(name,a,b,profile,material,n=3.1,verts=32,sub=2):
    """Continuous shaped armor: variable rounded cross-sections and compound curvature."""
    a,b=Vector(a),Vector(b);length=(b-a).length;vs=[]
    for row in profile:
        t,rx,ry=row[:3];xo=row[3] if len(row)>3 else 0;yo=row[4] if len(row)>4 else 0
        for i in range(verts):
            q=math.tau*i/verts;c=math.cos(q);s=math.sin(q)
            vs.append((xo+rx*math.copysign(abs(c)**(2/n),c),yo+ry*math.copysign(abs(s)**(2/n),s),(t-.5)*length))
    fs=[tuple(range(verts-1,-1,-1))]
    for j in range(len(profile)-1):
        for i in range(verts):fs.append((j*verts+i,j*verts+(i+1)%verts,(j+1)*verts+(i+1)%verts,(j+1)*verts+i))
    fs.append(tuple(range((len(profile)-1)*verts,len(profile)*verts)))
    o=mesh(name,vs,fs,material);o.location=(a+b)/2;o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler()
    if sub:m=o.modifiers.new('Continuous armor curvature','SUBSURF');m.levels=1;m.render_levels=sub
    return o

def roundpoly(pts,roundness=.11,steps=4):
    out=[]
    for i,p in enumerate(pts):
        p=Vector(p);a=p.lerp(Vector(pts[i-1]),roundness);b=p.lerp(Vector(pts[(i+1)%len(pts)]),roundness)
        for j in range(steps):
            t=j/(steps-1);out.append((1-t)**2*a+2*(1-t)*t*p+t*t*b)
    if sum(out[i].x*out[(i+1)%len(out)].y-out[(i+1)%len(out)].x*out[i].y for i in range(len(out)))<0:out.reverse()
    return out
def shell(name,pts,y,depth,material,bulge=.06,roundness=.12,slope=(0,0),smooth=True):
    """Domed armor panel with rolled edges, not a constant-depth extruded slab."""
    pts=roundpoly(pts,roundness);c=sum(pts,Vector((0,0)))/len(pts);count=len(pts);vs=[]
    for scale,off in [(1,depth), (1.005,.055),(.972,0),(.84,-bulge*.60),(.40,-bulge)]:
        for p in pts:
            q=c+(p-c)*scale;vs.append((q.x,y+off+slope[0]*(q.x-c.x)+slope[1]*(q.y-c.y),q.y))
    fs=[tuple(range(count-1,-1,-1))]
    for j in range(4):
        for i in range(count):fs.append((j*count+i,j*count+(i+1)%count,(j+1)*count+(i+1)%count,(j+1)*count+i))
    vs.append((c.x,y-bulge,c.y));ci=len(vs)-1
    for i in range(count):fs.append((4*count+i,4*count+(i+1)%count,ci))
    o=mesh(name,vs,fs,material,smooth)
    if smooth:
        normal=o.modifiers.new('Panel highlight control','WEIGHTED_NORMAL');normal.keep_sharp=True;normal.weight=75
    return o
def mirrored(name,s,pts,y,depth,material,**kwargs):
    if 'slope' in kwargs:kwargs['slope']=(kwargs['slope'][0]*s,kwargs['slope'][1])
    return shell(name,[(s*x,z) for x,z in pts],y,depth,material,**kwargs)
def panel(name,s,pts,y,material,bulge=.05,slope=(0,0)):
    # The exposed gasket sits just outside the metal's perimeter.
    cx=sum(x for x,z in pts)/len(pts);cz=sum(z for x,z in pts)/len(pts)
    gasket=[(cx+(x-cx)*1.045,cz+(z-cz)*1.045) for x,z in pts]
    mirrored(name+' • gasket',s,gasket,y+.055,.06,black,bulge=bulge*.75,slope=slope)
    return mirrored(name,s,pts,y,.12,material,bulge=bulge,slope=slope)
def blade_mesh(name,stations,y,material):
    # Each station is z / inner x / outer x. A diamond section creates the actual bevel.
    vs=[]
    for z,inside,outside in stations:
        width=outside-inside
        vs.extend([(inside,y,z),(inside+width*.35,y-.085,z),(outside,y-.005,z),(inside+width*.35,y+.065,z)])
    fs=[(3,2,1,0)]
    for j in range(len(stations)-1):
        for k in range(4):fs.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
    fs.append(tuple(range((len(stations)-1)*4,len(stations)*4)))
    if stations[0][2]>stations[0][1]:fs=[tuple(reversed(f)) for f in fs]
    return mesh(name,vs,fs,material,False,bevel=.006)
