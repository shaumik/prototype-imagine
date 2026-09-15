# Pass81 — backpack lighting correction

Started only after Pass80 was published at `0cfc4424b5fa50bfab28cab01f434bc272539d33`, remote main matched, and both canonical models, three actual80 renders and generated Study21 were downloaded from the immutable commit to `/private/tmp/phantom-verify-0cfc442`. Every SHA256 matched. Git clean. Both80 canonicals/model hash `63313bba33d3bc5009ecb32df9470eb31923726d1a12c7add7f85d6121f07fb9`.

Saved new `checkpoints/Phantom_Backpack_Pass81_Surface_Transitions.blend` through Blender UI before editing. Preserve80 and local approved root torso. Current close camera is `Verification - Backpack Close Rear Pass80`. Actual80 close image safely exported. Next: identify and smooth the faceted rear support shaft, diagnose pale backpack highlights with an isolated light contribution check, then refine demonstrated housing transition shortcomings. Use original guide as authority; supplementary Study21 critique in PASS80_NOTES. All Blender edits through UI only.

## Discarded support shading experiments

Picked the faceted shaft: `54 Steel - cannon trunnion mounts`, meshCylinder.005, including fixed uprights and paired upper/lower bearings. Whole-object AutoSmooth30 did not remove barrel bands. Whole-object ShadeSmooth softened machined faces and exposed longitudinal shading artifacts. Inspected existing SmoothByAngle30 modifier, tried IgnoreSharpness, tiny merge-by-distance .0001, outside-normal recalculation and ResetVectors; none established a clean result. Fully reverted through UI to saved81 baseline; no part of that trial retained.

Second trial selected equal-area lower barrel wall faces in rear orthographic EditFace wireframe. Hiding linked barrel components verified no additional loose cylinders inside; separate bearing-face discs and uprights remain. Attempted explicit face shading with flat caps and smooth walls, clearing sharp edges and removing the inherited SmoothByAngle modifier. During reselection, a dropped search shortcut interpreted text as viewport commands and distorted lower shaft vertices. Caught visually before saving, then fully reverted through UI to saved81 baseline again. **No support geometry, normal, modifier or shading changes from either trial are retained.** Initial81 baseline file SHA256 `b5bad04c8751680f8f17fd37ae7f9b736b441090664f703b77f5d1b62e91a74d`.

Next diagnose backpack highlight first; return to54 with search and text entry in separate verified calls. F3 history exposes native `Link Receivers to Emitter > Exclude` for lighting workflow. Avoid interpreting unsuccessful shading attempts as completed work.

## Retained backpack lighting correction

Temporary Studio Rim power0 diagnostic in rendered viewport established that its3000 power dominated the pale backpack highlights. Restored the original light to3000. Through native Link Receivers to Emitter > Exclude, appended exactly nine backpack mesh objects to its existing exclusion collection:53,56,57,84Steel,87,88,89,90,91. Existing cannon and shoulder exclusions remain. Excluded entries were inspected unchecked in Object Properties.

Duplicated ONLY Studio Rim through UI to `Backpack Rim - balanced Pass81`, independent light data `Area.009`. Kept location(2.4,4,9.6), Euler(-35,20,0), scale(4,4,4), white Area Square size1, Normalize on, Exposure0, Spread180, node Strength1. Set power750. Unlinked its inherited shared receiver collection on the duplicate only. Native Include created a new independent `Light Linking for Backpack Rim - balanced Pass81` containing ONLY the nine objects above; all nine verified checked together in the enlarged list. The shared58 cyan indicators and approved torso/helmet are not included.

Rendered viewport shows darker teal, brass and clearer exhaust separation. No geometry or material changes are retained in81. Saved through UI before full-resolution close-rear render. Saved trial SHA256 `030d2f066487855311e978cb7c181e85c3ee3e2b828e4a62ec16e3122ed3c182`. Full-resolution multiview exports and publication pending. Core roof transitions and54 support faceting remain unresolved.

## Actual render verification

- `Phantom_Backpack_Close_Rear_Pass81.png`:2000×1600, Cycles128,2m13.04s. SHA256 `32f7d1876703e747a70d15d34b45dcd04201c1e2bfb92fb78c9a83216a9154e1`. Exported to the correct render folder, dimensions checked and actual PNG opened before replacing RenderResult. Darker teal and brass read clearly, with round open exhausts and real grille spacing. The central surround remains overly rectangular and the54 barrels remain faceted; these are not lighting fixes.
- `Phantom_Backpack_Side_Pass81.png`:2000×1600, Cycles128,1m20.83s. SHA256 `56ee235504e1924db86e5e63fb2403162fbea467cd8b85f907c43c366a6f295a`. Correct path, dimensions and actual pixels checked. The previously pale pod side face is now dark teal with its physical recess legible. Long outer side surface and plain central core transitions remain simplified. Approved torso, helmet, arms, shoulders and cannon materials were not edited.

Rear assembly81 render started after selecting the exact existing `Verification - Rear Assemblies` camera and saving. No geometry changes between these views. Export and publication pending.

Rear81 completed1m31.35s, exported correctly as `Phantom_Backpack_Rear_Pass81.png`; actual file opened and verified2000×1600. SHA256 `8993c61b707705f392b43585c9eb9544847dfe48aa0443d32d17e719540a43d6`. Both pod highlights are controlled, brass remains legible, exhausts are open and the original-guide traced shoulder symmetry is retained. The core is still too rectangular behind the octagonal surround. No final/exact-quality claim.

Final81 saved model hash `d524b809096c597ee511fb72572c917081d7b7b1cec55b42ee9a7604acaaf5ba`, active existing Rear Assemblies camera. Versioned81, local assembly canonical and both Git canonicals match. Local approved root torso remains `2da7a2e05bd5afdfa585c5f5299be445180f3a5d24bfc2d94787de2319d37f89`. Despite the initial filename Surface_Transitions, retained81 is a lighting correction only; all support shading trials were discarded. No geometry or material changes.

Publication includes three actual renders and restart docs. Verify remote main and immutable downloads of both canonicals and all three PNGs before substantial82 geometry. Next refine the central graphite upper/side surround against the original rear/side overlays and accepted Study21 forms; correct54 faceting and perform concealed inner cannon/pivot/backing and combined-fit checks.
