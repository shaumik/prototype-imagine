// Each move has a short anticipation, a damaging sweep, and cancellable recovery.
export const BLADE_MOVES = Object.freeze({
  cut:    { name:'CUT',      duration:.21, activeAt:.018, activeUntil:.12, chainAt:.15, damage:4, reach:154, lift:0,   push:190, frames:[4,5,6,7] },
  rise:   { name:'RISE',     duration:.23, activeAt:.018, activeUntil:.14, chainAt:.17, damage:5, reach:166, lift:0,   push:220, frames:[8,9,10,11] },
  break:  { name:'BREAK',    duration:.32, activeAt:.045, activeUntil:.20, chainAt:.24, damage:9, reach:212, lift:0,   push:380, frames:[12,13,13,14] },
  up:     { name:'UPSLASH',  duration:.23, activeAt:.018, activeUntil:.14, chainAt:.17, damage:5, reach:172, lift:-1,  push:100, frames:[8,9,10,11] },
  down:   { name:'POGO',     duration:.34, activeAt:.035, activeUntil:.24, chainAt:.27, damage:5, reach:132, lift:1,   push:75,  frames:[15,15,15,15] }
});

export function attackFrame(attack) {
  const move=BLADE_MOVES[attack.kind], t=attack.elapsed;
  return move.frames[t<move.activeAt?0:t<move.activeAt+.06?1:t<move.activeUntil+.03?2:3];
}

export function attackBox(player, attack) {
  const move=BLADE_MOVES[attack.kind];
  if(attack.kind==='down')return {left:player.x-63,right:player.x+63,top:player.y-12,bottom:player.y+move.reach};
  if(attack.kind==='up')return {left:player.x-62,right:player.x+77,top:player.y-65-move.reach,bottom:player.y-60};
  return {left:player.x-28,right:player.x+move.reach,top:player.y-(attack.kind==='break'?167:145),bottom:player.y-4};
}

export function overlaps(box,x,y,rx,ry) {
  return x+rx>box.left&&x-rx<box.right&&y+ry>box.top&&y-ry<box.bottom;
}
