# PHANTOM — revised 3D reconstruction

Open `Phantom_Mecha_v2.blend` in Blender. The original version remains in the neighboring `phantom_mech` folder.

This revision follows the supplied rendered character sheet and the requested equipment changes:

- One blade mounted to each wrist; no handheld rifle.
- Two articulated cannons extending forward over the shoulders.
- A compact chest, higher waist, longer legs, and fuller thigh and calf armor.
- Shaped armor with compound curvature, rolled edges, and angular surface panels.
- A rebuilt helmet with narrow recessed eyes, a smaller jaw and chin, cheek vents, and fine antennae.
- Muted teal, bronze, and gunmetal materials with more restrained highlights.

## Images

- `phantom_v2_hero.png` — final 1600 × 2000 studio render.
- `phantom_v2_face.png` — final 1000 × 1000 helmet detail.
- `preview_front.png` — lower-resolution front view for inspecting proportions.

The Blender scene has separately editable components, organized collections, four cameras, and a packed reference image. It is an artistic reconstruction from a 2D reference, not a recovered original mesh. It is not rigged for animation or prepared for 3D printing.

`build_phantom_v2.py` and `modeling.py` reproduce the model in Blender; `render_final.py` renders the final images. Keep these scripts and `reference.jpg` in the same directory. No add-ons or external texture downloads are needed. Created with Blender 5.2.1 LTS.
