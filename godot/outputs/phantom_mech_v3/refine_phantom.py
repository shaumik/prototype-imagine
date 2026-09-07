import bpy, math, os, sys, json, random
from mathutils import Vector
OUT=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,OUT)
import mechanical as M
from mechanical import *
random.seed(53)

# The improved torso and leg forms are retained; the criticized assemblies are replaced.
for col in list(bpy.data.collections):
    if col.name.startswith(('04 •','06 •')):
        for o in list(col.objects):bpy.data.objects.remove(o,do_unlink=True)
        bpy.data.collections.remove(col)
    elif col.name.startswith('05 •'):
        for o in list(col.objects):
            if o.name.startswith(('Hand ','Wrist ')):bpy.data.objects.remove(o,do_unlink=True)
    elif col.name.startswith('07 •'):
        for o in list(col.objects):
            if o.name.startswith(('Cannon','Marking')):bpy.data.objects.remove(o,do_unlink=True)

group('04 • Lens helmet and layered face')
cyl('Neck inner spindle',(0,.08,9.12),(0,.08,9.48),.235,frame)
for z in [9.22,9.35]:ring('Neck bearing',(0,.08,z),.237,.025,steel,(0,0,1))
# Angular helmet envelope with a slightly curved rear, concealed beneath discrete plates.
prism('Helmet armored envelope',(0,.09,9.42),(0,.09,10.70),1.20,1.03,teal,.23,[(0,.69),(.10,.90),(.63,1),(.82,.94),(1,.54)],.045)
plate('Helmet central crown', [(-.16,10.30),(.16,10.30),(.20,10.78),(.12,10.92),(-.12,10.92),(-.20,10.78)],-.40,.35,teal,.028)
plate('Helmet face aperture',[(-.50,10.18),(.50,10.18),(.51,9.60),(.28,9.26),(-.28,9.26),(-.51,9.60)],-.525,.18,black,.025)
for s in [-1,1]:
    spl('Helmet crown side facet',s,[(.18,10.36),(.22,10.67),(.40,10.64),(.55,10.31),(.48,10.09),(.30,10.21)],-.44,.30,teal2,.026)
    spl('Helmet temple main shell',s,[(.45,10.38),(.59,10.27),(.66,9.70),(.55,9.35),(.34,9.28),(.38,9.79)],-.32,.59,teal,.028)
    # Gold bordered ear recess with retaining bolts and a lower louver bank.
    spl('Temple bronze pocket surround',s,[(.51,10.05),(.64,9.98),(.62,9.51),(.48,9.39),(.43,9.77)],-.575,.14,gold,.018)
    spl('Temple recessed pocket',s,[(.526,9.99),(.598,9.95),(.579,9.61),(.481,9.51),(.483,9.78)],-.60,.045,black,.014)
    for z in [9.91,9.80]:bolt('Temple recessed fastener',(s*.553,-.622,z),.042)
    for j in range(5):line('Temple cooling louver',[(s*.495,-.624,9.59+j*.027),(s*.565,-.624,9.64+j*.027)],frame,.010)
    # Long thin guards cover the cheek edges; the face remains a broad mask.
    spl('Cheek guard metallic border',s,[(.325,9.97),(.448,10.02),(.455,9.37),(.338,9.22),(.292,9.32)],-.674,.17,steel,.021)
    spl('Cheek guard teal plate',s,[(.341,9.94),(.413,9.97),(.414,9.40),(.346,9.29),(.323,9.34)],-.701,.08,teal,.016)
    for j in range(10):line('Cheek guard vertical vent',[(s*.357,-.724,9.36+j*.048),(s*.391,-.724,9.36+j*.048)],black,.008)
    spl('Jaw bronze structural rim',s,[(.272,9.73),(.340,9.61),(.258,9.32),(.123,9.18),(.096,9.33)],-.647,.16,gold,.014)
    bolt('Jaw service screw',(s*.245,-.72,9.39),.023)
    # Recessed glass eye pockets with a darker frame and lower bronze sill.
    spl('Eye socket alloy surround',s,[(.075,10.04),(.331,10.09),(.380,9.988),(.288,9.915),(.098,9.93)],-.676,.09,frame,.012)
    spl('Eye angular ice glass',s,[(.11,10.012),(.316,10.061),(.343,9.990),(.28,9.951),(.118,9.958)],-.706,.024,eye,.010)
    line('Eye inner illuminator',[(s*.137,-.731,9.978),(s*.290,-.731,10.005)],cyan,.009)
    spl('Eye lower bronze sill',s,[(.099,9.93),(.29,9.92),(.374,9.984),(.373,9.94),(.292,9.872),(.113,9.889)],-.681,.055,gold,.009)

# Vented mask with a restrained central ridge instead of a projecting nose.
vs=[(-.30,-.67,9.885),(0,-.765,9.885),(.30,-.67,9.885),
    (-.26,-.662,9.55),(0,-.752,9.48),(.26,-.662,9.55),
    (-.12,-.64,9.28),(0,-.72,9.245),(.12,-.64,9.28)]
vs+= [(x,y+.105,z) for x,y,z in vs]
fs=[(0,1,4,3),(1,2,5,4),(3,4,7,6),(4,5,8,7),
    (9,12,13,10),(10,13,14,11),(12,15,16,13),(13,16,17,14),
    (0,9,10,1),(1,10,11,2),(2,11,14,5),(5,14,17,8),(8,17,16,7),(7,16,15,6),(6,15,12,3),(3,12,9,0)]
mask=mesh('Broad faceted titanium mask',vs,fs,mouth,.016)
for zz in [9.713,9.620]:
    cutter=plate('Mask vent cutting tool',[(-.115,zz+.012),(0,zz+.038),(.115,zz+.012),(.115,zz-.020),(0,zz+.003),(-.115,zz-.020)],-.82,.32,black,0)
    cut(mask,cutter)
    plate('Mask dark vent interior',[(-.12,zz+.015),(0,zz+.040),(.12,zz+.015),(.12,zz-.025),(0,zz),(-.12,zz-.025)],-.648,.02,black,0)
plate('Chin recessed armored mount',[(-.105,9.51),(.105,9.51),(.11,9.16),(-.11,9.16)],-.741,.11,black,.018)
plate('Chin machined projection',[(-.073,9.49),(.073,9.49),(.061,9.17),(-.061,9.17)],-.793,.13,bronze,.018)

# Central optical assembly, retaining ring and blue faceted glass.
plate('Optical bridge armored housing',[(-.10,10.66),(.10,10.66),(.21,10.43),(.29,10.25),(.23,9.993),(0,9.91),(-.23,9.993),(-.29,10.25),(-.21,10.43)],-.602,.20,frame,.023)
cyl('Main lens recessed black baffle',(0,-.59,10.185),(0,-.748,10.185),.243,black)
tube('Main lens retaining barrel',(0,-.745,10.185),(0,-.825,10.185),.239,.207,steel)
ring('Main lens outer retaining lip',(0,-.833,10.185),.232,.014,frame)
ring('Main lens blue coating ring',(0,-.826,10.185),.201,.009,eye)
cyl('Main lens dark internal iris',(0,-.750,10.185),(0,-.762,10.185),.163,black)
ring('Main lens internal optical element',(0,-.771,10.185),.130,.016,blueglass)
for j in range(12):
    a=math.tau*j/12
    line('Main iris aperture detail',[(.080*math.cos(a),-.776,10.185+.080*math.sin(a)),(.142*math.cos(a+.25),-.777,10.185+.142*math.sin(a+.25))],steel,.005)
lens('Main faceted blue optical glass',(0,-.817,10.185),.201,blueglass)
for a in [math.pi/4,3*math.pi/4,5*math.pi/4,7*math.pi/4]:bolt('Main lens retaining screw',(.273*math.cos(a),-.81,10.185+.273*math.sin(a)),.018)

# Thick teal swept sensor fins, inset amber optics and bent bronze antennae.
for s in [-1,1]:
    spl('Swept teal sensor fin',s,[(.15,10.055),(.47,10.18),(1.22,11.13),(.93,10.89),(.34,10.44),(.15,10.31)],-.654,.123,teal,.014)
    line('Sensor fin machined edge',[(s*.44,-.786,10.23),(s*.87,-.78,10.83),(s*1.185,-.757,11.09)],steel,.008)
    spl('Fin optical socket frame',s,[(.31,10.286),(.38,10.45),(.51,10.438),(.51,10.315),(.403,10.225)],-.80,.042,bronze,.009)
    cyl('Fin amber optic housing',(s*.421,-.80,10.347),(s*.421,-.844,10.347),.068,black)
    ring('Fin amber optic lip',(s*.421,-.85,10.347),.062,.009,gold)
    lens('Fin amber optical glass',(s*.421,-.855,10.347),.050,amber)
    label('UNIT-005',(s*.648,-.792,10.653),.027)
    # Antennae are bent, broad, faceted blades anchored to visible hinges.
    spl('Bent bronze command antenna',s,[(.18,10.42),(.23,10.69),(.45,10.88),(.69,11.63),(.51,11.27),(.36,10.94),(.12,10.69)],-.355,.14,gold,.015)
    pivot('Antenna base hinge',(s*.23,-.343,10.515),.15,.082,(s*.65,-.6,.18))
    label('C-09',(s*.441,-.505,10.994),.025)
plate('Crest amber sensor recess',[(-.092,10.565),(.092,10.565),(.10,10.80),(-.10,10.80)],-.458,.035,black,.017)
cyl('Crest amber sensor housing',(0,-.46,10.693),(0,-.50,10.693),.073,bronze)
ring('Crest amber sensor lip',(0,-.509,10.693),.067,.009,steel)
lens('Crest amber sensor glass',(0,-.517,10.693),.056,amber)

group('05B • Articulated armored hands')
def finger_segment(name,a,b,width,depth=.105):
    a,b=Vector(a),Vector(b);d=b-a;q=d.to_track_quat('Z','Y');back=q@Vector((0,-1,0))
    cyl(name+' internal link',a,b,width*.29,frame)
    # Dorsal plates follow each link but always face the outside of the fist.
    projected=Vector((d.x,0,d.z)).normalized();side=Vector((-projected.z,0,projected.x))
    top=a.lerp(b,.17);bottom=b.lerp(a,.12)
    top.y-=depth+.046;bottom.y-=depth+.046
    corners=[top-side*width*.43,top+side*width*.43,bottom+side*width*.48,bottom-side*width*.48]
    vs=corners+[p+Vector((0,.062,0)) for p in corners]
    armor=mesh(name+' overlapping armor',vs,[(0,1,2,3),(4,7,6,5),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],teal,.010)
    line(name+' seam',[top-side*width*.30+projected*.024+Vector((0,-.013,0)),top+side*width*.30+projected*.024+Vector((0,-.013,0))],steel,.004)
for s in [-1,1]:
    x=s*3.05
    # The cuff is a short armored adapter around the rotating wrist, not a long exposed stem.
    prism('Wrist structural cuff',(x,-.22,6.02),(x,-.22,6.38),.80,.73,frame,.23,edge=.024)
    prism('Wrist upper bronze flange',(x,-.22,6.28),(x,-.22,6.36),.84,.77,gold,.22,edge=.013)
    cyl('Wrist rotary connector',(x,-.22,5.90),(x,-.22,6.11),.238,steel)
    for zz in [5.985,6.04]:ring('Wrist rotary seal',(x,-.22,zz),.24,.018,black,(0,0,1))
    for side in [-1,1]:
        line('Wrist cyan inset',[(x+side*.30,-.611,6.24),(x+side*.34,-.61,6.19),(x+side*.34,-.61,6.08),(x+side*.29,-.61,6.04)],cyan,.012)
    # Palm: broad articulated core, separate dorsal shell, gold knuckle bridge and sensor.
    prism('Palm structural cage',(x,-.17,5.51),(x,-.17,6.02),.71,.55,frame,.19,edge=.026)
    plate('Palm dorsal armor',[(x-.345,5.70),(x-.33,5.97),(x-.19,6.065),(x+.19,6.065),(x+.33,5.97),(x+.345,5.70),(x+.24,5.62),(x-.24,5.62)],-.502,.12,teal,.021)
    plate('Knuckle bronze bridge',[(x-.335,5.775),(x+.335,5.775),(x+.335,5.663),(x-.335,5.663)],-.585,.10,gold,.017)
    plate('Palm optical module',[(x-.103,5.81),(x-.118,5.94),(x,6.013),(x+.118,5.94),(x+.103,5.81)],-.642,.065,frame,.010)
    ring('Palm blue optic frame',(x,-.719,5.913),.067,.012,steel)
    cyl('Palm optical interior',(x,-.699,5.913),(x,-.709,5.913),.061,black)
    lens('Palm blue optical glass',(x,-.72,5.913),.055,blueglass)
    for dx in [-.27,-.17,.17,.27]:
        cyl('Knuckle amber sensor socket',(x+dx,-.65,5.727),(x+dx,-.686,5.727),.036,black)
        ring('Knuckle amber sensor rim',(x+dx,-.69,5.727),.029,.006,steel)
        lens('Knuckle amber sensor glass',(x+dx,-.694,5.727),.023,amber)
    for dx in [-.29,.29]:bolt('Palm cover screw',(x+dx,-.628,5.922),.017)
    label('UNIT-005',(x,-.64,5.985),.032)
    # Four fully separate fingers, each with three links and exposed transverse joints.
    for k,(dx,w,short) in enumerate([(-.26,.141,.05),(-.086,.151,0),(.086,.147,.02),(.25,.126,.105)]):
        xx=x+s*dx
        pts=[Vector((xx,-.21,5.594)),Vector((xx,-.275,5.305+short)),Vector((xx,-.04,5.113+short)),Vector((xx,.172,5.23+short))]
        for j in range(3):
            pivot('Finger %d joint %d'%(k+1,j+1),pts[j],w*1.1,.095 if j==0 else .078,(s,0,0))
            finger_segment('Finger %d segment %d'%(k+1,j+1),pts[j],pts[j+1],w,.101 if j<2 else .076)
        label('0%d'%(k+1),(xx,-.428,5.37+short),.019)
    # Opposed thumb folds across the inner edge of the fist.
    pts=[Vector((x-s*.364,-.10,5.86)),Vector((x-s*.47,-.34,5.59)),Vector((x-s*.40,-.46,5.33)),Vector((x-s*.22,-.43,5.23))]
    for j in range(3):
        pivot('Thumb joint %d'%j,pts[j],.205,.107,(s*.88,.33,.13))
        finger_segment('Thumb armored link %d'%j,pts[j],pts[j+1],.18,.102)
    # Small hand hoses run from the palm cage to the thumb actuator.
    line('Thumb hydraulic hose',[(x-s*.20,-.43,5.92),(x-s*.37,-.42,5.85),(x-s*.43,-.39,5.65)],black,.021)

joint_finish=material('V3 / brushed finger bearings','637078',.82,.38,wear=True)
for ob in M.COL.objects:
    if ob.type=='MESH':
        for slot in ob.material_slots:
            if slot.material==steel:slot.material=joint_finish

group('06 • Deployment carriages and curved wrist blades')
def catmull(points,steps=5):
    out=[];ps=[Vector(p) for p in points]
    for i in range(len(ps)-1):
        a=ps[max(0,i-1)];b=ps[i];c=ps[i+1];d=ps[min(len(ps)-1,i+2)]
        for j in range(steps):
            t=j/steps;out.append(.5*((2*b)+(-a+c)*t+(2*a-5*b+4*c-d)*t*t+(-a+3*b-3*c+d)*t*t*t))
    out.append(ps[-1]);return out
blade_metal=material('V3 / longitudinal blade steel','839EA9',.87,.28,wear=True)
blade_edge=material('V3 / polished cutting edge','CADDE1',.91,.20)
for s in [-1,1]:
    a=Vector((s*2.91,.10,7.47));b=Vector((s*3.48,-.015,5.98));d=(b-a).normalized();q=d.to_track_quat('Z','Y')
    prism('Wrist blade internal deployment rail',a,b,.30,.39,frame,.21,edge=.018)
    prism('Wrist blade removable armored cover',a+d*.13+Vector((s*.095,-.13,0)),b-d*.16+Vector((s*.095,-.13,0)),.29,.15,teal,.20,edge=.017)
    for side in [-1,1]:cyl('Blade carriage guide shaft',a+d*.2+Vector((side*.085,0,.02)),b-d*.20+Vector((side*.085,0,.02)),.027,steel)
    for t in [.31,.83]:
        p=a.lerp(b,t);prism('Blade carriage mounting saddle',p-d*.06,p+d*.06,.40,.47,bronze,.20,edge=.010)
        bolt('Blade saddle captive bolt',p+Vector((s*.19,-.23,0)),.025)
    prism('Blade bronze throat',b-d*.10,b+d*.12,.44,.48,gold,.23,edge=.021)
    prism('Blade throat recessed slot',b+d*.10,b+d*.132,.275,.18,black,.12,edge=.006)
    # A broad saber with real cross-sectional bevels, a recessed fuller, and a tapered point.
    raw=[(6.04,3.46,3.68,-.035),(5.75,3.49,3.82,-.08),(5.38,3.56,3.97,-.15),
         (4.86,3.65,4.11,-.24),(4.31,3.77,4.27,-.31),(3.77,3.91,4.42,-.37),
         (3.27,4.07,4.51,-.41),(2.82,4.27,4.56,-.43),(2.47,4.565,4.57,-.44)]
    rows=catmull(raw,5);fractions=[0,.21,.27,.41,.47,.86,1,.47];heights=[0,-.095,-.053,-.053,-.095,-.025,0,.065]
    vs=[]
    for z,inside,outside,y in rows:
        w=outside-inside;taper=min(1,max(.08,w/.27))
        for frac,hh in zip(fractions,heights):vs.append((s*(inside+frac*w),y+hh*taper,z))
    fs=[tuple(range(8))]
    for j in range(len(rows)-1):
        for k in range(8):fs.append((j*8+k,j*8+(k+1)%8,(j+1)*8+(k+1)%8,(j+1)*8+k))
    fs.append(tuple(range((len(rows)-1)*8,len(rows)*8)))
    o=mesh('LEFT forged wrist saber' if s<0 else 'RIGHT forged wrist saber',vs,fs,blade_metal,.003)
    o.data.materials.append(frame);o.data.materials.append(blade_edge)
    for j in range(len(rows)-1):
        o.data.polygons[1+j*8+2].material_index=1
        o.data.polygons[1+j*8+5].material_index=2
    # A root fastener and engraved serial identify the removable blade, without an exposed handle.
    bolt('Blade root retaining screw',(s*3.57,-.144,5.79),.025)

group('07B • Articulated shoulder autocannons')
for s in [-1,1]:
    a=Vector((s*1.82,1.53,10.95));d=Vector((0,-1,.205)).normalized();b=a+d*5.5;q=d.to_track_quat('Z','Y');u=q@Vector((1,0,0));v=q@Vector((0,1,0))
    def at(t,x=0,y=0):return a+d*t+u*x+v*y
    prism('Cannon articulated shoulder strut',(s*1.26,.78,9.39),(s*1.82,1.25,10.84),.47,.62,frame,.20,edge=.027)
    prism('Cannon strut armored front plate',(s*1.34,.41,9.72),(s*1.81,.93,10.88),.35,.12,teal,.19,edge=.016)
    cyl('Cannon recoil support piston',(s*1.38,1.33,9.68),(s*1.81,1.56,10.73),.072,steel)
    cyl('Cannon recoil piston sleeve',(s*1.38,1.33,9.68),(s*1.59,1.44,10.19),.11,frame)
    pivot('Cannon elevation trunnion',(s*1.82,.97,10.75),.87,.29,(1,0,0))
    # Stepped angular breech, with separate upper and side armor instead of one rounded capsule.
    prism('Cannon stepped receiver',at(-.16),at(1.62),.99,.91,frame,.18,[(0,.72),(.10,1),(.68,1),(.86,.86),(1,.72)],.025)
    prism('Cannon teal receiver upper plate',at(.04,0,.405),at(1.30,0,.405),.80,.145,teal,.15,[(0,.88),(.08,1),(.85,1),(1,.72)],.018)
    for side in [-1,1]:
        box('Cannon receiver side removable cover',at(.69,side*.505,-.015),(.075,.48,1.11),teal,.022,q)
        for j in range(4):box('Cannon receiver recessed ventilation slot',at(.34+j*.15,side*.547,-.04),(.019,.265,.052),black,.009,q)
        for t in [.25,1.12]:bolt('Cannon receiver service screw',at(t,side*.55,.23),.026,u*side)
    cyl('Cannon rear breech lock',at(-.18),at(-.29),.286,steel)
    cyl('Cannon rear breech inset',at(-.297),at(-.301),.214,black)
    ring('Cannon rear locking ring',at(-.307),.235,.020,bronze,d)
    # The actual barrel is a hollow tube inside an open, railed shroud.
    tube('Cannon primary rifled barrel',at(1.24),at(5.54),.202,.143,frame)
    for t in [1.5,1.67,1.83,4.10,4.30]:tube('Cannon barrel support collar',at(t),at(t+.085),.247,.198,steel)
    prism('Cannon long upper rail shroud',at(1.55,0,.24),at(4.51,0,.24),.57,.21,teal,.20,[(0,.86),(.08,1),(.87,.87),(1,.64)],.018)
    for side in [-1,1]:
        prism('Cannon open shroud side rail',at(1.68,side*.31,.02),at(4.44,side*.31,.02),.092,.35,steel,.12,edge=.011)
        cyl('Cannon exposed gas return tube',at(1.76,side*.255,-.21),at(4.50,side*.255,-.21),.058,bronze)
        for t in [2.0,2.8,3.6,4.31]:ring('Cannon gas tube retaining collar',at(t,side*.255,-.21),.064,.012,frame,d)
        for j in range(5):box('Cannon rail machining notch',at(2.1+j*.37,side*.361,.075),(.015,.094,.092),black,.006,q)
    prism('Cannon lower longitudinal brace',at(1.65,0,-.258),at(4.48,0,-.258),.22,.084,frame,.15,edge=.011)
    # Angular muzzle brake with a genuine open bore and three cross-drilled exhaust ports.
    brake=prism('Cannon angular ported muzzle brake',at(4.56),at(5.50),.74,.79,frame,.22,[(0,.82),(.11,1),(.81,1),(1,.87)],.020)
    cutter=cyl('Muzzle bore cutting tool',at(4.43),at(5.66),.252,black,n=64,edge=0);cut(brake,cutter)
    for j in range(3):
        cutter=box('Muzzle gas port cutting tool',at(4.78+j*.205,0,.10),(1.1,.118,.086),black,0,q);cut(brake,cutter)
    tube('Muzzle exposed inner barrel',at(4.48),at(5.53),.242,.182,steel)
    ring('Muzzle bore machined retaining lip',at(5.544),.211,.024,steel,d)
    tube('Muzzle dark recessed bore',at(4.45),at(5.545),.181,.135,black)
    for j in range(8):
        aa=math.tau*j/8
        line('Muzzle rifling groove',[at(4.55,.139*math.cos(aa+.14),.139*math.sin(aa+.14)),at(5.51,.139*math.cos(aa),.139*math.sin(aa))],steel,.005)
    box('Cannon muzzle upper wear plate',at(4.98,0,.411),(.35,.030,.54),steel,.012,q)
    box('Cannon receiver bronze identification tab',at(.57,-s*.508,.235),(.035,.107,.40),gold,.014,q)

gun_finish=material('V3 / dark cannon chassis','293841',.64,.43,wear=True)
gun_alloy=material('V3 / satin cannon rails','536A74',.74,.39,wear=True)
for ob in M.COL.objects:
    if ob.type=='MESH':
        for slot in ob.material_slots:
            if slot.material==frame:slot.material=gun_finish
            elif slot.material==steel:slot.material=gun_alloy

# Pack all supplied design references into the revised scene.
group('99B • Hand and face construction references')
for name in ['face_reference.jpg','hand_reference.jpg']:
    im=bpy.data.images.load(os.path.join(OUT,name));im.pack();o=bpy.data.objects.new(name,None);M.COL.objects.link(o);o.empty_display_type='IMAGE';o.data=im;o.hide_render=True;o.hide_viewport=True

scene=bpy.context.scene
def cam(name,loc,target,scale):
    data=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,data);scene.collection.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=scale;data.passepartout_alpha=.95;return o
hero=bpy.data.objects['01 • Hero'];hero.data.ortho_scale=15.9
face=cam('V3 • Face inspection',(1.45,-20,11.15),(0,-.3,10.15),2.50)
hand=cam('V3 • Hand inspection',(6.4,-11,7.55),(3.03,-.19,5.76),2.18)
cannon=cam('V3 • Cannon inspection',(9,-7,14),(1.4,-.8,11.50),6.70)
scene.camera=hero
scene.cycles.samples=48;scene.cycles.adaptive_threshold=.065;scene.cycles.use_denoising=True
scene.cycles.max_bounces=7;scene.cycles.glossy_bounces=3;scene.cycles.diffuse_bounces=2;scene.cycles.transmission_bounces=5
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for dd in prefs.devices:dd.use=dd.type=='METAL'
scene.cycles.device='GPU';scene.render.resolution_x=1600;scene.render.resolution_y=2000;scene.render.resolution_percentage=100
scene.render.filepath=os.path.join(OUT,'phantom_v3_hero.png');scene['revision']='V3: mechanical hand reconstruction, lens helmet from close-up reference, curved fullered wrist sabers, open-barrel shoulder autocannons.'
for screen in bpy.data.screens:
    for ar in screen.areas:
        if ar.type=='VIEW_3D':ar.spaces.active.overlay.show_overlays=False;ar.spaces.active.region_3d.view_perspective='CAMERA';ar.spaces.active.region_3d.view_camera_zoom=-5
bpy.ops.object.select_all(action='DESELECT');bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha_v3.blend'))
print('V3_MODEL_SAVED',len(scene.objects),flush=True)
if '--preview' in sys.argv:
    scene.cycles.samples=16;scene.cycles.adaptive_threshold=.13
    jobs=[(face,'preview_face.png',720,720),(hand,'preview_hand.png',720,720),(cannon,'preview_cannon.png',850,600),(hero,'preview_hero.png',750,950)]
    for c,file,w,h in jobs:
        scene.camera=c;scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.filepath=os.path.join(OUT,file)
        print('PREVIEW_START',file,flush=True);bpy.ops.render.render(write_still=True);print('PREVIEW_DONE',file,flush=True)
