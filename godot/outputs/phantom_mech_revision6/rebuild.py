import bpy,math,os,sys,json
from mathutils import Vector,Matrix
OUT=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,OUT)
bpy.ops.wm.open_mainfile(filepath=os.path.join(os.path.dirname(OUT),'phantom_mech_traced','Phantom_Traced.blend'))
import mechanical as M
from mechanical import mesh,box,cyl,ring,line,plate,prism,tube,bolt
# Replace the faulty components completely. Previous .blend files are untouched.
killcols=('04 •','07 •','08 •','12 •')
keys=['thorax','waist','helmet','neck','pectoral','chest','sternum','reactor','lower breastplate','clavicle','collar','lower leg','knee','greave','calf','ankle','foot','cannon','muzzle','bore','blade']
for ob in list(bpy.data.objects):
    if any(c.name.startswith('REFERENCE') for c in ob.users_collection):continue
    if any(c.name.startswith(killcols) for c in ob.users_collection) or any(k in ob.name.lower() for k in keys):
        if ob.type not in ['CAMERA','LIGHT']:bpy.data.objects.remove(ob,do_unlink=True)
# Retain thigh outlines but reduce their inflated depth to match the new lower legs.
for ob in bpy.data.objects:
    if 'thigh' not in ob.name.lower() or any(c.name.startswith('REFERENCE') for c in ob.users_collection):continue
    if ob.type=='MESH':
        inverse=ob.matrix_world.inverted()
        for v in ob.data.vertices:
            p=ob.matrix_world@v.co;p.y=.08+(p.y-.08)*.60;v.co=inverse@p
        ob.data.update()
    elif ob.type=='CURVE':
        inverse=ob.matrix_world.inverted()
        for sp in ob.data.splines:
            for v in sp.points:
                p=ob.matrix_world@Vector(v.co[:3]);p.y=.08+(p.y-.08)*.60;v.co=(* (inverse@p),1)

# Clean finish, with small changes in metal roughness instead of swollen smoothing.
palette={'teal':'365D66','teal2':'476F78','dark':'262E34','graphite':'40474D','steel':'839195','silver':'BCCBD0','gold':'AC8556','black':'111B21','red':'A65342','green':'275F47','cyan':'67E5EB','helmet':'26434C','mask':'586A6F','head_steel':'6E7D83','head_red':'7B4538'}
mat={k:M.material('R6 / '+k,v,.68 if k not in ['black','cyan'] else .3,.36 if k not in ['black'] else .5,glow=1.4 if k=='cyan' else 0) for k,v in palette.items()}
for k,m in mat.items():
    ns=m.node_tree.nodes;lk=m.node_tree.links;p=ns.get('Principled BSDF')
    n=ns.new('ShaderNodeTexNoise');n.inputs['Scale'].default_value=210;n.inputs['Detail'].default_value=2
    r=ns.new('ShaderNodeMapRange');r.inputs['From Min'].default_value=0;r.inputs['From Max'].default_value=1;r.inputs['To Min'].default_value=.30;r.inputs['To Max'].default_value=.43
    lk.new(n.outputs['Fac'],r.inputs['Value']);lk.new(r.outputs['Result'],p.inputs['Roughness'])
# Existing shoulder, hip, and arm pieces use the same finish.
alias={'teal':'teal','teal_light':'teal2','graphite':'graphite','alloy':'steel','silver':'silver','bronze':'gold','black':'black','red':'red','green':'green','cyan':'cyan'}
for ob in bpy.data.objects:
    if ob.type not in ['MESH','CURVE']:continue
    for slot in ob.material_slots:
        if slot.material and ' • ' in slot.material.name:
            key=slot.material.name.rsplit(' • ',1)[-1]
            if key in alias:slot.material=mat[alias[key]]
M.steel=mat['steel'];M.black=mat['black'];M.bronze=mat['gold'];M.frame=mat['graphite']
def group(name):return M.group('R6 • '+name)
def bevel_plate(name,points,y,depth,key,edge=.018):
    # A single explicit plane or planar slope. No silhouette inflation.
    vs=[(x,y(x,z) if callable(y) else y,z) for x,z in points];n=len(vs)
    vs += [(x,yy+depth,z) for x,yy,z in vs]
    fs=[tuple(range(n)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    return mesh(name,vs,fs,mat[key],edge)
def mirrored(points,sign):return [(sign*x,z) for x,z in points]
def loft(name,sections,key,edge=.022):
    # z, center x, center y, width, depth: eight-sided structural cross-sections.
    outline=[(-.36,-.5),(.36,-.5),(.5,-.34),(.5,.34),(.36,.5),(-.36,.5),(-.5,.34),(-.5,-.34)]
    vs=[(cx+w*u,cy+d*v,z) for z,cx,cy,w,d in sections for u,v in outline]
    fs=[tuple(range(7,-1,-1))]
    for j in range(len(sections)-1):
        for i in range(8):fs.append((j*8+i,j*8+(i+1)%8,(j+1)*8+(i+1)%8,(j+1)*8+i))
    fs.append(tuple(range(len(vs)-8,len(vs))))
    ob=mesh(name,vs,fs,mat[key],edge);ob['cross_sections']=json.dumps(sections);return ob

group('Shallow chest and central torso')
loft('Unified torso chassis',[(4.61,0,.03,.68,.55),(4.91,0,.03,1.04,.74),(5.31,0,-.015,1.56,.94),(5.76,0,-.02,1.70,.96),(6.02,0,.035,1.48,.73)],'dark',.045)
for s in [-1,1]:
    p=[(.06,5.97),(.48,6.00),(.79,5.89),(.82,5.60),(.72,5.45),(.27,5.48),(.10,5.67)]
    bevel_plate('Pectoral shallow armor '+str(s),mirrored(p,s),lambda x,z:-.54+.25*(z-5.65),.13,'graphite',.032)
    # Recessed intakes sit in one shallow breastplate plane.
    p=[(.29,5.52),(.76,5.58),(.83,5.47),(.77,5.26),(.33,5.22),(.25,5.33)]
    bevel_plate('Bronze intake frame '+str(s),mirrored(p,s),-.64,.15,'gold',.024)
    p=[(.34,5.45),(.74,5.49),(.73,5.32),(.35,5.29)]
    bevel_plate('Intake dark cavity '+str(s),mirrored(p,s),-.655,.012,'black',.018)
    for z in [5.34,5.395]:
        bevel_plate('Intake inset louver',mirrored([(.37,z),(.70,z+.035),(.70,z+.049),(.37,z+.014)],s),-.672,.016,'steel',.003)
    # Flat side access panels, following the chassis taper.
    vs=[(s*.73,-.32,5.19),(s*.80,-.35,5.67),(s*.80,.23,5.75),(s*.60,.36,5.15)]
    n=len(vs);ob=mesh('Torso side access armor',vs+[(x-s*.065,y,z) for x,y,z in vs],[(0,1,2,3),(4,5,6,7),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],mat['teal'],.025)
    for z in [5.31,5.39,5.47]:
        c=Vector((s*.814,.1,z));line('Side torso cooling groove',[c+Vector((0,-.16,0)),c+Vector((0,.10,.045))],mat['black'],.012)
bevel_plate('Sternum upper keystone',[(-.23,5.99),(.23,5.99),(.25,5.66),(.16,5.49),(-.16,5.49),(-.25,5.66)],lambda x,z:-.53+.25*(z-5.65),.12,'graphite',.025)
bevel_plate('Central bronze reactor surround',[(-.20,5.51),(.20,5.51),(.34,5.27),(.25,4.98),(0,4.86),(-.25,4.98),(-.34,5.27)],-.555,.12,'gold',.025)
bevel_plate('Reactor recessed gasket',[(-.155,5.40),(.155,5.40),(.24,5.23),(.18,5.04),(-.18,5.04),(-.24,5.23)],-.579,.035,'black',.017)
bevel_plate('Green reactor inset',[(-.12,5.355),(.12,5.355),(.185,5.22),(.14,5.08),(-.14,5.08),(-.185,5.22)],-.604,.024,'green',.022)
bevel_plate('Lower sternum armor',[(-.18,5.02),(.18,5.02),(.25,4.90),(.13,4.76),(-.13,4.76),(-.25,4.90)],-.435,.13,'graphite',.027)
loft('Waist compression frame',[(4.17,0,.025,.76,.47),(4.39,0,.025,.79,.52),(4.67,0,.025,.71,.49)],'black',.023)
for z in [4.28,4.38,4.48]:box('Abdominal segmented armor',(0,-.263,z),(.47,.055,.065),mat['graphite'],.018)
for s in [-1,1]:
    cyl('Oblique abdominal hydraulic body',(s*.37,-.02,4.24),(s*.46,-.02,4.56),.063,mat['steel'])
    cyl('Abdominal piston rod',(s*.46,-.02,4.56),(s*.52,-.02,4.83),.032,mat['steel'])

# Head is a compact mechanical helmet on an actual visible neck.
group('Helmet from the parts construction guide')
box('Neck mounting deck',(0,.02,6.035),(.68,.59,.09),mat['graphite'],.06)
cyl('Neck swivel column',(0,-.06,6.04),(0,-.06,6.40),.145,mat['black'])
for z in [6.10,6.21,6.30]:ring('Neck rotary retaining ring',(0,-.06,z),.147,.022,mat['steel'],(0,0,1))
box('Neck front protective shield',(0,-.238,6.21),(.20,.059,.205),mat['graphite'],.025)
box('Neck center drive insert',(0,-.274,6.21),(.072,.018,.12),mat['steel'],.013)
for s in [-1,1]:
    cyl('Neck rear actuator',(s*.20,.18,6.06),(s*.23,.19,6.40),.045,mat['steel'])
    bevel_plate('Collar cheek guard',mirrored([(.27,6.025),(.42,6.07),(.45,6.20),(.38,6.32),(.29,6.27)],s),-.25,.18,'gold',.021)
loft('Faceted helmet shell',[(6.37,0,-.015,.59,.52),(6.60,0,-.02,.79,.69),(6.94,0,-.04,.79,.71),(7.08,0,-.01,.53,.56)],'helmet',.032)
bevel_plate('Helmet face opening',[(-.34,6.83),(.34,6.83),(.34,6.51),(.22,6.35),(-.22,6.35),(-.34,6.51)],-.43,.10,'black',.033)
for s in [-1,1]:
    bevel_plate('Layered temple cheek armor',mirrored([(.22,6.84),(.37,6.85),(.435,6.69),(.40,6.38),(.28,6.32),(.18,6.45),(.21,6.64)],s),-.47,.16,'helmet',.022)
    bevel_plate('Cheek inner machined edge',mirrored([(.23,6.66),(.29,6.72),(.33,6.48),(.29,6.38),(.23,6.43)],s),-.495,.026,'head_steel',.010)
    bevel_plate('Sensor socket',mirrored([(.035,6.765),(.33,6.82),(.315,6.715),(.085,6.682)],s),-.50,.065,'black',.010)
    bevel_plate('Cyan recessed eye strip',mirrored([(.085,6.744),(.295,6.787),(.275,6.765),(.095,6.728)],s),-.524,.012,'cyan',.004)
    bevel_plate('Brow armored swept wing',mirrored([(.01,6.805),(.22,6.93),(.58,7.155),(.46,6.982),(.21,6.824),(.05,6.76)],s),-.568,.084,'graphite',.012)
    bevel_plate('Brow machined bevel',mirrored([(.015,6.802),(.23,6.946),(.58,7.155),(.50,7.087),(.225,6.916),(.058,6.818)],s),-.581,.023,'head_steel',.004)
    bevel_plate('Gold V fin',mirrored([(.20,6.90),(.30,7.045),(.505,7.47),(.473,7.455),(.253,7.052),(.145,6.953)],s),-.525,.09,'gold',.009)
    cyl('Gold fin pivot sleeve',(s*.225,-.46,6.99),(s*.225,-.529,6.99),.034,mat['graphite'])
    bolt('Gold fin root socket',(s*.225,-.539,6.99),.021,(0,-1,0))
    box('Ear mechanical carrier',(s*.407,.01,6.64),(.11,.37,.39),mat['graphite'],.032)
    box('Ear recessed vent',(s*.471,.005,6.64),(.025,.23,.28),mat['black'],.015)
    for z in [6.54,6.60,6.66,6.72]:box('Ear cooling fin',(s*.488,.00,z),(.035,.18,.018),mat['steel'],.005)
    for yy in [-.11,.115]:bolt('Helmet ear fastener',(s*.481,yy,6.80),.018,(s,0,0))
bevel_plate('Forehead crest',[(-.115,7.095),(.115,7.095),(.17,6.97),(.12,6.856),(0,6.788),(-.12,6.856),(-.17,6.97)],lambda x,z:-.49-.11*(7.09-z),.15,'helmet',.018)
bevel_plate('Forehead sensor frame',[(-.07,7.067),(.07,7.067),(.085,6.954),(-.085,6.954)],-.517,.030,'black',.014)
bevel_plate('Forehead flat status light',[(-.041,7.041),(.041,7.041),(.050,6.98),(-.050,6.98)],-.532,.012,'cyan',.006)
# A connected two-facet mask with actual machined openings.
outline=[(-.18,6.688),(0,6.665),(.18,6.688),(.16,6.49),(.075,6.402),(0,6.385),(-.075,6.402),(-.16,6.49)]
vs=[(x,-.62+.26*abs(x),z) for x,z in outline];vs += [(x,y+.078,z) for x,y,z in vs]
fs=[(0,1,5,6,7),(1,2,3,4,5),(8,15,14,13,9),(9,13,12,11,10)]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
mask=mesh('Continuous faceted face mask',vs,fs,mat['mask'],.010)
for z,w in [(6.616,.135),(6.56,.14),(6.508,.105)]:
    cutter=box('Temporary mask vent cutter',(0,-.58,z),(w,.25,.017),mat['black'],.004)
    M.cut(mask,cutter)
M.bevel(mask,.0025)
bevel_plate('Small red chin module',[(-.041,6.467),(.041,6.467),(.054,6.414),(.032,6.358),(-.032,6.358),(-.054,6.414)],-.641,.072,'head_red',.012)
# Panel seams on the rear cap, with a flush central spine.
box('Helmet rear center spine',(0,.343,6.74),(.16,.027,.41),mat['helmet'],.029)
for s in [-1,1]:line('Helmet crown seam',[(s*.26,.22,6.89),(s*.23,.12,7.039),(s*.17,-.15,7.07)],mat['black'],.005)

group('Tapered lower legs with controlled depth')
for s in [-1,1]:
    stations=[(.71,s*1.50,.07,.43,.44),(1.10,s*1.45,.08,.43,.46),(1.85,s*1.28,.11,.56,.60),(2.18,s*1.18,.12,.60,.64),(2.45,s*1.10,.12,.51,.56)]
    loft('Straight tapered greave '+str(s),stations,'teal',.035)
    def legx(z):return 1.50-(z-.71)*.40/1.74
    pts=[(legx(2.25)-.20,2.25),(legx(2.25)+.20,2.25),(legx(1.93)+.21,1.93),(legx(.93)+.15,.93),(legx(.77),.77),(legx(.93)-.16,.93),(legx(1.93)-.21,1.93)]
    bevel_plate('Shin forward armor '+str(s),mirrored(pts,s),lambda x,z:-.18-.065*(z-.71),.085,'teal2',.022)
    pts=[(legx(2.40)-.20,2.40),(legx(2.40)+.20,2.40),(legx(2.22)+.18,2.22),(legx(2.12),2.12),(legx(2.22)-.18,2.22)]
    bevel_plate('Bronze knee saddle '+str(s),mirrored(pts,s),-.272,.105,'gold',.024)
    kc=Vector((s*1.02,.10,2.70));axis=Vector((s,0,0))
    cyl('Knee central joint',kc-axis*.19,kc+axis*.19,.162,mat['black'])
    cyl('Knee to greave load bearing link',kc,(s*1.12,.12,2.34),.13,mat['graphite'])
    for e in [-1,1]:
        cyl('Knee machined pivot',kc+axis*(e*.19),kc+axis*(e*.235),.121,mat['steel'])
        ring('Knee recessed edge',kc+axis*(e*.24),.083,.012,mat['graphite'],axis)
    p=[(.83,2.93),(1.05,3.00),(1.19,2.87),(1.29,2.48),(1.12,2.40),(.94,2.52)]
    bevel_plate('Angular knee guard '+str(s),mirrored(p,s),-.246,.17,'teal',.032)
    for zz in [1.11,2.08]:
        for xx in [-.13,.13]:bolt('Shin armor flush fastener',(s*(legx(zz)+xx),-.18-.065*(zz-.71)-.018,zz),.022,(0,-1,0))
    # The calf cover is a shallow plate, not the whole outline revolved into a bulb.
    yz=[(-.10,2.23),(.24,2.22),(.37,2.02),(.29,1.74),(.16,1.39),(-.07,1.36),(-.16,1.78)]
    vs=[(s*(legx(z)+.28),y,z) for y,z in yz];n=len(vs)
    vs += [(x-s*.068,y,z) for x,y,z in vs]
    fs=[tuple(range(n)),tuple(range(n,2*n))]+[(j,(j+1)%n,(j+1)%n+n,j+n) for j in range(n)]
    mesh('Calf shallow access shield '+str(s),vs,fs,mat['graphite'],.027)
    for z in [1.56,1.71,1.86]:
        x=s*(legx(z)+.316);line('Calf side vent slot',[(x,.10,z),(x,.27,z+.015)],mat['black'],.009)
    for xoff in [-.115,.115]:
        cyl('Rear lower leg piston',(s*1.30+xoff,.415,1.89),(s*1.43+xoff,.34,1.14),.033,mat['steel'])
    for z in [1.21,1.45]:
        x=s*legx(z);box('Rear shin status frame',(x,.37,z),(.19,.078,.22),mat['graphite'],.025)
        box('Rear shin cyan inset',(x,.414,z),(.085,.016,.14),mat['cyan'],.01)
    ac=Vector((s*1.50,.08,.61));cyl('Ankle rotating core',ac-Vector((.27,0,0)),ac+Vector((.27,0,0)),.128,mat['black'])
    for e in [-1,1]:ring('Ankle retaining ring',ac+Vector((e*.24,0,0)),.115,.022,mat['steel'],(1,0,0))
    # A stable foot with planar sole, bevelled toe, and a short heel.
    x=s*1.50
    footprint=[(-.29,-.69),(.24,-.69),(.34,-.48),(.30,.31),(.20,.42),(-.22,.42),(-.33,.25),(-.34,-.46)]
    vs=[(x+u,y,.025) for u,y in footprint]+[(x+u*.88,y*.89,(.29 if y<-.45 else .42)) for u,y in footprint]
    fs=[tuple(range(7,-1,-1)),tuple(range(8,16))]+[(i,(i+1)%8,(i+1)%8+8,i+8) for i in range(8)]
    mesh('Planar armored foot '+str(s),vs,fs,mat['graphite'],.033)
    vs=[(x-.23,-.60,.315),(x+.21,-.60,.315),(x+.235,-.12,.446),(x-.25,-.12,.446)]
    mesh('Foot machined instep',vs+[(a,b,c-.05) for a,b,c in vs],[(0,1,2,3),(4,5,6,7),(0,4,5,1),(1,5,6,2),(2,6,7,3),(3,7,4,0)],mat['steel'],.022)
    loft('Ankle upper armor '+str(s),[(.43,x,-.06,.53,.46),(.61,x,-.11,.48,.39),(.77,x,-.025,.32,.31)],'teal',.024)
    box('Foot rear heel block',(x,.30,.23),(.46,.21,.34),mat['dark'],.039)

for ob in list(bpy.data.objects):
    if ob.type=='MESH' and ob.name.startswith(('Planar armored foot','Foot machined instep','Foot rear heel block','Ankle upper armor')):
        if ob.name.startswith(('Planar armored foot','Foot machined instep')):
            center=sum((ob.matrix_world@v.co for v in ob.data.vertices),Vector())/len(ob.data.vertices);sgn=1 if center.x>0 else -1
        else:sgn=1 if ob.location.x>0 or (ob.location.length<.001 and sum(v.co.x for v in ob.data.vertices)>0) else -1
        pivot=Vector((sgn*1.50,.08,0));rot=Matrix.Rotation(sgn*.14,4,'Z')
        transform=Matrix.Translation(pivot)@rot@Matrix.Translation(-pivot)
        ob.matrix_world=transform@ob.matrix_world

# Straight-spined steel blades, mechanically independent of the fist.
group('Forearm blades with diamond cross section')
for s in [-1,1]:
    a=Vector((s*1.85,-.015,4.92));b=Vector((s*2.43,-.08,4.02));axis=(b-a).normalized()
    prism('Blade carriage main chassis',a,b,.245,.245,mat['graphite'],.22,edge=.023)
    q=axis.to_track_quat('Z','Y');n=q@Vector((0,-1,0));u=q@Vector((1,0,0))
    prism('Carriage layered upper rail',a+n*.147+axis*.10,b+n*.147-axis*.12,.155,.047,mat['steel'],.2,edge=.009)
    prism('Carriage recessed central track',a+n*.177+axis*.17,b+n*.177-axis*.18,.070,.020,mat['black'],.13,edge=.004)
    prism('Carriage bronze exit collar',b-axis*.10,b+axis*.025,.282,.274,mat['gold'],.19,edge=.015)
    for t in [.22,.68]:
        c=a.lerp(b,t);end=c-Vector((s*.28,0,0));prism('Forearm blade mounting bracket',end,c,.15,.14,mat['dark'],.2,edge=.017)
        bolt('Carrier flush screw',c+n*.145,.022,n)
    # Blade width is orthogonal to its length; neither cross-section twists along it.
    direction=axis.copy();width_axis=Vector((s*.72,-.69,0));width_axis=(width_axis-direction*width_axis.dot(direction)).normalized();normal=direction.cross(width_axis).normalized()
    root=b+axis*.028;length=2.36
    rows=[(0,.15),(.06,.245),(.70,.245),(.84,.19),(.94,.10),(1,.001)]
    vs=[]
    for t,w in rows:
        c=root+direction*(t*length);half=.022*(1-t*.85)
        vs.extend([c,c+width_axis*(w*.42)+normal*half,c+width_axis*w,c+width_axis*(w*.42)-normal*half])
    fs=[(0,1,2,3)]
    for j in range(len(rows)-1):
        for k in range(4):fs.append((j*4+k,j*4+(k+1)%4,(j+1)*4+(k+1)%4,(j+1)*4+k))
    fs.append(tuple(range(len(vs)-4,len(vs))))
    blade=mesh('Rigid diamond-section blade '+str(s),vs,fs,mat['silver'],.002)
    blade['width_max']=.245;blade['length']=length;blade['thickness_root']=.044;blade['construction']='Straight spine, fixed cross-section orientation, tapered cutting edge'
    line('Blade spine bevel',[root+normal*.006,root+direction*(length*.85)+normal*.003],mat['steel'],.007)

# Shorter stepped rail cannons with real recessed muzzle cavities.
group('Shoulder cannon receivers and elevation mounts')
for s in [-1,1]:
    x=s*1.16
    a=Vector((x,1.33,7.37));b=Vector((x,-1.27,7.56));axis=(b-a).normalized();up=Vector((0,.073,1)).normalized();right=Vector((1,0,0))
    prism('Cannon box section shroud',a,b-axis*.10,.54,.52,mat['teal'],.16,sections=[(0,.9),(.10,1.1),(.24,1.1),(.30,.82),(.84,.82),(.88,1),(1,1)],edge=.019)
    prism('Cannon rear receiver',a-axis*.10,a+axis*.63,.65,.62,mat['graphite'],.23,edge=.027)
    for edge in [-1,1]:
        off=right*(edge*.293)
        prism('Cannon side rail',a+axis*.71+off,b-axis*.32+off,.075,.27,mat['graphite'],.16,edge=.012)
        line('Cannon bronze cooling rail',[a+axis*.76+right*(edge*.335)-up*.085,b-axis*.37+right*(edge*.335)-up*.085],mat['gold'],.012)
        for t in [.70,.76,.82]:
            c=a.lerp(b,t)+right*(edge*.304)
            line('Cannon cooling slot',[c-up*.09,c+up*.04+axis*.018],mat['black'],.013)
        box('Receiver side access plate',a+axis*.26+right*(edge*.344),(.048,.29,.20),mat['teal2'],.026)
        for zz in [-.13,.13]:bolt('Receiver case fastener',a+axis*.37+right*(edge*.355)+up*zz,.020,right*edge)
    # An eight-sided rim around a cavity, open rather than covered by the shroud.
    c=b+axis*.07;out=[(-.20,-.31),(.20,-.31),(.30,-.21),(.30,.21),(.20,.31),(-.20,.31),(-.30,.21),(-.30,-.21)]
    inner=[(u*.78,v*.80) for u,v in out];vs=[]
    for depth,pts in [(-.20,out),(.08,out),(.08,inner),(-.12,inner)]:
        vs.extend([c+right*u+up*v+axis*depth for u,v in pts])
    fs=[]
    for j in range(4):
        for k in range(8):fs.append((j*8+k,j*8+(k+1)%8,((j+1)%4)*8+(k+1)%8,((j+1)%4)*8+k))
    mesh('Recessed muzzle sleeve',vs,fs,mat['graphite'],.012)
    prism('Muzzle internal dark plate',c-axis*.122,c-axis*.119,.45,.47,mat['black'],.16,edge=.005)
    for dx,dz in [(0,.17),(-.085,.045),(.085,.045),(0,-.13)]:
        p=c+right*dx+up*dz-axis*.06
        tube('Muzzle recessed bore',p-axis*.056,p+axis*.018,.049,.035,mat['steel'],32)
        ring('Muzzle bore bronze lip',p+axis*.02,.042,.006,mat['gold'],axis)
    # A compact load-bearing mount places the head ahead of the backpack column.
    prism('Cannon support spine',(x,.69,6.10),(x,.77,7.18),.35,.35,mat['graphite'],.20,edge=.032)
    hc=Vector((x,.76,7.14));cyl('Cannon trunnion',hc-right*.23,hc+right*.23,.16,mat['steel'])
    for edge in [-1,1]:
        cyl('Elevation pivot cap',hc+right*(edge*.231),hc+right*(edge*.263),.111,mat['graphite'],n=12)
        ring('Elevation bearing ring',hc+right*(edge*.270),.09,.012,mat['gold'],right)
    cyl('Elevation hydraulic sleeve',(x,1.01,6.19),(x,.96,6.69),.067,mat['dark'])
    cyl('Elevation hydraulic rod',(x,.96,6.69),(x,.89,7.11),.034,mat['steel'])
    box('Cannon rear emitter frame',(x,.90,6.18),(.27,.13,.37),mat['dark'],.035)
    box('Cannon rear cyan inset',(x,.974,6.18),(.105,.015,.23),mat['cyan'],.016)

# Store both the new guide and original references, with clear provenance.
ref=bpy.data.collections.new('REFERENCE • R6 generated construction guide');bpy.context.scene.collection.children.link(ref)
im=bpy.data.images.load(os.path.join(OUT,'construction_guide.png'));im.pack()
ob=bpy.data.objects.new('AI construction guide • not a Blender render',None);ref.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=im;ob.empty_display_size=12;ob.location=(0,3,4);ob.rotation_euler=(math.pi/2,0,0);ob.hide_render=True;ref.hide_viewport=True
s=bpy.context.scene;s['Revision']='R6 controlled cross-sections and independent mechanical assemblies';s['Guide provenance']='AI-generated reference. Actual render files use this Blender mesh.'
# Side inspection uses flat lighting from both directions so depth cannot hide in shadow.
M.group('R6 • Inspection lighting')
ld=bpy.data.lights.new('Side inspection softbox','AREA');ld.energy=1000;ld.shape='DISK';ld.size=7
lo=bpy.data.objects.new('Side inspection softbox',ld);M.COL.objects.link(lo);lo.location=(-7,1,7);lo.rotation_euler=(Vector((0,0,4))-lo.location).to_track_quat('-Z','Y').to_euler()
s.view_settings.look='AgX - Medium High Contrast';s.cycles.samples=24;s.cycles.use_denoising=True;s.cycles.adaptive_threshold=.10
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
s.cycles.device='GPU';s.camera=bpy.data.objects['CAM • Three quarter geometry'];s.camera.location=(-11,-20,8.5);s.camera.rotation_euler=(Vector((0,0,4))-s.camera.location).to_track_quat('-Z','Y').to_euler();s.camera.data.ortho_scale=9.5
bpy.data.objects['CAM • Front traced alignment'].data.ortho_scale=9.3
s.render.resolution_x=1100;s.render.resolution_y=1300;s.render.resolution_percentage=100;s.view_layers[0].material_override=None
for text0 in list(bpy.data.texts):
    if 'READ ME' in text0.name:bpy.data.texts.remove(text0)
t=bpy.data.texts.new('READ ME • Revision 6');t.write('Revision 6 replaces the inflated chest, lower legs, helmet, blades and shoulder cannon meshes. New parts use explicit cross-section dimensions and planar armored shells.\n\nThe AI-generated construction guide is packed in the REFERENCE collection. It is a design reference, not an image of this mesh. The supplied original images remain packed too.\n\nThe actual renders include color, side/front views and neutral clay inspection. Fine surface detail remains an approximation.\n')
assert all(math.isfinite(f) for o in bpy.data.objects if o.type=='MESH' for v in o.data.vertices for f in v.co)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Revision6.blend'))
print('MODEL_SAVED',len(bpy.data.objects),flush=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
clay=M.material('R6 inspection clay','8C989F',.05,.63)
for view in (['side_clay','front_clay','side','hero'] if '--preview' in args else []):
    name='CAM • Side traced alignment' if 'side' in view else ('CAM • Front traced alignment' if 'front' in view else 'CAM • Three quarter geometry')
    s.camera=bpy.data.objects[name];s.view_layers[0].material_override=clay if 'clay' in view else None
    bpy.data.objects['Ground'].hide_render=view!='hero'
    s.render.resolution_x=700 if 'side' in view else 880;s.render.resolution_y=1000;s.cycles.samples=12
    s.render.filepath=os.path.join(OUT,'preview_'+view+'.png');bpy.ops.render.render(write_still=True);print('RENDERED',view,flush=True)
