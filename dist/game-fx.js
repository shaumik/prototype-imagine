export function drawPowerEffects(ctx,w,time){
 const p=w.player,b=w.buffs||{},gear=w.loadout||{};
 ctx.save();ctx.translate(p.x,p.y-75);ctx.lineCap='round';
 const ring=(color,rx,ry,angle=0,alpha=.7)=>{ctx.strokeStyle=color;ctx.globalAlpha=alpha;ctx.shadowColor=color;ctx.shadowBlur=13;ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(0,0,rx,ry,angle,0,Math.PI*2);ctx.stroke();};
 if(b.storm>0){for(let i=0;i<3;i++){const a=time*4.5+i*Math.PI*2/3,x=Math.cos(a)*105,y=Math.sin(a)*61;ctx.save();ctx.translate(x,y);ctx.rotate(a+.7);ctx.globalAlpha=.9;ctx.shadowColor='#b69cff';ctx.shadowBlur=18;ctx.strokeStyle='#e7dbff';ctx.lineWidth=4;ctx.beginPath();ctx.moveTo(-18,-7);ctx.quadraticCurveTo(0,12,25,0);ctx.stroke();ctx.restore();}ring('#b296ff',105,61,0,.16);}
 if(b.wings>0){ctx.globalAlpha=.6;ctx.shadowColor='#8aefff';ctx.shadowBlur=14;ctx.strokeStyle='#b7f8ff';for(let side of [-1,1])for(let i=0;i<3;i++){ctx.lineWidth=4-i;ctx.beginPath();ctx.moveTo(-23,-24+i*9);ctx.quadraticCurveTo(-65-i*17,-55+side*23,-110-i*12,-70+side*45+i*10+Math.sin(time*7)*8);ctx.stroke();}}
 if(b.rapid>0){ctx.globalAlpha=.9;ctx.strokeStyle='#ffe89e';ctx.shadowColor='#ffdc74';ctx.shadowBlur=10;ctx.lineWidth=3;for(let i=0;i<3;i++){ctx.beginPath();ctx.arc(55+i*9,-8,13+i,Math.sin(time*11)+i,Math.sin(time*11)+i+4);ctx.stroke();}}
 if(b.pierce>0){ctx.strokeStyle='#e1bcff';ctx.lineWidth=2;ctx.globalAlpha=.85;for(let i=0;i<3;i++){ctx.beginPath();ctx.moveTo(61+i*12,-19);ctx.lineTo(69+i*12,-8);ctx.lineTo(61+i*12,3);ctx.stroke();}}
 if(b.magnet>0||gear.core==='magnet'){ring('#a2ffd4',82,84,time*.7,.35);ring('#a2ffd4',45,76,-time,.35);}
 if(gear.core==='boost'){ctx.globalAlpha=.75;ctx.shadowColor='#78e9ff';ctx.shadowBlur=16;ctx.strokeStyle='#b7f4ff';ctx.lineWidth=6;for(let y of [-16,0]){ctx.beginPath();ctx.moveTo(-34,y);ctx.lineTo(-70-(p.dash>0?75:15+Math.sin(time*32)*10),y+10);ctx.stroke();}}
 if(b.overdrive>0||w.flowActive>0){const color=w.flowActive>0?'#c5a3ff':'#ffb289';ring(color,65,90,0,.6);ctx.globalAlpha=.7;ctx.strokeStyle=color;ctx.lineWidth=3;for(let i=0;i<5;i++){const y=-60+i*25;ctx.beginPath();ctx.moveTo(-38,y);ctx.quadraticCurveTo(-90,y+Math.sin(time*12+i)*20,-155-i*13,y+20);ctx.stroke();}}
 ctx.restore();
}
export function drawCombatReadouts(ctx,w,time){
 ctx.save();ctx.textAlign='center';
 for(const e of w.enemies){if(!e.maxHp)continue;const color=e.type==='guard'?'#ffc78b':e.type==='rusher'?'#ff99ae':'#bceadc';ctx.fillStyle='#0e283dc9';ctx.fillRect(e.x-26,e.y-65,52,4);ctx.fillStyle=color;ctx.fillRect(e.x-26,e.y-65,52*Math.max(0,e.hp/e.maxHp),4);if(e.type==='guard'){ctx.strokeStyle='#ffd99e';ctx.globalAlpha=.65;ctx.lineWidth=2;ctx.beginPath();ctx.ellipse(e.x-31,e.y,12,38,0,-Math.PI/2,Math.PI/2);ctx.stroke();ctx.globalAlpha=1;}}
 for(const f of w.floating){ctx.globalAlpha=Math.min(1,f.life*3);ctx.fillStyle=f.color;ctx.font=`700 ${f.size||18}px Arial`;ctx.shadowColor='#102032';ctx.shadowBlur=7;ctx.fillText(f.text,f.x,f.y);}
 if(w.boss?.coreOpen>0&&w.phase==='boss'){ctx.fillStyle='#c7ffdd';ctx.font='700 16px Arial';ctx.fillText('CORE OPEN',w.boss.x,w.boss.y-156);}
 if(w.boss?.telegraph>.35&&w.phase==='boss'){const b=w.boss;ctx.globalAlpha=b.telegraph*.7;ctx.strokeStyle='#ffbc85';ctx.fillStyle='#ff98671a';ctx.lineWidth=2;ctx.setLineDash([14,12]);const y=b.pattern==='LOW WAVE'?670:b.pattern==='HIGH SWEEP'?560:null;if(y){ctx.fillRect(145,y-25,1250,50);ctx.beginPath();ctx.moveTo(145,y);ctx.lineTo(1395,y);ctx.stroke();}ctx.setLineDash([]);ctx.globalAlpha=1;ctx.fillStyle='#ffe2c2';ctx.font='700 17px Arial';ctx.fillText(b.pattern,b.x,b.y-156);}
 ctx.restore();
}
