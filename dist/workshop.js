import {CHASSIS,EQUIPMENT} from './loadout.js';
import {PRICES,BUILD_NAMES,BUILD_HINTS} from './progression.js';
import {drawPowerEffects} from './game-fx.js';
const ART_INDEX={spread:1,rail:0,arc:5,breaker:5,siphon:5,cannon:0,missiles:1,drone:2,boost:4,aegis:3,magnet:3};
export class Workshop {
 constructor(root,art,animation,onLaunch){
  this.root=root;this.art=art;this.animation=animation;this.onLaunch=onLaunch;
  this.pixelRatio=Math.min(2,Math.max(1,window.devicePixelRatio||1));
  const canvas=root.querySelector('#build-preview');canvas.width=330*this.pixelRatio;canvas.height=310*this.pixelRatio;
  root.addEventListener('click',e=>{
   const slot=e.target.closest('[data-slot]');if(slot){this.slot=slot.dataset.slot;this.selected=this.world.loadout[this.slot];this.renderEquipment();return;}
   const part=e.target.closest('[data-part]');if(part){this.selected=part.dataset.part;this.renderEquipment();return;}
   if(e.target.closest('#buy-part'))this.buy();
   if(e.target.closest('#test-build')){this.testTime=performance.now()/1000;this.testKind=this.testKind==='blade'?'buster':'blade';}
  });
  root.querySelector('#launch-stage').addEventListener('click',()=>onLaunch({chassis:this.world.chassis,loadout:{...this.world.loadout},scrap:this.world.scrap,owned:[...this.world.owned]}));
 }
 open(world){
  this.world=world;this.chassis=world.chassis;this.complete=world.completed;this.slot='shoulder';this.selected=world.loadout.shoulder;this.testTime=-10;this.testKind='blade';
  this.root.classList.remove('hidden');
  this.root.querySelector('#workshop-title').textContent=this.complete?'One hell of a ride.':'The pit stop.';
  this.root.querySelector('#workshop-status').textContent=this.complete?'DAYDREAM COMPLETE · 02 / 02':'ROUTE 07 · SIGNAL CLEARED';
  this.root.querySelector('#workshop-next').textContent=this.complete?'Refit your runner and take the two-stage route again.':'Spend your scrap. Build your advantage for Harbor Afterglow.';
  this.root.querySelector('#launch-stage').textContent=this.complete?'RIDE AGAIN →':'TO THE HARBOR →';
  const r=world.results||{rank:'C',kills:0,bestChain:0,parries:0,bonus:180};
  this.root.querySelector('#run-results').innerHTML=`<div class="result-rank"><small>RIDE RANK</small><strong>${r.rank}</strong></div><div><strong>${r.kills}</strong><small>DEFEATED</small></div><div><strong>${r.bestChain}×</strong><small>BEST CHAIN</small></div><div><strong>${r.parries}</strong><small>PARRIES</small></div><div><strong>+${r.bonus}</strong><small>CLEAR BONUS</small></div>`;
  this.root.querySelector('.workshop-note').textContent='Purchased parts stay with you through the next stage and retries. Temporary powers fade at the pit stop. Repairs are on the house.';
  this.renderEquipment();this.root.querySelector('#launch-stage').focus();
 }
 renderEquipment(){
  const w=this.world;
  this.loadout={...w.loadout,[this.slot]:this.selected};
  this.root.querySelector('#shop-wallet').textContent=w.scrap.toLocaleString();
  this.root.querySelector('#shop-tabs').innerHTML=Object.entries(BUILD_NAMES).map(([id,name])=>`<button type="button" data-slot="${id}" aria-pressed="${id===this.slot}">${name}</button>`).join('');
  this.root.querySelector('#equipment-options').innerHTML=EQUIPMENT[this.slot].map(item=>{
   const owned=w.owned.has(item.id),equipped=w.loadout[this.slot]===item.id;
   return `<button type="button" data-part="${item.id}" aria-pressed="${item.id===this.selected}" class="shop-part ${equipped?'equipped':''}"><canvas width="180" height="112" data-art="${item.id}" aria-hidden="true"></canvas><span class="part-price">${equipped?'EQUIPPED':owned?'OWNED':PRICES[item.id]+' SCRAP'}</span><strong>${item.name}</strong><small>${item.desc}</small></button>`;
  }).join('');
  const item=EQUIPMENT[this.slot].find(i=>i.id===this.selected),owned=w.owned.has(item.id),equipped=w.loadout[this.slot]===item.id,cost=owned?0:PRICES[item.id];
  this.root.querySelector('#part-name').textContent=item.name;
  this.root.querySelector('#part-description').textContent=BUILD_HINTS[item.id]||'Your original equipment. Always available.';
  const button=this.root.querySelector('#buy-part');button.textContent=equipped?'EQUIPPED':owned?'EQUIP PART':w.scrap<cost?`NEED ${cost-w.scrap} MORE SCRAP`:`BUY & EQUIP · ${cost} SCRAP`;button.disabled=equipped||w.scrap<cost;
  this.root.querySelector('#build-name').textContent=CHASSIS[w.chassis].name;
  this.root.querySelector('#preview-label').textContent=equipped?'CURRENT BUILD':'PREVIEW · NOT EQUIPPED';
  this.root.querySelector('#build-stats').textContent=`6 armor · ${this.loadout.core==='boost'?'0.30':'0.48'}s dash`;
  this.root.querySelector('#build-summary').textContent=Object.entries(w.loadout).filter(([slot,id])=>!['pulse','standard','stock','none'].includes(id)).map(([slot,id])=>EQUIPMENT[slot].find(i=>i.id===id).name).join(' + ')||'Stock runner · ready for an upgrade';
  for(const c of this.root.querySelectorAll('[data-art]')){const ctx=c.getContext('2d'),id=c.dataset.art;ctx.clearRect(0,0,180,112);if(ART_INDEX[id]!==undefined){if(id==='breaker')ctx.filter='hue-rotate(180deg)';if(id==='siphon')ctx.filter='hue-rotate(100deg)';const idx=ART_INDEX[id],im=this.art.modules?.[idx]?.image;if(im){const scale=Math.min(135/im.width,78/im.height);ctx.drawImage(im,90-im.width*scale/2,56-im.height*scale/2,im.width*scale,im.height*scale);}}else{ctx.strokeStyle='#8baba6';ctx.lineWidth=2;ctx.strokeRect(71,38,38,38);ctx.fillStyle='#bdd4ce';ctx.font='22px Arial';ctx.textAlign='center';ctx.fillText('—',90,65);}}
 }
 buy(){const result=this.world.purchase(this.slot,this.selected);const status=this.root.querySelector('#shop-message');status.textContent=result.ok?'Equipped. Your new part is ready.':result.reason;this.renderEquipment();}
 draw(time){
  if(this.root.classList.contains('hidden'))return;
  const canvas=this.root.querySelector('#build-preview'),ctx=canvas.getContext('2d');ctx.setTransform(this.pixelRatio,0,0,this.pixelRatio,0,0);ctx.clearRect(0,0,330,310);ctx.imageSmoothingQuality='high';
  ctx.strokeStyle='#5aa59b30';ctx.lineWidth=1;ctx.beginPath();ctx.ellipse(165,276,100,15,0,0,Math.PI*2);ctx.stroke();
  const age=performance.now()/1000-this.testTime,attack=age>=0&&age<.33&&this.testKind==='blade'?{kind:'break',elapsed:age}:null;
  const p={x:153,y:260,grounded:true,vy:0,land:0,dash:0,recoil:age<.3&&this.testKind==='buster'?Math.exp(-age*20)*3:0,attack};
  ctx.save();ctx.translate(150,260);ctx.scale(1.25,1.25);ctx.translate(-150,-260);
  this.animation.draw(ctx,p,0,{},1);this.art.draw(ctx,p,0,this.loadout,time,1);
  drawPowerEffects(ctx,{player:p,loadout:this.loadout,buffs:{},barrier:0,flowActive:0},time);
  if(age<.4&&this.testKind==='buster'){ctx.strokeStyle='#c9ffe6';ctx.lineWidth=5;ctx.shadowColor='#76ffe3';ctx.shadowBlur=14;ctx.beginPath();ctx.moveTo(p.x+75+age*220,p.y-83);ctx.lineTo(p.x+110+age*220,p.y-83);ctx.stroke();}
  ctx.restore();
 }
 close(){this.root.classList.add('hidden');}
}
