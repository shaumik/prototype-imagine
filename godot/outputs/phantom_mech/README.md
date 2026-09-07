# PHANTOM — Mecha unit N-07

A detailed, editable Blender interpretation of the supplied front / side / rear character sheet.

Open **Phantom_Mecha.blend** in Blender. The scene contains separate armor and mechanical components, named collections, procedural metal and ceramic materials, the packed original reference, five cameras, and a lit studio stage. It opens on the hero camera. Use the middle mouse button to orbit, or the camera list to inspect the front, rear, side, and helmet views.

## Rendered views

- `phantom_hero.png` — 2000 × 2250 studio portrait.
- `phantom_rear.png` — 1600 × 1800 rear three-quarter view, showing backpack and thrusters.
- `phantom_detail.png` — 1800 × 1600 helmet, chest, and shoulder detail.
- `phantom_front.png` — 1600 × 1800 frontal view.

## Model details

Layered teal ceramic armor, gold trim, machined bevels, dark titanium framing, emerald chest core, amber eyes, helmet antennae, shoulder fins, twin cannons, left-hand rifle, energized right-arm blade, rear thrusters, cooling grilles, fasteners, engraved seams, hydraulic rods, bearing rings, and separately modeled finger segments.

This is a hard-surface artistic reconstruction. The reference is a stylized drawing with differing cannon orientation between views; the model prioritizes its frontal silhouette and interprets hidden geometry. It is not an exact recovered mesh. The model is not rigged, UV-unwrapped, optimized for a game, or prepared for 3D printing. Materials use procedural shading; the source image is packed into the Blender file for reference.

## Rebuild and render

`build_phantom.py` creates the scene in Blender's Python environment. `render_phantom.py` renders the saved scene with Cycles and the Mac's Metal GPU. Both scripts save outputs beside themselves. No external add-ons or texture downloads are required.

Created in Blender 5.2.1 LTS using the user-supplied image `Gemini_Generated_Image_8j46k08j46k08j46.jpg`.
