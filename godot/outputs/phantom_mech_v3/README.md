# PHANTOM — mechanical detail revision

Open **Phantom_Mecha_v3.blend** in Blender. The scene includes the body from revision 2 and newly built hands, wrist blades, shoulder cannons, and helmet.

## Revised assemblies

- **Hands:** broad armored palms, separate fingers and opposed thumbs, three links per finger, exposed pivot bearings, overlapping plates, wrist cuffs, optical sensors, and hydraulic hoses.
- **Wrist blades:** paired deployment carriages, guide rods, mounting saddles, curved forged blade geometry, cutting bevels, and recessed longitudinal channels. The blades are mounted outside the hands.
- **Cannons:** stepped angular receivers, recoil supports, railed barrel shrouds, gas return tubes, and ported muzzle brakes with open recessed bores.
- **Face:** a central blue optical lens, thick teal sensor fins, amber sensors, bent bronze antennae, recessed eyes, a broad vented titanium mask, and layered cheek and jaw armor following the supplied close-up.

## Renders

- `phantom_v3_hero.png` — 1600 × 2000 full-body view.
- `phantom_v3_face.png` — 1100 × 1100 face detail.
- `phantom_v3_hand.png` — 1100 × 1100 hand and wrist mount detail.
- `phantom_v3_cannon.png` — 1100 × 800 shoulder weapon detail.
- `phantom_v3_blade.png` — 1100 × 1400 wrist blade and deployment mount detail.

All design references are packed into the editable Blender scene. Components are separately named and organized into collections. This remains an artistic reconstruction from the supplied images, not the original mesh used to create them. It is not rigged or prepared for fabrication.

`base_body.blend`, `mechanical.py`, and `refine_phantom.py` can reproduce the revision: open the base scene in Blender and run the refinement script. `render_final.py` produces the final images. Keep the scripts and reference images together. Created using Blender 5.2.1 LTS.
