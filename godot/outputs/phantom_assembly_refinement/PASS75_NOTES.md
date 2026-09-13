# Pass75 — exposed shoulder returns, September 12 PDT / September 13 UTC

The model remains unfinished. This pass changes two shoulder material assignments, isolates their original fill, and adds a weaker fill restricted to those two objects. It does not change geometry, the approved torso/helmet, cannon construction, or backpack construction. The user correctly called out that the model still does not resemble the useful generated reference shapes: this material/light correction does not address the larger silhouette discrepancy. Prioritize concrete shoulder geometry next.

## Start and preservation

The local editable, matching recovery checkpoint and both published canonical paths were checked at SHA256 `00aac2039a65410a373e7b313f75c1f49a96685f086eadb7ccda5809d75798ee`. GitHub main was independently verified at `3c85a551911d47acaee6ecba24f2f83754a8425e`. The untouched model was copied to `checkpoints/Phantom_PrePass75_20260913.blend` before editing. The local root `outputs/Phantom_Reference_Manual.blend` remains the approved torso file, SHA256 `2da7a2e05bd5afdfa585c5f5299be445180f3a5d24bfc2d94787de2319d37f89`.

Blender main-window pointer control repeatedly failed with `windowNotFoundAtPosition` and `noWindowsAvailable`, despite keyboard responses and readable screenshots. Reacquisition, connection reset, window raise, zoom, fill, half-screen placement, fullscreen and normal-window restoration were tried. A separate `Phantom_Control_Troubleshooting_20260913.blend` preserved the intervening UI state. Automatic review rejected an initial Revert attempt because of unsaved state; it was not performed. After the separate save was verified, the untouched pre-pass file was opened through the file dialog, safely restoring the starting scene. No troubleshooting geometry is used in the refinement.

Reliable workaround: use the secondary Image Editor window as the working editor. Click inside it, then Shift-F5 for 3D Viewport, Shift-F9 for Outliner, and Shift-F7 for Properties. The main window can remain open. An actual render resets this secondary window to Image Editor. Click inside the image before editor shortcuts. File dialogs can still have stale bounds: reacquire Blender, use the dialog AX zoom button when needed, click the filename separately and verify the caret before typing. Verify the saved file before replacing RenderResult.

## Cannon inspection and regenerated baseline evidence

New actual front and hero renders of the retained recovery model are saved as `renders/Phantom_Assemblies_Front_PrePass75.png` and `renders/Phantom_Assemblies_Hero_PrePass75.png`. Both are 2000 × 1600, Cycles 128 samples. The front took 1m14.09s; the hero took 1m54.27s. Both files were exported, inspected and checked for dimensions. These replace historical Pass29 images as current baseline evidence.

The front shows matched cannon orientation and four open round bores per muzzle. The hero and recovered side show retained layered inner/outer service cassettes and attached pivots. No demonstrated cannon defect was rebuilt during this pass. Exhaustive close-up backing-clearance and underside checks remain part of continued verification; do not claim the new two views alone prove every concealed connection.

## Direct diagnosis and retained correction

From the actual rear camera, selecting the bright upper tip identified `85 Teal - swept shoulder top panels`; selecting the adjacent exposed vertical end identified `06 Graphite - shoulder armor foundations`. Rendered viewport selection confirmed both identities.

Studio Rim's existing receiver list was inspected. Both object06 and object85 were already excluded, alongside the established cannon and shoulder exclusions. Those links were preserved.

Object85 had one shared material slot, `Teal - ceramic metal armor`, originally with 23 users: base color #365D66, metallic .42, roughness .46, coat weight 0. A single-user copy named `Teal - shoulder exposed returns` was made through the UI, with base color #2D4D58, metallic .42, roughness .62, coat weight 0, retaining the existing bump connection. Object85 uses this copy. Only the third, teal slot on mixed-material object06 was changed to that same copy; its graphite and gold slots remain intact. The new material has two users.

The material-only TrialA was saved and rendered, and FAILED to remove the washed-out tip. Its checkpoint `Phantom_Shoulders_Pass75_TrialA.blend` and actual `Phantom_Shoulders_Rear_Pass75_TrialA.png` are preserved as a rejected incomplete correction. Do not present it as a successful fix.

Studio Fill was identified at location (8,-6,9), rotation (55,50,0), scale (5,5,5), normalized area power 1500, exposure 0, square size 1. Temporarily setting its power to 0 in the rendered viewport removed the white tip, establishing its contribution. Power was immediately restored to 1500 and verified in the light data panel. A new `Light Linking for Studio Fill` receiver collection contains exactly object06 and object85, both EXCLUDED. Other scene objects retain the original fill. No light transform, global intensity or Studio Rim change is retained.

TrialB rear (2000 × 1600, Cycles128, 1m09.57s) removed the white upper and vertical end faces. However, the actual Side TrialB (2000 × 1600, Cycles128, 1m11.77s) made the outer recess too dark. Both are preserved with TrialB filenames and the TrialB checkpoint. This was an incomplete correction.

A duplicate fill named `Shoulder Fill - exposed returns`, with independent light data `Area.008`, retains the original fill transform, white color, square size1 and normalization, but has power350. Its independent receiver collection `Shoulder exposed return receivers` contains exactly object06 and object85, both INCLUDED. The original Studio Fill remains power1500 with those same two objects EXCLUDED. The new light and both inclusion checkboxes were explicitly verified in Properties.

Final actual side (2m59.10s) and rear (2m38.14s) were exported, dimensions checked at2000 ×1600 and visually inspected. Side restores recess readability; rear has reduced tip washout but a lighter end face remains, so this is not a complete color or shape match. No further lighting iteration is justified before addressing the larger geometry discrepancy. Side SHA256 `219733e591a278a61bf6f9fa3d0071949078832c4c3add090409ce194643c241`; rear `e54ab3e1e461e8d1f7d918ee381779217d9c53c7c270f0717765a990ea2fe73f`.

Saved versioned model and current canonical SHA256 `12f24dbbdf6b5c69eb08d2485e04b64f4ea7cb1c2224f44657fc3de464f0850c`. Rear verification camera is active. No geometry was changed in75. This checkpoint preserves a partial material/light correction and current evidence before the substantial geometry work requested by the user.

## Remaining work

LATEST USER STEERING: The user explicitly asked to make the actual model look exactly like the generated images and expressed frustration at the lack of shape progress. Use generated Study17 as the direct shoulder form target, preserving the approved torso and helmet. Prioritize visible geometric convergence: tapered shell, thin brass band, layered root armor and shaped underside. Earlier caution about preserving every existing shoulder contour must not be used to avoid the substantial reshaping the user now requests. Still resolve physical connections in actual geometry and show actual renders beside the study.

The shoulder roof is still too broad in depth, the front/rear brass fascia have thick side edges, and underside construction is plain. A coherent depth taper must affect the roof, fascia, foundation, covers and fasteners together so the clearances and attachments are preserved. Do not simply shrink loose panels and leave fasteners behind. Follow the latest direct generated-reference target above. Inspect return overlaps obliquely and the guard mounting tabs from a genuinely inner-facing angle.

The backpack remains pale and bulky; exhaust exterior faceting and the two unidentified exhaust-adjacent discs remain pending. Work remains in the requested assembly order. No AAA or finished claim is justified.

Generated studies 15–17 are stored separately in `supplementary_references`. Their useful construction ideas and rejected design drift are documented in `Study15_16_NOTES.md` and `Study17_NOTES.md`. They are not model renders.
