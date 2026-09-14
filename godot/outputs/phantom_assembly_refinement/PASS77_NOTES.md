# Pass77 — continuous shoulder shells

Latest saved checkpoint: `Phantom_Shoulders_Pass77_Continuous_Armor.blend`, SHA256 `ddf3ba4b4c2fe34225f5aeebe26a173096a1008d045b68ad92f8731048f2008f`. Current canonical copies match this file. The pass is verified by actual hero and side renders; the overall refinement remains unfinished. The sections below preserve the trial and correction history.

All Blender geometry, camera actions, and rendering used CUA through the Blender interface. No Blender scripts or Python were used.

## Lock interruption recovered

User unlocked the Mac. Cancelled the visible Save Changes Before Closing dialog; did not quit or discard changes. Saved the live scene separately through Save As to `checkpoints/Phantom_Pass77_Live_Interrupted_20260913.blend`, SHA256 `75168e0e813825fc65db282713ac927ff3d08f12cff1668edbb0dd5f6478bf3b`. This preserves the new wing and unfinished root cube. Older interrupted autosave and notes remain separately preserved. Prior GitHub main backup `2a606eee663cb31a5b3240bf63c86211ad563d60` was verified by remote ref and downloading/hash-checking both autosave and notes.

## Geometry retained so far

The exact earlier wing construction is documented in `interrupted_pass77_20260913/INTERRUPTED_PASS77_NOTES.md`. Object85 is now `85 Teal - continuous shoulder wing shells`: a closed extruded, sloped, chamfered shell, retaining Mirror, Pass76 lattice, material and lighting links. The old45 outer front/rear panels had already been removed before the interruption.

Rebuilt93 `93 Teal - chamfered shoulder root shells` from the verified default cube. Applied mesh SX.36, SY.635, SZ.275, GX1.435, GY.065, GZ7.99; all-vertex global median verified(1.435,.065,7.99). Selected upper four vertices in front orthographic Xray; median verified(1.435,.065,8.265). SY.78, SX.82. Detected that pivot was still 3D Cursor, causing an unwanted upper-center shift. Explicitly changed pivot to Median Point and corrected selected upper vertices GX+.2583, GY+.0143, restoring upper center(1.435,.065). Lower outer pair was positively verified at(1.795,.065,7.715), then GX-.055. Recalculated outside normals, beveled all edges.04,1segment,profile.5,LoopSlideON,ClampOverlapOFF, verified in F9. Final pre-bevel all-vertex median(1.4213,.065,7.99). The cap has a narrower top and controlled chamfers.

Selected protruding old cladding by picking actual visible surfaces:45front root plate and94inner return. Hid45front/rear temporarily for comparison, then removed94 and both45 objects after confirming93 provides the replacement closed shell. Deleted45front/rear individually from the filtered Outliner; the45 search is now empty. These objects remain recoverable in Pass76 and the live interrupted copy. Guards83, fins84, brass46/46.001, return covers95 and fasteners86/96 retained.

An exposed tiny rectangle in the outer tip was positively identified as06foundation, protruding through85. Isolated06, front orthographic vertex Xray, selected full outer-end vertex group, global median verified(2.9763,.11081,8.2285). Issued GX-.06 before exiting EditMode. Exact resulting coordinate and cover fit still need separate verification; do not assume the render alone proves the intended displacement.

## Current save and validation

Saved through UI to `checkpoints/Phantom_Shoulders_Pass77_Continuous_Armor.blend`, SHA256 `760f31040e96d63630f493601dd9c767d53c1d9822efd0474f9fccbcf0c701f0`. Hero camera selected and verified before Ctrl+KP0. Actual Hero77 rendering at2000x1600/128Cycles; export pending when this note was created. Canonical paths still point to verified76 until77 evidence is exported and checked.

Early render shows the continuous shell and clean root face, but the root is still too blocky and its bright corner chamfer needs inspection. Study17 remains the direct visible-form target; Study19 offers internal tab/yoke cues, while its oversized socket and altered axis are rejected. Do not label77 complete or reference-matching yet. Side/rear and genuinely inner/underside actual renders remain necessary, as do backpack refinement and concealed cannon support checks. Approved torso/helmet preserved.

## TrialA render and correction

Actual Hero TrialA finished in3m38.04s and was exported, viewed and verified2000x1600. Preserved as `renders/Phantom_Shoulders_Hero_Pass77_TrialA.png`, SHA256 `f8acb8a2889e500aaa22afe684caecab918e49ee0b1c26350e408d779165a209`. Its matching760f3104 model is also preserved as `checkpoints/Phantom_Shoulders_Pass77_TrialA_PrePlanar.blend`.

TrialA shows a diagonal shading patch across85's long front face, consistent with a nonplanar face and the inherited lattice distorting its corners. Through UI:85 EditMode all faces selected, MakePlanarFaces factor1, iterations10; removed ONLY85's Lattice modifier (Mirror and SmoothByAngle retained; parent relationship retained). Selected its full outer-tip vertex group in front orthographic Xray, local median(3.1516,.065,8.2466); explicitly verified MedianPoint pivot. SY.47 directly tapers the tip. Selected all faces, MakePlanarFaces factor1 iterations10 again, verified in F9, then recalculated outside normals. Top solid view confirmed the symmetric tapered footprint. This replaces85's indirect lattice taper with direct mesh taper; other shoulder objects retain76 lattice.

Object93 still had inherited Graphite/Gold/Teal slots. Replaced only its Teal slot with existing `Teal - shoulder exposed returns` (now3users), then entered EditMode, selected all cap faces and explicitly Assigned that slot. This ensures the newly constructed cap actually uses the intended teal; no shared material values were changed. Side camera selected and verified through Outliner before activation. Saved77 again and started corrected Side77 render. Final hero/side exports and checkpoint publication remain pending at this note revision.

UI lesson: after closing F9/popups or returning from a file dialog, some keyboard actions are silently ignored until the pointer re-enters the editor. Scrolling inside the3D viewport moves the pointer without deselecting geometry; use it before subsequent shortcuts. After render export, click inside the ImageEditor body before ShiftF9; otherwise an intended Outliner search may rename the image datablock. An accidental RenderResult name change was immediately restored; it did not change model geometry or exported pixels.

## Corrected actual renders verified

- `renders/Phantom_Shoulders_Side_Pass77.png`:2000x1600,128Cycles,1m44.96s; SHA256 `bee9a5027a03250aef1be582b62a150485279cd15d63bd7644187fb7ded82439`.
- `renders/Phantom_Shoulders_Hero_Pass77.png`:2000x1600,128Cycles,2m48.07s; SHA256 `47639974248084fc35030e97fd987dc1c69b95358f6955403ff504917e457309`.

Both exports were checked for actual filename, dimensions and visible image contents before replacing RenderResult. Corrected hero removes the conspicuous diagonal patch and bright root-corner stripe present in TrialA. The continuous shells, sloping roof walls and thin brass fascia now read coherently in hero and side. The root remains simpler and more boxy than Study17, and a broad dark band remains above the brass edge. Inner mount tabs and underside construction still need close actual views. Rear77 has not yet been rendered. Backpack remains pale and bulky; exhaust faceting and two unidentified gray discs remain pending. No final/AAA/exact-match claim.

Latest Blender save uses the hero camera; no unsaved geometry or render pending. Last RenderResult is corrected Hero77, already exported. The local root approved torso file remains SHA256 `2da7a2e05bd5afdfa585c5f5299be445180f3a5d24bfc2d94787de2319d37f89`.

Export shortcut may fail to open a dialog when focus is stale. Inspect the returned window before clicking a zoom button: only zoom an actual FileView. F11 can expose another editor window instead of an image; change that editor through its type menu to ImageEditor, then select RenderResult. Small1059x631 save dialogs work after reacquiring the app, raising the window, a separate first filename click and a second confirmed text-entry click; filename(471,610), Save(986,611). A maximized dialog is not always necessary.
