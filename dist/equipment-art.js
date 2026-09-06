import {extractAtlas} from './atlas.js';
export class EquipmentArt{
 load(modules){this.modules=extractAtlas(modules,6,3);}
 module(ctx,index,x,y,width,alpha=1){if(!this.modules)return;const img=this.modules[index].image,height=img.height/img.width*width;ctx.save();ctx.globalAlpha=alpha;ctx.drawImage(img,x,y,width,height);ctx.restore();}
 draw(ctx,p,stride,loadout,time=0,alpha=1){
  if(loadout.core==='boost')this.module(ctx,4,p.x-53,p.y-112,45,alpha);

  if(loadout.primary==='rail')this.module(ctx,0,p.x+16,p.y-107,58,alpha);
  if(loadout.primary==='spread')this.module(ctx,1,p.x+36,p.y-108,40,alpha);
  if(loadout.blade!=='standard'&&!p.attack){ctx.save();ctx.translate(p.x-43,p.y-79);ctx.rotate(2.35);if(loadout.blade==='breaker')ctx.filter='hue-rotate(180deg)';if(loadout.blade==='siphon')ctx.filter='hue-rotate(100deg)';this.module(ctx,5,-8,-10,loadout.blade==='arc'?100:82,alpha);ctx.restore();}
  if(loadout.shoulder==='cannon')this.module(ctx,0,p.x-17,p.y-144,100,alpha);
  if(loadout.shoulder==='missiles')this.module(ctx,1,p.x-24,p.y-140,66,alpha);
  if(loadout.shoulder==='drone')this.module(ctx,2,p.x-65,p.y-190+Math.sin(time*4)*7,54,alpha);
  if(loadout.core==='aegis')this.module(ctx,3,p.x+20,p.y-112,48,alpha*.8);
 }
}
