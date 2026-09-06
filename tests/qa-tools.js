import {world,enterStage} from '/game.js';
const panel=document.createElement('nav');panel.style='position:fixed;bottom:0;left:0;z-index:100;background:#102a36;padding:8px;display:flex;gap:8px';panel.setAttribute('aria-label','Development playtest');
function button(name,fn){const b=document.createElement('button');b.textContent=name;b.onclick=fn;panel.append(b);}
button('Finish current stage',()=>{if(world.inWorkshop)return;world.paused=false;world.over=false;world.phase='boss';world.boss={hp:1,maxHp:72,x:1220,y:530};world.hurtBoss(1);for(let i=0;i<400&&!world.inWorkshop;i++)world.update(1/120);});
button('Powerup fixture',()=>{world.player.hp=2;for(const id of ['repair','rapid','shield','overdrive','pierce','magnet','nova'])world.collectPower(id);});
button('Boss fixture',()=>{world.phase='braking';world.phaseTime=4.1;world.update(.01);});
document.body.append(panel);
