// Recover soft alpha at a magenta matte edge and remove its color contribution.
// This preserves antialiasing instead of keeping purple pixels around hard cutouts.
export function removeMatte(data,matte=[255,0,255]){
 const [mr,mg,mb]=matte,range=(mr+mb)/2-mg;
 for(let i=0;i<data.length;i+=4){if(data[i+3]===0)continue;
  const r=data[i],g=data[i+1],b=data[i+2],spill=Math.max(0,Math.min(r-g,b-g));
  const a=Math.max(0,Math.min(1,1-spill/Math.max(1,range)));
  if(a<.025){data[i+3]=0;continue;}
  if(spill>1){data[i]=Math.max(0,Math.min(255,(r-(1-a)*mr)/a));data[i+1]=Math.max(0,Math.min(255,(g-(1-a)*mg)/a));data[i+2]=Math.max(0,Math.min(255,(b-(1-a)*mb)/a));data[i+3]=Math.round(data[i+3]*a);}
 }
}
export function extractAtlas(img,count,cols){
 const c=document.createElement('canvas');c.width=img.width;c.height=img.height;const cx=c.getContext('2d',{willReadFrequently:true});cx.drawImage(img,0,0);const source=cx.getImageData(0,0,c.width,c.height),d=source.data,n=c.width*c.height,labels=new Int32Array(n),queue=new Int32Array(n),components=[];
 if(d[3]>240&&Math.min(d[0],d[2])-d[1]>40)removeMatte(d,[d[0],d[1],d[2]]);
 for(let i=0;i<n;i++)if(d[i*4+3]<12)labels[i]=-1;
 let label=0;
 for(let start=0;start<n;start++)if(labels[start]===0){label++;let head=0,tail=1,l=c.width,r=0,t=c.height,b=0;queue[0]=start;labels[start]=label;
  while(head<tail){const i=queue[head++],x=i%c.width,y=Math.floor(i/c.width);l=Math.min(l,x);r=Math.max(r,x);t=Math.min(t,y);b=Math.max(b,y);
   const visit=next=>{if(next>=0&&next<n&&labels[next]===0){labels[next]=label;queue[tail++]=next;}};
   if(x)visit(i-1);if(x<c.width-1)visit(i+1);visit(i-c.width);visit(i+c.width);
  }
  if(tail>700)components.push({label,l,r,t,b,size:tail});
 }
 const chosen=components.sort((a,b)=>b.size-a.size).slice(0,count).sort((a,b)=>(a.t+a.b)-(b.t+b.b)),ordered=[];
 for(let row=0;row<count/cols;row++)ordered.push(...chosen.slice(row*cols,(row+1)*cols).sort((a,b)=>a.l-b.l));
 if(ordered.length!==count)throw Error('Incomplete animation atlas');
 return ordered.map(part=>{const out=document.createElement('canvas');out.width=part.r-part.l+1;out.height=part.b-part.t+1;const ctx=out.getContext('2d'),pixels=ctx.createImageData(out.width,out.height);
  for(let y=0;y<out.height;y++)for(let x=0;x<out.width;x++){const from=(y+part.t)*c.width+x+part.l,to=(y*out.width+x)*4;if(labels[from]===part.label)for(let k=0;k<4;k++)pixels.data[to+k]=d[from*4+k];}
  ctx.putImageData(pixels,0,0);return {image:out,...part};});
}
