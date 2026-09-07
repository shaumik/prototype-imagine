import bpy, bmesh, math, os, sys, json
from mathutils import Vector, Matrix
OUT=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,OUT)
import mechanical as M
from mechanical import *
scene=bpy.context.scene

# Coated armor and dark machined metal share restrained, physically based finishes.
def finish(name,color,metal,rough):
    m=material('V4 / '+name,color,metal,rough)
    ns=m.node_tree.nodes;lk=m.node_tree.links;p=ns.get('Principled BSDF')
    n=ns.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=290;n.inputs['Detail'].default_value=2
    ramp=ns.new('ShaderNodeMapRange');ramp.inputs['To Min'].default_value=rough-.045;ramp.inputs['To Max'].default_value=rough+.045
    lk.new(n.outputs['Fac'],ramp.inputs['Value']);lk.new(ramp.outputs[0],p.inputs['Roughness'])
    b=ns.new('ShaderNodeBump');b.inputs['Strength'].default_value=.09;b.inputs['Distance'].default_value=.0011
    lk.new(n.outputs['Fac'],b.inputs['Height']);lk.new(b.outputs['Normal'],p.inputs['Normal'])
    return m
teal=finish('petrol ceramic coating','29434B',.43,.40)
teal2=finish('blue teal panel coating','3B555E',.46,.41)
gold=finish('muted bronze trim','947448',.74,.42)
bronze=finish('recessed bronze mechanism','51473A',.77,.41)
frame=finish('black phosphate chassis','272E34',.58,.42)
steel=finish('machined bearing steel','56636B',.83,.35)
black=finish('internal graphite','10161B',.27,.50)
mouth=finish('satin titanium face plate','758482',.61,.42)
for k in ['teal','teal2','gold','bronze','frame','steel','black','mouth']:setattr(M,k,globals()[k])
for ob in scene.objects:
    if not hasattr(ob.data,'materials'):continue
    for slot in ob.material_slots:
        mat=slot.material
        if not mat:continue
        n=mat.name.lower()
        if any(t in n for t in ['studio','optic','emitter','crystal','signal','stencil','markings']):continue
        if any(t in n for t in ['bronze trim','champagne','brushed bronze']):slot.material=gold
        elif 'bronze' in n:slot.material=bronze
        elif any(t in n for t in ['deep teal','recess','flexible boot']):slot.material=black
        elif any(t in n for t in ['blue steel','edge armor']):slot.material=teal2
        elif any(t in n for t in ['petrol','teal']):slot.material=teal
        elif any(t in n for t in ['satin alloy','mask satin']):slot.material=mouth
        elif any(t in n for t in ['gunmetal','exposed alloy','finger bearings']):slot.material=steel
        elif any(t in n for t in ['graphite','titanium','cannon chassis']):slot.material=frame

# Replace domed panel fans with clean planar faces and small manufactured edge radii.
cleaned=0
for ob in list(scene.objects):
    if ob.type!='MESH' or not any(m.name=='Panel highlight control' for m in ob.modifiers):continue
    vs=ob.data.vertices;n=(len(vs)-1)//5
    if len(vs)!=n*5+1 or n<8:continue
    front=[v.co.copy()+Vector((0,-.018,0)) for v in vs[2*n:3*n]]
    back=[v.co.copy() for v in vs[:n]]
    faces=[tuple(range(n)),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    mats=list(ob.data.materials);me=bpy.data.meshes.new(ob.name+' clean manufactured surface');me.from_pydata(front+back,[],faces);me.update()
    bm=bmesh.new();bm.from_mesh(me);bmesh.ops.recalc_face_normals(bm,faces=list(bm.faces));bm.to_mesh(me);bm.free()
    ob.data=me
    for mat in mats:me.materials.append(mat)
    ob.modifiers.clear();bevel(ob,.020 if 'gasket' not in ob.name else .009);cleaned+=1

# Rebuild the face around compact recessed sensors. The previous round optics are removed.
head=bpy.data.collections.get('04 • Lens helmet and layered face');M.COL=head
for ob in list(head.objects):
    if ob.name.startswith(('Neck','Main ','Optical bridge','Eye ','Fin optical','Fin amber','Crest amber')):
        bpy.data.objects.remove(ob,do_unlink=True)
mask=bpy.data.objects.get('Broad faceted titanium mask')
if mask:
    for vertex in mask.data.vertices:
        vertex.co.z+=.065*max(0,min(1,(vertex.co.z-9.80)/.085))
sensor=material('V4 / recessed cyan sensor glass','5AD5E3',.15,.22,2.0)
for s in [-1,1]:
    spl('Recessed eye cavity',s,[(.054,10.069),(.375,10.17),(.398,10.034),(.116,9.991)],-.687,.06,black,.009)
    spl('Narrow flat eye sensor',s,[(.111,10.068),(.348,10.135),(.351,10.091),(.142,10.037)],-.716,.012,sensor,.004)
    spl('Upper armored eye brow',s,[(.0,10.094),(.109,10.196),(.495,10.340),(.482,10.210),(.138,10.080)],-.748,.095,frame,.013)
    spl('Lower eye sill',s,[(.109,9.997),(.395,10.047),(.389,10.018),(.135,9.967)],-.705,.055,steel,.006)
    # The former gold circles become quiet, recessed industrial panel details.
    spl('Fin inset service panel',s,[(.308,10.29),(.43,10.42),(.49,10.42),(.435,10.31),(.362,10.27)],-.786,.032,frame,.007)
plate('Narrow armored forehead keel',[(-.070,10.16),(.070,10.16),(.167,10.53),(.122,10.69),(-.122,10.69),(-.167,10.53)],-.695,.13,teal,.019)
plate('Forehead flat sensor pocket',[(-.078,10.63),(.078,10.63),(.088,10.83),(-.088,10.83)],-.453,.028,black,.008)
plate('Forehead rectangular sensor',[(-.047,10.66),(.047,10.66),(.051,10.797),(-.051,10.797)],-.483,.017,sensor,.006)
for ob in list(head.objects):
    if ob.name.startswith(('Swept teal','Sensor fin machined','Stencil / UNIT')):
        # Fin tips are more restrained than the previous oversized silhouette.
        mat=Matrix.Diagonal((.86,1,.94,1));mat=Matrix.Translation((0,0,10.15))@mat@Matrix.Translation((0,0,-10.15))
        ob.matrix_world=mat@ob.matrix_world
    transform=Matrix.Translation((0,.02,9.72))@Matrix.Diagonal((.91,.78,.76,1))@Matrix.Translation((0,0,-9.16))
    ob.matrix_world=transform@ob.matrix_world
head.name='04 • Compact helmet and recessed sensor slits'

group('04B • Visible cervical mechanism')
cyl('Neck flexible internal column',(0,.12,9.10),(0,.12,9.84),.213,black)
for z in [9.20,9.34,9.48,9.62,9.76]:
    ring('Neck stacked rotary seal',(0,.12,z),.215,.020,frame,(0,0,1))
for s in [-1,1]:
    a=Vector((s*.34,-.02,9.20));b=Vector((s*.21,-.04,9.78))
    cyl('Neck exposed piston rod',a,b,.047,steel)
    cyl('Neck piston lower sleeve',a,a.lerp(b,.49),.072,frame)
    ring('Neck piston gland',a.lerp(b,.48),.074,.009,bronze,b-a)
    cyl('Neck rear stabilizer',(s*.25,.27,9.22),(s*.22,.23,9.78),.048,bronze)
    bolt('Neck lower coupling',(s*.34,-.09,9.25),.026)
box('Neck front vertebral plate',(0,-.116,9.48),(.22,.07,.23),frame,.015)
for z in [9.45,9.51]:box('Neck front cooling recess',(0,-.156,z),(.13,.009,.014),black,.003)
cyl('Neck upper helmet bearing',(0,.10,9.77),(0,.10,9.86),.253,steel)

# Hands hang in a neutral orientation: thumbs forward and palms toward the body.
oldhands=bpy.data.collections.get('05B • Articulated armored hands')
for ob in list(oldhands.objects):bpy.data.objects.remove(ob,do_unlink=True)
bpy.data.collections.remove(oldhands)
for ob in list(scene.objects):
    if ob.name.startswith('Finger articulation split'):bpy.data.objects.remove(ob,do_unlink=True)

def phalange(name,a,b,width,depth=.14):
    a,b=Vector(a),Vector(b);delta=b-a
    prism(name+' enclosed metal link',a.lerp(b,.10),b.lerp(a,.08),width,depth,frame,.20,edge=.009)
    # A real enclosure wraps the link, with an overlapping dorsal plate on its outside.
    projected=Vector((delta.x,0,delta.z)).normalized();cross=Vector((-projected.z,0,projected.x))
    top=a.lerp(b,.14);bottom=b.lerp(a,.10)
    top.y-=depth*.51+.021;bottom.y-=depth*.51+.021
    corners=[top-cross*width*.47,top+cross*width*.47,bottom+cross*width*.43,bottom-cross*width*.43]
    verts=corners+[p+Vector((0,.041,0)) for p in corners]
    mesh(name+' overlapping dorsal armor',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],teal2,.007)

def handjoint(name,p,w,r):
    p=Vector(p);axis=Vector((1,0,0))
    cyl(name+' black gasket',p-axis*w*.53,p+axis*w*.53,r*.92,black)
    cyl(name+' steel bearing',p-axis*w*.48,p+axis*w*.48,r,steel)
    for side in [-1,1]:
        cyl(name+' flush cap',p+axis*side*w*.495,p+axis*side*w*.521,r*.70,frame)
        bolt(name+' recessed screw',p+axis*side*w*.526,r*.22,axis*side)

for s in [-1,1]:
    group('05B • '+('Left' if s<0 else 'Right')+' neutral enclosed fist')
    cyl('Wrist rotary adapter',(0,0,-.095),(0,0,.16),.237,frame)
    for z in [-.068,.064,.118]:ring('Wrist rotary seal',(0,0,z),.237,.012,steel,(0,0,1))
    prism('Wrist cuff end armor',(0,0,.06),(0,0,.18),.64,.56,frame,.20,edge=.016)
    prism('Palm compact structural core',(0,0,-.12),(0,0,-.60),.652,.456,frame,.18,[(0,.90),(.12,1),(.82,1),(1,.83)],.019)
    prism('Palm enclosed heel',(0,.025,-.43),(0,.025,-.875),.578,.406,frame,.21,edge=.015)
    plate('Dorsal hand armor',[(-.31,-.22),(-.22,-.09),(.23,-.09),(.31,-.22),(.29,-.52),(.20,-.58),(-.25,-.55)],-.259,.062,teal,.014)
    plate('Dorsal hand center overlay',[(-.13,-.13),(.23,-.13),(.27,-.25),(.24,-.48),(-.11,-.51)],-.330,.045,teal2,.008)
    line('Dorsal hand longitudinal seam',[(-.103,-.383,-.16),(-.098,-.383,-.44)],steel,.003)
    for xx in [-.235,.23]:bolt('Palm service fastener',(xx,-.338,-.27),.014)
    prism('Palm knuckle support crossbeam',(-.275,-.095,-.56),(.275,-.095,-.56),.15,.25,frame,.18,edge=.010)
    # Broad side armor encloses the palm without covering the thumb articulation.
    for side in [-1,1]:
        box('Palm side protection',(side*.316,.025,-.315),(.052,.30,.30),teal,.015)
        box('Palm heel lateral armor',(side*.297,.025,-.657),(.055,.269,.27),frame,.021)
    for k,(xx,w,short) in enumerate([(-.239,.139,.035),(-.078,.147,0),(.082,.141,.024),(.237,.125,.085)]):
        pts=[Vector((xx,-.10,-.565)),Vector((xx,-.229,-.773+short)),Vector((xx,.023,-.883+short)),Vector((xx,.139,-.638+short))]
        for j in range(3):
            handjoint('Finger %d hinge %d'%(k+1,j+1),pts[j],w,.073 if j==0 else .061)
            phalange('Finger %d phalanx %d'%(k+1,j+1),pts[j],pts[j+1],w*.95,.151 if j==0 else .13)
    # The shorter opposed thumb lays diagonally across the curled index and middle fingers.
    pts=[Vector((-.331,.022,-.269)),Vector((-.379,-.174,-.483)),Vector((-.271,-.329,-.657)),Vector((-.092,-.363,-.710))]
    for j in range(3):
        handjoint('Thumb buried pivot %d'%j,pts[j],.171,.073)
        phalange('Thumb protective segment %d'%j,pts[j],pts[j+1],.174,.176)
        a,b=pts[j],pts[j+1];delta=Vector((0,b.y-a.y,b.z-a.z)).normalized();cross=Vector((0,-delta.z,delta.y))
        start=a.lerp(b,.12);end=b.lerp(a,.09)
        start.x=end.x=min(a.x,b.x)-.082
        corners=[start-cross*.085,start+cross*.085,end+cross*.085,end-cross*.085]
        verts=corners+[p+Vector((.034,0,0)) for p in corners]
        mesh('Thumb radial protective plate',verts,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],teal2,.008)
    line('Thumb short actuator hose',[(-.247,-.226,-.206),(-.341,-.244,-.32),(-.353,-.222,-.41)],black,.014)
    p=Vector((s*3.05,-.22,6.12))
    tilt=Vector((0,0,-1)).rotation_difference(Vector((s*.17,-.045,-1)).normalized()).to_matrix().to_4x4()
    xf=Matrix.Translation(p)@tilt@Matrix.Rotation(s*math.pi/2,4,'Z')@Matrix.Diagonal((s,1,1,1))
    for ob in M.COL.objects:ob.matrix_world=xf@ob.matrix_world

# Weapons are fully replaced rather than dressed with another layer of boxes.
for col in list(bpy.data.collections):
    if col.name.startswith(('06 •','07B •')):
        for ob in list(col.objects):bpy.data.objects.remove(ob,do_unlink=True)
        bpy.data.collections.remove(col)

print('BODY_FACE_HANDS_REBUILT',cleaned,flush=True)

group('06 • Forearm mounted sabers with hand clearance')
blade_metal=finish('ground blade flats','63757E',.87,.31)
blade_edge=finish('honed steel cutting bevel','ADBBC0',.91,.23)
for s in [-1,1]:
    a=Vector((s*3.035,.01,7.59));b=Vector((s*3.72,-.115,6.31));d=(b-a).normalized();q=d.to_track_quat('Z','Y')
    # A short pair of brackets anchors the independent carrier to the forearm shell.
    for t in [.28,.80]:
        p=a.lerp(b,t);arm=p-Vector((s*.32,0,0))
        prism('Forearm blade standoff bracket',arm,p,.22,.30,frame,.15,edge=.014)
        cyl('Forearm bracket dowel',p-Vector((s*.045,0,0)),p+Vector((s*.060,0,0)),.060,steel)
        bolt('Blade bracket recessed screw',p+Vector((s*.065,0,0)),.026,(s,0,0))
    prism('Blade carrier internal channel',a,b,.32,.34,black,.14,edge=.012)
    prism('Blade carrier upper armor',a-d*.02,b-d*.14,.355,.405,frame,.12,[(0,.68),(.10,1),(.69,1),(.90,.87),(1,.83)],.018)
    prism('Blade carrier outer service plate',a+Vector((s*.12,-.14,0))+d*.12,b+Vector((s*.12,-.14,0))-d*.20,.255,.085,teal,.16,edge=.010)
    for t in [.24,.48,.71]:
        p=a.lerp(b,t)+Vector((s*.13,-.198,0))
        prism('Blade carrier inset slot',p-d*.065,p+d*.065,.105,.015,black,.10,edge=.003)
    for side in [-1,1]:cyl('Blade internal sliding guide',a+d*.17+Vector((side*.084,.11,0)),b-d*.05+Vector((side*.084,.11,0)),.025,steel)
    prism('Forearm blade exit throat',b-d*.065,b+d*.065,.38,.405,gold,.18,edge=.012)
    prism('Blade exit dark aperture',b+d*.057,b+d*.079,.268,.22,black,.14,edge=.004)
    rows=[(6.33,3.70,3.91,-.13),(6.10,3.73,4.07,-.17),(5.80,3.77,4.14,-.21),
          (5.31,3.89,4.30,-.26),(4.76,4.01,4.45,-.31),(4.17,4.14,4.58,-.35),
          (3.61,4.29,4.70,-.38),(3.12,4.45,4.77,-.40),(2.77,4.75,4.79,-.41)]
    # Closely spaced interpolation keeps the sweep continuous without ballooning its outline.
    interp=[]
    for j in range(len(rows)-1):
        for k in range(4):interp.append(Vector(rows[j]).lerp(Vector(rows[j+1]),k/4))
    interp.append(Vector(rows[-1]));vs=[]
    fractions=[0,.16,.25,.43,.51,.83,1,.5];depths=[0,-.053,-.027,-.027,-.056,-.026,0,.054]
    for z,inner,outer,y in interp:
        taper=min(1,(outer-inner)/.25)
        vs.extend((s*(inner+(outer-inner)*t),y+h*taper,z) for t,h in zip(fractions,depths))
    fs=[tuple(range(8))]
    for j in range(len(interp)-1):
        for k in range(8):fs.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k))
    fs.append(tuple(range((len(interp)-1)*8,len(interp)*8)))
    ob=mesh(('Left' if s<0 else 'Right')+' forearm saber',vs,fs,blade_metal,.002)
    ob.data.materials.append(black);ob.data.materials.append(blade_edge)
    for j in range(len(interp)-1):
        ob.data.polygons[1+j*8+2].material_index=1
        ob.data.polygons[1+j*8+5].material_index=2

group('07B • Armored multibore shoulder cannon assemblies')
gunpaint=finish('cannon petrol armored casing','263D44',.48,.43)
gunpanel=finish('cannon alternate armor plates','30474E',.47,.41)
gunblack=finish('cannon blackened steel muzzle','24292E',.72,.39)
for s in [-1,1]:
    a=Vector((s*1.66,1.30,10.89));d=Vector((0,-1,.14)).normalized();q=d.to_track_quat('Z','Y');u=q@Vector((1,0,0));v=q@Vector((0,1,0))
    def at(t,x=0,y=0):return a+d*t+u*x+v*y
    def sidepanel(name,points,offset,thickness,mat):
        n=len(points);vs=[at(t,offset,h) for t,h in points]+[at(t,offset+thickness,h) for t,h in points]
        fs=[tuple(range(n)),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
        return mesh(name,vs,fs,mat,.011)
    # Short armored cradle carries the weapon directly over the backpack/shoulder bearing.
    mountbase=Vector((s*1.30,.94,9.31));mounttop=at(.36,0,-.40)
    prism('Cannon armored elevation cradle',mountbase,mounttop,.53,.71,frame,.13,[(0,.80),(.1,.9),(.63,1),(1,.75)],.022)
    prism('Cannon cradle bronze rim',mountbase+Vector((0,-.355,.15)),mounttop+Vector((0,-.355,-.06)),.35,.07,bronze,.15,edge=.010)
    cyl('Cannon main elevation bearing',mounttop-u*.48,mounttop+u*.48,.245,gunblack)
    for side in [-1,1]:
        tube('Cannon bearing annular face',mounttop+u*side*.47,mounttop+u*side*.50,.208,.14,steel)
        cyl('Cannon bearing recessed hub',mounttop+u*side*.50,mounttop+u*side*.513,.134,frame)
        bolt('Cannon bearing axle screw',mounttop+u*side*.52,.045,u*side)
    for dx in [-.19,.19]:
        p=mountbase+Vector((dx,.23,.18));end=at(-.03,dx,-.35)
        cyl('Cannon recoil actuator rod',p,end,.049,steel);cyl('Cannon recoil actuator sleeve',p,p.lerp(end,.62),.078,gunblack)
    # Receiver geometry breaks into substantial modules and overlapping armour panels.
    prism('Cannon breech receiver foundation',at(-.25),at(1.45),.91,.82,gunblack,.16,[(0,.76),(.08,1),(.53,1),(.70,.9),(1,.76)],.024)
    prism('Cannon receiver top sloped cap',at(-.11,0,.35),at(1.32,0,.31),.71,.16,gunpaint,.13,[(0,.72),(.16,1),(.61,1),(1,.66)],.016)
    prism('Cannon rear recoil housing',at(-.46),at(-.13),.79,.72,gunblack,.17,edge=.019)
    prism('Cannon rear recessed access plate',at(-.477),at(-.463),.52,.47,frame,.20,edge=.012)
    for side in [-1,1]:
        sidepanel('Cannon stepped receiver side panel',[(.0,-.20),(.06,.20),(.40,.30),(.90,.24),(1.13,.10),(1.19,-.21),(.88,-.29),(.19,-.28)],side*.454,side*.072,gunpaint)
        sidepanel('Cannon receiver secondary panel',[(.14,-.125),(.18,.105),(.44,.19),(.70,.16),(.87,.055),(.81,-.14)],side*.530,side*.025,gunpanel)
        sidepanel('Cannon recessed receiver stripe',[(.23,-.05),(.71,.01),(.73,.057),(.24,.008)],side*.559,side*.010,black)
        for t,h in [(.12,.17),(.94,.14),(.97,-.17),(.23,-.22)]:bolt('Cannon receiver captive fastener',at(t,side*.548,h),.020,u*side)
        for j in range(4):
            sidepanel('Cannon rear receiver exhaust slit',[(.015+j*.10,-.17),(.041+j*.10,-.06),(.064+j*.10,-.06),(.038+j*.10,-.17)],side*.55,side*.006,black)
    # A continuous long polygonal shroud reproduces the silhouette of the supplied cannon.
    prism('Cannon continuous barrel housing',at(1.12),at(4.63),.67,.55,gunblack,.17,[(0,1),(.06,1),(.90,.78),(1,.74)],.015)
    prism('Cannon long upper armor spine',at(1.16,0,.225),at(4.55,0,.179),.55,.14,gunpaint,.12,[(0,1),(.045,1),(.96,.72),(1,.68)],.012)
    prism('Cannon lower heat shield',at(1.34,0,-.233),at(4.42,0,-.194),.42,.08,frame,.13,edge=.011)
    for side in [-1,1]:
        sidepanel('Cannon longitudinal recessed channel',[(1.28,-.15),(1.28,.17),(4.46,.13),(4.46,-.12)],side*.342,side*.012,black)
        sidepanel('Cannon long upper side shroud plate',[(1.22,.17),(1.41,.257),(4.38,.198),(4.55,.113),(1.48,.078)],side*.358,side*.036,gunpaint)
        sidepanel('Cannon long lower side shroud plate',[(1.35,-.167),(1.52,-.067),(4.52,-.099),(4.39,-.192),(1.41,-.234)],side*.356,side*.038,gunpanel)
        line('Cannon machined longitudinal inset',[at(1.61,side*.400,.008),at(4.16,side*.400,-.023)],bronze,.012)
        for t in [1.48,2.95,4.32]:bolt('Cannon shroud fastener',at(t,side*.405,-.137),.018,u*side)
        for j in range(5):
            sidepanel('Cannon shroud cooling vent',[(1.60+j*.13,-.137),(1.625+j*.13,-.083),(1.655+j*.13,-.083),(1.632+j*.13,-.137)],side*.400,side*.006,black)
    # Deep rectangular muzzle recess with four separate dark bores; no bright round end cap.
    prism('Cannon muzzle armored rear collar',at(4.42),at(4.67),.76,.75,gunpaint,.16,edge=.017)
    muzzle=prism('Cannon recessed multibore muzzle frame',at(4.63),at(5.18),.77,.81,gunblack,.18,[(0,1),(.12,1),(.87,.92),(1,.89)],.017)
    cutter=prism('Muzzle window cutter',at(4.49),at(5.32),.536,.588,black,.17,edge=.035);cut(muzzle,cutter)
    face=prism('Cannon deep internal bore plate',at(4.79),at(4.92),.546,.605,frame,.17,edge=.008)
    for xx,hh in [(-.135,.154),(.135,.154),(-.135,-.154),(.135,-.154)]:
        cutter=cyl('Bore aperture cutter',at(4.66,xx,hh),at(5.01,xx,hh),.106,black,n=48,edge=0);cut(face,cutter)
        tube('Cannon recessed barrel liner',at(4.23,xx,hh),at(4.96,xx,hh),.104,.078,gunblack)
        ring('Cannon bore retaining ring',at(4.973,xx,hh),.092,.009,steel,d)
        ring('Cannon inner bore step',at(4.93,xx,hh),.079,.005,bronze,d)
    for side in [-1,1]:
        sidepanel('Muzzle side wear insert',[(4.74,-.13),(4.74,.13),(5.00,.12),(5.05,-.11)],side*.384,side*.014,frame)
        for j in range(3):sidepanel('Muzzle side pressure relief slot',[(4.77+j*.08,-.056),(4.78+j*.08,.062),(4.805+j*.08,.062),(4.795+j*.08,-.056)],side*.402,side*.005,black)
    prism('Cannon muzzle upper reinforcement',at(4.72,0,.386),at(5.10,0,.360),.33,.07,gunpaint,.12,edge=.008)
    print('CANNON_REBUILT',s,flush=True)

group('99C • V4 assembly design guide')
im=bpy.data.images.load(os.path.join(OUT,'parts_design_guide.png'));im.pack()
ob=bpy.data.objects.new('Design study — generated reference, not model render',None);M.COL.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=im;ob.hide_render=True;ob.hide_viewport=True

def camera(name,loc,target,scale):
    ob=bpy.data.objects.get(name)
    if not ob:
        data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);scene.collection.objects.link(ob)
    ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();ob.data.type='ORTHO';ob.data.ortho_scale=scale;ob.data.passepartout_alpha=.95
    return ob
hero=camera('V4 • Hero',(8,-30,11.8),(0,-.20,6.14),15.7)
front=camera('V4 • Front proportion check',(0,-30,9),(0,-.15,6.25),15.0)
facecam=camera('V4 • Helmet and neck',(2.2,-15,11.8),(0,-.20,10.37),3.05)
handcam=camera('V4 • Hand construction',(9,-9,7.0),(3.13,-.19,5.83),2.23)
armcam=camera('V4 • Blade and wrist clearance',(9,-12,7.5),(3.79,-.12,5.19),5.9)
guncam=camera('V4 • Cannon construction',(9,-6,14.0),(1.7,-.45,11.25),6.4)
scene.camera=hero
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.15
for name,power in [('Key softbox',1800),('Neutral frontal fill',900),('Cool rear strip',1650),('Warm rear strip',850),('Overhead reflection',650)]:
    if name in bpy.data.objects:bpy.data.objects[name].data.energy=power
scene.view_settings.exposure=.10;scene.view_settings.look='AgX - Medium High Contrast'
floor=bpy.data.objects.get('Seamless studio floor')
if floor:floor.location.z=-.05
scene['revision']='V4: inward-facing palms and side-on fists; forearm-mounted saber clearance; compact flat sensor helmet and exposed mechanical neck; continuous armored multibore shoulder cannons; clean planar body panels.'
scene.cycles.use_denoising=True;scene.cycles.max_bounces=7;scene.cycles.diffuse_bounces=2;scene.cycles.glossy_bounces=3;scene.cycles.transmission_bounces=3
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for device in prefs.devices:device.use=device.type=='METAL'
scene.cycles.device='GPU';scene.cycles.samples=48;scene.cycles.adaptive_threshold=.075
scene.render.resolution_x=1600;scene.render.resolution_y=2100;scene.render.resolution_percentage=100;scene.render.filepath=os.path.join(OUT,'phantom_v4_hero.png')
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha_v4.blend'))
print('V4_SAVED',len(scene.objects),flush=True)
if '--preview' in sys.argv:
    scene.cycles.samples=16;scene.cycles.adaptive_threshold=.13
    jobs=[(front,'preview_front.png',750,1000),(facecam,'preview_face.png',760,760),(handcam,'preview_hand.png',760,760),(armcam,'preview_blade.png',680,950),(guncam,'preview_cannon.png',950,680),(hero,'preview_hero.png',750,1000)]
    if '--quick-check' in sys.argv:jobs=[jobs[0],jobs[1],jobs[2],jobs[-1]]
    for cam,file,w,h in jobs:
        scene.camera=cam;scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.filepath=os.path.join(OUT,file)
        print('PREVIEW_START',file,flush=True);bpy.ops.render.render(write_still=True);print('PREVIEW_DONE',file,flush=True)
