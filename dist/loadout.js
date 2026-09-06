export const CHASSIS={phantom:{name:'Phantom',hp:6,description:'Light runner · 6 armor · fast dash'}};
export const EQUIPMENT={
 primary:[{id:'pulse',name:'Pulse buster',desc:'Fast, precise energy bolts.'},{id:'spread',name:'Tri-shot',desc:'Three bolts cover a wider angle.'},{id:'rail',name:'Rail driver',desc:'Slower shots pierce three targets.'}],
 blade:[{id:'standard',name:'Cyber blade',desc:'Balanced three-hit combo.'},{id:'arc',name:'Arc saber',desc:'Longer reach and +1 damage.'},{id:'breaker',name:'Breaker edge',desc:'+3 damage on every blade hit.'},{id:'siphon',name:'Siphon blade',desc:'Every fourth defeat repairs 1 armor.'}],
 shoulder:[{id:'none',name:'Empty mount',desc:'No auxiliary weapon.'},{id:'cannon',name:'Shoulder cannon',desc:'Auto-aimed heavy shot every 2.4s.'},{id:'missiles',name:'Homing pod',desc:'Two guided rockets every 3s.'},{id:'drone',name:'Wing drone',desc:'A companion fires every 0.9s.'}],
 core:[{id:'stock',name:'Balanced core',desc:'Standard armor and dash recharge.'},{id:'boost',name:'Boost pack',desc:'Dash recharges in 0.30s.'},{id:'aegis',name:'Aegis emitter',desc:'Blocks one hit; recharges in 10s.'},{id:'magnet',name:'Salvage magnet',desc:'Draws nearby pickups toward you.'}]
};
export const DEFAULT_LOADOUT={primary:'pulse',blade:'standard',shoulder:'none',core:'stock'};
export function equipmentFor(){return EQUIPMENT;}
export function normalizeLoadout(value={}){return Object.fromEntries(Object.entries(EQUIPMENT).map(([slot,items])=>[slot,items.some(x=>x.id===value[slot])?value[slot]:DEFAULT_LOADOUT[slot]]));}
export const PICKUPS=[
 {id:'repair',name:'REPAIR',short:'+',color:'#b9ffd0',desc:'Restore 2 armor'},
 {id:'rapid',name:'RAPID FIRE',short:'RF',color:'#ffeaa3',desc:'Faster fire · 12s'},
 {id:'shield',name:'BARRIER',short:'SH',color:'#8edfff',desc:'Absorb 3 hits'},
 {id:'overdrive',name:'OVERDRIVE',short:'OD',color:'#ffaed2',desc:'Double weapon damage · 10s'},
 {id:'pierce',name:'PIERCING',short:'PX',color:'#d2bcff',desc:'Shots pierce enemies · 12s'},
 {id:'magnet',name:'MAGNET',short:'MG',color:'#aaffe6',desc:'Pull pickups toward you · 15s'},
 {id:'storm',name:'STORM HALO',short:'SH',color:'#d2bcff',desc:'Orbiting blades · until pit stop'},
 {id:'wings',name:'PHANTOM WINGS',short:'PW',color:'#9eefff',desc:'Triple jump · until pit stop'},
 {id:'nova',name:'NOVA',short:'N',color:'#fff2d1',desc:'Clear bullets and nearby enemies'}
];
export const STAGES=[{name:'The Long Way Home',boss:'Signal Warden',duration:60},{name:'Harbor Afterglow',boss:'Harbor Sentinel',duration:64}];
