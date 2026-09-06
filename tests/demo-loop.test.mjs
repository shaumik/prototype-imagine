import test from 'node:test';
import assert from 'node:assert/strict';
import {World,GROUND} from '../dist/engine.js';
import {PRICES} from '../dist/progression.js';
import {spawnWave} from '../dist/encounters.js';
const tick=(w,seconds,keys={})=>{for(let i=0;i<seconds*120;i++)w.update(1/120,keys);};
const clear=w=>{w.phase='boss';w.boss={x:1200,y:530,hp:1,maxHp:72};w.hurtBoss(10);tick(w,3.1);};

test('shop transactions are atomic, owned swaps are free, and unpurchased parts cannot launch',()=>{
 const w=new World();w.reset(false);assert.equal(w.purchase('core','boost').ok,false);
 clear(w);assert.equal(w.scrap,180);const start=w.scrap;
 assert(w.purchase('core','boost').ok);assert.equal(w.scrap,start-PRICES.boost);
 assert.equal(w.purchase('shoulder','cannon').ok,false);assert.equal(w.loadout.shoulder,'none');
 assert.equal(w.purchase('madeup','boost').ok,false);
 assert(w.purchase('core','stock').ok);assert(w.purchase('core','boost').ok);assert.equal(w.scrap,start-PRICES.boost);
 assert(w.advanceStage({loadout:{...w.loadout,shoulder:'cannon'}}));assert.equal(w.loadout.shoulder,'none');assert.equal(w.loadout.core,'boost');
});
test('stage retries roll back earned scrap but preserve purchased build and remaining wallet',()=>{
 const w=new World();w.reset(false);clear(w);w.purchase('blade','arc');const balance=w.scrap;w.advanceStage();
 w.gainScrap(75);w.collectPower('wings');w.player.hp=0;w.over=true;w.retryStage();
 assert.equal(w.stage,2);assert.equal(w.loadout.blade,'arc');assert(w.owned.has('arc'));assert.equal(w.scrap,balance);assert.equal(w.buffs.wings,0);assert.equal(w.stats.kills,0);
});
test('temporary powers clear at the pit stop, wings enable a third jump, and Flow lasts seven seconds',()=>{
 const w=new World();w.reset(false);w.collectPower('wings');assert(w.jump());assert(w.jump());assert(w.jump());assert.equal(w.jump(),false);
 w.collectPower('storm');assert.equal(w.buffs.storm,Infinity);w.gainFlow(100);assert(w.activateFlow());assert.equal(w.activateFlow(),false);assert.equal(w.damageMultiplier,2);w.phase='boss';tick(w,7.1);assert.equal(w.flowActive,0);assert.equal(w.damageMultiplier,1);
 clear(w);assert(Object.values(w.buffs).every(n=>n===0));assert.equal(w.flow,0);assert.equal(w.barrier,0);
});
test('guards resist buster fire while blade and dash damage break armor',()=>{
 const w=new World();w.reset(false);spawnWave(w,'guards');const guard=w.enemies[0];
 w.hurtEnemy(guard,4);assert.equal(guard.hp,8);w.hurtEnemy(guard,4,'blade');assert.equal(guard.hp,4);w.hurtEnemy(guard,4,'dash');assert(guard.dead);assert.equal(w.scrap,18);
});
test('authored routes differ, all boss patterns have warnings, and waves can be jumped',()=>{
 for(const stage of [1,2]){const events=[],w=new World((t,d)=>events.push([t,d]));w.reset(false,{stage});w.player.invincible=100;tick(w,6);assert(events.some(([t])=>t==='cue'));assert(w.beatIndex>=3);
  w.phase='braking';w.phaseTime=4.1;w.update(.01);const patterns=new Set();
  for(let i=0;i<11*120;i++){w.update(1/120);if(w.boss.telegraph>.3)patterns.add(w.boss.pattern);}
  assert.deepEqual([...patterns].sort(),['FAN BURST','HIGH SWEEP','LOW WAVE']);assert(w.hostile.some(b=>b.wave)||w.boss.cycle>=3);
 }
});

function drive(w){
 const dt=1/120;let jumpLock=0;
 for(let i=0;i<180*120&&!w.inWorkshop&&!w.over;i++){
  const p=w.player;const enemy=w.enemies.find(e=>!e.dead&&e.x>p.x-40&&e.x<p.x+180);
  const hazard=w.hazards.some(h=>h.x>p.x-80&&h.x<p.x+220);
  const bullet=w.hostile.some(b=>b.x>p.x&&b.x<p.x+200&&Math.abs(b.y-p.y+55)<75);
  jumpLock-=dt;
  if((hazard||bullet)&&p.grounded&&jumpLock<=0){w.jump();jumpLock=.55;}
  if(enemy&&p.dashCooldown===0&&Math.abs(enemy.y-p.y+55)<75)w.requestDash(1);
  if(w.flow>=100)w.activateFlow();
  if(w.phase==='boss'&&p.x>880)w.requestDash(-1);
  w.update(dt,{shoot:true,slash:!!enemy,right:p.x<570,left:p.x>790});
 }
 return {over:w.over,shop:w.inWorkshop,kills:w.stats.kills,damage:w.stats.damage,scrap:w.scrap,time:w.time};
}
test('a mixed-action route completes both levels and funds meaningful equipment',()=>{
 const w=new World();w.reset(false);const first=drive(w);assert(first.shop,JSON.stringify(first));assert(first.kills>=10);assert(first.scrap>=PRICES.cannon+PRICES.boost);
 w.purchase('shoulder','cannon');w.purchase('core','boost');if(w.scrap>=PRICES.arc)w.purchase('blade','arc');
 w.advanceStage();const second=drive(w);assert(second.shop&&w.completed,JSON.stringify(second));assert(w.time<180);
});
