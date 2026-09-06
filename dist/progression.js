import {DEFAULT_LOADOUT, EQUIPMENT, normalizeLoadout} from './loadout.js';

export const PRICES = {
 pulse:0, spread:140, rail:160, standard:0, arc:120, breaker:150, siphon:130,
 none:0, cannon:200, missiles:190, drone:170, stock:0, boost:110, aegis:120, magnet:80
};
export const BUILD_NAMES = {primary:'ARM CANNON', blade:'CYBER BLADE', shoulder:'SUPPORT MOUNT', core:'REACTOR'};
export const BUILD_HINTS = {
 spread:'A three-barrel muzzle replaces the pulse buster.', rail:'A long accelerator barrel extends the arm cannon.',
 arc:'A longer cyan energy blade unfolds.', breaker:'A broad amber blade replaces the saber.', siphon:'A violet blade draws energy from defeated enemies.',
 cannon:'A heavy cannon mounts above your shoulder.', missiles:'A twin rocket pod mounts above your shoulder.', drone:'A wing drone flies at your side.',
 boost:'Twin thrusters ignite on your back.', aegis:'An emitter and blue shield wrap your armor.', magnet:'A salvage ring pulses around your reactor.'
};
export function initProgression(world,options={}) {
 world.scrap=Math.max(0,Math.floor(options.scrap||0));
 world.owned=new Set(Object.values(DEFAULT_LOADOUT));
 for(const id of options.owned||[])if(Object.values(EQUIPMENT).flat().some(item=>item.id===id))world.owned.add(id);
 // Explicit reset loadouts support saved builds; the shop checks ownership at purchase and launch.
 for(const id of Object.values(world.loadout))world.owned.add(id);
 world.stageStartScrap=world.scrap;world.stageStartOwned=[...world.owned];
 world.flow=0;world.flowActive=0;world.flowReadyAnnounced=false;world.floating=[];
 world.stats={kills:0,parries:0,pogos:0,bestChain:0,damage:0,scrap:0,flowBursts:0};
 world.results=null;
}
export function purchase(world,slot,id) {
 if(!world.inWorkshop)return {ok:false,reason:'Visit the pit stop first.'};
 const item=EQUIPMENT[slot]?.find(item=>item.id===id);
 if(!item)return {ok:false,reason:'That part does not fit this slot.'};
 const cost=world.owned.has(id)?0:PRICES[id];
 if(world.scrap<cost)return {ok:false,reason:`Need ${cost-world.scrap} more scrap.`};
 world.scrap-=cost;world.owned.add(id);world.loadout[slot]=id;
 world.emit('purchase',{name:item.name,cost});return {ok:true,cost};
}
export function ownedLoadout(world,value) {
 const normalized=normalizeLoadout(value);
 return Object.fromEntries(Object.entries(normalized).map(([slot,id])=>[slot,world.owned.has(id)?id:world.loadout[slot]]));
}
export function addScrap(world,n,x=world.player.x,y=world.player.y-145) {
 world.scrap+=n;world.stats.scrap+=n;
 world.floating.push({text:`+${n}`,x,y,life:.9,color:'#ffe5a0',size:19});
}
export function addFlow(world,n) {
 if(world.demo||world.flowActive>0)return;
 world.flow=Math.min(100,world.flow+n);
 if(world.flow===100&&!world.flowReadyAnnounced){world.flowReadyAnnounced=true;world.emit('flowReady');}
}
export function activateFlow(world) {
 if(world.demo||world.paused||world.over||world.inWorkshop||world.flow<100||world.flowActive>0)return false;
 world.flow=0;world.flowActive=7;world.flowReadyAnnounced=false;world.stats.flowBursts++;
 world.player.invincible=Math.max(world.player.invincible,.8);world.player.dashCooldown=0;
 world.hostile=[];world.shake=7;world.burst(world.player.x,world.player.y-70,'#d1b4ff',50,480);world.emit('flow');return true;
}
export function finishStage(world) {
 const stats=world.stats,rank=stats.damage===0&&stats.kills>=10?'S':stats.damage<=3&&stats.kills>=6?'A':stats.kills>=3?'B':'C';
 const bonus=180+({S:80,A:40,B:20,C:0}[rank]);
 addScrap(world,bonus);world.results={...stats,rank,bonus,total:world.score};
 world.buffs=Object.fromEntries(Object.keys(world.buffs).map(id=>[id,0]));world.barrier=0;world.flow=0;world.flowActive=0;world.pickups=[];
}
