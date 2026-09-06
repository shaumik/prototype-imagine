import test from 'node:test';
import assert from 'node:assert/strict';
import {World,GROUND} from '../dist/engine.js';
import {BLADE_MOVES,attackFrame,attackBox,overlaps} from '../dist/combat.js';

function setup(){
 const events=[],w=new World((kind,data)=>events.push({type:kind,...data}));w.reset(false);w.phase='boss';w.speed=0;
 const step=(seconds,keys={})=>{for(let i=0;i<Math.ceil(seconds*120);i++)w.update(1/120,keys);};
 const until=(condition,max=2)=>{for(let i=0;i<max*120&&!condition();i++)w.update(1/120,{});assert(condition(),'Condition should be reached');};
 const enemy=(x=w.player.x+120,y=GROUND-80,hp=30)=>{const e={x,y,hp,phase:0,fire:99,hit:0,dead:false};w.enemies.push(e);return e;};
 return {w,events,step,until,enemy};
}

test('a cut has anticipation, hits once, and cannot hit behind the runner',()=>{
 const {w,step,enemy}=setup(),front=enemy(),behind=enemy(w.player.x-120);
 w.slash();assert.equal(front.hp,30);step(.008);assert.equal(front.hp,30);step(.06);assert.equal(front.hp,26);
 step(.12);assert.equal(front.hp,26);assert.equal(behind.hp,30);
});

test('a short press is one swing; holding chains cut, rise, break',()=>{
 const {w,events,step}=setup();w.slash();step(.05,{slash:true});step(.5);assert.equal(events.filter(e=>e.type==='slash').length,1);
 w.reset(false);w.phase='boss';w.speed=0;events.length=0;step(1,{slash:true});
 assert.deepEqual(events.filter(e=>e.type==='slash').slice(0,3).map(e=>e.step),[1,2,3]);
 assert.deepEqual(events.filter(e=>e.type==='swing').slice(0,3).map(e=>e.kind),['cut','rise','break']);
});

test('buffered taps connect during recovery and stale chains reset',()=>{
 const {w,step,until}=setup();w.slash();step(.11);w.slash();until(()=>w.player.attack?.kind==='rise');
 step(.12);w.slash();until(()=>w.player.attack?.kind==='break');step(.95);w.slash();assert.equal(w.player.attack.kind,'cut');
});

test('finisher primes a piercing buster and shooting respects active melee',()=>{
 const {w,step,until}=setup();w.player.chainStep=2;w.player.chainTimer=1;w.slash();
 assert.equal(w.shoot(),false);step(.12);assert(w.player.overcharge>0);until(()=>w.player.attack?.elapsed>=BLADE_MOVES.break.chainAt);
 assert.equal(w.shoot(),true);assert.equal(w.player.attack,null);assert.equal(w.shots[0].charged,true);assert.equal(w.shots[0].damage,6);assert.equal(w.shots[0].pierce,3);assert(w.player.muzzle>0&&w.player.recoil>1);assert.equal(w.player.overcharge,0);
});

test('ordinary buster shots animate and deal damage only once per target',()=>{
 const {w,step,enemy}=setup(),e=enemy(w.player.x+300,GROUND-83);
 assert(w.shoot());assert(w.player.shotTime>0&&w.player.muzzle>0);assert.equal(w.shoot(),false);
 step(.3);assert.equal(e.hp,28);assert.equal(w.shots.length,0);
});

test('powered bolts pierce separate enemies without duplicate hits',()=>{
 const {w,step,enemy}=setup(),a=enemy(w.player.x+250,GROUND-83),b=enemy(w.player.x+360,GROUND-83);
 w.player.overcharge=1;w.shoot();step(.3);assert.equal(a.hp,24);assert.equal(b.hp,24);
});

test('pogo bounce refreshes air jump and dash; directional hitboxes stay distinct',()=>{
 const {w,until,enemy}=setup(),p=w.player;p.y=500;p.grounded=false;p.vy=50;p.jumps=2;p.dashCooldown=1;const e=enemy(p.x,590,20);
 w.slash('down');until(()=>e.hp<20);assert.equal(e.hp,15);assert(p.vy<0);assert.equal(p.jumps,1);assert.equal(p.dashCooldown,0);
 const up=attackBox(p,{kind:'up'});assert(overlaps(up,p.x,p.y-190,10,10));assert(!overlaps(up,p.x,p.y+60,10,10));
 w.jump();assert.equal(p.jumps,2);
});

test('downward strikes bounce off energized roadside hazards',()=>{
 const {w,until}=setup(),p=w.player;p.y=565;p.grounded=false;p.vy=100;p.dashCooldown=1;
 w.hazards.push({x:p.x-50,w:100,y:GROUND,type:'energy'});w.slash('down');until(()=>p.vy<0);assert.equal(p.hp,6);assert.equal(p.dashCooldown,0);
});

test('blade can parry hostile shots and hitstop keeps the car moving',()=>{
 const {w,step}=setup(),p=w.player;w.speed=470;w.hostile.push({x:p.x+120,y:p.y-60,vx:-200,vy:0,life:3,r:8});
 w.slash();while(w.hostile.length)w.update(1/120,{});assert.equal(w.hostile.length,0);assert.equal(p.hp,6);assert(w.hitStop>0);
 const road=w.worldX,pose=p.attack.elapsed;w.update(1/120,{});assert(w.worldX>road);assert.equal(p.attack.elapsed,pose);
});

test('dash cancels attacks, pause blocks actions, and reset clears combat state',()=>{
 const {w}=setup();w.slash();w.dash();assert.equal(w.player.attack,null);assert(w.player.dash>0);
 w.paused=true;const n=w.shots.length;assert.equal(w.shoot(),false);assert.equal(w.slash(),false);assert.equal(w.shots.length,n);
 w.reset(false);assert.equal(w.player.chainStep,0);assert.equal(w.player.overcharge,0);assert.equal(w.hitStop,0);assert.equal(w.impacts.length,0);
});

test('all combat poses stay inside the 16-frame atlas',()=>{
 for(const kind of Object.keys(BLADE_MOVES))for(let t=0;t<BLADE_MOVES[kind].duration;t+=.005){const f=attackFrame({kind,elapsed:t});assert(Number.isInteger(f)&&f>=0&&f<16);}
});


test('impact does not freeze steering or jump physics',()=>{
 const {w}=setup(),p=w.player;w.hitStop=.03;const x=p.x;w.jump();const y=p.y;w.update(1/120,{right:true});assert(p.x>x);assert(p.y<y);
});
test('tap jumps lower than held jumps and landing consumes buffered input',()=>{
 const apex=release=>{const {w,step}=setup();w.jump();step(.05);if(release)w.releaseJump();let y=GROUND;for(let i=0;i<120;i++){w.update(1/120,{});y=Math.min(y,w.player.y);}return y;};
 assert(apex(true)>apex(false)+50);
 const {w}=setup(),p=w.player;p.y=GROUND-2;p.vy=300;p.jumps=2;p.grounded=false;p.coyote=0;w.jump();w.update(1/120,{});assert(p.vy<0);assert.equal(p.jumps,1);
});
test('left dash, cooldown buffering, and release preserve player control',()=>{
 const {w,step}=setup(),p=w.player,x=p.x;w.requestDash(-1);step(.08);assert(p.x<x);step(.3);w.requestDash(1);step(.11);assert(p.dash>0);step(.25);const stopped=p.x;step(.2);assert.equal(p.x,stopped);
});
test('opening is forgiving and boss arrival replenishes health',()=>{
 const {w}=setup();w.phase='run';w.time=6;w.spawnSection();assert.equal(w.hazards.length,0);
 w.phase='braking';w.phaseTime=4;w.player.hp=2;w.update(1/120,{});assert.equal(w.player.hp,4);assert.equal(w.boss.hp,72);
});
