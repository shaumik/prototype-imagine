// Each beat gives the player a readable setup, a useful power, and a payoff.
const ROUTES = [
 [
  [1,'cue','WARM UP','Z fires · X cuts · ↑ jumps twice'],
  [2,'power','rapid'],[4,'wave','scouts'],[8,'section','steps'],
  [11,'cue','CLOSE THE DISTANCE','Dash through enemies. Cut to earn Flow.'],
  [12,'power','shield'],[13,'wave','convoy'],[17,'section','vault'],
  [20,'power','storm'],[21,'cue','STORM HALO','Orbiting blades cut anything you pass.'],[22,'wave','rush'],
  [26,'section','highroad'],[29,'wave','mixed'],[31,'power','overdrive'],
  [33,'cue','BREAK THROUGH','Blade finishers prime a charged buster shot.'],[34,'wave','convoy'],
  [36,'power','magnet'],[38,'section','vault'],[41,'wave','rush'],[44,'power','repair'],[47,'wave','mixed'],
  [51,'power','pierce'],[52,'wave','convoy'],[55,'cue','LAST STRETCH','The signal is turning red.']
 ],
 [
  [1,'cue','HARBOR AFTERGLOW','New gear. New rhythm.'],[2,'power','wings'],[4,'wave','mixed'],
  [7,'section','highroad'],[10,'wave','rush'],[13,'power','rapid'],
  [15,'cue','BREAK THEIR GUARD','Amber guards resist buster shots. Cut or dash.'],[16,'wave','guards'],
  [20,'section','vault'],[23,'power','storm'],[24,'wave','mixed'],
  [28,'section','highroad'],[31,'wave','guards'],[34,'power','shield'],
  [36,'cue','OWN THE FAST LANE','Parry orange shots with your blade to charge Flow.'],
  [37,'wave','rush'],[40,'section','steps'],[43,'power','overdrive'],[44,'wave','mixed'],
  [46,'power','nova'],[48,'wave','guards'],[51,'power','repair'],[52,'section','vault'],[55,'wave','rush'],
  [59,'cue','ONE LAST RED LIGHT','Jump the low waves. Dash through the high sweep.']
 ]
];
export function spawnWave(w,kind) {
 const formations={scouts:[[0,-78,'scout'],[190,-78,'scout']],convoy:[[0,-78,'scout'],[170,-78,'scout'],[340,-78,'scout']],
  rush:[[0,-82,'rusher'],[220,-82,'rusher'],[440,-165,'scout']],mixed:[[0,-78,'guard'],[260,-180,'scout'],[440,-78,'rusher']],
  guards:[[0,-78,'guard'],[210,-175,'scout'],[390,-78,'guard']]};
 for(const [offset,height,type] of formations[kind]){const hp=type==='guard'?10:type==='rusher'?5:4;w.enemies.push({x:1670+offset,y:690+height,originY:690+height,hp,maxHp:hp,type,phase:offset/100,fire:type==='guard'?2.3:3.2,hit:0,dead:false});}
}
export function section(w,kind) {
 const x=1700;
 const layouts={steps:[[0,82,270],[310,155,270],[610,82,260]],vault:[[0,100,250],[420,135,290]],highroad:[[0,80,230],[280,155,240],[580,205,320]]};
 for(const [offset,height,width] of layouts[kind]){
  w.platforms.push({x:x+offset,y:690-height,w:width,h:32});
  for(let i=0;i<4;i++)w.orbs.push({x:x+offset+35+i*(width-60)/4,y:690-height-40,taken:false});
 }
 if(kind==='vault')w.hazards.push({x:x+280,y:690,w:95,type:'energy',hit:false});
 if(kind==='highroad')w.orbs.push({x:x+700,y:445,taken:false,value:20});
}
export function updateEncounters(w) {
 const beats=ROUTES[w.stage-1];
 while(w.beatIndex<beats.length&&w.time>=beats[w.beatIndex][0]){
  const [,kind,value,detail]=beats[w.beatIndex++];
  if(kind==='wave')spawnWave(w,value);
  else if(kind==='section')section(w,value);
  else if(kind==='power')w.pickups.push({x:1450,y:625,id:value});
  else w.emit('cue',{title:value,detail});
 }
}
export function updateBoss(w,dt) {
 const b=w.boss,p=w.player;b.cycle??=0;b.attack??=3;b.hit=Math.max(0,(b.hit||0)-dt);
 b.y=w.stage===2?525+Math.sin(w.phaseTime*1.15)*82:548+Math.sin(w.phaseTime*1.5)*57;
 b.x=1240+Math.sin(w.phaseTime*.7)*65;
 b.coreOpen=Math.max(0,(b.coreOpen||0)-dt);b.attack-=dt;b.telegraph=Math.max(0,Math.min(1,1-b.attack/1.15));
 const next=b.cycle%3;b.pattern=next===0?'FAN BURST':next===1?'LOW WAVE':'HIGH SWEEP';
 if(b.attack<=0){
  b.cycle++;b.coreOpen=1.2;b.attack=b.hp<b.maxHp*.4?2.5:3.15;
  if(next===0){const a=Math.atan2(p.y-65-b.y,p.x-b.x),spread=w.stage===2?2:1;
   for(let j=-spread;j<=spread;j++)w.hostile.push({x:b.x-75,y:b.y,vx:Math.cos(a+j*.25)*340,vy:Math.sin(a+j*.25)*340,life:5,r:10});
  }else if(next===1){for(let j=0;j<(w.stage===2?3:2);j++)w.hostile.push({x:1410+j*190,y:670,vx:-440,vy:0,life:5,r:21,wave:true});}
  else {for(let j=0;j<(w.stage===2?5:3);j++)w.hostile.push({x:1410+j*155,y:560,vx:-470,vy:0,life:5,r:16});}
  // A boss fight always offers a second chance to charge Flow and recover armor.
  if(b.cycle%3===0){w.pickups.push({x:650,y:615,id:'repair',stationary:true,ttl:10});}
  w.emit('bossShot');
 }
 if(Math.abs(b.x-p.x)<95&&Math.abs(b.y-(p.y-55))<100&&p.dash<=0)w.hurt();
}
