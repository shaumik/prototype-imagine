# Pass76 — tapered shoulder shell, September13 UTC

Geometry checkpoint saved and verified in hero and side renders; further refinement remains required. All scene actions use Blender's interface through CUA. No scripts, Python, or scripted geometry were used. User's latest direction is direct visual convergence on generated Study17. Preserve approved torso and helmet. Pass75 was published and remotely verified before this geometry work.

## Prior checkpoint remote verification

GitHub main was verified at `4e0e76838d1c92d928938f3e653fb8b90b4f3bc4`. Both canonical blends and final75 rear/side PNGs were downloaded from that immutable commit into `/private/tmp/phantom-verify-4e0e768`. Both blend hashes matched `12f24dbbdf6b5c69eb08d2485e04b64f4ea7cb1c2224f44657fc3de464f0850c`; side219733e5… and reare54ab3e1… matched the local files exactly.

## Geometry changes made and saved

Saved separate working file `checkpoints/Phantom_Shoulders_Pass76_Tapered_Shell.blend` through SaveAs before editing. Pass75 and current canonical remain preserved until Pass76 is verified and published.

Created UI lattice `Shoulder Depth Cage Pass76`, location(-.14,.065,7.8), scale(6.4,2,2), rotation0. Lattice resolution U6,V2,W2, all three interpolation modes Linear. While lattice remained active, selected numbered meshes with pattern `?? *shoulder*`, then Parent > Lattice Deform. Outliner hierarchy confirms the fascia objects under this cage; verify the full receiver/modifier list when inspecting remaining pieces.

In lattice EditMode top view, selected both outermost X control columns. Verified local median(0,0,0), including both Z levels. Scaled only Y by.45 around the median. Other columns remained unchanged. Global X control positions are -3.34,-2.06,-.78,.50,1.78,3.06. This narrows each outer wing progressively beyond the inner control at worldX1.78 and its mirror; preserves root dimensions. Top-view actual geometry visibly changed from almost rectangular footprints to tapered wings. Oblique solid view shows shared taper through roof, face, cover and fastener layers. The cage remains editable and is not rendered.

Front fascia `46 Gold - shoulder sweep borders`: isolated, verified active mesh, vertex Xray, right orthographic. Selected only the back-side vertex groups including their bevel vertices. Global selection median before(-.14,-.32248,7.6501). Moved GY-.18, verified medianY-.50248. Outer face and recess geometry remain at original front positions. Approximate gross depth reduces from.279 to.099 before lattice deformation. No global scale of the whole fascia or its front detailing was used.

Rear fascia `46 Gold - shoulder sweep borders.001`: isolated, verified active mesh, vertex Xray, right orthographic. Selected inner-side vertex groups including bevel vertices. Global selection median before(-.14,.55096,7.6501). Moved GY+.10; verified medianY.65096. Approximate gross depth reduces from.18 to.08 before lattice deformation. Outer face and fastener positions remain unchanged.

Returned ObjectMode, XrayOFF, localviewOFF. Exact camera identities were verified in Outliner before activation. Actual hero76 completed2m11.96s and side76 completed1m11.46s; both exported, dimension-checked2000x1600 and visually inspected. Both128Cycles. Side camera active in saved model. Model SHA256 `0cc2901e106015c2ef1b68e0bbf5aef9b0d52a320f4d4418b026db52f0357453`.

Hero image SHA256 `b5bf59f0e5c78285055f488c62a1c712a770642e4f62a60a17570761db9703ef`; side `da6e835206f809975b2826912d75c34ab59483ef009ce513ddc27eab72fe4895`.

Actual comparison: depth taper and thinner fascia are clearly visible in both views, with closed outer end and fasteners retained on the sloping fascia. Root dimensions and approved body remain preserved. Major remaining mismatch: upper armor still reads as a flat lid over vertical face panels and boxy root covers. It needs a chamfered/sloped continuous upper profile and shaped root cap, then underside connection refinement. End recess and lower support structures remain visually crude. The checkpoint is an incremental geometry improvement, not completion.

## Required next checks and further work

Continue close inspection of outer return overlaps, normals and fastener seating. The thinner fascia spans95's end-cover boundaries in original Y space, and the two renders show retained closure; closer underside/rear verification is still necessary. Check full cage child/modifier list. Root shell and underside need substantial reshaping toward the generated reference. Backpack and concealed cannon/mount checks remain pending.

Generated Study18 was added using the original guide and Study17 as inputs. Its useful chamfer/underside details and misleading OUTER END label are critiqued in `supplementary_references/Study18_NOTES.md`. It is not model evidence.

CUA: when the window loses focus, AX Raise on the fresh window index restores keyboard action without deselecting vertices. A middle click can rotate the viewport; reset exact orthographic view before box selection. Do not assume a command applied if the screenshot remains unchanged.
