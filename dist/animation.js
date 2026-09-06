import {BLADE_MOVES} from './combat.js';
const clamp=(n,a,b)=>Math.max(a,Math.min(b,n));
// Authored full-body poses: preserve the silhouette and anatomy at every frame.
export class Animation {
 constructor(){this.atlases={};this.reset();}
 reset(){this.stride=0;this.airTime=0;this.wasGrounded=true;this.previous=null;this.transition=1;}
 load(name,image,cols,rows){
  const surface=document.createElement('canvas');surface.width=image.width;surface.height=image.height;
  const c=surface.getContext('2d',{willReadFrequently:true});c.drawImage(image,0,0);
  const pixels=c.getImageData(0,0,surface.width,surface.height),d=pixels.data;
  // Decode the explicit magenta atlas matte; teal weapon light remains untouched.
  for(let i=0;i<d.length;i+=4){const excess=Math.min(d[i],d[i+2])-d[i+1];if(excess>65&&d[i]>120&&d[i+2]>100)d[i+3]=0;}
  c.putImageData(pixels,0,0);
  const frames=[];
  for(let row=0;row<rows;row++)for(let col=0;col<cols;col++){
   const x0=Math.round(col*image.width/cols),x1=Math.round((col+1)*image.width/cols),y0=Math.round(row*image.height/rows),y1=Math.round((row+1)*image.height/rows);
   let l=x1,r=x0,t=y1,b=y0,bodyBottom=y0;
   for(let y=y0;y<y1;y++)for(let x=x0;x<x1;x++){const i=(y*image.width+x)*4;if(d[i+3]>120){l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y);if(!(d[i+1]>d[i]*1.3&&d[i+2]>d[i]*1.3))bodyBottom=Math.max(bodyBottom,y);}}
   if(r<=l||b<=t)throw Error('Empty animation frame '+name+':'+frames.length);
   // Root follows the central armor, not the long blade extending out of the cell.
   let sum=0,count=0;
   for(let y=Math.round(t+(bodyBottom-t)*.32);y<t+(bodyBottom-t)*.58;y++)for(let x=l;x<=r;x++){const i=(y*image.width+x)*4;if(d[i+3]>180&&!(d[i+1]>d[i]*1.3&&d[i+2]>d[i]*1.3)){sum+=x;count++;}}
   frames.push({x:l,y:t,w:r-l+1,h:b-t+1,rootX:count?sum/count:(l+r)/2,rootY:bodyBottom,bodyHeight:bodyBottom-t});
  }
  // Hand-registered hip roots keep the helmet, body and cannon at a stable scale.
  const registration={run:{scale:.42,roots:[[190,440],[570,440],[953,440],[1335,440],[191,916],[576,916],[957,916],[1335,916]]},jump:{scale:.42,roots:[[184,442],[567,404],[950,400],[1320,357],[183,899],[572,906],[954,929],[1320,909]]},blade:{scale:.50,roots:[[180,342],[504,342],[824,342],[1222,342],[184,680],[537,680],[901,680],[1230,680],[166,1018],[510,1018],[852,1018],[1220,1018]]}}[name];
  frames.forEach((f,i)=>{f.rootX=registration.roots[i][0];f.rootY=registration.roots[i][1];});
  this.atlases[name]={image:surface,frames,scale:registration.scale};
 }
 update(dt,p,speed,keys){if(p.grounded){this.airTime=0;this.stride+=dt*(speed>20?14:keys.left||keys.right?14:0);}else this.airTime+=dt;this.wasGrounded=p.grounded;}
 pose(p,speed,keys){
  if(p.attack&&p.attack.kind!=='down'){
   const a=p.attack,m=BLADE_MOVES[a.kind],sequence=a.kind==='rise'||a.kind==='up'?[4,1,5,6,7]:a.kind==='break'?[8,0,9,10,11]:[0,3,1,2,3];
   const t=a.elapsed/m.duration,index=Math.min(4,Math.floor(t*5));
   return {atlas:'blade',frame:sequence[index],angle:Math.sin(t*Math.PI)*.025};
  }
  if(p.dash>0)return {atlas:'run',frame:3,angle:-.12};
  if(p.attack?.kind==='down')return {atlas:'jump',frame:3,angle:.12};
  if(!p.grounded){const frame=this.airTime<.05?0:p.vy<-500?1:p.vy<-100?2:p.vy<120?3:p.vy<650?4:5;return {atlas:'jump',frame,angle:clamp(p.vy/25000,-.035,.035)};}
  if(p.land>0)return {atlas:'jump',frame:p.land>.055?6:7};
  return {atlas:'run',frame:speed<20&&!keys.left&&!keys.right?0:Math.floor(this.stride)%8};
 }
 drawFrame(ctx,pose,x,y,alpha=1){const a=this.atlases[pose.atlas];if(!a)return;const f=a.frames[pose.frame];ctx.save();ctx.translate(x,y);ctx.rotate(pose.angle||0);ctx.globalAlpha=alpha;ctx.drawImage(a.image,f.x,f.y,f.w,f.h,(f.x-f.rootX)*a.scale,(f.y-f.rootY)*a.scale,f.w*a.scale,f.h*a.scale);ctx.restore();}
 draw(ctx,p,speed,keys,alpha){
  ctx.save();ctx.translate(p.x,p.y);
  const landing=p.land>0?Math.sin(p.land/.1*Math.PI)*.035:0;
  ctx.scale(1+landing,1-landing);this.drawFrame(ctx,this.pose(p,speed,keys),-p.recoil*2,0,alpha);ctx.restore();
 }
}
