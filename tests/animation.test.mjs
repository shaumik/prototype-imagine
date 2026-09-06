import test from 'node:test';
import assert from 'node:assert/strict';
import {Animation} from '../dist/animation.js';
import {World} from '../dist/engine.js';
import {BLADE_MOVES} from '../dist/combat.js';
test('unloaded artwork cannot stop the game loop',()=>{const a=new Animation();assert.doesNotThrow(()=>a.drawFrame({}, {atlas:'run',frame:0},0,0));});
test('jump follows ascent, apex, descent and landing while all blade poses exist',()=>{
 const a=new Animation(),p=new World().player,keys={};p.grounded=false;a.airTime=.1;
 const frames=[-800,-300,0,300,800].map(v=>{p.vy=v;return a.pose(p,470,keys).frame;});assert.deepEqual(frames,[1,2,3,4,5]);
 p.grounded=true;p.land=.09;assert.equal(a.pose(p,470,keys).frame,6);
 for(const kind of ['cut','rise','break','up'])for(let elapsed=0;elapsed<BLADE_MOVES[kind].duration;elapsed+=.005){p.attack={kind,elapsed};const pose=a.pose(p,470,keys);assert(pose.frame>=0&&pose.frame<12);}
});
