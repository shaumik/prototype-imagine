import {CHASSIS,DEFAULT_LOADOUT,normalizeLoadout,PICKUPS,STAGES} from './loadout.js';
import {initProgression,purchase,ownedLoadout,addScrap,addFlow,activateFlow,finishStage} from './progression.js';
import {updateEncounters,updateBoss} from './encounters.js';
import {BLADE_MOVES,attackBox,overlaps} from './combat.js';
export const GROUND = 690;
export const DASH_COOLDOWN = .48;
export const clamp = (n,a,b) => Math.max(a,Math.min(b,n));
export class World {
 constructor(onEvent=()=>{}) { this.onEvent=onEvent; this.reset(true); }
 reset(demo=false,options={}) {
  this.stage=options.stage===2?2:1;this.chassis="phantom";this.loadout=normalizeLoadout(options.loadout||DEFAULT_LOADOUT);this.stageStartScore=options.score||0;this.inWorkshop=false;this.completed=false;
  this.demo=demo; this.time=0; this.worldX=0; this.speed=470; this.phase='run'; this.phaseTime=0; this.over=false; this.paused=false;
  this.player={x:demo?890:490,y:GROUND,vy:0,hp:CHASSIS[this.chassis].hp,maxHp:CHASSIS[this.chassis].hp,jumps:0,grounded:true,coyote:.12,jumpBuffer:0,jumpReleased:false,dashBuffer:0,dashDirection:1,dash:0,dashCooldown:0,dashHits:new Set(),shotCooldown:0,shotTime:0,muzzle:0,recoil:0,overcharge:0,slash:0,attack:null,slashBuffer:null,chainStep:0,chainTimer:0,slashHeld:0,invincible:0,land:0};
  this.platforms=[];this.hazards=[];this.enemies=[];this.shots=[];this.hostile=[];this.orbs=[];this.particles=[];this.ghosts=[];this.score=this.stageStartScore;this.combo=0;this.comboTimer=0;
  this.spawnDistance=1100;this.spawnEnemy=6;this.boss=null;this.shake=0;this.flash=0;this.hitStop=0;this.impacts=[];this.demoAction=1.5;this.ghostTimer=0;this.lastStage=0;this.pickups=[];this.pickupClock=5;this.pickupIndex=0;this.buffs={rapid:0,overdrive:0,pierce:0,magnet:0,storm:0,wings:0};this.barrier=0;this.aegisReady=this.loadout.core==="aegis";this.aegisTimer=0;this.supportCooldown=.8;this.supportFlash=0;this.defeats=0;this.beatIndex=0;this.stormCooldown=0;initProgression(this,options);
 }
 get stageInfo(){return STAGES[this.stage-1];}
 get dashRecharge(){return this.flowActive>0?.22:this.loadout.core==='boost'?.30:DASH_COOLDOWN;}
 get damageMultiplier(){return this.buffs.overdrive>0||this.flowActive>0?2:1;}
 retryStage(){this.reset(false,{stage:this.stage,chassis:this.chassis,loadout:this.loadout,score:this.stageStartScore,scrap:this.stageStartScrap,owned:this.stageStartOwned});}
 purchase(slot,id){return purchase(this,slot,id);}
 activateFlow(){return activateFlow(this);}
 gainFlow(n){addFlow(this,n);}
 gainScrap(n,x,y){addScrap(this,n,x,y);}
 advanceStage(config={}){if(!this.inWorkshop||this.stage!==1)return false;const options={stage:2,chassis:this.chassis,loadout:ownedLoadout(this,config.loadout||this.loadout),score:this.score,scrap:this.scrap,owned:[...this.owned]};this.reset(false,options);return true;}
 collectPower(id){const item=PICKUPS.find(x=>x.id===id);if(!item)return false;
  if(id==='repair')this.player.hp=Math.min(this.player.maxHp,this.player.hp+2);
  else if(id==='shield')this.barrier=Math.min(3,this.barrier+3);
  else if(id==='nova'){this.hostile=[];for(const e of this.enemies)if(e.x<1600)this.hurtEnemy(e,12);if(this.phase==='boss')this.hurtBoss(8);this.burst(this.player.x,this.player.y-60,'#fff2d1',65,650);}
  else this.buffs[id]=['storm','wings'].includes(id)?Infinity:id==='overdrive'?10:id==='magnet'?15:12;
  this.score+=75;this.gainFlow(8);this.burst(this.player.x,this.player.y-75,item.color,32,340);this.emit('powerup',item);return true;
 }
 support(dt){this.supportCooldown-=dt;this.supportFlash=Math.max(0,this.supportFlash-dt);const kind=this.loadout.shoulder;if(kind==='none'||this.supportCooldown>0||!['run','boss'].includes(this.phase))return;
  const p=this.player,target=this.enemies.find(e=>!e.dead&&e.x>p.x&&e.x<1500)||(this.phase==='boss'?this.boss:null);if(!target)return;
  this.supportCooldown=kind==='cannon'?2.4:kind==='missiles'?3:.9;this.supportFlash=.15;
  for(let i=0;i<(kind==='missiles'?2:1);i++){const x=p.x+25,y=p.y-(kind==='drone'?165:135)-i*12,angle=Math.atan2(target.y-y,target.x-x),speed=kind==='missiles'?700:1250;
   this.shots.push({x,y,vx:Math.cos(angle)*speed,vy:Math.sin(angle)*speed,life:2,damage:(kind==='cannon'?7:kind==='missiles'?4:2)*this.damageMultiplier,charged:kind==='cannon',pierce:1,hits:new Set(),age:0,support:kind,homing:kind==='missiles'});}
  this.emit('support',{kind});
 }
 emit(type,data={}) { this.onEvent(type,data); }
 burst(x,y,color,count=12,power=250) {for(let i=0;i<count;i++){const a=Math.random()*Math.PI*2,s=(.25+Math.random())*power;this.particles.push({x,y,vx:Math.cos(a)*s,vy:Math.sin(a)*s,life:.3+Math.random()*.5,max:.8,color,size:2+Math.random()*4});}}
 jump() {const p=this.player;if(this.over||this.paused)return false;p.jumpBuffer=.14;p.jumpReleased=false;return this.tryJump();}
 releaseJump(){const p=this.player;p.jumpReleased=true;if(p.vy<-330)p.vy=-330;}
 tryJump(){const p=this.player;if(p.jumpBuffer<=0||p.jumps>=(this.buffs.wings>0?3:2))return false;
  if(!p.grounded&&p.coyote<=0&&p.jumps===0)p.jumps=1;
  p.dash=0;p.vy=p.jumpReleased?-330:p.jumps===0?-850:-780;p.jumps++;p.jumpBuffer=0;p.grounded=false;p.coyote=0;
  this.burst(p.x,p.y,'#b5ffe7',9,170);this.emit('jump',{double:p.jumps===2});return true;
 }
 requestDash(direction=1){if(this.over||this.paused)return;this.player.dashBuffer=.14;this.player.dashDirection=direction;this.dash();}
 shoot(){
  const p=this.player;if(this.over||this.paused||p.shotCooldown>0||p.dash>0)return false;
  if(p.attack&&p.attack.elapsed<BLADE_MOVES[p.attack.kind].chainAt)return false;
  if(p.attack){p.attack=null;p.slash=0;}
  const charged=p.overcharge>0||this.flowActive>0;p.overcharge=0;p.shotCooldown=(charged?.25:this.loadout.primary==='rail'?.30:.18)/(this.buffs.rapid>0?1.8:1);p.shotTime=.18;p.muzzle=charged?.12:.085;p.recoil=charged?1.7:1;p.lastShotCharged=charged;
  const rail=this.loadout.primary==='rail';for(const angle of this.loadout.primary==='spread'&&!charged?[-.18,0,.18]:[0])this.shots.push({x:p.x+74,y:p.y-83,vx:(charged||rail?1850:1500)*Math.cos(angle),vy:1500*Math.sin(angle),life:1.4,damage:(charged?6:rail?4:2)*this.damageMultiplier,charged:charged||rail,pierce:charged||rail||this.buffs.pierce>0?3:1,hits:new Set(),age:0});
  this.burst(p.x+74,p.y-83,charged?'#efffca':'#b8ffed',charged?9:3,110);
  this.emit('shoot',{charged});return true;
 }
 slash(direction='forward'){
  const p=this.player;if(this.over||this.paused)return false;
  if(direction==='down'&&p.grounded)direction='forward';
  if(p.attack||p.dash>0){p.slashBuffer={direction,ttl:.2};return false;}
  const continuing=p.chainTimer>0;
  if(direction==='forward')p.chainStep=continuing?p.chainStep%3+1:1;
  const kind=direction==='down'?'down':direction==='up'?'up':['cut','rise','break'][p.chainStep-1];
  const move=BLADE_MOVES[kind];
  p.attack={kind,elapsed:0,hits:new Set(),bounced:false,activated:false};p.slash=move.duration;p.slashBuffer=null;p.chainTimer=move.duration+.48;p.shotTime=0;p.muzzle=0;
  this.emit('slash',{kind,step:p.chainStep});return true;
 }
 impact(x,y,kind='shot'){
  const heavy=kind==='break',melee=kind!=='shot'&&kind!=='charged';
  this.impacts.push({x,y,kind,life:heavy?.3:.22,max:heavy?.3:.22,angle:Math.random()*Math.PI});
  this.burst(x,y,melee?'#d9fff1':'#c5ffed',heavy?20:8,heavy?340:230);
  this.shake=Math.max(this.shake,heavy?8:melee?3.5:1.1);
  if(melee)this.hitStop=Math.max(this.hitStop,heavy?.028:.014);
  this.emit('impact',{kind});
 }
 bounce(attack){
  if(attack.bounced)return;attack.bounced=true;const p=this.player;
  p.vy=-665;p.jumps=1;p.grounded=false;p.dashCooldown=0;p.invincible=Math.max(p.invincible,.16);attack.elapsed=.25;
  this.burst(p.x,p.y+15,'#d4fff0',15,270);this.stats.pogos++;this.gainFlow(14);this.emit('pogo');
 }
 updateBlade(dt){
  const p=this.player,a=p.attack;
  if(p.slashBuffer){p.slashBuffer.ttl-=dt;if(p.slashBuffer.ttl<=0)p.slashBuffer=null;}
  if(a){const move=BLADE_MOVES[a.kind];a.elapsed+=dt;p.slash=Math.max(0,move.duration-a.elapsed);
   if(a.elapsed>=move.activeAt&&!a.activated){a.activated=true;this.emit('swing',{kind:a.kind});if(a.kind==='break')p.overcharge=1.4;}
   if(a.elapsed>=move.activeAt&&a.elapsed<=move.activeUntil){
    const box=attackBox(p,a);if(this.loadout.blade==='arc'){if(a.kind==='down')box.bottom+=45;else if(a.kind==='up')box.top-=45;else box.right+=45;}const bladeDamage=(move.damage+(this.loadout.blade==='breaker'?3:this.loadout.blade==='arc'?1:0))*this.damageMultiplier;
    for(const e of this.enemies){if(!e.dead&&!a.hits.has(e)&&overlaps(box,e.x,e.y,37,34)){a.hits.add(e);this.hurtEnemy(e,bladeDamage,'blade');this.gainFlow(4);e.knockback=move.push;this.impact(e.x,e.y,a.kind);if(a.kind==='down')this.bounce(a);}}
    const b=this.boss;if(b&&this.phase==='boss'&&!a.hits.has(b)&&overlaps(box,b.x,b.y,84,94)){a.hits.add(b);this.hurtBoss(bladeDamage,'blade');this.gainFlow(5);this.impact(clamp(p.x,b.x-70,b.x+70),clamp(p.y-65,b.y-70,b.y+70),a.kind);if(a.kind==='down')this.bounce(a);}
    for(const b of this.hostile){if(b.life>0&&!a.hits.has(b)&&overlaps(box,b.x,b.y,b.r,b.r)){a.hits.add(b);b.life=0;this.score+=20;this.impact(b.x,b.y,'parry');this.stats.parries++;this.gainFlow(20);this.gainScrap(4,b.x,b.y);this.emit('parry');if(a.kind==='down')this.bounce(a);}}
    if(a.kind==='down')for(const h of this.hazards){if(h.type==='energy'&&!a.hits.has(h)&&overlaps(box,h.x+h.w/2,GROUND-15,h.w/2,15)){a.hits.add(h);this.impact(p.x,GROUND-20,'down');this.bounce(a);}}
   }
   if(p.slashBuffer&&a.elapsed>=move.chainAt){const direction=p.slashBuffer.direction;p.attack=null;this.slash(direction);}
   else if(a.elapsed>=move.duration){p.attack=null;p.slash=0;}
  }else if(p.slashBuffer&&p.dash<=0){const direction=p.slashBuffer.direction;p.slashBuffer=null;this.slash(direction);}
 }
 dash(){const p=this.player;if(this.over||this.paused||p.dashCooldown>0)return;p.attack=null;p.slash=0;p.slashBuffer=null;p.dashHits.clear();p.dashBuffer=0;p.dash=.16;p.dashCooldown=this.dashRecharge;p.invincible=Math.max(p.invincible,.22);p.vy=0;this.emit('dash');}
 hurt(){const p=this.player;if(this.demo||p.invincible>0||this.over)return;if(this.barrier>0||this.aegisReady){if(this.barrier>0)this.barrier--;else {this.aegisReady=false;this.aegisTimer=10;}p.invincible=.5;this.burst(p.x,p.y-60,'#8edfff',14,250);this.emit('blocked');return;}p.hp--;this.stats.damage++;this.flow=Math.max(0,this.flow-18);this.flowReadyAnnounced=this.flow===100;p.invincible=1.6;this.combo=0;this.shake=12;this.flash=.18;this.burst(p.x,p.y-50,'#ffb58b',16,300);this.emit('hurt');if(p.hp<=0){this.over=true;this.emit('death',{score:this.score});}}
 hurtEnemy(e,n,source='shot'){if(e.dead)return;if(e.type==='guard'&&source==='shot')n=Math.max(1,Math.ceil(n*.4));e.hp-=n;e.hit=.13;if(e.hp<=0){e.dead=true;this.defeats++;this.stats.kills++;this.gainFlow(13);this.gainScrap(e.type==='guard'?18:12,e.x,e.y-50);if(this.loadout.blade==='siphon'&&this.defeats%4===0)this.player.hp=Math.min(this.player.maxHp,this.player.hp+1);this.score+=100;this.combo++;this.comboTimer=4.5;this.stats.bestChain=Math.max(this.stats.bestChain,this.combo);this.burst(e.x,e.y,'#ffc897',23,320);this.shake=Math.max(this.shake,3);this.emit('kill');}}
 hurtBoss(n,source='blade'){const b=this.boss;if(!b||b.hp<=0||this.phase!=='boss')return;if((b.coreOpen||0)<=0&&source==='shot')n*=.25;b.hp=Math.max(0,b.hp-n);b.hit=.12;this.burst(b.x-40,b.y,'#ffcf9b',5,190);if(b.hp===0){this.score+=2500;this.burst(b.x,b.y,'#ffe5af',90,520);this.phase='leaving';this.phaseTime=0;this.shake=20;this.emit('bossDefeated');}}
 spawnSection(){const x=1690, elevated=this.time>30;const pattern=this.time<14?0:(Math.floor(this.worldX/1600)+(this.stage===2?2:0))%4;
  if(pattern===0){this.platforms.push({x,y:GROUND-82,w:310,h:33});this.platforms.push({x:x+360,y:GROUND-164,w:310,h:32});this.orbs.push({x:x+90,y:GROUND-124,taken:false},{x:x+380,y:GROUND-206,taken:false});}
  else if(pattern===1){this.hazards.push({x:x+70,y:GROUND,w:80,type:'energy',hit:false});this.platforms.push({x:x+250,y:GROUND-110,w:240,h:34});this.orbs.push({x:x+350,y:GROUND-153,taken:false});}
  else if(pattern===2){this.platforms.push({x,y:GROUND-100,w:260,h:32});this.platforms.push({x:x+330,y:GROUND-(elevated?195:150),w:230,h:32});this.hazards.push({x:x+700,y:GROUND,w:95,type:'gap',hit:false});this.orbs.push({x:x+100,y:GROUND-143,taken:false},{x:x+430,y:GROUND-(elevated?240:195),taken:false});}
  else {this.hazards.push({x:x+100,y:GROUND,w:85,type:'energy',hit:false});this.platforms.push({x:x+380,y:GROUND-80,w:310,h:35});for(let j=0;j<3;j++)this.orbs.push({x:x+430+j*75,y:GROUND-125,taken:false});}
 }
 update(dt,keys={}){
  if(this.over||this.paused||this.inWorkshop)return;dt=Math.min(dt,.034);this.time+=dt;this.phaseTime+=dt;const p=this.player;
  if(!this.demo){if(this.phase==='run'&&this.time>this.stageInfo.duration){this.phase='braking';this.phaseTime=0;this.emit('braking');}
   if(this.phase==='braking'&&this.phaseTime>4){this.phase='boss';this.phaseTime=0;this.speed=0;p.hp=Math.min(p.maxHp,p.hp+2);p.invincible=2;this.boss={x:1270,y:480,hp:this.stage===2?112:72,maxHp:this.stage===2?112:72,attack:3.4,telegraph:0,hit:0,cycle:0};this.platforms=[];this.hazards=[];this.enemies=[];this.orbs=[];this.hostile=[];this.emit('boss');}
   if(this.phase==='leaving'&&this.phaseTime>3){this.speed=0;finishStage(this);this.inWorkshop=true;this.completed=this.stage===2;this.paused=true;this.emit('workshop',{stage:this.stage,score:this.score,complete:this.completed});return;}}
  this.flowActive=Math.max(0,this.flowActive-dt);for(const f of this.floating){f.life-=dt;f.y-=dt*42;f.x-=this.speed*dt*.15;}this.floating=this.floating.filter(f=>f.life>0).slice(-30);
  for(const key of Object.keys(this.buffs))this.buffs[key]=Math.max(0,this.buffs[key]-dt);if(this.loadout.core==='aegis'&&!this.aegisReady){this.aegisTimer-=dt;if(this.aegisTimer<=0)this.aegisReady=true;}this.support(dt);
  const target=this.phase==='braking'?0:this.phase==='boss'?0:this.time>23?535:470;this.speed+=(target-this.speed)*Math.min(1,dt*(this.phase==='braking'?1.25:.6));if(this.speed<.3)this.speed=0;
  const movement=this.speed*dt;this.worldX+=movement;this.shake=Math.max(0,this.shake-dt*28);this.flash=Math.max(0,this.flash-dt);this.comboTimer-=dt;if(this.comboTimer<0)this.combo=0;
  // Hold only the blade pose on impact; locomotion and input keep their full timestep.
  const realDt=dt,bladeDt=this.hitStop>0?0:dt;this.hitStop=Math.max(0,this.hitStop-realDt);
  for(const field of ['dash','dashCooldown','shotCooldown','shotTime','muzzle','overcharge','chainTimer','invincible','land','jumpBuffer','dashBuffer'])p[field]=Math.max(0,p[field]-dt);
  p.recoil*=Math.exp(-dt*24);if(p.chainTimer<=0&&!p.attack)p.chainStep=0;
  if(this.demo){this.demoAction-=dt;if(this.demoAction<=0){this.demoAction=1.6+Math.random()*1.5;this.jump();}if(this.enemies.some(e=>e.x>p.x&&e.x<p.x+650))this.shoot();if(this.enemies.some(e=>Math.abs(e.x-p.x)<170))this.slash();}
  if(keys.slash){p.slashHeld+=realDt;if(p.slashHeld>=.17||!p.attack&&!p.slashBuffer)this.slash(keys.down?'down':keys.up?'up':'forward');}else p.slashHeld=0;if(keys.shoot)this.shoot();if(p.dashBuffer>0)this.dash();
  if(p.jumpBuffer>0)this.tryJump();
  this.updateBlade(bladeDt);
  const maxX=this.phase==='boss'?1240:1230;let horizontal=(keys.right?1:0)-(keys.left?1:0);
  if(p.dash>0){if(this.boss&&this.phase==='boss'&&!p.dashHits.has(this.boss)&&Math.hypot(this.boss.x-p.x,this.boss.y-p.y+55)<140){p.dashHits.add(this.boss);this.hurtBoss(5,'dash');this.gainFlow(8);this.impact(this.boss.x,this.boss.y,'dash');}p.x+=p.dashDirection*1080*dt;p.vy=0;for(const e of this.enemies)if(!p.dashHits.has(e)&&Math.abs(e.x-p.x)<95&&Math.abs(e.y-p.y+55)<95){p.dashHits.add(e);this.hurtEnemy(e,5,'dash');this.gainFlow(5);this.impact(e.x,e.y,'dash');}}
  else {p.x+=horizontal*440*dt;}
  p.x=clamp(p.x,160,maxX);const oldY=p.y;
  if(p.dash<=0)p.vy+= (p.vy<0?2350:3000)*dt;p.y+=p.vy*dt;p.grounded=false;p.coyote=Math.max(0,p.coyote-dt);
  for(const list of [this.platforms,this.hazards,this.orbs])for(const item of list)item.x-=movement;
  for(const plat of this.platforms){if(p.vy>=0&&oldY<=plat.y+8&&p.y>=plat.y&&p.x+20>plat.x&&p.x-20<plat.x+plat.w){p.y=plat.y;p.vy=0;p.grounded=true;}}
  const inGap=this.hazards.some(h=>h.type==='gap'&&p.x>h.x+8&&p.x<h.x+h.w-8);
  if(p.y>=GROUND&&p.vy>=0&&!inGap){p.y=GROUND;p.vy=0;p.grounded=true;}
  if(p.grounded){if(p.jumps>0){p.land=.10;this.burst(p.x,p.y,'#dbd8bb',6,110);this.emit('land');}p.jumps=0;p.coyote=.12;if(p.jumpBuffer>0)this.tryJump();}
  if(p.y>815){this.hurt();p.y=GROUND-220;p.vy=-300;p.jumps=1;p.x+=140;p.invincible=Math.max(p.invincible,1.5);}
  for(const h of this.hazards){if(h.type==='energy'&&p.x>h.x-12&&p.x<h.x+h.w+12&&p.y>GROUND-45)this.hurt();}
  for(const o of this.orbs){if(!o.taken&&Math.abs(o.x-p.x)<45&&Math.abs(o.y-(p.y-40))<75){o.taken=true;this.score+=50;this.gainScrap(o.value||5,o.x,o.y);this.gainFlow(3);this.burst(o.x,o.y,'#d1ffd1',12,190);this.emit('collect');}}
  if(!this.demo&&this.phase==='run')updateEncounters(this);
  for(const item of this.pickups){if(!item.stationary)item.x-=movement;if(item.ttl!==undefined){item.ttl-=dt;if(item.ttl<=0)item.taken=true;}const dx=p.x-item.x,dy=p.y-55-item.y;if((this.loadout.core==='magnet'||this.buffs.magnet>0)&&Math.hypot(dx,dy)<320){item.x+=dx*dt*8;item.y+=dy*dt*8;}if(Math.abs(dx)<48&&Math.abs(dy)<70){item.taken=true;this.collectPower(item.id);}}
  this.pickups=this.pickups.filter(x=>!x.taken&&x.x>-100);
  if(this.loadout.core==='magnet'||this.buffs.magnet>0)for(const o of this.orbs){if(Math.hypot(o.x-p.x,o.y-p.y+40)<320){o.x+=(p.x-o.x)*dt*8;o.y+=(p.y-40-o.y)*dt*8;}}
  if(this.demo){this.spawnDistance-=movement;if(this.spawnDistance<=0){this.spawnSection();this.spawnDistance=1850+Math.random()*450;}this.spawnEnemy-=dt;if(this.spawnEnemy<=0){this.spawnEnemy=this.time<23?4.8+Math.random()*1.2:3.5+Math.random()*1.5;this.enemies.push({x:1680,y:Math.random()>.4?GROUND-75:GROUND-185,originY:Math.random()>.4?GROUND-75:GROUND-185,hp:4,phase:Math.random()*6,fire:2.4,hit:0,dead:false});}}
  this.platforms=this.platforms.filter(x=>x.x+x.w>-150);this.hazards=this.hazards.filter(x=>x.x+x.w>-150);this.orbs=this.orbs.filter(x=>x.x>-150&&!x.taken);
  for(const e of this.enemies){e.x-=movement*.84+dt*(e.type==='rusher'?200:38)*(this.flowActive>0?.6:1);e.x+=(e.knockback||0)*dt;e.knockback=(e.knockback||0)*Math.exp(-dt*5);e.y+=Math.sin(this.time*3+e.phase)*dt*22;e.hit=Math.max(0,e.hit-dt);e.fire-=dt;if(!e.dead&&this.time>14&&e.fire<=0&&e.x>p.x+100&&e.x<1450&&!this.demo){e.fire=3.6;const a=Math.atan2(p.y-65-e.y,p.x-e.x);this.hostile.push({x:e.x-25,y:e.y,vx:Math.cos(a)*265,vy:Math.sin(a)*265,life:5,r:7});}if(!e.dead&&Math.abs(e.x-p.x)<55&&Math.abs(e.y-(p.y-55))<65&&p.dash<=0&&e.hit<=0)this.hurt();}
  this.enemies=this.enemies.filter(e=>e.x>-150&&!e.dead);
  for(const s of this.shots){if(s.homing){const target=this.enemies.find(e=>!e.dead&&e.x>s.x)||(this.phase==='boss'?this.boss:null);if(target){const angle=Math.atan2(target.y-s.y,target.x-s.x);s.vx+=(Math.cos(angle)*760-s.vx)*dt*5;s.vy=((s.vy||0)+(Math.sin(angle)*760-(s.vy||0))*dt*5);}}s.x+=s.vx*dt;s.y+=(s.vy||0)*dt;s.life-=dt;s.age+=dt;for(const e of this.enemies){if(!e.dead&&s.life>0&&!s.hits.has(e)&&Math.abs(s.x-e.x)<(s.charged?69:53)&&Math.abs(s.y-e.y)<(s.charged?58:45)){s.hits.add(e);this.hurtEnemy(e,s.damage,s.support?'support':'shot');this.impact(e.x,s.y,s.charged?'charged':'shot');if(--s.pierce<=0)s.life=0;}}if(this.boss&&this.phase==='boss'&&s.life>0&&!s.hits.has(this.boss)&&Math.abs(s.x-this.boss.x)<95&&Math.abs(s.y-this.boss.y)<115){s.hits.add(this.boss);this.hurtBoss(s.damage,s.charged?'charged':s.support?'support':'shot');this.impact(this.boss.x-75,s.y,s.charged?'charged':'shot');s.life=0;}}
  this.shots=this.shots.filter(s=>s.life>0&&s.x<1700);
  if(this.boss&&this.phase==='boss')updateBoss(this,dt);
  for(const b of this.hostile){b.x+=b.vx*dt*(this.flowActive>0?.58:1);b.y+=b.vy*dt*(this.flowActive>0?.58:1);b.life-=dt;if(Math.abs(b.x-p.x)<(b.r+19)&&Math.abs(b.y-(p.y-51))<(b.r+35)){this.hurt();b.life=0;}}
  this.hostile=this.hostile.filter(b=>b.life>0&&b.x>-100&&b.y>-100&&b.y<820);
  this.stormCooldown-=dt;if(this.buffs.storm>0&&this.stormCooldown<=0){this.stormCooldown=.32;for(const e of this.enemies)if(Math.hypot(e.x-p.x,e.y-p.y+65)<145){this.hurtEnemy(e,3,'storm');this.impact(e.x,e.y,'storm');}if(this.boss&&this.phase==='boss'&&Math.hypot(this.boss.x-p.x,this.boss.y-p.y+65)<190)this.hurtBoss(2);}
  this.ghostTimer-=dt;if(this.ghostTimer<=0){this.ghostTimer=p.dash>0?.022:p.attack?.035:.075;this.ghosts.push({x:p.x-15,y:p.y,life:p.dash>0?.32:p.attack?.22:.15,attack:p.attack?{kind:p.attack.kind,elapsed:p.attack.elapsed}:null,frame:p.dash>0?5:p.jumps?4:Math.floor(this.time*16)%4});}
  for(const g of this.ghosts){g.life-=dt;g.x-=movement*.7;}this.ghosts=this.ghosts.filter(g=>g.life>0);
  for(const q of this.particles){q.life-=dt;q.x+=q.vx*dt-movement*.35;q.y+=q.vy*dt;q.vy+=460*dt;}this.particles=this.particles.filter(q=>q.life>0).slice(-250);
  for(const i of this.impacts){i.life-=dt;i.x-=movement*.35;}this.impacts=this.impacts.filter(i=>i.life>0).slice(-40);
  if(p.grounded&&this.speed>50&&Math.random()<.5)this.particles.push({x:p.x-20,y:p.y-2,vx:-100-Math.random()*90,vy:-Math.random()*40,life:.35,max:.35,color:'#d5d7c1',size:1+Math.random()*3});
 }
}
