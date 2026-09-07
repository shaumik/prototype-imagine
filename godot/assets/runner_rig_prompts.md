# Continuous runner artwork

Generated with the built-in image-generation tool. Final project asset: `assets/runner_rig.png`.

## Character parts

Use case: stylized-concept.
Asset type: production modular 2D character sprite atlas for a fast side-scrolling action platformer. Twelve SEPARATE armor/body parts, not animation frames, not full characters. These parts will be attached to a continuously animated skeleton in Godot.
Character design: original sleek futuristic cyber runner with athletic adult proportions, cool dark navy undersuit, deep cobalt blue and ivory armor panels, narrow luminous cyan visor and restrained mint energy details, small orange scarf. Sharp elegant silhouette, angular helmet with one swept-back fin, tapered armor, compact powerful cannon. Premium crisp CEL-SHADED ANIME game artwork: razor-clean dark outlines, 2-3 flat hard-edged tonal regions per surface. NO painterly brush strokes, soft rendering, realistic textures, pixel art, blocky pixels, chibi proportions, oversized round toy boots.
Canvas: landscape 1536x1152, EXACT uniform FOUR COLUMNS and THREE ROWS, twelve 384x384 square cells. Each item alone and centered in its cell, completely isolated with at least 30px clean margin, no overlaps. All parts show the SAME SIDE PROFILE of a character facing RIGHT. Orthographic side elevation, no perspective foreshortening. The parts are intentionally separate game assets; no human injury or anatomy.
Background: perfectly flat uniform pure MAGENTA #FF00FF everywhere including openings. No background scene, shadows, labels, text, numbers, visible grid or borders.
Cell contents, reading left-to-right:
ROW 1:
1. Helmeted HEAD ONLY, right-facing profile with slim glowing cyan visor, armored jaw, sharp swept-back fin. Neck connection at bottom. No torso or shoulders.
2. TORSO ONLY, upright right-facing side profile, shoulder/chest at TOP, waist at BOTTOM. Narrow navy abdomen, cobalt chest with a crisp ivory chest plate and restrained teal reactor detail. No head, arms, shoulders, scarf, pelvis or legs. Fully draw the hidden side of torso so attached arms may rotate freely.
3. PELVIS / HIP ARMOR ONLY, upright right-facing profile, slim articulated waist belt at TOP, hip pivots near BOTTOM, angular ivory/cobalt overlapping armor. No abdomen or legs.
4. Integrated FOREARM CANNON ONLY, horizontally aimed RIGHT, elbow connection at LEFT, muzzle at RIGHT. Beautiful compact tapered cobalt/ivory shell, black muzzle opening with cyan inner rim. No hand, arm or body.
ROW 2:
5. THIGH armor segment ONLY, hanging vertically DOWN: hip pivot at TOP, knee pivot at BOTTOM. Long slim angular cobalt shell over navy joint, right-profile, fully isolated and straight. No shin or hip.
6. SHIN armor segment ONLY, hanging vertically DOWN: round articulated knee connection at TOP, ankle connection at BOTTOM. Long sleek cobalt/ivory shin guard, right-profile, taper to ankle. No thigh, foot or boot.
7. FOOT / BOOT ONLY, horizontal sole with toe pointing RIGHT, ankle socket above the rear third. Compact angular boot, navy sole, cobalt body, ivory toe cap, small cyan ankle detail. No shin, no knee. Avoid huge chunky shoes.
8. SHOULDER armor cap ONLY, compact angular cobalt/ivory pad around dark mechanical ball pivot, side profile. No torso or arm.
ROW 3:
9. UPPER ARM segment ONLY, straight vertically DOWN, shoulder connection at TOP, elbow connection at BOTTOM. Slim dark articulated undersuit with cobalt plate, no shoulder cap, no forearm.
10. Sword-side FOREARM AND CLOSED GLOVED FIST as one piece, straight vertically DOWN, elbow at TOP, gripping fist at BOTTOM. Slim ivory/cobalt wrist guard and dark navy glove. No upper arm, no sword attached.
11. CYBER SABER only, oriented horizontally RIGHT, compact dark hilt and guard at LEFT, long narrow mint/cyan-white energy blade extending RIGHT to a sharp point. Clean solid hard-edged light blade, no big soft glow.
12. ORANGE SCARF TAIL only, knot attachment at RIGHT edge, a narrow long forked cloth tail streams horizontally LEFT with a subtle flowing S curve. Flat orange/coral cel shading, no body or neck.
Maintain the same drawing style, outlines, lighting and armor design across every component. Components should each occupy most of their own cell; the engine sets their final relative sizes. Draw complete part silhouettes with overlapping connection caps so joints can rotate without gaps. This is a clean technically usable layered-animation asset sheet, not a concept-art poster.

## Background extraction

Use case: background-extraction. Edit this EXACT modular armor part sheet. Replace the ENTIRE dark navy/gray backdrop and ALL colored ambient haze and glow outside the twelve physical component silhouettes with perfectly UNIFORM FLAT PURE MAGENTA #FF00FF (RGB 255,0,255). This must be a flat chroma-key color, absolutely no gradients or glow outside the silhouettes. Preserve EVERY existing component, its drawing, detailed armor design, outlines, internal colors, sharp edges, scale, exact positions, image dimensions and layout UNCHANGED. Keep the head, torso, pelvis, cannon, thigh, shin, boot, shoulder, upper arm, forearm/fist, sword and scarf exactly as they are. Background gaps and all empty space become identical #FF00FF. The sword blade remains sharp cyan-white, with no external diffuse green glow. Scarf outline stays crisp, no orange halo. Do not add text or grid lines. Do not repaint or redraw any of the components. This is a technical background replacement to make these sprites usable in a game.

Source generation: exec-d773bfe5-43a8-4881-a65a-eadfb9d2d706.png. Final source: exec-9d85d5cc-121c-4ffb-9aa3-a838e73587af.png.

