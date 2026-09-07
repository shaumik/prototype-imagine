import bpy, bmesh, math, os, sys, json
from mathutils import Vector, Matrix
OUT=os.path.dirname(os.path.abspath(__file__));sys.path.insert(0,OUT)
from trace_data import *
import mechanical as M
from mechanical import mesh,bevel,box,cyl,ring,line,bolt,plate,prism,tube,cut

bpy.ops.object.select_all(action='SELECT');bpy.ops.object.delete(use_global=False)
for col in list(bpy.data.collections):bpy.data.collections.remove(col)
def group(name):return M.group(name)
def rgb(h):return M.rgb(h)
source=bpy.data.images.load('/Users/shaumikmondal/Downloads/Gemini_Generated_Image_rkxrc3rkxrc3rkxr.jpg');source.pack()

palette={'teal':'385D65','teal_light':'4C737D','graphite':'44464B','alloy':'737C7E','silver':'B4C3C6','bronze':'AF8556','black':'12171D','red':'B3503F','green':'275A35','cyan':'5DE8ED'}
plain={};photo={}
for key,color in palette.items():
    m=M.material('Traced • '+key,color,.55 if key not in ['silver','alloy','bronze'] else .76,.40,glow=1.2 if key=='cyan' else 0)
    plain[key]=m
    p=m.copy();p.name='Reference projection • '+key
    ns=p.node_tree.nodes;lk=p.node_tree.links;shader=ns.get('Principled BSDF')
    tex=ns.new('ShaderNodeTexImage');tex.image=source;tex.interpolation='Linear';tex.extension='EXTEND'
    mix=ns.new('ShaderNodeMixRGB');mix.name='Original image influence';mix.label='Original sheet color, 0 = plain finish';mix.inputs[0].default_value=0.0;mix.inputs[1].default_value=(*rgb(color),1)
    lk.new(tex.outputs['Color'],mix.inputs[2]);lk.new(mix.outputs[0],shader.inputs['Base Color'])
    shader.inputs['Metallic'].default_value=.58;shader.inputs['Roughness'].default_value=.42
    photo[key]=p
M.steel=plain['alloy'];M.black=plain['black'];M.bronze=plain['bronze'];M.frame=plain['graphite']

def F(u,v,y=0):return Vector(((u-FRONT_CENTER)/SCALE,y,(FLOOR-v)/SCALE))
def side_y(u):return (SIDE_CENTER-u)/SCALE
def mirrored(points):return [(2*FRONT_CENTER-u,v) for u,v in points]
def span(poly,v):
    lo=min(p[1] for p in poly);hi=max(p[1] for p in poly);v=max(lo+.00001,min(hi-.00001,v));xs=[]
    for a,b in zip(poly,poly[1:]+poly[:1]):
        if (a[1]<=v<b[1]) or (b[1]<=v<a[1]):xs.append(a[0]+(b[0]-a[0])*(v-a[1])/(b[1]-a[1]))
    return (min(xs),max(xs)) if xs else (min(p[0] for p in poly),max(p[0] for p in poly))

def project(ob,key,mode='auto',info=None,mirror_front=False):
    if ob.type!='MESH':return
    ob.data.materials.clear();ob.data.materials.append(photo[key]);ob.data.materials.append(plain[key])
    uv=ob.data.uv_layers.new(name='Original character sheet projection')
    normalmatrix=ob.matrix_world.to_3x3().inverted().transposed()
    for p in ob.data.polygons:
        n=normalmatrix@p.normal
        view=mode
        if mode=='auto':view='front' if n.y<-.48 else ('rear' if n.y>.48 else 'side')
        if mode=='front' and n.y>-.35:p.material_index=1
        if mode=='rear' and n.y<.35:p.material_index=1
        for li in p.loop_indices:
            co=ob.matrix_world@ob.data.vertices[ob.data.loops[li].vertex_index].co
            v=FLOOR-co.z*SCALE
            if view=='front':
                u=FRONT_CENTER+co.x*SCALE
                if mirror_front:u=2*FRONT_CENTER-u
                su,sv=u+331,v+203
            elif view=='rear':su,sv=REAR_CENTER-co.x*SCALE+1510,v+203
            else:
                if info:
                    f0,f1,s0,s1=info;v=s0+(v-f0)/(f1-f0)*(s1-s0)
                su,sv=SIDE_CENTER-co.y*SCALE+1044,v+203
            uv.data[li].uv=(su/2048,1-sv/1119)
    ob['reference_source']='Gemini_Generated_Image_rkxrc3rkxrc3rkxr.jpg'
    ob['construction']='Geometry traced from front outline and side depth profile'

cores={}
def volume(name,fp,sp,key,mirror_uv=False,n=3.3):
    f0,f1=min(v for u,v in fp),max(v for u,v in fp);s0,s1=min(v for u,v in sp),max(v for u,v in sp)
    samples={f0+.14,f1-.14}
    samples.update(v for u,v in fp if f0+.14<v<f1-.14)
    samples.update(f0+(f1-f0)*k/36 for k in range(1,36))
    rows=sorted(samples);vs=[];count=48
    for vv in rows:
        xl,xr=span(fp,vv);sv=s0+(vv-f0)/(f1-f0)*(s1-s0);sl,sr=span(sp,sv)
        cx=(xl+xr)/2;cy=side_y((sl+sr)/2);rx=max(.002,(xr-xl)/200);ry=max(.003,(sr-sl)/200)
        for j in range(count):
            t=math.tau*j/count;cc=math.cos(t);ss=math.sin(t)
            vs.append(((cx-FRONT_CENTER)/100+rx*math.copysign(abs(cc)**(2/n),cc),cy+ry*math.copysign(abs(ss)**(2/n),ss),(FLOOR-vv)/100))
    fs=[tuple(range(count))]
    for j in range(len(rows)-1):
        for k in range(count):fs.append((j*count+k,j*count+(k+1)%count,(j+1)*count+(k+1)%count,(j+1)*count+k))
    fs.append(tuple(range((len(rows)-1)*count,len(rows)*count)))
    ob=mesh(name,vs,fs,plain[key],0)
    for p in ob.data.polygons:p.use_smooth=len(p.vertices)==4
    project(ob,key,'auto',(f0,f1,s0,s1),mirror_uv)
    ob['front_trace']=json.dumps(fp);ob['side_trace']=json.dumps(sp)
    smooth=ob.modifiers.new('Small surface fairing','SMOOTH');smooth.factor=.16;smooth.iterations=3
    data={'object':ob,'front':fp,'side':sp,'range':(f0,f1,s0,s1),'n':n,'mirror_uv':mirror_uv}
    cores[name]=data;return data

def front_depth(core,u,v):
    fp,sp=core['front'],core['side'];f0,f1,s0,s1=core['range'];v=max(f0+.2,min(f1-.2,v))
    l,r=span(fp,v);sv=s0+(v-f0)/(f1-f0)*(s1-s0);sl,sr=span(sp,sv)
    cy=side_y((sl+sr)/2);ry=(sr-sl)/200;n=core['n'];x=max(-.985,min(.985,(u-(l+r)/2)/max((r-l)/2,.01)))
    return cy-ry*(max(.001,1-abs(x)**n))**(1/n)

def frontpanel(name,pts,key,core=None,offset=.025,thick=.055,y=None,mirror_uv=False):
    from mathutils.geometry import tessellate_polygon
    def depth(u,v):
        
        if y is not None:return y-offset
        l,r=span(core['front'],v)
        return front_depth(core,(l+r)/2,v)-offset-.055
    # A tessellated surface follows the traced volume instead of extending a tangent
    # plane beyond its valid region. The boundary retains the original drawn outline.
    verts=[];fs=[];lookup={}
    def vertex(u,v,back=False):
        key0=(round(u,4),round(v,4),back)
        if key0 not in lookup:
            lookup[key0]=len(verts);verts.append(F(u,v,depth(u,v)+(thick+offset+.10 if back else 0)))
        return lookup[key0]
    triangles=tessellate_polygon([[Vector((u,v,0)) for u,v in pts]])
    for tri in triangles:
        a,b,c=[Vector((*pts[t],0)) if isinstance(t,int) else t for t in tri];n=max(2,min(24,int(max((b-a).length,(c-a).length,(c-b).length)/3)+1))
        for i in range(n):
            for j in range(n-i):
                def q(ii,jj):
                    p=a+(b-a)*(ii/n)+(c-a)*(jj/n);return vertex(p.x,p.y)
                fs.append((q(i,j),q(i+1,j),q(i,j+1)))
                if j<n-i-1:fs.append((q(i+1,j),q(i+1,j+1),q(i,j+1)))
    for a,b in zip(pts,pts[1:]+pts[:1]):
        n=max(2,int(math.dist(a,b)/5)+1)
        for j in range(n):
            u=a[0]+(b[0]-a[0])*j/n;v=a[1]+(b[1]-a[1])*j/n
            un=a[0]+(b[0]-a[0])*(j+1)/n;vn=a[1]+(b[1]-a[1])*(j+1)/n
            fs.append((vertex(u,v),vertex(un,vn),vertex(un,vn,True),vertex(u,v,True)))
    ob=mesh(name,verts,fs,plain[key],0)
    for f in ob.data.polygons:f.use_smooth=len(f.vertices)==3
    project(ob,key,'front',core['range'] if core else None,mirror_uv)
    ob['front_trace']=json.dumps(pts)
    if key!='black':
        path=[F(u,v,depth(u,v)-.004) for u,v in pts]
        line('Fine machined edge • '+name,path+[path[0]],plain[key],.0045)
    return ob

group('01 • Body volumes from traced outlines')
for item in VOLUMES:
    if item['name']=='Waist':
        item['front']=[(338,321),(354,334),(369,351),(399,351),(415,335),(431,321),(433,351),(423,365),(343,365),(332,351)]
        item['side']=[(229,318),(265,327),(284,346),(287,368),(277,382),(250,385),(232,367),(222,344)]
    if item['name']=='Pelvic core':item['front']=[(383+(u-383)*.78,v) for u,v in item['front']]
    if item['name']=='Forearm':continue
    for mirrored_side in ([False,True] if item.get('mirror') else [False]):
        name=item['name']+(' R' if mirrored_side else (' L' if item.get('mirror') else ''))
        volume(name,mirrored(item['front']) if mirrored_side else item['front'],item['side'],item['mat'])
for side in ['R','L']:
    pts=GAUNTLET_RIGHT if side=='R' else mirrored(GAUNTLET_RIGHT)
    volume('Forearm '+side,pts,GAUNTLET_SIDE,'teal_light',side=='L')

group('02 • Traced front armor panels')
offsets={}
for item in PANELS:
    for flip in ([False,True] if item.get('mirror') else [False]):
        suffix=(' R' if flip else ' L') if item.get('mirror') else ''
        corename=item['core']+suffix
        if corename not in cores:corename=item['core']
        co=cores[corename];pts=mirrored(item['pts']) if flip else item['pts']
        layers={'Shoulder upper main plate':.045,'Shoulder inner teal plate':.045,'Shoulder bronze wrap':.090,'Shoulder lower graphite plate':.135,
        'Pectoral graphite armor':.040,'Chest intake bronze surround':.10,'Chest intake dark pocket':.14,
        'Sternum upper facet':.045,'Sternum bronze reactor frame':.085,'Reactor recessed hexagon':.12,'Reactor green crystal':.155,'Lower breastplate keel':.12,
        'Upper hip front plate':.040,'Front skirt main armor':.055,'Front skirt inset':.085,'Belt central carrier':.090,'Belt red marker':.13,'Pelvic central long plate':.1,
        'Knee crown inset':.05,'Knee bronze marker':.09,'Greave central armor':.045,'Greave bronze knee saddle':.1,'Calf outside armor':.035,'Calf inside armor':.04,
        'Ankle upper plate':.05,'Ankle locking tab':.10,'Foot pale instep':.05,'Foot toe bumper':.10}
        extra=layers.get(item['name'],.05)
        frontpanel(item['name']+suffix,pts,item['mat'],co,extra)

# The asymmetric panel edges below are traced directly from the clean right forearm.
for side in ['R','L']:
    flip=side=='L';co=cores['Forearm '+side]
    for name,key,pts,off in [
        ('Forearm inset armor','teal',[(535,339),(552,331),(568,349),(579,373),(581,385),(568,388),(554,361),(544,355)],.035),
        ('Forearm alloy wrist cuff','alloy',[(556,388),(591,376),(601,391),(600,403),(578,415),(559,407)],.030),
        ('Forearm front dark recess','graphite',[(527,343),(537,339),(548,353),(560,379),(559,393),(546,387),(533,363)],.065)]:
        frontpanel(name+' '+side,mirrored(pts) if flip else pts,key,co,off,mirror_uv=flip)

group('03 • Joint mechanisms aligned to the sheet')
for sign in [-1,1]:
    def p(u,v,y=0):return F(FRONT_CENTER+sign*(u-FRONT_CENTER),v,y)
    # Shoulder, elbow, hip, knee and ankle axes come from the visible joint centers.
    for name,u,v,r,y in [('Shoulder',455,221,.19,.16),('Elbow',515,301,.15,.05),('Hip',420,428,.18,.02),('Knee',465,551,.145,.23),('Ankle',522,725,.115,.14)]:
        c=p(u,v,y);axis=Vector((sign,0,0));cyl(name+' rubber bearing',c-axis*.15,c+axis*.15,r,plain['black'])
        cyl(name+' outer bearing',c+axis*.14,c+axis*.19,r*.72,plain['alloy'])
        ring(name+' bearing edge',c+axis*.196,r*.59,.010,plain['graphite'],axis)
    # A compact neck follows the narrow gap visible in the sheet.
cyl('Neck visible rotary column',F(383,210,.03),F(383,191,.03),.16,plain['graphite'])
for v in [197,202,208]:ring('Neck rotary seal',F(383,v,.03),.163,.013,plain['alloy'],(0,0,1))

group('04 • Helmet and face traced at source pixel coordinates')
helmet=cores['Helmet shell']
# Keep the low-resolution sheet projection off the face: these details are real plates.
def face(name,pts,key,y,depth=.04,edge=.006):
    ob=plate(name,[(F(u,v).x,F(u,v).z) for u,v in pts],y,depth,plain[key],edge);ob['front_trace']=json.dumps(pts);return ob
fy=-.665
face('Dark recessed face opening',[(353,147),(411,147),(415,170),(404,192),(384,198),(363,192),(351,173)],'black',fy+.055,.11)
for flip in [False,True]:
    fn=lambda ps:mirrored(ps) if flip else ps
    face('Helmet layered cheek',fn([(346,145),(359,156),(365,164),(362,190),(353,190),(344,177)]),'teal',fy-.015,.11)
    face('Helmet inset cheek edge',fn([(350,152),(357,160),(358,181),(359,189),(352,186),(348,177)]),'alloy',fy-.032,.035)
    face('Temple mechanical surround',fn([(340,142),(348,145),(346,170),(341,178),(336,170),(336,149)]),'graphite',fy+.06,.12)
    for vv in [149,157,166]:
        ps=fn([(339,vv),(344,vv),(344,vv+4),(339,vv+4)]);face('Temple recessed rectangular slot',ps,'black',fy+.038,.020,.002)
    face('Eye recessed angular pocket',fn([(355,154),(380,159),(377,165),(363,163)]),'black',fy-.031,.035)
    face('Eye thin flat sensor',fn([(359,156),(376,160),(372,162),(363,160)]),'silver',fy-.064,.015,.002)
    face('Swept silver V brow',fn([(316,108),(323,112),(349,137),(383,156),(380,161),(344,141),(318,115)]),'alloy',fy-.050,.046,.004)
    face('Brow bright machined edge',fn([(317,108),(323,111),(350,136),(382,156),(380,157),(348,139)]),'silver',fy-.072,.02,.002)
    face('Traced gold antenna',fn([(337,69),(341,72),(357,112),(365,126),(378,137),(379,145),(360,132),(354,121)]),'bronze',-.40,.065,.005)
face('Helmet central crest',[(372,101),(393,101),(395,127),(371,128)],'teal',-.435,.16,.01)
face('Forehead sensor recess',[(376,112),(390,112),(390,126),(376,126)],'black',-.474,.035,.003)
face('Forehead cyan flat sensor',[(379,115),(388,115),(389,124),(378,124)],'cyan',-.491,.014,.002)
face('Traced central forehead facet',[(371,128),(394,127),(393,140),(383,155),(373,142)],'teal_light',fy-.078,.055,.004)
maskpts=[(365,165),(399,165),(397,177),(389,190),(377,189),(369,179)]
mask=face('Compact traced face mask',maskpts,'alloy',fy-.054,.080,.010)
for vv in [170,174,178]:
    face('Mask fine vent',[(378,vv),(388,vv),(388,vv+1.15),(378,vv+1.15)],'graphite',fy-.138,.012,.001)
face('Red lower chin module',[(380,180),(386,180),(391,189),(388,198),(380,198),(376,190)],'red',fy-.088,.08,.010)

group('05 • Compact hands traced from the supplied fist')
for side in ['R','L']:
    flip=side=='L';pts=mirrored(HAND_FRONT) if flip else HAND_FRONT
    hand=volume('Traced fist '+side,pts,HAND_SIDE,'graphite',flip,n=3.9)
    for name,key,pts in [
        ('Opposed thumb','alloy',[(574,414),(583,417),(582,429),(575,438),(570,449),(563,448),(563,439),(569,430)]),
        ('Curled fingers lower armor','graphite',[(575,446),(582,440),(596,438),(602,447),(596,457),(582,461),(570,457)]),
        ('Index outer pad','alloy',[(584,429),(590,426),(599,433),(598,439),(586,441),(580,445),(576,443)])]:
        frontpanel(name+' '+side,mirrored(pts) if flip else pts,key,hand,.095 if 'thumb' in name else (.065 if 'Index' in name else .035),mirror_uv=flip)
    # Actual narrow divisions across the curled finger bank remain visible in clay views.
    for j in range(3):
        u=580+j*5
        if flip:u=766-u
        y=front_depth(hand,u,453)-.045
        line('Curled finger articulation groove',[F(u,448,y),F(u+(-1 if flip else 1)*2,455,y)],plain['black'],.005)

group('06 • Traced skirt side armor')
for sign in [-1,1]:
    for name,pts,key in [
        ('Floating lateral hip plate',[(304,350),(315,355),(310,378),(298,401),(283,410),(270,403),(272,382),(285,358)],'teal'),
        ('Trailing hip armor fin',[(291,401),(307,419),(291,451),(274,472),(252,486),(245,482),(258,453),(273,420)],'teal')]:
        pp=pts if sign<0 else mirrored(pts);core=cores['Thigh L' if sign<0 else 'Thigh R']
        frontpanel(name+str(sign),pp,key,core,.01,thick=.13,y=.0)

print('TRACED_BODY_COMPLETE',len(bpy.data.objects),flush=True)

def sideplate(name,pts,x,thick,key):
    vs=[(x,side_y(u),(FLOOR-v)/100) for u,v in pts]
    vs += [(x+thick,y,z) for _,y,z in vs]
    n=len(pts);fs=[tuple(range(n)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    ob=mesh(name,vs,fs,plain[key],.014);project(ob,key,'side');ob['side_trace']=json.dumps(pts);return ob

group('07 • Shoulder cannons traced from side silhouette')
for sign in [-1,1]:
    xc=sign*1.16
    sideplate('Cannon main stepped receiver '+str(sign),CANNON_SIDE,xc-.26,.52,'teal')
    # Broad flat rail housings follow the source, with a separate rectangular muzzle.
    for name,pts,key,thick in [
        ('Long inset barrel rail',[(153,65),(355,34),(347,63),(165,94)],'alloy',.023),
        ('Lower barrel spine',[(170,108),(349,81),(364,99),(165,126)],'graphite',.03),
        ('Receiver cheek',[(49,73),(114,61),(139,87),(130,116),(101,137),(57,135),(45,115)],'teal_light',.05),
        ('Receiver metal inset',[(59,83),(120,73),(126,91),(63,106)],'alloy',.065),
        ('Muzzle angular sleeve',[(359,37),(419,18),(423,52),(414,95),(362,109),(347,96)],'graphite',.055)]:
        for edge in [-1,1]:sideplate(name+' '+str(sign)+str(edge),pts,xc+edge*.267,edge*thick,key)
    direction=Vector((0,-1,.12)).normalized();up=Vector((0,.12,1)).normalized()
    center=Vector((xc,side_y(439),(FLOOR-53)/100))
    prism('Chamfered rectangular muzzle frame',center-direction*.13,center+direction*.035,.55,.73,plain['alloy'],.13,edge=.012)
    prism('Recessed dark muzzle face',center+direction*.038,center+direction*.042,.432,.609,plain['black'],.13,edge=.008)
    for dx,dz in [(0,.205),(-.095,.070),(.095,.070),(0,-.135)]:
        c=center+Vector((dx,0,0))+up*dz+direction*.044
        tube('Small recessed cannon bore',c-direction*.08,c+direction*.006,.045,.029,plain['bronze'],32)
        cyl('Bore darkness',c-direction*.08,c-direction*.078,.030,plain['black'],edge=0)
    fp=[(241,84),(296,84),(299,118),(307,159),(306,184),(288,199),(255,196),(239,179),(235,151),(240,114)]
    if sign>0:fp=mirrored(fp)
    sp=[(97,122),(143,125),(166,146),(174,199),(167,229),(144,243),(117,226),(99,196),(93,162)]
    volume('Shoulder cannon support '+str(sign),fp,sp,'graphite')
    for yy,zz in [(1.07,6.45),(.92,6.24)]:
        c=Vector((xc,yy,zz));cyl('Cannon elevation hinge',c-Vector((.34,0,0)),c+Vector((.34,0,0)),.16,plain['alloy'])
    # Rear glowing exhaust is a rectangular inset, not a round barrel end.
    c=Vector((xc,1.14,6.02));box('Cannon rear emitter frame',c,(.38,.13,.63),plain['graphite'],.06)
    box('Cannon rear cyan emitter',c+Vector((0,.073,0)),(.15,.020,.43),plain['cyan'],.025)

group('08 • Paired forearm blade carriers')
for side in ['R','L']:
    flip=side=='L';sign=-1 if flip else 1
    carriage=[(574,260),(582,258),(594,276),(611,308),(625,339),(635,370),(638,403),(628,432),(611,429),(602,411),(593,382),(583,354),(569,322),(560,299),(560,278)]
    sp=[(185,309),(200,310),(217,329),(243,362),(275,400),(279,426),(261,432),(238,413),(211,377),(185,345),(174,320)]
    volume('Blade deployment housing '+side,mirrored(carriage) if flip else carriage,sp,'graphite',flip,n=5)
    # The blade exits its independent forearm housing beyond and outside the fist.
    fp=mirrored(BLADE_FRONT) if flip else BLADE_FRONT
    f0,f1=min(v for u,v in fp),max(v for u,v in fp);s0,s1=415,704
    rows=sorted(set([f0+.15,f1-.15]+[v for u,v in fp if f0<v<f1]+[f0+(f1-f0)*k/28 for k in range(1,28)]))
    vs=[]
    for v in rows:
        l,r=span(fp,v);sl,sr=span(BLADE_SIDE,s0+(v-f0)/(f1-f0)*(s1-s0));yy=side_y((sl+sr)/2)
        edge_l=side_y(sr if flip else sl);edge_r=side_y(sl if flip else sr)
        for u,dep in [(l,edge_l),((l+r)*.5,yy-.035),(r,edge_r),((l+r)*.5,yy+.035)]:vs.append(F(u,v,dep))
    fs=[(0,1,2,3)]
    for j in range(len(rows)-1):
        for i in range(4):fs.append((4*j+i,4*j+(i+1)%4,4*(j+1)+(i+1)%4,4*(j+1)+i))
    fs.append(tuple(range(len(vs)-4,len(vs))))
    ob=mesh('Traced curved wrist blade '+side,vs,fs,plain['silver'],.003)
    ob['front_trace']=json.dumps(fp);ob['side_trace']=json.dumps(BLADE_SIDE)
    for p in ob.data.polygons:p.use_smooth=True
    # Narrow darker spine follows the inner sweep; all of it remains outside the hand.
    pts=[(625,397),(644,435),(667,480),(689,523),(699,547)]
    path=[]
    for u,v in pts:
        sl,sr=span(BLADE_SIDE,s0+(v-f0)/(f1-f0)*(s1-s0));l,r=span(BLADE_FRONT,v);frac=max(0,min(1,(u-l)/max(r-l,.01)));path.append(F(766-u if flip else u,v,side_y(sl+(sr-sl)*frac)-.045))
    line('Blade dark longitudinal spine '+side,path,plain['alloy'],.025)

# Side-facing armor plates are drawn from the profile view as well as the front.
group('09 • Side profile armor and exposed mechanisms')
for sign in [-1,1]:
    for name,pts,key,xc in [
        ('Shoulder bronze side rim',[(184,119),(217,116),(233,143),(244,181),(241,202),(226,207),(214,191),(197,187),(182,198)],'bronze',1.57),
        ('Shoulder dark side vent',[(193,125),(212,123),(224,159),(191,159)],'black',1.595),
        ('Upper arm layered side plate',[(195,198),(222,201),(236,214),(229,233),(214,237),(199,230)],'teal_light',1.45),
        ('Calf contoured outer shield',[(172,558),(196,552),(216,568),(221,589),(218,612),(198,634),(175,644),(152,633),(141,614),(145,587)],'graphite',1.52)]:
        sideplate(name+str(sign),pts,sign*xc,sign*.07,key)
    for v in [134,139,144,149,154]:sideplate('Shoulder vent louver',[(195,v),(218,v),(219,v+1.8),(195,v+1.8)],sign*1.611,sign*.012,'graphite')

def rearplate(name,pts,key,y,thick=.06):
    vs=[((REAR_CENTER-u)/100,y,(FLOOR-v)/100) for u,v in pts]
    vs += [(x,yy-thick,z) for x,yy,z in vs]
    n=len(pts);fs=[tuple(range(n)),tuple(range(n,2*n))]+[(i,(i+1)%n,(i+1)%n+n,i+n) for i in range(n)]
    ob=mesh(name,vs,fs,plain[key],.014);project(ob,key,'rear');return ob

group('10 • Rear armor traced from rear view')
for item in REAR_PANELS:
    name=item['name'];yy=.29 if 'pelvic' in name else 1.03;thick=.12
    if 'main armor' in name:thick=.64
    if 'equipment' in name:yy+=.10;thick=.22
    if 'turbine' in name:yy+=.12 if 'frame' in name else .17
    if 'vent' in name:yy+=.15
    rearplate(name,item['pts'],item['mat'],yy,thick)
for sign in [-1,1]:
    c=Vector((sign*.64,1.05,4.98));d=Vector((0,.32,-1)).normalized()
    tube('Rear thruster nozzle',c-d*.22,c+d*.12,.18,.133,plain['alloy'])
    cyl('Rear thruster inner glow',c,c+d*.012,.13,plain['cyan'])
    for z in [5.63,5.73]:box('Backpack cyan rectangular vent',(sign*.56,1.155,z),(.19,.025,.065),plain['cyan'],.008)
    for z,x in [(1.40,1.10),(1.11,1.16)]:
        box('Rear calf vent frame',(sign*x,.47,z),(.23,.06,.31),plain['graphite'],.04)
        box('Rear calf cyan inset',(sign*x,.51,z),(.13,.02,.20),plain['cyan'],.02)

group('11 • Recessed details and joint bridges')
for sign in [-1,1]:
    a=F(383+sign*125,290,.1);b=F(383+sign*146,326,.1)
    cyl('Elbow visible actuator',a,b,.10,plain['alloy'])
    for off in [-.08,.08]:cyl('Elbow dark piston rod',a+Vector((off,-.08,0)),b+Vector((off,-.08,0)),.027,plain['graphite'])
    pts=[(312,251),(345,259),(346,271),(315,263)]
    if sign>0:pts=mirrored(pts)
    frontpanel('Chest deep intake opening '+str(sign),pts,'black',cores['Thorax'],.17)
    pts=[(316,259),(343,266),(343,269),(316,262)]
    if sign>0:pts=mirrored(pts)
    frontpanel('Chest inner intake bar '+str(sign),pts,'alloy',cores['Thorax'],.195,thick=.024)
frontpanel('Pelvis rectangular vent surround',[(374,434),(392,434),(392,466),(374,466)],'black',cores['Pelvic core'],.13)
for v in [439,445,451,457]:frontpanel('Pelvis vent slat',[(377,v),(389,v),(389,v+2),(377,v+2)],'alloy',cores['Pelvic core'],.16,thick=.02)
for sign in [-1,1]:
    c=Vector((sign*.64,1.05,4.98));d=Vector((0,.32,-1)).normalized()
    cyl('Thruster luminous exhaust',c+d*.08,c+d*.65,.115,plain['cyan'],r2=.006,n=32,edge=0)

for flip in [False,True]:
    fn=lambda pts:mirrored(pts) if flip else pts
    face('Raised clavicle support',fn([(304,175),(324,176),(332,199),(325,213),(307,208),(301,193)]),'graphite',-.13,.40,.035)
    face('Collar bronze cheek',fn([(345,188),(353,205),(355,216),(349,220),(339,209),(340,191)]),'bronze',-.33,.13,.018)
    cc=F(447 if flip else 319,201,-.143)
    ring('Clavicle recessed socket',cc,.046,.013,plain['alloy'],(0,-1,0))
    cyl('Clavicle socket darkness',cc,cc+Vector((0,-.006,0)),.032,plain['black'])
    co=cores['Forearm L' if flip else 'Forearm R']
    frontpanel('Forearm upper armor cup',fn([(515,317),(529,322),(554,309),(564,315),(563,326),(531,339),(517,333)]),'teal_light',co,.1,mirror_uv=flip)
    frontpanel('Forearm status plate',fn([(560,335),(571,332),(577,350),(570,357),(564,351)]),'teal_light',co,.10,mirror_uv=flip)

# Closed finger chains: four compact curled digits across the palm depth.
for sign in [-1,1]:
    for j in range(4):
        yy=-.43+j*.092
        ps=[Vector((sign*x,yy,z)) for x,z in [(2.09,3.80),(2.20,3.64),(2.12,3.47),(2.01,3.48)]]
        for k,(a,b) in enumerate(zip(ps,ps[1:])):
            prism('Closed finger armored link',a,b,.077,.061,plain['teal' if k==0 else 'graphite'],.17,edge=.009)
        for c in ps[1:-1]:
            cyl('Finger hinge barrel',c+Vector((0,-.042,0)),c+Vector((0,.042,0)),.038,plain['alloy'],n=24,edge=.002)
            cyl('Finger hinge recessed pin',c+Vector((0,-.044,0)),c+Vector((0,-.046,0)),.018,plain['black'],n=20,edge=0)
# Circular turbine hardware is modeled over the rear reference panel.
c=Vector((.005,1.245,5.65));axis=Vector((0,1,0))
cyl('Turbine supporting housing',c-axis*.22,c-axis*.025,.222,plain['graphite'])
ring('Rear turbine metallic retaining ring',c,.205,.028,plain['bronze'],axis)
cyl('Rear turbine inset hub',c-axis*.025,c-axis*.005,.169,plain['graphite'])
for k in range(8):
    a=math.tau*k/8;pp=c+Vector((math.sin(a)*.15,.001,math.cos(a)*.15))
    cyl('Turbine radial fastener',pp,pp+axis*.014,.014,plain['alloy'],n=8,edge=.001)
# Fine material variation remains procedural and does not depend on the reference image.
for mat in list(plain.values())+list(photo.values()):
    ns=mat.node_tree.nodes;lk=mat.node_tree.links;sh=ns.get('Principled BSDF')
    noise=ns.new('ShaderNodeTexNoise');noise.inputs['Scale'].default_value=180;noise.inputs['Detail'].default_value=2
    bump=ns.new('ShaderNodeBump');bump.inputs['Strength'].default_value=.11;bump.inputs['Distance'].default_value=.0014
    lk.new(noise.outputs['Fac'],bump.inputs['Height']);lk.new(bump.outputs['Normal'],sh.inputs['Normal'])
# An optically thin volume gives the short exhaust plumes soft edges.
plume=bpy.data.materials.new('Soft cyan exhaust');plume.use_nodes=True
ns=plume.node_tree.nodes;ns.clear();out=ns.new('ShaderNodeOutputMaterial');vol=ns.new('ShaderNodeVolumePrincipled')
vol.inputs['Density'].default_value=.4;vol.inputs['Color'].default_value=(.2,.8,1,1);vol.inputs['Emission Color'].default_value=(.06,.7,1,1);vol.inputs['Emission Strength'].default_value=2.2
plume.node_tree.links.new(vol.outputs['Volume'],out.inputs['Volume'])
for ob in bpy.data.objects:
    if ob.name.startswith('Thruster luminous exhaust'):ob.data.materials.clear();ob.data.materials.append(plume)

group('12 • Armor traced from the visible side profile')
def contour_side_panel(name,pts,co,sign,key,offset=.02):
    f0,f1,s0,s1=co['range'];vs=[]
    for u,sv in pts:
        fv=f0+(sv-s0)/(s1-s0)*(f1-f0);l,r=span(co['front'],fv)
        xx=((r if sign>0 else l)-383)/100+sign*offset
        vs.append(Vector((xx,side_y(u),(804-fv)/100)))
    n=len(vs);center=sum(vs,Vector())/n;vs.append(center)
    fs=[(j,(j+1)%n,n) for j in range(n)]
    ob=mesh(name,vs,fs,plain[key],0)
    for face0 in ob.data.polygons:
        if face0.normal.x*sign<0:face0.flip()
    ob.data.update()
    sol=ob.modifiers.new('Armor side thickness','SOLIDIFY');sol.thickness=offset+.09;sol.offset=-1
    bevel(ob,.008)
    line('Side plate edge '+name,vs[:n]+[vs[0]],plain[key],.005)
    return ob
for sign in [-1,1]:
    co=cores['Thorax']
    for name,pts,key,off in [
        ('Thorax layered side armor',[(249,207),(278,216),(304,235),(331,247),(349,266),(329,293),(298,319),(270,315),(251,292),(237,260)],'graphite',.025),
        ('Bronze chest side intake surround',[(293,226),(318,236),(343,251),(362,256),(371,267),(364,276),(347,286),(329,278),(313,265),(301,259)],'bronze',.065),
        ('Chest side dark intake',[(315,246),(336,253),(330,266),(311,258)],'black',.10),
        ('Reactor side green facet',[(338,283),(356,286),(335,310),(315,319),(314,305)],'green',.065)]:contour_side_panel(name+str(sign),pts,co,sign,key,off)
    co=cores['Shoulder armor R' if sign>0 else 'Shoulder armor L']
    contour_side_panel('Shoulder side gold frame',[(185,119),(217,116),(231,143),(244,181),(241,202),(225,207),(214,191),(196,187),(182,198)],co,sign,'bronze',.03)
    contour_side_panel('Shoulder inset vent',[(193,126),(213,124),(223,158),(191,158)],co,sign,'black',.062)
    for v in [134,140,146,152]:contour_side_panel('Shoulder horizontal vent slat',[(195,v),(219,v),(219,v+2),(195,v+2)],co,sign,'graphite',.07)
    xc=sign*1.16
    for edge in [-1,1]:
        for u in [313,320,327,334,341]:sideplate('Cannon barrel cooling slot',[(u,73),(u+3,72),(u+5,64),(u+2,65)],xc+edge*.306,edge*.003,'black')
        for u in [369,378,387,396]:sideplate('Muzzle sleeve vent slot',[(u,68),(u+2,68),(u+6,54),(u+4,54)],xc+edge*.325,edge*.003,'black')

# Original aligned images remain available inside Blender for continued manual tracing.
refs=group('REFERENCE • Original orthographic images • non rendering')
for name,filename,pos,rot,width in [
    ('FRONT reference','front.png',(-.03,2.7,3.98),(math.pi/2,0,0),7.60),
    ('SIDE reference','side.png',(3.0,.15,3.98),(math.pi/2,0,-math.pi/2),4.60),
    ('REAR reference','rear.png',(.005,-2.7,3.98),(math.pi/2,0,math.pi),4.95)]:
    im=bpy.data.images.load(os.path.join(OUT,'reference_checks',filename));im.pack()
    ob=bpy.data.objects.new(name,None);refs.objects.link(ob);ob.empty_display_type='IMAGE';ob.data=im;ob.empty_display_size=width;ob.location=pos;ob.rotation_euler=rot
    ob.color[3]=.52;ob.empty_image_depth='BACK';ob.hide_render=True;ob.hide_select=True
for item in VOLUMES:
    for flip in ([False,True] if item.get('mirror') else [False]):
        pts=mirrored(item['front']) if flip else item['front']
        cv=bpy.data.curves.new('Traced outline • '+item['name'],'CURVE');cv.dimensions='3D';cv.bevel_depth=.003
        sp=cv.splines.new('POLY');sp.points.add(len(pts)-1)
        for p,(u,v) in zip(sp.points,pts):p.co=(*F(u,v,2.68),1)
        sp.use_cyclic_u=True;ob=bpy.data.objects.new('TRACE • '+item['name']+(' mirrored' if flip else ''),cv);refs.objects.link(ob);cv.materials.append(plain['cyan']);ob.hide_render=True
refs.hide_viewport=True

studio=group('STUDIO • Cameras and lighting')
floor=M.material('Studio charcoal','626970',.04,.76)
box('Ground',(0,0,-.07),(200,200,.10),floor,0)
def camera(name,loc,target,ortho):
    data=bpy.data.cameras.new(name);ob=bpy.data.objects.new(name,data);studio.objects.link(ob);ob.location=loc;ob.rotation_euler=(Vector(target)-ob.location).to_track_quat('-Z','Y').to_euler();data.type='ORTHO';data.ortho_scale=ortho;data.lens=70;return ob
cams={
    'front':camera('CAM • Front traced alignment',(0,-24,4.0),(0,0,4.0),8.75),
    'side':camera('CAM • Side traced alignment',(-24,0,4.0),(0,0,4.0),8.75),
    'rear':camera('CAM • Rear traced alignment',(0,24,4.0),(0,0,4.0),8.75),
    'hero':camera('CAM • Three quarter geometry',(-12,-20,10),(0,0,4.0),9.8),
    'face':camera('CAM • Face inspection',(-2,-12,7.1),(0,-.2,6.52),2.25),
    'hand':camera('CAM • Hand and blade inspection',(10,-17,7),(2.5,-.3,3.57),4.8),
}
def area(name,loc,power,size,color=(1,1,1),target=(0,0,4)):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.shape='DISK';d.size=size;d.color=color;o=bpy.data.objects.new(name,d);studio.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Key softbox',(-5,-9,12),1900,8,(1,.94,.86))
area('Front fill',(6,-6,7),1300,7,(.85,.93,1))
area('Rim',(1,5,11),2300,6)
scene=bpy.context.scene;scene.render.engine='CYCLES';scene.cycles.samples=40;scene.cycles.use_denoising=True;scene.cycles.adaptive_threshold=.08
try:
    prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
    for d in prefs.devices:d.use=d.type=='METAL'
    scene.cycles.device='GPU'
except Exception as e:print('GPU',e)
scene.world.color=(.32,.32,.32);scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast'
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGBA';scene.render.film_transparent=False
scene.render.resolution_percentage=100
scene.camera=cams['hero']
scene['Model method']='Real volumes from manually traced front silhouettes and side depth profiles; original image projection is separately adjustable in materials.'
scene['Weapon configuration']='Paired outer forearm blades, per earlier user request'
scene['Source']='Original supplied three-view rendered character sheet, packed in this file'
readme=bpy.data.texts.new('READ ME • Tracing and material modes')
readme.write('PHANTOM — TRACED RECONSTRUCTION\n\nThe original front, side, and back images are packed in the REFERENCE collection. Enable its viewport visibility to inspect alignment.\n\nBody volumes were built from front outline traces with depth taken from the side profile. Individual armor panels, face features, blades, cannon bores, and joints are separate meshes.\n\nReference projection materials use the original sheet for color and some surface detail. This includes baked lighting from the source. Set Original image influence to 0 to inspect plain material colors, or use the clay render. This is a reconstruction from three imperfectly consistent images, not a scan.\n\nThe paired wrist blades follow the earlier requested configuration.\n')
for screen in bpy.data.screens:
    for area0 in screen.areas:
        if area0.type=='VIEW_3D':
            area0.spaces.active.region_3d.view_perspective='CAMERA';area0.spaces.active.overlay.show_overlays=False
scene.render.resolution_x=1200;scene.render.resolution_y=1400
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Traced.blend'))
print('SAVED_TRACED_SCENE',len(bpy.data.objects),flush=True)
args=sys.argv[sys.argv.index('--')+1:] if '--' in sys.argv else []
preview='--preview' in args
views=(['front'] if '--frontcheck' in args else (['side'] if '--sidecheck' in args else ['front','side','hero','clay'])) if preview else ['front','side','rear','hero','clay','face','hand']
clay=M.material('Inspection clay','A5AFB4',.05,.65)
for view in views:
    scene.camera=cams['hero' if view=='clay' else view]
    bpy.data.objects['Ground'].hide_render=view in ['front','side','rear']
    scene.view_layers[0].material_override=clay if view=='clay' else None
    scene.cycles.samples=16 if preview else 32
    scene.render.resolution_x=((760 if preview else (850 if view in ['side','rear'] else 1100)) if view not in ['face','hand'] else 1000)
    scene.render.resolution_y=(900 if preview else 1300) if view not in ['face','hand'] else 1000
    scene.render.filepath=os.path.join(OUT,('preview_' if preview else '')+view+'.png')
    bpy.ops.render.render(write_still=True)
    print('RENDERED',view,flush=True)
scene.view_layers[0].material_override=None;scene.camera=cams['hero']
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Traced.blend'))
