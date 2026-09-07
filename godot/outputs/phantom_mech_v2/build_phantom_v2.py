import os, sys, math, json, time
OUT=os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,OUT)
from modeling import *

# Adult proportions: compact thorax, high pelvis, long substantial armored legs.
group('02 • Contoured torso')
pod('Thoracic monocoque',(0,.10,7.35),(0,.10,9.30),[(0,.54,.43),(.035,.58,.46),(.28,.85,.60),(.57,1.24,.68),(.84,1.21,.63),(.97,.98,.49),(1,.95,.47)],frame,n=3.3)
pod('Abdominal armored core',(0,.04,6.73),(0,.04,8.00),[(0,.48,.35),(.03,.50,.37),(.28,.59,.42),(.68,.69,.45),(.95,.67,.41),(1,.64,.38)],steel,n=2.7)
for s in (-1,1):
    cyl('Thoracic side actuator',(s*.69,.25,7.13),(s*1.02,.25,8.45),.105,frame)
    cyl('Thoracic exposed piston',(s*.63,.25,6.95),(s*.84,.25,7.69),.052,silver)
    panel('Pectoral formed armor',s,[(.29,9.17),(.81,9.32),(1.24,9.11),(1.34,8.48),(1.14,8.07),(.69,7.89),(.40,8.26)],-.65,frame,.10,slope=(.11,.06))
    mirrored('Pectoral shoulder facet',s,[(.46,9.13),(.82,9.20),(1.16,9.02),(1.20,8.75),(.67,8.68)],-.80,.15,steel,bulge=.045,slope=(.15,.03))
    mirrored('Chest intake bronze lip',s,[(.40,8.69),(1.23,8.87),(1.25,8.41),(.49,8.20)],-.87,.13,gold,bulge=.028,roundness=.15,slope=(.1,.02))
    mirrored('Chest intake deep recess',s,[(.53,8.60),(1.12,8.72),(1.14,8.47),(.59,8.33)],-.963,.04,black,bulge=.012,roundness=.18,slope=(.1,.02))
    for j in range(3):line('Chest recessed louvers',[(s*.59,-.995,8.38+j*.062),(s*1.085,-.950,8.50+j*.062)],bronze,.013)
    mirrored('Collar raised bronze rail',s,[(.38,9.18),(.42,9.52),(.58,9.48),(.63,9.10),(.49,8.99)],-.38,.31,gold,bulge=.035)
    for j in range(3):
        mirrored('Abdominal overlapping flank',s,[(.23,7.85-j*.27),(.58,8.00-j*.27),(.76,7.86-j*.27),(.58,7.56-j*.27),(.28,7.48-j*.27)],-.45+j*.035,.13,steel,bulge=.055)
    for x,z in [(1.12,9.02),(.78,8.00)]:bolt('Pectoral flush fastener',(s*x,-.79,z),.022)
    label('PH-07' if s==1 else 'RX / 03',(s*.88,-.883,8.98),.048)
shell('Sternum graphite crown',[(-.37,9.25),(.37,9.25),(.44,8.90),(.27,8.63),(-.27,8.63),(-.44,8.90)],-.76,.25,frame,bulge=.09)
shell('Reactor sculpted surround',[(-.31,8.51),(.31,8.51),(.48,8.07),(.24,7.68),(-.24,7.68),(-.48,8.07)],-.81,.18,bronze,bulge=.06)
shell('Reactor dark inset',[(-.25,8.37),(.25,8.37),(.33,8.09),(.19,7.87),(-.19,7.87),(-.33,8.09)],-.918,.04,black,bulge=.028)
shell('Emerald crystal',[(-.18,8.29),(.18,8.29),(.24,8.10),(.14,7.94),(-.14,7.94),(-.24,8.10)],-.958,.045,core,bulge=.075,roundness=.035,smooth=False)
shell('Lower sternum keel',[(-.28,7.78),(.28,7.78),(.38,7.54),(.19,7.25),(-.19,7.25),(-.38,7.54)],-.56,.12,frame,bulge=.07)
for j in range(3):box('Sternum recessed service slot',(0,-.64,7.38+j*.074),(.22,.015,.023),black,.006)
cyl('Waist articulation',(0,.06,6.56),(0,.06,6.95),.55,black)
for z in [6.67,6.80]:ring('Waist bearing seal',(0,.06,z),.545,.03,steel)

group('03 • Pelvis and full leg armor')
pod('Pelvic carrier',(0,.05,5.77),(0,.05,6.78),[(0,.66,.43),(.04,.74,.47),(.38,.94,.51),(.75,.94,.50),(.98,.77,.43),(1,.72,.4)],frame,n=3.5)
shell('Belt central plate',[(-.28,6.85),(.28,6.85),(.36,6.43),(.25,6.14),(-.25,6.14),(-.36,6.43)],-.57,.22,teal,bulge=.09)
shell('Belt small red signal',[(-.16,6.75),(.16,6.75),(.20,6.54),(.10,6.39),(-.10,6.39),(-.20,6.54)],-.715,.045,red,bulge=.028)
shell('Pelvic codpiece',[(-.24,6.36),(.24,6.36),(.29,5.53),(.16,5.28),(-.16,5.28),(-.29,5.53)],-.60,.25,tealdark,bulge=.07)
box('Codpiece vent housing',(0,-.677,5.55),(.24,.075,.40),frame,.05)
for j in range(5):box('Codpiece cooling slot',(0,-.720,5.41+j*.065),(.14,.018,.027),black,.005)
for s in (-1,1):
    hip=(s*.77,.09,5.99);knee=(s*1.22,.03,3.85);ankle=(s*1.49,.07,1.02)
    sphere('Hip multi-axis bearing',hip,(.38,.41,.41),black)
    pod('Thigh structural bone',hip,knee,[(0,.22,.26),(.08,.27,.3),(.5,.29,.3),(.94,.23,.26),(1,.2,.22)],frame)
    pod('Thigh continuous sculpted armor',(s*.85,.08,5.99),(s*1.21,.06,4.00),[(0,.43,.45),(.035,.49,.50),(.25,.61,.59),(.56,.59,.60),(.79,.46,.49),(.97,.31,.37),(1,.29,.35)],teal,n=2.7)
    panel('Thigh front compound armor',s,[(.48,5.86),(.79,6.01),(1.21,5.85),(1.52,4.77),(1.38,4.11),(1.15,3.98),(.84,4.47),(.59,5.24)],-.49,teal,.16,slope=(.06,-.01))
    mirrored('Thigh subtle raised segment',s,[(.81,5.71),(1.12,5.58),(1.30,4.82),(1.19,4.43),(.94,4.80),(.71,5.33)],-.645,.065,teal2,bulge=.04)
    line('Thigh longitudinal panel groove',[(s*.65,-.638,5.51),(s*.75,-.684,5.12),(s*.96,-.672,4.65),(s*1.10,-.64,4.46)],tealdark,.016)
    # Broad skirts wrap over the hip and partially overlap the thigh.
    pod('Outer hip floating shell',(s*1.04,.03,6.59),(s*1.34,.10,5.64),[(0,.18,.31),(.06,.24,.38),(.32,.29,.44),(.75,.22,.4),(.97,.15,.28),(1,.13,.25)],tealdark,n=2.6)
    panel('Hip skirt front armor',s,[(.37,6.68),(.91,6.91),(1.28,6.56),(1.11,5.66),(.62,5.29),(.39,5.63)],-.67,teal,.12,slope=(.09,-.035))
    mirrored('Hip skirt embossed inset',s,[(.54,6.42),(.86,6.63),(1.04,6.39),(.94,5.86),(.66,5.60),(.51,5.77)],-.806,.075,teal2,bulge=.055)
    mirrored('Hip lateral trailing fin',s,[(1.24,6.44),(1.47,6.15),(1.71,5.13),(1.44,5.33),(1.14,5.87)],-.17,.31,teal,bulge=.09)
    line('Skirt small seam',[(s*.58,-.879,6.50),(s*.85,-.878,6.65),(s*1.02,-.808,6.48)],tealdark,.012)
    for x,z in [(.54,6.35),(.97,5.91)]:bolt('Skirt retaining screw',(s*x,-.871,z),.023)
    # Knee hinge is mostly shrouded, with compact concentric bearings.
    cyl('Knee hinge',(s*1.22-.42,.09,3.85),(s*1.22+.42,.09,3.85),.255,frame)
    cyl('Knee outer cap',(s*1.22+s*.40,.09,3.85),(s*1.22+s*.49,.09,3.85),.18,steel)
    ring('Knee axle retaining ring',(s*1.22+s*.50,.09,3.85),.145,.019,bronze,(s,0,0))
    panel('Elongated kneecap',s,[(1.04,4.26),(1.34,4.34),(1.53,3.91),(1.50,3.43),(1.29,3.23),(1.02,3.45),(.93,3.96)],-.70,teal2,.15)
    mirrored('Kneecap small bronze tab',s,[(1.12,4.27),(1.29,4.31),(1.36,4.15),(1.23,4.06),(1.10,4.12)],-.78,.07,gold,bulge=.024)
    pod('Shin continuous greave',(s*1.25,.09,3.53),(s*1.47,.06,1.06),[(0,.39,.48),(.03,.45,.55),(.22,.57,.64),(.44,.55,.60),(.75,.37,.43),(.96,.30,.36),(1,.28,.33)],teal,n=2.6)
    panel('Shin forward armor',s,[(1.05,3.34),(1.46,3.46),(1.62,3.08),(1.51,2.34),(1.60,1.39),(1.35,1.10),(1.08,1.40),(1.13,2.17),(.96,2.85)],-.56,teal,.15,slope=(.05,0))
    # Organic crescent calf housings provide the mass missing in the first model.
    mirrored('Calf external crescent guard',s,[(1.56,3.55),(1.85,3.39),(2.01,2.92),(1.88,2.38),(1.59,1.91),(1.43,2.28),(1.49,2.97)],-.13,.78,frame,bulge=.17,roundness=.24,slope=(.1,0))
    mirrored('Calf internal crescent guard',s,[(1.01,3.42),(.83,3.31),(.72,2.79),(.87,2.32),(1.12,1.96),(1.23,2.40)],-.06,.6,frame,bulge=.12,roundness=.22)
    mirrored('Shin bronze knee saddle',s,[(1.02,3.32),(1.26,3.10),(1.58,3.33),(1.60,2.98),(1.42,2.65),(1.17,2.72)],-.716,.12,gold,bulge=.055)
    line('Greave formed seam',[(s*1.24,-.727,2.60),(s*1.23,-.731,2.20),(s*1.34,-.737,1.78)],teal2,.018)
    for k in range(2):box('Calf fine bronze inlay',(s*1.83,-.228,2.7-k*.13),(.035,.018,.12),gold,.01)
    cyl('Rear leg ram outer',(s*1.25,.60,1.53),(s*1.10,.60,2.94),.078,frame)
    cyl('Rear leg ram polished rod',(s*1.13,.60,2.73),(s*1.07,.60,3.51),.043,silver)
    for zz in [1.6,1.94]:box('Rear calf luminous insert',(s*1.56,.535,zz),(.16,.07,.21),cyan,.035)
    sphere('Ankle rotary knuckle',ankle,(.30,.31,.29),black)
    cyl('Ankle side swivel',(s*1.49+s*.21,.11,1.03),(s*1.49+s*.37,.11,1.03),.16,steel)
    # Shaped boots, tapered toes and layered insteps.
    pod('Foot shaped sole',(s*1.55,-1.10,.20),(s*1.47,.60,.23),[(0,.40,.12),(.03,.47,.15),(.22,.49,.16),(.55,.46,.16),(.91,.37,.14),(1,.33,.12)],frame,n=3.9)
    pod('Foot sculpted main boot',(s*1.55,-1.03,.41),(s*1.46,.45,.54),[(0,.37,.11),(.03,.42,.15),(.30,.44,.24),(.64,.38,.29),(.95,.30,.22),(1,.27,.17)],steel,n=3.1)
    panel('Ankle tapered front armor',s,[(1.17,1.43),(1.41,1.59),(1.65,1.35),(1.86,.79),(1.66,.60),(1.20,.74),(1.10,1.02)],-.57,teal,.10,slope=(0,.25))
    pod('Foot toe alloy cap',(s*1.56,-1.08,.41),(s*1.55,-.60,.58),[(0,.34,.08),(.04,.38,.11),(.45,.39,.10),(.98,.31,.08),(1,.29,.07)],silver,n=4)
    box('Heel armored buffer',(s*1.47,.53,.40),(.61,.32,.35),frame,.10)
    for yy in [-.94,-.7,-.42,-.13,.17,.42]:box('Foot sole traction insert',(s*1.52,yy,.075),(.76,.07,.05),rubber,.016)
    for x,z in [(1.37,1.25),(1.67,.83)]:bolt('Ankle panel fastener',(s*x,-.686,z),.026)

# The helmet is built independently so the face remains small, recessed and mechanical.
group('04 • Helmet and recessed face')
cyl('Neck gimbal',(0,.10,9.06),(0,.10,9.57),.25,frame)
ring('Neck upper bearing',(0,.10,9.43),.24,.025,steel)
pod('Helmet continuous crown',(0,.07,9.46),(0,.07,10.73),[(0,.31,.35),(.035,.43,.43),(.20,.58,.49),(.53,.62,.52),(.74,.56,.48),(.91,.37,.36),(.98,.23,.25),(1,.20,.22)],teal,n=2.6)
shell('Visor recessed dark surround',[(-.46,10.20),(0,10.10),(.46,10.20),(.43,9.71),(.23,9.43),(-.23,9.43),(-.43,9.71)],-.526,.10,black,bulge=.035,roundness=.10)
for s in (-1,1):
    mirrored('Helmet swept temple shell',s,[(.36,10.42),(.58,10.35),(.67,9.93),(.58,9.49),(.34,9.38),(.33,9.75)],-.38,.43,tealdark,bulge=.095,roundness=.19)
    mirrored('Face side cheek guard',s,[(.32,10.03),(.46,10.12),(.46,9.59),(.26,9.41),(.20,9.65)],-.62,.13,frame,bulge=.042,roundness=.08)
    mirrored('Face fine cheek alloy',s,[(.28,9.94),(.35,9.96),(.34,9.66),(.23,9.52),(.19,9.61)],-.684,.065,steel,bulge=.022,roundness=.06)
    mirrored('Eye narrow recessed slit',s,[(.085,10.015),(.359,10.071),(.332,10.008),(.11,9.966)],-.642,.025,optic,bulge=.006,roundness=.045)
    mirrored('Brow low armored ridge',s,[(.055,10.105),(.425,10.21),(.423,10.13),(.095,10.036)],-.672,.08,frame,bulge=.014,roundness=.04)
    # Small cheek vents, with no large white triangular face plates.
    for j in range(4):line('Cheek micro vent',[(s*.405,-.69,9.76+j*.06),(s*.459,-.64,9.78+j*.06)],black,.012)
    cyl('Temple mounting pivot',(s*.55,-.08,9.95),(s*.67,-.08,9.95),.16,frame)
    cyl('Temple pivot center',(s*.67,-.08,9.95),(s*.697,-.08,9.95),.105,steel)
    # Slender curved antennae and narrow swept alloy V-fins.
    pod('Gold tapered antenna',(s*.21,.04,10.40),(s*.62,.16,11.39),[(0,.068,.065),(.04,.073,.066),(.38,.048,.044),(.75,.025,.021),(.97,.006,.006),(1,.003,.003)],gold,n=2.2,verts=20,sub=1)
    mirrored('Helmet narrow swept V fin',s,[(.027,10.13),(.17,10.12),(.92,10.71),(.74,10.61),(.28,10.28)],-.701,.075,silver,bulge=.008,roundness=.025,smooth=False)
shell('Face central sculpted mask',[(-.105,10.03),(.105,10.03),(.185,9.78),(.11,9.48),(-.11,9.48),(-.185,9.78)],-.694,.08,steel,bulge=.086,roundness=.09)
for j in range(4):line('Face mask breathing groove',[(-.104,-.786,9.66+j*.061),(0,-.801,9.648+j*.061),(.104,-.786,9.66+j*.061)],black,.009)
shell('Face narrow nose bridge',[(-.038,10.08),(.038,10.08),(.065,9.85),(0,9.79),(-.065,9.85)],-.798,.043,silver,bulge=.016,roundness=.06)
shell('Face restrained red chin',[(-.061,9.65),(.061,9.65),(.073,9.49),(0,9.44),(-.073,9.49)],-.782,.06,red,bulge=.018,roundness=.12)
shell('Forehead integrated crest',[(-.10,10.17),(.10,10.17),(.15,10.66),(.09,10.88),(-.09,10.88),(-.15,10.66)],-.452,.27,tealdark,bulge=.036,roundness=.13)
shell('Forehead cyan lens',[(-.062,10.51),(.062,10.51),(.071,10.68),(-.071,10.68)],-.53,.035,cyan,bulge=.009,roundness=.14)
for s in (-1,1):
    mirrored('Helmet crown faceted panel',s,[(.115,10.32),(.20,10.61),(.41,10.57),(.51,10.32),(.35,10.19)],-.418,.065,teal2,bulge=.018,roundness=.05,slope=(.16,.21))
    line('Helmet upper panel separation',[(s*.17,-.442,10.35),(s*.25,-.411,10.54),(s*.38,-.361,10.51)],tealdark,.009)

group('05 • Swept shoulders and arm armor')
for s in (-1,1):
    shoulder=(s*1.87,.17,9.18);elbow=(s*2.39,.08,7.82);wrist=(s*2.99,-.21,6.15)
    cyl('Shoulder coupling',(s*1.02,.18,9.14),(s*2.08,.18,9.14),.31,steel)
    sphere('Shoulder spherical bearing',shoulder,(.41,.44,.45),black)
    # Long compound surfaces with rolled edges rather than extruded planar wings.
    mirrored('Shoulder swept primary shell',s,[(1.18,9.97),(2.13,10.34),(3.31,10.51),(3.46,10.40),(3.21,9.93),(2.20,9.42),(1.48,9.37)],-.17,.87,teal,bulge=.16,roundness=.13,slope=(.17,.07))
    mirrored('Shoulder inner crown segment',s,[(1.28,10.02),(1.94,10.25),(2.18,10.02),(1.83,9.72),(1.42,9.67)],-.36,.15,teal2,bulge=.07,slope=(.17,.09))
    mirrored('Shoulder outer crown segment',s,[(2.09,10.31),(3.30,10.43),(3.12,10.07),(2.34,9.75),(2.23,10.0)],-.28,.13,teal,bulge=.07,slope=(.17,.09))
    mirrored('Shoulder bronze swept trim',s,[(1.43,9.74),(1.87,9.92),(3.39,10.17),(3.31,9.86),(2.10,9.24),(1.65,9.16)],-.48,.19,gold,bulge=.065,roundness=.12,slope=(.13,.02))
    mirrored('Shoulder dark underside',s,[(1.65,9.45),(3.27,9.92),(3.05,9.50),(2.32,9.06),(1.78,8.98)],-.22,.72,frame,bulge=.13,roundness=.17,slope=(.12,.03))
    panel('Shoulder molded joint cap',s,[(1.42,9.63),(1.76,9.65),(2.10,9.33),(2.03,8.85),(1.67,8.93),(1.41,9.22)],-.66,frame,.105,slope=(.09,0))
    mirrored('Shoulder cap inset alloy',s,[(1.52,9.48),(1.73,9.50),(1.95,9.27),(1.91,9.02),(1.72,9.09),(1.52,9.30)],-.783,.06,steel,bulge=.035,roundness=.14)
    for k in range(2):mirrored('Shoulder rear trailing vane',s,[(2.25+k*.29,9.58),(2.49+k*.25,9.35),(2.70+k*.22,8.61),(2.44+k*.21,8.83)],.41,.30,tealdark,bulge=.07,roundness=.18)
    cyl('Upper arm internal actuator',shoulder,elbow,.24,frame)
    pod('Upper arm contoured sleeve',(s*2.00,.11,9.03),(s*2.29,.07,8.04),[(0,.31,.36),(.04,.36,.43),(.25,.42,.48),(.57,.38,.45),(.92,.25,.30),(1,.22,.26)],teal,n=2.8)
    mirrored('Biceps floating formed panel',s,[(1.79,8.90),(2.23,8.87),(2.47,8.30),(2.28,8.02),(1.98,8.17),(1.76,8.59)],-.38,.13,teal2,bulge=.095)
    for k in range(2):
        cyl('Elbow exposed hydraulic shaft',(s*(2.16+k*.22),-.21,8.27),(s*(2.29+k*.22),-.21,7.69),.055,silver)
        cyl('Elbow piston sleeve',(s*(2.16+k*.22),-.21,8.29),(s*(2.23+k*.22),-.21,7.98),.089,frame)
    cyl('Elbow transverse hinge',(s*2.39-.31,.08,7.82),(s*2.39+.31,.08,7.82),.225,frame)
    cyl('Elbow bearing face',(s*2.39+s*.31,.08,7.82),(s*2.39+s*.38,.08,7.82),.148,steel)
    cyl('Forearm structural skeleton',elbow,wrist,.23,frame)
    pod('Forearm organic gauntlet',(s*2.47,.01,7.61),(s*2.93,-.20,6.25),[(0,.30,.34),(.035,.37,.41),(.26,.48,.50),(.48,.46,.50),(.83,.32,.36),(.97,.29,.31),(1,.27,.29)],teal,n=2.6)
    panel('Gauntlet front armored shell',s,[(2.14,7.56),(2.59,7.69),(2.91,7.12),(3.19,6.48),(3.02,6.13),(2.68,6.28),(2.31,6.94)],-.51,teal2,.14,slope=(.03,0))
    mirrored('Gauntlet raised dark inset',s,[(2.39,7.35),(2.59,7.45),(2.79,7.02),(2.93,6.57),(2.73,6.60),(2.51,7.03)],-.686,.07,frame,bulge=.065)
    line('Gauntlet cyan upper indicator',[(s*2.29,-.638,7.48),(s*2.59,-.676,7.57)],cyan,.021)
    line('Gauntlet lower seam',[(s*2.68,-.684,6.68),(s*2.82,-.679,6.38)],tealdark,.02)
    cyl('Wrist rotating collar',(s*2.97,-.20,6.30),(s*3.06,-.24,6.00),.285,steel)
    for z in [6.11,6.03]:ring('Wrist flexible seal',(s*3.035,-.22,z),.247,.026,rubber)
    pod('Hand metacarpal armor',(s*3.07,-.23,5.52),(s*3.06,-.23,5.99),[(0,.21,.22),(.04,.24,.27),(.45,.26,.30),(.92,.25,.27),(1,.21,.23)],frame,n=3.5)
    for k in range(4):
        xx=s*(2.86+k*.133);zz=5.80-abs(1.5-k)*.018
        sphere('Hand formed knuckle',(xx,-.525,zz),(.062,.10,.094),steel)
        pod('Hand curled finger',(xx,-.50,5.46),(xx,-.56,5.72),[(0,.045,.052),(.06,.053,.068),(.4,.059,.076),(.9,.052,.063),(1,.047,.052)],frame,n=3.2,verts=16,sub=1)
        line('Finger articulation split',[(xx-.047,-.584,5.60),(xx+.047,-.584,5.60)],black,.008)
    pod('Hand opposed thumb',(s*2.76,-.34,5.60),(s*2.81,-.51,5.90),[(0,.075,.08),(.1,.09,.095),(.6,.09,.10),(1,.06,.07)],frame,verts=20,sub=1)

group('06 • Paired wrist-mounted blades')
for s in (-1,1):
    pod('Wrist blade armored deployment carriage',(s*2.72,.02,7.65),(s*3.23,-.10,6.03),[(0,.12,.17),(.045,.18,.25),(.27,.21,.29),(.75,.18,.24),(.96,.12,.19),(1,.10,.16)],frame,n=3.3)
    mirrored('Wrist blade outer shroud',s,[(2.80,7.58),(3.01,7.38),(3.31,6.46),(3.36,6.02),(3.16,5.90),(2.91,6.59)],-.24,.31,steel,bulge=.075,roundness=.18)
    mirrored('Wrist blade bronze collar',s,[(3.12,6.38),(3.31,6.47),(3.44,6.18),(3.23,6.08)],-.34,.20,gold,bulge=.035)
    stations=[(6.19,3.23,3.42),(5.91,3.28,3.52),(5.39,3.39,3.65),(4.85,3.54,3.85),(4.23,3.71,4.04),(3.64,3.87,4.22),(3.08,4.02,4.34),(2.63,4.16,4.40),(2.35,4.38,4.39)]
    stations=[(z,s*a,s*b) for z,a,b in stations]
    o=blade_mesh('LEFT wrist blade' if s<0 else 'RIGHT wrist blade',stations,-.31,blade)
    # A separate narrow honed edge follows the full blade curvature.
    edge_stations=[(z,b-(b-a)*.12,b) for z,a,b in stations]
    blade_mesh('Wrist blade sharpened edge',edge_stations,-.319,edge)
    line('Blade engraved spine channel',[(s*3.36,-.401,5.83),(s*3.56,-.401,4.98),(s*3.78,-.401,4.13),(s*4.10,-.40,3.05)],frame,.013)
    for x,z in [(3.32,5.94),(3.57,4.96)]:bolt('Blade spine rivet',(s*x,-.405,z),.018)

group('07 • Backpack and forward shoulder cannons')
pod('Backpack main contoured reactor',(0,1.05,7.70),(0,1.05,9.80),[(0,.47,.32),(.025,.58,.40),(.2,.87,.48),(.68,.97,.48),(.93,.73,.38),(1,.63,.31)],frame,n=3.4)
pod('Backpack central spine',(0,1.50,7.94),(0,1.50,9.42),[(0,.26,.18),(.06,.32,.23),(.45,.35,.27),(.92,.29,.22),(1,.23,.17)],tealdark,n=3.6)
for s in (-1,1):
    pod('Backpack coolant housing',(s*.69,1.49,8.37),(s*.69,1.49,9.60),[(0,.20,.20),(.04,.28,.27),(.28,.29,.31),(.73,.29,.31),(.97,.22,.22),(1,.20,.20)],steel,n=3.7)
    for j in range(3):box('Backpack coolant light',(s*.69,1.809,8.91+j*.14),(.28,.035,.071),cyan,.014)
    for j in range(4):box('Backpack heat exchanger vane',(s*.68,1.81,8.50+j*.067),(.27,.035,.024),black,.006)
    # The cannons are mounted above each shoulder and extend forward, as in the side reference.
    a=Vector((s*1.48,1.28,10.59));b=Vector((s*1.48,-3.50,11.79));axis=(b-a).normalized()
    pod('Cannon articulated support',(s*1.22,.77,9.23),(s*1.48,.89,10.79),[(0,.24,.28),(.045,.32,.36),(.45,.38,.41),(.88,.31,.32),(1,.26,.26)],frame,n=3.6)
    cyl('Cannon elevation hinge',(s*1.48-.43,.88,10.54),(s*1.48+.43,.88,10.54),.31,steel)
    cyl('Cannon hinge outer cap',(s*1.48+s*.44,.88,10.54),(s*1.48+s*.50,.88,10.54),.225,frame)
    ring('Cannon hinge retaining ring',(s*1.48+s*.51,.88,10.54),.16,.025,steel,(s,0,0))
    pod('Cannon continuous barrel housing',a,b,[(0,.32,.35),(.025,.39,.43),(.16,.45,.49),(.30,.42,.44),(.40,.35,.35),(.79,.34,.33),(.97,.37,.39),(1,.36,.38)],steel,n=4.0)
    q=axis.to_track_quat('Z','Y');u=q@Vector((1,0,0));v=q@Vector((0,1,0))
    box('Cannon longitudinal top rail',(a+b)/2+v*.387,(.22,.045,(b-a).length*.66),frame,.022,rot=q.to_euler())
    for side in [-1,1]:
        box('Cannon side inset strip',(a+b)/2+u*(side*.358)-v*.035,(.034,.21,(b-a).length*.52),tealdark,.018,rot=q.to_euler())
        for j in range(3):
            bolt('Cannon rail fastener',a+axis*(1.70+j*.45)+u*(side*.393),.022,u*side)
    pod('Cannon top teal armor',a+v*.38+axis*.25,b+v*.31-axis*.41,[(0,.25,.075),(.035,.30,.11),(.19,.31,.14),(.38,.29,.11),(.89,.26,.09),(1,.22,.065)],tealdark,n=3.6)
    for side in [-1,1]:
        pod('Cannon lateral machined rail',a+u*(side*.39)+axis*.63,b+u*(side*.33)-axis*.47,[(0,.045,.15),(.05,.066,.17),(.85,.063,.15),(1,.045,.13)],frame,n=4,verts=24,sub=1)
    pod('Cannon reinforced muzzle shroud',b-axis*.43,b+axis*.15,[(0,.44,.46),(.04,.49,.51),(.20,.52,.54),(.78,.52,.54),(.97,.46,.49),(1,.45,.48)],frame,n=4.5)
    pod('Cannon inset muzzle mask',b+axis*.15,b+axis*.18,[(0,.386,.420),(.08,.403,.434),(.9,.403,.434),(1,.386,.420)],black,n=4.5,verts=40,sub=1)
    for xx,yy in [(0,.24),(-.17,.03),(.17,.03),(0,-.21)]:
        p=b+axis*.20+u*xx+v*yy
        cyl('Cannon muzzle socket',p,p+axis*.01,.102,bronze,verts=32)
        cyl('Cannon recessed bore',p+axis*.011,p+axis*.014,.072,black,verts=32)
        ring('Cannon bore machined lip',p+axis*.016,.078,.011,steel,axis)
    for j in range(5):
        p=a+axis*(.5+j*.115)-v*.465
        line('Cannon breech cooling cut',[p-u*.20,p+u*.20],black,.016)
    p=a+axis*.45-v*.47
    label('CAUTION',tuple(p),.042)
    # Short, dark thruster wells with bright ion rings, not solid plastic flame cones.
    ta=Vector((s*.65,1.39,8.39));tb=Vector((s*.84,1.76,7.48));d=(tb-ta).normalized()
    pod('Thruster contoured nacelle',ta,tb,[(0,.22,.23),(.04,.27,.28),(.23,.31,.32),(.70,.32,.33),(.93,.36,.36),(1,.35,.35)],frame,n=2.1)
    cyl('Thruster metallic nozzle collar',tb-d*.15,tb,.365,steel,.33)
    cyl('Thruster dark interior',tb,tb+d*.01,.269,black)
    ring('Thruster ion ring',tb+d*.019,.23,.028,cyan,d)
    cyl('Thruster luminous well',tb+d*.015,tb+d*.021,.175,cyan)
    line('Backpack armored cable',[(s*.55,1.35,7.84),(s*.87,1.19,7.51),(s*.79,.86,7.04),(s*.53,.59,6.75)],rubber,.064)
    # Rear skirt panels and exposed thigh cylinders finish the complete 3D silhouette.
    mirrored('Rear skirt floating armor',s,[(.23,6.54),(1.01,6.69),(1.30,5.72),(.73,5.32),(.31,5.60)],.60,.40,teal,bulge=.06)
    for j in range(2):cyl('Rear thigh exposed ram',(s*(.79+j*.25),.65,4.47),(s*(.69+j*.25),.65,5.49),.055,steel)
ring('Rear reactor bronze surround',(0,1.802,8.90),.27,.042,gold,(0,1,0))
cyl('Rear reactor inset',(0,1.77,8.90),(0,1.83,8.90),.209,black)
line('Rear power mark',[(.145*math.cos(a),1.848,8.90+.145*math.sin(a)) for a in [math.radians(140+i*9) for i in range(30)]],bronze,.023)
line('Rear power mark stem',[(0,1.85,8.92),(0,1.85,9.12)],gold,.024)

group('90 • Neutral studio')
ground=mat('Studio / charcoal','232C36',.08,.62)
box('Seamless studio floor',(0,0,-.13),(2000,2000,.20),ground,.01)
def area(name,loc,target,power,h,size,ysize=None):
    d=bpy.data.lights.new(name,'AREA');d.energy=power;d.color=rgb(h);d.shape='RECTANGLE';d.size=size;d.size_y=ysize or size
    o=bpy.data.objects.new(name,d);COL.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler()
area('Key softbox',(-6,-9,15),(0,0,7),1800,'F7F1E8',6,9)
area('Neutral frontal fill',(5,-8,9),(0,0,7),1100,'DCE6EE',5,7)
area('Cool rear strip',(5,4,13),(0,0,7),2200,'BCD6E5',5,8)
area('Warm rear strip',(-5,4,10),(0,0,7),1300,'E7CDB0',4,8)
area('Overhead reflection',(0,0,16),(0,0,6),950,'EDF1F5',5)
scene=bpy.context.scene;scene.world=bpy.data.worlds.new('Neutral studio world');scene.world.use_nodes=True
scene.world.node_tree.nodes['Background'].inputs['Color'].default_value=(*rgb('A5AFBC'),1)
scene.world.node_tree.nodes['Background'].inputs['Strength'].default_value=.32
group('91 • Cameras')
def camera(name,loc,target,scale):
    d=bpy.data.cameras.new(name);o=bpy.data.objects.new(name,d);COL.objects.link(o);o.location=loc;o.rotation_euler=(Vector(target)-o.location).to_track_quat('-Z','Y').to_euler();d.type='ORTHO';d.ortho_scale=scale;d.passepartout_alpha=.95;return o
hero=camera('01 • Hero',(14,-29,12.0),(0,-.30,6.15),15.0)
front=camera('02 • Front',(0,-30,8.0),(0,-.2,6.0),14.5)
head=camera('03 • Face',(5,-20,11.6),(0,-.16,10.08),3.25)
rear=camera('04 • Rear',(-15,29,12),(0,.1,6.15),14.7)
scene.camera=hero
group('99 • Reference')
ref=bpy.data.images.load(os.path.join(OUT,'reference.jpg'));ref.pack()
o=bpy.data.objects.new('Supplied revised reference',None);COL.objects.link(o);o.empty_display_type='IMAGE';o.data=ref;o.hide_render=True;o.hide_viewport=True
scene.render.engine='CYCLES';scene.cycles.samples=48;scene.cycles.use_denoising=True
scene.cycles.max_bounces=6;scene.cycles.glossy_bounces=3;scene.cycles.diffuse_bounces=2;scene.cycles.adaptive_threshold=.05
prefs=bpy.context.preferences.addons['cycles'].preferences;prefs.compute_device_type='METAL';prefs.get_devices()
for d in prefs.devices:d.use=d.type=='METAL'
scene.cycles.device='GPU'
scene.render.resolution_x=1400;scene.render.resolution_y=1700;scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG';scene.render.image_settings.color_mode='RGB';scene.render.image_settings.color_depth='8'
scene.view_settings.view_transform='AgX';scene.view_settings.look='AgX - Medium High Contrast';scene.view_settings.exposure=.25
scene.render.filepath=os.path.join(OUT,'phantom_v2_hero.png')
scene['revision']='Second reconstruction from revised rendering reference: curved armor, adult proportions, small recessed face, paired wrist blades, forward shoulder cannons.'
for screen in bpy.data.screens:
    for a in screen.areas:
        if a.type=='VIEW_3D':
            a.spaces.active.shading.type='MATERIAL';a.spaces.active.overlay.show_overlays=False;a.spaces.active.region_3d.view_perspective='CAMERA';a.spaces.active.region_3d.view_camera_zoom=-4
bpy.ops.object.select_all(action='DESELECT')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(OUT,'Phantom_Mecha_v2.blend'))
print('V2_SAVED',len(scene.objects),'objects',flush=True)
if '--preview' in sys.argv:
    scene.cycles.samples=12;scene.cycles.adaptive_threshold=.12
    for cam,file,w,h in [(front,'preview_front.png',700,900),(head,'preview_face.png',650,650),(hero,'preview_hero.png',700,900)]:
        scene.camera=cam;scene.render.resolution_x=w;scene.render.resolution_y=h;scene.render.filepath=os.path.join(OUT,file)
        print('PREVIEW_START',file,flush=True);bpy.ops.render.render(write_still=True);print('PREVIEW_COMPLETE',file,flush=True)
