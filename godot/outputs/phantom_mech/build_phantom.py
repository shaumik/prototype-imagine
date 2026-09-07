import bpy, math, os, random, sys
from mathutils import Vector

OUT = os.path.dirname(os.path.abspath(__file__))
REFERENCE = os.path.join(OUT, 'reference.jpg')
if not os.path.exists(REFERENCE):
    REFERENCE = '/Users/shaumikmondal/Downloads/Gemini_Generated_Image_8j46k08j46k08j46.jpg'
random.seed(18)
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)
for d in list(bpy.data.collections):
    if d.name != 'Collection': bpy.data.collections.remove(d)
base = bpy.data.collections.get('Collection'); base.name = 'PHANTOM | assembly'
collections = {}
def group(name):
    if name not in collections:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c); collections[name] = c
    return collections[name]
current = group('01 | Torso and core')
def register(obj, name, mat=None):
    obj.name = name
    for c in list(obj.users_collection): c.objects.unlink(obj)
    current.objects.link(obj)
    if mat: obj.data.materials.append(mat)
    return obj
def rgb(hex):
    a = [int(hex[i:i+2],16)/255 for i in (0,2,4)]
    return tuple(v/12.92 if v<0.04045 else ((v+.055)/1.055)**2.4 for v in a)
def material(name, color, metal=0, rough=.4, glow=0, texture=False):
    m=bpy.data.materials.new(name); m.use_nodes=True
    p=m.node_tree.nodes.get('Principled BSDF'); c=(*rgb(color),1)
    p.inputs['Base Color'].default_value=c; p.inputs['Metallic'].default_value=metal; p.inputs['Roughness'].default_value=rough
    if glow:
        p.inputs['Emission Color'].default_value=c; p.inputs['Emission Strength'].default_value=glow
    if texture:
        n=m.node_tree.nodes.new('ShaderNodeTexNoise'); n.inputs['Scale'].default_value=145; n.inputs['Detail'].default_value=2
        bump=m.node_tree.nodes.new('ShaderNodeBump'); bump.inputs['Strength'].default_value=.12; bump.inputs['Distance'].default_value=.014
        m.node_tree.links.new(n.outputs['Fac'],bump.inputs['Height']); m.node_tree.links.new(bump.outputs['Normal'],p.inputs['Normal'])
    return m
teal=material('ARMOR • deep petrol ceramic','24606B',.7,.3,texture=True)
blue=material('ARMOR • blue teal secondary','34818B',.62,.29,texture=True)
darkteal=material('ARMOR • shadow teal','17363F',.65,.33)
gold=material('TRIM • anodized warm gold','E8AB51',.72,.29,texture=True)
gold_dark=material('TRIM • aged brass','8C5C31',.72,.33)
graphite=material('CHASSIS • graphite titanium','343840',.8,.3,texture=True)
steel=material('MECHANISM • gunmetal','65717A',.78,.3,texture=True)
silver=material('EDGE • machined alloy','C6D9DE',.78,.23)
black=material('RECESS • carbon black','0A141B',.35,.42)
rubber=material('JOINT • elastomer','1A2026',.12,.56)
red=material('SIGNAL • vermilion','D4523D',.42,.3)
cyan=material('LIGHT • ion cyan','59E7FF',.2,.22,5)
ice=material('LIGHT • blade edge','B7F7FF',.55,.21,1.1)
green=material('CORE • emerald lens','2DE0A8',.35,.2,1.3)
amber=material('LIGHT • amber optics','FFBC58',.3,.23,3)
white=material('MARKINGS • warm white','B9D0D2',.35,.4)

def bevel(o, width=.05, seg=3):
    mod=o.modifiers.new('Machined edge radii','BEVEL'); mod.width=width; mod.segments=seg
    mod=o.modifiers.new('Face weighted normals','WEIGHTED_NORMAL'); mod.keep_sharp=True; mod.weight=50
    return o
def box(name, loc, scale, mat, width=.04, rot=None):
    bpy.ops.mesh.primitive_cube_add(size=1, location=loc); o=register(bpy.context.object,name,mat); o.scale=scale
    bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
    if rot: o.rotation_euler=rot
    if width: bevel(o,width)
    return o
def mesh(name, verts, faces, mat, width=.03, side=None):
    m=bpy.data.meshes.new(name); m.from_pydata(verts,[],faces); m.update()
    o=bpy.data.objects.new(name,m); current.objects.link(o); m.materials.append(mat)
    if side:
        m.materials.append(side)
        for p in m.polygons: p.material_index=0 if p.index==0 else 1
    if width: bevel(o,width)
    return o
def plate(name, pts, front, back, mat, width=.035, side=None):
    pts=list(pts)
    if sum(pts[i][0]*pts[(i+1)%len(pts)][1]-pts[(i+1)%len(pts)][0]*pts[i][1] for i in range(len(pts)))<0: pts.reverse()
    n=len(pts); vs=[(x,front,z) for x,z in pts]+[(x,back,z) for x,z in pts]
    fs=[tuple(range(n)),tuple(range(2*n-1,n-1,-1))]+[(i,i+n,(i+1)%n+n,(i+1)%n) for i in range(n)]
    return mesh(name,vs,fs,mat,width,side)
def symplate(name, s, pts, front, back, mat, width=.035, side=None):
    return plate(name,[ (s*x,z) for x,z in pts],front,back,mat,width,side)
def cylinder(name,a,b,r,mat,verts=32,r2=None):
    a,b=Vector(a),Vector(b); d=b-a
    bpy.ops.mesh.primitive_cone_add(vertices=verts,radius1=r,radius2=r if r2 is None else r2,depth=d.length,location=(a+b)/2)
    o=register(bpy.context.object,name,mat); o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); bevel(o,.018,2)
    for p in o.data.polygons: p.use_smooth=len(p.vertices)==4
    return o
def sphere(name,loc,scale,mat):
    bpy.ops.mesh.primitive_uv_sphere_add(segments=24,ring_count=12,location=loc); o=register(bpy.context.object,name,mat); o.scale=scale
    for p in o.data.polygons:p.use_smooth=True
    return o
def torus(name,loc,major,minor,mat,axis=(0,0,1)):
    bpy.ops.mesh.primitive_torus_add(major_radius=major,minor_radius=minor,major_segments=40,minor_segments=10,location=loc)
    o=register(bpy.context.object,name,mat); o.rotation_euler=Vector(axis).to_track_quat('Z','Y').to_euler()
    for p in o.data.polygons:p.use_smooth=True
    return o
def beam(name,a,b,w,d,mat,taper=.8):
    a,b=Vector(a),Vector(b); length=(b-a).length
    ring=[(-.34,-.5),(.34,-.5),(.5,-.34),(.5,.34),(.34,.5),(-.34,.5),(-.5,.34),(-.5,-.34)]
    vs=[]
    for z,k in [(0,.83),(.1,1),(length-.1,taper),(length,taper*.85)]:vs.extend([(x*w*k,y*d*k,z-length/2) for x,y in ring])
    fs=[tuple(range(7,-1,-1)),tuple(range(24,32))]
    for j in range(3):
        for i in range(8):fs.append((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i))
    o=mesh(name,vs,fs,mat,.035); o.location=(a+b)/2; o.rotation_euler=(b-a).to_track_quat('Z','Y').to_euler(); return o
def line(name,points,mat,r=.018):
    c=bpy.data.curves.new(name,'CURVE'); c.dimensions='3D'; c.bevel_depth=r;c.bevel_resolution=2
    s=c.splines.new('POLY'); s.points.add(len(points)-1)
    for p,co in zip(s.points,points):p.co=(*co,1)
    o=bpy.data.objects.new(name,c);current.objects.link(o);c.materials.append(mat);return o
def bolt(name,x,y,z,r=.045,axis=(0,-1,0)):
    v=Vector(axis);a=Vector((x,y,z));cylinder(name+' • hex socket',a,a+v*.018,r,steel,6)
    cylinder(name+' • bore',a+v*.018,a+v*.023,r*.39,black,12)
def label(name, text,loc,size=.1,mat=white,rotation=(math.pi/2,0,0),align='CENTER'):
    c=bpy.data.curves.new(name,'FONT');c.body=text;c.size=size;c.align_x=align;c.extrude=.0007;c.space_character=1.1
    o=bpy.data.objects.new(name,c);current.objects.link(o);o.location=loc;o.rotation_euler=rotation;c.materials.append(mat);return o
def vent(name,center,w,h,rows=5,mat=steel):
    x,y,z=center;box(name+' • recess',(x,y,z),(w,.08,h),black,.04)
    for i in range(rows):box(name+' • vane %02d'%i,(x,y-.045,z-h*.38+i*h*.76/max(1,rows-1)),(w*.78,.065,h/(rows*2.1)),mat,.009,rot=(.2,0,0))

# TORSO: a compact skeleton under independently layered armor.
box('Central thoracic chassis',(0,.05,7.25),(2.45,1.45,2.12),graphite,.22)
beam('Sternum structural spine',(0,.2,5.35),(0,.2,8.6),.82,.85,steel,1)
for s in (-1,1):
    sphere('Upper torso swivel',(s*.97,.1,7.7),(.55,.64,.64),rubber)
    symplate('Pectoral outer frame',s,[(.18,8.12),(1.1,8.28),(1.58,7.8),(1.46,6.8),(.69,6.48),(.34,7.04)],-.85,.15,graphite,.09)
    symplate('Pectoral teal shell',s,[(.32,8.01),(1.08,8.13),(1.43,7.72),(1.32,7.08),(.65,6.91),(.4,7.28)],-.98,-.6,teal,.065)
    symplate('Chest gold intake surround',s,[(.44,7.55),(1.36,7.77),(1.4,7.26),(.48,7.03)],-1.10,-.94,gold,.045)
    symplate('Chest intake recessed aperture',s,[(.57,7.45),(1.23,7.59),(1.25,7.34),(.58,7.2)],-1.147,-1.095,black,.028)
    for k in range(3):
        line('Chest intake • grille',[(s*.61,-1.17,7.26+k*.075),(s*1.20,-1.17,7.39+k*.075)],steel,.015)
    symplate('Collar alloy cap',s,[(.30,8.12),(.6,8.5),(1.2,8.54),(1.44,8.25),(1.26,8.05)],-.72,-.25,steel,.045)
    symplate('Collar gold line',s,[(.28,8.08),(.42,8.5),(.55,8.44),(.46,8.02)],-.88,-.70,gold,.024)
    for x,z in [(1.22,7.99),(1.3,6.96),(.55,7.84)]:bolt('Chest fastener',s*x,-1.005,z,.032)
    cylinder('Rib piston sleeve',(s*.83,-.18,5.7),(s*1.11,-.18,6.61),.14,graphite)
    cylinder('Rib piston rod',(s*.79,-.18,5.6),(s*1.11,-.18,6.61),.07,silver)
    for j in range(3):
        symplate('Floating abdominal rib',s,[(.27,6.8-j*.32),(.87,6.81-j*.3),(1.02,6.58-j*.3),(.6,6.35-j*.3),(.31,6.4-j*.3)],-.57+j*.06,.05,steel,.035)
plate('Sternum gold cradle',[(-.39,7.97),(.39,7.97),(.62,7.37),(.5,6.83),(0,6.48),(-.5,6.83),(-.62,7.37)],-1.025,-.4,gold,.05)
plate('Upper sternum ceramic',[(-.29,7.98),(.29,7.98),(.36,7.65),(.21,7.37),(-.21,7.37),(-.36,7.65)],-1.12,-1.03,graphite,.04)
plate('Reactor • armored bezel',[(-.31,7.28),(.31,7.28),(.5,6.94),(.29,6.55),(-.29,6.55),(-.5,6.94)],-1.14,-.7,black,.035)
plate('Reactor • faceted emerald',[(-.22,7.17),(.22,7.17),(.33,6.94),(.17,6.72),(-.17,6.72),(-.33,6.94)],-1.205,-1.12,green,.027)
plate('Lower torso keel',[(-.39,6.49),(.39,6.49),(.33,6.16),(.19,5.94),(-.19,5.94),(-.33,6.16)],-.74,-.25,graphite,.04)
for j in range(3):box('Abdominal center inset',(0,-.80,6.17+j*.075),(.34,.04,.026),steel,.004)
label('Chest identification','PH / 07',(.94,-1.022,7.87),.10)
label('Chest service stencil','REACTOR',(-.91,-1.028,7.87),.065)

current=group('02 | Pelvis and legs')
cylinder('Waist azimuth bearing',(0,0,5.27),(0,0,5.76),.67,black,48)
for z in [5.36,5.49,5.63]:torus('Waist bearing race',(0,0,z),.65,.035,steel)
box('Pelvic frame',(0,.12,4.99),(2.12,1.04,.96),graphite,.17)
plate('Pelvic central armor',[(-.43,5.51),(.43,5.51),(.53,5.13),(.36,4.76),(-.36,4.76),(-.53,5.13)],-.69,-.22,teal,.06)
plate('Belt warning bezel',[(-.22,5.48),(.22,5.48),(.27,5.2),(.14,5.02),(-.14,5.02),(-.27,5.2)],-.79,-.67,gold_dark,.025)
plate('Belt signal jewel',[(-.15,5.40),(.15,5.40),(.18,5.20),(.10,5.09),(-.10,5.09),(-.18,5.20)],-.835,-.77,red,.022)
plate('Central codpiece',[(-.31,4.96),(.31,4.96),(.35,4.27),(.18,4.12),(-.18,4.12),(-.35,4.27)],-.7,-.05,graphite,.045)
vent('Pelvis cooling slots',(0,-.753,4.39),.31,.35,4)
for s in (-1,1):
    hip=(s*.88,.12,4.72);knee=(s*1.25,-.05,3.03);ankle=(s*1.46,.12,.94)
    sphere('Hip universal joint',hip,(.46,.48,.46),rubber)
    cylinder('Hip bearing',(s*.93,-.18,4.67),(s*1.43,-.18,4.67),.30,steel,24)
    beam('Femur • chassis',hip,knee,.66,.71,graphite)
    beam('Thigh • full armor',(s*.95,.03,4.63),(s*1.21,-.06,3.27),.94,.99,teal,.8)
    symplate('Thigh front segmented shell',s,[(.65,4.47),(1.3,4.52),(1.56,3.72),(1.32,3.19),(.86,3.49)],-.65,-.38,teal,.065)
    symplate('Thigh center inlay',s,[(.84,4.36),(1.2,4.32),(1.37,3.72),(1.22,3.45),(1.01,3.62)],-.716,-.65,blue,.027)
    line('Thigh recessed panel seam',[(s*.81,-.731,4.17),(s*1.00,-.731,3.71),(s*1.14,-.731,3.60)],darkteal,.025)
    symplate('Skirt • outer floating armor',s,[(1.13,5.31),(1.46,5.13),(1.83,3.98),(1.56,4.08),(1.08,4.59)],-.13,.48,darkteal,.06)
    symplate('Skirt • front plate black gasket',s,[(.45,5.28),(.91,5.49),(1.4,5.21),(1.22,4.40),(.7,4.1),(.43,4.45)],-.86,-.35,black,.05)
    symplate('Skirt • front teal shield',s,[(.49,5.22),(.94,5.39),(1.32,5.15),(1.15,4.47),(.74,4.22),(.51,4.49)],-.935,-.85,teal,.042)
    symplate('Skirt • faceted inlay',s,[(.71,5.05),(1.12,5.14),(1.02,4.59),(.76,4.43),(.66,4.57)],-.991,-.935,blue,.025)
    line('Skirt engraved perimeter',[(s*.6,-1.019,5.16),(s*.72,-1.019,5.21),(s*1.19,-1.019,5.02)],steel,.012)
    for x,z in [(.60,5.13),(1.08,4.5)]:bolt('Skirt captive bolt',s*x,-1.005,z,.027)
    label('Skirt serial','07' if s==1 else 'PH',(s*.96,-1.022,4.75),.15)
    cylinder('Knee • lateral axis',(s*1.25-.51,0,3.01),(s*1.25+.51,0,3.01),.33,graphite)
    cylinder('Knee • exposed alloy bearing',(s*1.25+s*.48,0,3.01),(s*1.25+s*.56,0,3.01),.21,steel)
    bolt('Knee axial bolt',s*1.25+s*.57,0,3.01,.083,(s,0,0))
    symplate('Knee • raised kneecap',s,[(1.04,3.43),(1.38,3.48),(1.61,2.91),(1.44,2.57),(1.06,2.73),(.97,3.07)],-.72,-.18,blue,.065)
    symplate('Knee • gold marker',s,[(1.13,3.44),(1.32,3.46),(1.38,3.29),(1.24,3.16),(1.11,3.24)],-.80,-.69,gold,.025)
    beam('Tibia • chassis',(s*1.28,.12,2.79),ankle,.65,.69,graphite,.75)
    beam('Shin • main armored greave',(s*1.3,.05,2.72),(s*1.46,.10,1.12),1.02,1.05,teal,.72)
    symplate('Calf • outer graphite guard',s,[(1.49,2.75),(1.82,2.6),(1.86,2.02),(1.6,1.39),(1.42,1.64),(1.38,2.27)],-.34,.56,graphite,.075)
    symplate('Calf • inner graphite guard',s,[(1.0,2.72),(.82,2.49),(.86,1.96),(1.09,1.51),(1.21,1.79),(1.2,2.43)],-.18,.48,graphite,.06)
    symplate('Shin • gold knee guard',s,[(.99,2.77),(1.22,2.64),(1.54,2.8),(1.56,2.46),(1.35,2.21),(1.10,2.29)],-.70,-.24,gold,.045)
    symplate('Shin • central long panel',s,[(1.15,2.29),(1.48,2.37),(1.53,1.41),(1.75,1.09),(1.56,.85),(1.14,1.02),(1.10,1.3)],-.68,-.4,teal,.05)
    line('Shin • routed seam',[(s*1.23,-.744,2.11),(s*1.25,-.744,1.46),(s*1.45,-.744,1.2)],blue,.022)
    for k in range(3):box('Shin • gold service ticks',(s*1.74,-.397,2.08-k*.09),(.055,.02,.045),gold,.006)
    cylinder('Rear lower-leg hydraulic outer',(s*1.24,.55,1.23),(s*1.12,.55,2.52),.105,graphite)
    cylinder('Rear lower-leg hydraulic polished rod',(s*1.12,.55,2.18),(s*1.06,.55,2.79),.06,silver)
    for zz in [1.3,1.51]:box('Calf rear luminous vent',(s*1.51,.656,zz),(.17,.055,.14),cyan,.022)
    sphere('Ankle joint',ankle,(.34,.35,.30),rubber)
    cylinder('Ankle outer pivot',(s*1.46+s*.21,.09,1.00),(s*1.46+s*.4,.09,1.00),.21,steel)
    # feet: broad wedge with a forward toe and separate armored instep.
    x=s*1.48
    vs=[(x-.49,-1.05,.18),(x+.49,-1.05,.18),(x+.47,.72,.18),(x-.47,.72,.18),
        (x-.45,-1.03,.43),(x+.45,-1.03,.43),(x+.42,.55,.77),(x-.42,.55,.77)]
    mesh('Foot • armored wedge sole',vs,[(0,3,2,1),(0,1,5,4),(1,2,6,5),(2,3,7,6),(3,0,4,7),(4,5,6,7)],graphite,.07)
    box('Foot • rubber tread base',(x,-.13,.14),(.97,1.81,.2),rubber,.06)
    for yy in [-.85,-.58,-.31,.02,.32,.58]:box('Foot • sole tread',(x,yy,.10),(1.01,.10,.10),black,.013)
    box('Foot • toe alloy cap',(x,-.69,.49),(.69,.59,.14),silver,.055,rot=(.17,0,0))
    box('Foot • dorsal teal plate',(x,-.14,.73),(.69,.71,.22),teal,.08,rot=(.22,0,0))
    box('Foot • heel block',(x,.58,.48),(.67,.43,.51),graphite,.055)
    for xx in [-.37,.37]:bolt('Foot toe fastener',x+xx,-1.043,.36,.036)

current=group('03 | Helmet and antennae')
cylinder('Neck • swivel column',(0,0,8.17),(0,0,8.88),.31,graphite)
for z in [8.52,8.65,8.79]:torus('Neck • bearing race',(0,0,z),.30,.04,steel)
box('Helmet • central head shell',(0,0,9.21),(1.17,1.0,1.29),teal,.20)
plate('Helmet • crown faceted brow',[(-.61,9.25),(-.64,9.6),(-.37,9.99),(.37,9.99),(.64,9.6),(.61,9.25),(0,9.39)],-.53,.32,teal,.055)
plate('Helmet • brow center face',[(-.46,9.67),(0,9.87),(.46,9.67),(.42,9.47),(0,9.37),(-.42,9.47)],-.63,-.48,blue,.038)
plate('Helmet • visor dark aperture',[(-.52,9.38),(0,9.27),(.52,9.38),(.43,8.97),(0,8.79),(-.43,8.97)],-.65,-.39,black,.035)
for s in (-1,1):
    symplate('Helmet • cheek armor',s,[(.39,9.26),(.57,9.38),(.62,8.86),(.37,8.72),(.26,8.95)],-.70,-.1,graphite,.035)
    symplate('Helmet • cheek machined insert',s,[(.31,9.08),(.43,9.22),(.45,8.91),(.3,8.82),(.19,8.91)],-.772,-.68,silver,.018)
    symplate('Optic • amber slit',s,[(.08,9.25),(.42,9.32),(.34,9.17),(.12,9.14)],-.726,-.66,amber,.012)
    symplate('Optic • upper armored brow',s,[(.04,9.36),(.50,9.46),(.53,9.38),(.10,9.26)],-.77,-.63,graphite,.018)
    box('Helmet • temporal module',(s*.64,0,9.2),(.21,.64,.64),darkteal,.07)
    vent('Helmet • side respirator',(s*.59,-.345,9.05),.16,.32,4)
    cylinder('Antenna • gold swept horn',(s*.26,-.11,9.64),(s*.7,.01,10.68),.12,gold,6,.021)
    cylinder('Antenna • horn socket',(s*.22,-.11,9.55),(s*.31,-.08,9.83),.15,gold_dark,12,.1)
    symplate('Helmet • V-fin',s,[(.05,9.5),(.20,9.41),(.92,10.13),(.47,9.89)],-.84,-.68,silver,.015)
    bolt('Helmet • temporal mounting',s*.54,-.4,9.14,.042)
plate('Helmet • forehead central crest',[(-.12,9.48),(.12,9.48),(.17,10.07),(.09,10.24),(-.09,10.24),(-.17,10.07)],-.62,-.06,darkteal,.03)
box('Helmet • forehead sensor',(0,-.69,9.92),(.19,.12,.29),graphite,.025)
box('Helmet • forehead emerald glass',(0,-.756,9.95),(.115,.025,.15),green,.014)
plate('Helmet • central face mask',[(-.12,9.19),(.12,9.19),(.19,8.94),(.1,8.82),(-.1,8.82),(-.19,8.94)],-.83,-.57,silver,.022)
plate('Helmet • red chin',[(-.09,9.04),(.09,9.04),(.13,8.85),(0,8.73),(-.13,8.85)],-.91,-.78,red,.023)

current=group('04 | Shoulders and arms')
for s in (-1,1):
    shoulder=(s*1.86,.03,7.92); elbow=(s*2.23,-.02,6.63); wrist=(s*2.63,-.32,5.42)
    cylinder('Shoulder • axle',(s*1.18,.08,7.93),(s*2.16,.08,7.93),.36,steel)
    sphere('Shoulder • ball joint',shoulder,(.48,.49,.51),graphite)
    symplate('Pauldron • swept main shell',s,[(1.34,8.61),(2.87,9.02),(3.22,9.02),(3.09,8.61),(2.42,8.02),(1.66,7.89)],-.42,.76,teal,.075)
    symplate('Pauldron • facet cap',s,[(1.48,8.64),(2.05,8.82),(2.31,8.55),(1.63,8.19)],-.49,-.4,blue,.035)
    symplate('Pauldron • outer facet',s,[(2.18,8.85),(3.08,8.95),(2.96,8.62),(2.4,8.36)],-.49,-.4,teal,.035)
    symplate('Pauldron • gold wing rail',s,[(1.56,8.31),(1.91,8.5),(3.16,8.72),(3.06,8.48),(2.01,7.99),(1.65,7.9)],-.59,-.33,gold,.042)
    symplate('Pauldron • dark lower wing',s,[(1.82,8.09),(2.97,8.48),(2.79,8.05),(2.21,7.66),(1.92,7.65)],-.37,.44,graphite,.05)
    symplate('Pauldron • shoulder cup',s,[(1.47,8.15),(1.80,8.29),(2.13,7.96),(2.04,7.43),(1.66,7.49),(1.4,7.85)],-.78,-.27,graphite,.085)
    symplate('Pauldron • inset face',s,[(1.55,8.07),(1.79,8.16),(2.01,7.93),(1.94,7.59),(1.7,7.65),(1.54,7.87)],-.875,-.78,steel,.035)
    for x,z in [(1.71,7.79),(2.63,8.67)]:bolt('Shoulder • countersunk fastener',s*x,-.90 if x<2 else -.505,z,.04)
    for k in range(2):
        symplate('Shoulder • trailing auxiliary fin',s,[(2.2+k*.27,8.12),(2.44+k*.27,8.05),(2.62+k*.27,7.39),(2.32+k*.27,7.60)],.40,.66,darkteal,.038)
    label('Pauldron • unit stencil','PHANTOM' if s==1 else 'N-07',(s*2.49,-.515,8.72),.1)
    beam('Humerus • central actuator',shoulder,elbow,.51,.56,graphite)
    beam('Upper arm • teal sleeve',(s*1.98,0,7.69),(s*2.18,-.015,6.92),.75,.80,teal,.85)
    symplate('Upper arm • front inlay',s,[(1.75,7.44),(2.24,7.45),(2.32,7.07),(2.06,6.82),(1.82,7.03)],-.466,-.3,blue,.033)
    for k in range(2):
        cylinder('Elbow • exposed hydraulic ram',(s*(2.02+k*.23),-.30,6.98),(s*(2.14+k*.23),-.30,6.51),.071,silver)
    cylinder('Elbow • pivot',(s*2.23-.39,-.02,6.65),(s*2.23+.39,-.02,6.65),.27,graphite)
    cylinder('Elbow • gold bearing',(s*(2.23+.4),-.02,6.65),(s*(2.23+.44),-.02,6.65),.18,gold_dark)
    beam('Forearm • structural frame',elbow,wrist,.66,.74,graphite)
    beam('Forearm • bulky teal gauntlet',(s*2.28,-.07,6.45),(s*2.59,-.29,5.54),1.01,.96,teal,.72)
    symplate('Forearm • sculpted face plate',s,[(2.01,6.47),(2.5,6.56),(2.81,5.72),(2.68,5.40),(2.26,5.51),(2.08,5.99)],-.72,-.5,blue,.055)
    symplate('Forearm • central graphite insert',s,[(2.15,6.24),(2.4,6.30),(2.61,5.77),(2.52,5.6),(2.33,5.69)],-.787,-.72,graphite,.034)
    line('Forearm • cyan status strip',[(s*2.14,-.795,6.39),(s*2.49,-.795,6.47)],cyan,.026)
    line('Forearm • engraved lower seam',[(s*2.30,-.806,5.82),(s*2.43,-.806,5.49)],teal,.024)
    cylinder('Wrist • articulated coupling',(s*2.6,-.3,5.49),(s*2.7,-.35,5.18),.32,steel)
    for j in range(3):torus('Wrist • flexible seal',(s*(2.65+j*.022),-.335,5.32-j*.065),.28,.029,rubber)
    box('Hand • armored metacarpus',(s*2.73,-.34,5.02),(.55,.57,.55),graphite,.085)
    for f in range(4):
        xx=s*(2.52+f*.135)
        box('Hand • individual knuckle',(xx,-.647,5.06),(.113,.14,.18),steel,.027)
        box('Hand • curled finger proximal',(xx,-.64,4.87),(.116,.17,.18),graphite,.025)
        box('Hand • curled finger tip',(xx,-.53,4.73),(.116,.23,.13),graphite,.025)
    box('Hand • articulated thumb',(s*2.44,-.54,4.95),(.2,.24,.31),steel,.04,rot=(0,s*-.35,0))
    symplate('Gauntlet • tiny gold trim',s,[(2.81,5.82),(2.94,5.78),(2.84,5.5),(2.76,5.49)],-.49,-.3,gold,.018)

current=group('05 | Backpack and twin cannons')
box('Backpack • main reactor housing',(0,1.03,7.39),(2.33,.92,1.86),graphite,.17)
box('Backpack • spine armor',(0,1.56,7.37),(.78,.29,1.61),darkteal,.10)
for s in (-1,1):
    box('Backpack • radiator pod',(s*.78,1.54,7.40),(.59,.33,1.26),steel,.08)
    for k in range(3):box('Backpack • cyan grille',(s*.79,1.724,7.48+k*.14),(.31,.038,.064),cyan,.01)
    for k in range(4):box('Backpack • lower exhaust slat',(s*.77,1.73,7.03+k*.085),(.32,.04,.027),black,.007)
    # Swept vertical cannon silhouette matches the frontal asset-sheet view.
    a=Vector((s*1.36,.86,8.22));b=Vector((s*1.36,-.04,11.15));axis=(b-a).normalized()
    beam('Cannon • pivot support',(s*.95,1.04,7.76),a,.51,.58,steel,1)
    cylinder('Cannon • tilt trunnion',(s*1.02,.83,8.59),(s*1.73,.83,8.59),.36,graphite)
    cylinder('Cannon • tilt trunnion cap',(s*1.7,.83,8.59),(s*1.81,.83,8.59),.25,steel)
    beam('Cannon • main armored barrel',a,b,.83,.90,steel,.92)
    beam('Cannon • dorsal rail',a+Vector((0,.40,.1)),b+Vector((0,.37,-.02)),.30,.16,graphite,1)
    beam('Cannon • teal front inset',a+Vector((0,-.43,.3)),b+Vector((0,-.40,-.36)),.49,.10,darkteal,.8)
    beam('Cannon • inner raised rail',a+Vector((s*.41,0,.35)),b+Vector((s*.38,0,-.32)),.09,.42,graphite,.9)
    tip=b+axis*.12
    beam('Cannon • heavy muzzle shroud',b-axis*.37,b+axis*.19,1.01,1.07,graphite,.92)
    # Muzzle bores point along the cannon axis, with a rectangular ventral face too.
    q=axis.to_track_quat('Z','Y');xx=q@Vector((1,0,0));yy=q@Vector((0,1,0))
    for k in [-1,1]:
        end=b+axis*.213+yy*(k*.20)
        cylinder('Cannon • recessed muzzle',end-axis*.015,end+axis*.025,.17,black,24)
        torus('Cannon • muzzle retaining ring',end+axis*.03,.158,.024,steel,axis)
        cylinder('Cannon • recessed red chamber',end+axis*.028,end+axis*.032,.075,red,24)
    # Front-facing receiver plate: distinct paired bores in the front silhouette.
    box('Cannon • frontal muzzle mask',(s*1.36,-.505,10.90),(.62,.1,.57),black,.10)
    for k in [-1,1]:
        cylinder('Cannon • frontal twin aperture',(s*1.36,-.567,10.9+k*.13),(s*1.36,-.589,10.9+k*.13),.089,gold_dark,24)
        cylinder('Cannon • frontal aperture bore',(s*1.36,-.59,10.9+k*.13),(s*1.36,-.593,10.9+k*.13),.055,black,24)
    box('Cannon • status module',(s*1.36,.262,9.30),(.3,.16,.44),graphite,.045)
    box('Cannon • cyan status strip',(s*1.36,.171,9.31),(.12,.025,.23),cyan,.02)
    for k in range(4):
        bolt('Cannon • receiver bolt',s*(1.36+.28),-.223+k*.075,9.73-k*.24,.034)
    # Articulated rocket nozzles and rings; emission stays compact for studio rendering.
    a=Vector((s*.71,1.39,7.02));b=Vector((s*.85,1.80,6.19));axis=(b-a).normalized()
    cylinder('Thruster • armored base',a,b,.30,graphite,32,.38)
    cylinder('Thruster • titanium nozzle',b-axis*.17,b,.39,steel,32,.35)
    cylinder('Thruster • black nozzle cavity',b,b+axis*.035,.28,black)
    torus('Thruster • glowing lip',b+axis*.044,.237,.038,cyan,axis)
    cylinder('Thruster • ion core',b+axis*.024,b+axis*.11,.20,cyan,32,.16)
    cylinder('Thruster • tapered ion plume',b+axis*.11,b+axis*.62,.16,cyan,32,.013)
    for k in range(4):
        box('Backpack • trunnion cooling fin',(s*1.17,1.4,8.07+k*.12),(.23,.46,.045),graphite,.01)
torus('Backpack • reactor circular frame',(0,1.759,7.65),.32,.063,gold,(0,1,0))
cylinder('Backpack • reactor center',(0,1.7,7.65),(0,1.78,7.65),.23,black)
line('Backpack • power glyph',[(.14*math.cos(a),1.803,7.65+.14*math.sin(a)) for a in [math.radians(135+i*9) for i in range(31)]],amber,.027)
line('Backpack • power glyph stem',[(0,1.813,7.71),(0,1.813,7.91)],amber,.033)
box('Backpack • lower spine guard',(0,1.3,6.61),(.55,.48,.72),graphite,.08)
for k in range(4):box('Backpack • lower spine vent',(0,1.552,6.42+k*.12),(.29,.035,.052),black,.009)

current=group('06 | Rifle and energized blade')
# Long left-arm rifle with two muzzles, fore-end rails, cell, trigger and magazine.
rear=Vector((-2.81,-.76,6.38));tip=Vector((-3.83,-1.11,2.95));axis=(tip-rear).normalized()
beam('Rifle • primary receiver',rear,tip-axis*.71,.76,.84,steel,.8)
beam('Rifle • barrel outer shroud',rear+axis*1.52,tip,.58,.67,darkteal,.85)
beam('Rifle • front machined rail',rear+Vector((0,-.45,0))+axis*.39,tip+Vector((0,-.35,0))-axis*.52,.15,.095,silver,.85)
beam('Rifle • longitudinal upper rail',rear+Vector((-.41,0,0)),tip+Vector((-.31,0,0))-.36*axis,.16,.3,graphite,.85)
beam('Rifle • muzzle block',tip-axis*.38,tip+axis*.16,.72,.78,graphite,.86)
q=axis.to_track_quat('Z','Y');yy=q@Vector((0,1,0))
for s in [-1,1]:
    pos=tip+axis*.18+yy*(s*.15)
    cylinder('Rifle • bore collar',pos,pos+axis*.06,.13,steel,32)
    cylinder('Rifle • deep bore',pos+axis*.061,pos+axis*.067,.091,black,32)
beam('Rifle • battery magazine',(-2.68,-.51,5.89),(-2.31,-.40,5.48),.45,.6,graphite,.9)
box('Rifle • cell status inset',(-2.63,-1.188,5.81),(.17,.043,.24),black,.025)
for k in range(3):box('Rifle • amber charge meter',(-2.63,-1.215,5.74+k*.063),(.1,.018,.025),amber,.005)
beam('Rifle • underbarrel auxiliary tube',(-3.11,-.64,5.73),(-3.72,-.85,3.43),.29,.31,graphite,.8)
beam('Rifle • shoulder scope',(-2.73,-.72,6.39),(-2.95,-.80,5.84),.39,.35,graphite,.85)
for k in range(5):
    p=rear+axis*(.6+k*.16)+Vector((-.21,-.45,0));box('Rifle • receiver cooling slit',p,(.18,.028,.038),black,.006,rot=(0,.28,0))
label('Rifle • armament stencil','K-09',(-3.17,-1.191,4.53),.12,rotation=(math.pi/2,0,-.29))

# Right arm-mounted shield / blade. Asymmetric steel spine and a narrow luminous edge.
plate('Blade • forearm mounting shield',[(2.70,6.57),(2.96,6.35),(3.21,5.35),(3.06,4.89),(2.87,5.23),(2.72,6.04)],-.36,.14,graphite,.046)
plate('Blade • mounting shield silver face',[(2.83,6.37),(2.93,6.20),(3.1,5.40),(3.02,5.20),(2.94,5.4)],-.42,-.35,steel,.03)
plate('Blade • gold throat',[(2.96,5.26),(3.13,5.33),(3.24,5.07),(3.06,4.99)],-.49,-.25,gold,.022)
blade_pts=[(3.11,5.05),(3.25,4.87),(3.53,3.94),(3.89,3.02),(4.10,2.23),(4.11,1.82),(3.85,2.19),(3.62,2.94),(3.26,3.91),(3.03,4.80)]
plate('Blade • full forged alloy profile',blade_pts,-.45,-.25,silver,.022,graphite)
plate('Blade • dark reinforced spine',[(3.07,4.85),(3.16,4.88),(3.45,3.94),(3.80,3.01),(4.02,2.22),(3.88,2.44),(3.67,3.05),(3.34,3.95)],-.493,-.44,steel,.014)
plate('Blade • energized cutting edge',[(3.24,4.9),(3.31,4.68),(3.59,3.9),(3.94,2.99),(4.14,2.22),(4.11,1.82),(4.06,2.24),(3.83,3.02),(3.48,3.96),(3.19,4.9)],-.473,-.43,ice,.009)
for k in range(3):bolt('Blade • spine rivet',3.20+k*.20,-.512,4.47-k*.55,.025)

# Additional rear waist panels and armored cables.
current=group('07 | Rear service detail')
for s in (-1,1):
    symplate('Rear skirt • layered petal',s,[(.23,5.18),(1.15,5.1),(1.31,4.48),(.64,4.30),(.28,4.57)],.61,1.00,darkteal,.045)
    box('Rear skirt • teal insert',(s*.71,1.017,4.77),(.59,.09,.44),teal,.07)
    for k in range(3):box('Rear skirt • vent',(s*.69,1.067,4.67+k*.08),(.37,.025,.027),black,.005)
    line('Power cable • armored route',[(s*.78,1.1,6.37),(s*1.03,.95,6.00),(s*.96,.63,5.66),(s*.68,.48,5.48)],rubber,.075)
    for k in range(2):cylinder('Rear thigh • actuator',(s*(.89+k*.3),.51,3.5),(s*(.79+k*.3),.51,4.35),.065,silver)
    label('Rear backpack • caution','HOT / EXHAUST',(s*.72,1.741,7.21),.059,rotation=(math.pi/2,0,math.pi))

# STUDIO: restrained dark exhibition stage, broad reflections, warm / cool rim lights.
current=group('90 | Studio')
floor=material('STUDIO • charcoal floor','151F2C',.22,.39)
stage=material('STUDIO • platform','202C36',.72,.32)
cylinder('Display plinth',(0,0,-.30),(0,0,-.03),5.40,stage,128)
torus('Plinth • outer silver reveal',(0,0,-.08),5.33,.018,steel)
torus('Plinth • cyan inset guide',(0,0,-.019),4.90,.012,cyan)
for i in range(48):
    a=i*math.tau/48
    box('Plinth • radial tick',(5.13*math.sin(a),5.13*math.cos(a),-.019),(.022,.13 if i%4==0 else .064,.009),gold if i%4==0 else steel,.002,rot=(0,0,-a))
box('Studio ground',(0,0,-.42),(200,200,.2),floor,.02)
label('Plinth • front designation','P H A N T O M', (0,-4.15,-.012),.32,white,rotation=(0,0,0))
label('Plinth • front specification','MECHA UNIT   /   N-07', (0,-4.53,-.012),.13,steel,rotation=(0,0,0))

def area(name,loc,target,power,color,size,shape='DISK',size_y=None):
    d=bpy.data.lights.new(name,'AREA'); d.energy=power; d.color=rgb(color);d.shape=shape;d.size=size
    if shape=='RECTANGLE':d.size_y=size_y or size
    o=bpy.data.objects.new(name,d);current.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();return o
area('Key • large neutral softbox',(3,-9,15),(0,0,6.0),2400,'E4F0FF',8,'DISK')
area('Fill • tall left strip',(-7,-5,8),(0,0,6),1800,'8FCAE0',6,'RECTANGLE',10)
area('Rim • cold edge',(5,4,11),(0,0,6),3000,'6BCEFF',6,'RECTANGLE',9)
area('Rim • warm left',(-5,4,10),(0,0,6),2600,'FFD29A',5,'RECTANGLE',8)
area('Front • helmet catchlight',(0,-7,10),(0,0,8),800,'FFFFFF',4)
area('Top • overhead',(0,1,16),(0,0,5),1900,'EDF3FF',5)
scene=bpy.context.scene
scene.world=bpy.data.worlds.new('Midnight studio ambient');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(*rgb('8196B2'),1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.26

current=group('91 | Cameras')
def camera(name,loc,target,ortho):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);current.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=ortho;d.lens=55;return o
hero=camera('CAM 01 • Hero',(15,-28,14.6),(0,0,5.5),14.35)
front=camera('CAM 02 • Front',(0,-28,7.7),(0,0,5.6),13.5)
rearcam=camera('CAM 03 • Rear',(-15,26,13.4),(0,.2,5.5),14.1)
detail=camera('CAM 04 • Helmet and torso',(10,-23,12.2),(0,-.1,8.25),7.0)
sidecam=camera('CAM 05 • Side',(24,0,8),(0,0,5.6),13.5)
scene.camera=hero

current=group('99 | Reference (non-rendering)')
ref=bpy.data.images.load(REFERENCE);ref.pack()
o=bpy.data.objects.new('Original image • front / side / rear',None);current.objects.link(o);o.empty_display_type='IMAGE';o.data=ref;o.empty_display_size=16;o.location=(0,4,6);o.rotation_euler=(math.pi/2,0,0);o.hide_render=True;o.hide_viewport=True

scene.render.engine='CYCLES'
scene.cycles.samples=96
scene.cycles.use_denoising=True
scene.cycles.preview_samples=24
scene.cycles.max_bounces=7
scene.cycles.diffuse_bounces=3
scene.cycles.glossy_bounces=4
scene.cycles.transparent_max_bounces=4
scene.cycles.adaptive_threshold=.035
p=bpy.context.preferences.addons['cycles'].preferences
try:
    p.compute_device_type='METAL';p.get_devices()
    for d in p.devices:d.use=d.type=='METAL'
    scene.cycles.device='GPU'
except Exception:scene.cycles.device='CPU'
scene.render.resolution_x=1600;scene.render.resolution_y=1800;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.image_settings.color_depth='8'
scene.render.film_transparent=False
scene.view_settings.view_transform='AgX'
try:scene.view_settings.look='AgX - Medium High Contrast'
except:pass
scene.view_settings.exposure=.7
scene.render.filepath=os.path.join(OUT,'phantom_hero.png')
scene['PROJECT']='PHANTOM / N-07 — modeled from supplied character sheet'
scene['MODEL_NOTES']='Detailed hard-surface interpretation; separate meshes and materials. No rig, UV unwrap, or animation.'
scene['REFERENCE']=REFERENCE
scene['DELIVERABLES']='Hero, rear and detail renders; editable native scene; rebuild script.'
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.region_3d.view_perspective='CAMERA'
            a.spaces.active.shading.type='MATERIAL'
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha.blend'))
print('PHANTOM_BUILD_COMPLETE',len([o for o in scene.objects if o.type=='MESH']),'mesh objects',flush=True)
if '--preview' in sys.argv:
    scene.render.resolution_percentage=48;scene.cycles.samples=24;scene.cycles.adaptive_threshold=.07
    scene.render.filepath=os.path.join(OUT,'preview.png');bpy.ops.render.render(write_still=True)
elif '--render' in sys.argv:
    bpy.ops.render.render(write_still=True)
print('PHANTOM_DONE',flush=True)
