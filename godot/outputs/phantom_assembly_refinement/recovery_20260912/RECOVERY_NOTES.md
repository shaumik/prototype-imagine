# Phantom recovery — 2026-09-12

The original workspace directory was absent when work resumed. The cause is unknown; this does not establish permanent deletion. The original path has been recreated to hold recovery files. No original workspace model, old render, or historical checkpoint has been overwritten during recovery.

## Secured autosave

Original: `/private/var/folders/gx/c7k2rpt10ld79vhctl78yggr0000gn/T/Phantom_Reference_Manual_57123_autosave.blend`

Preserved copy here: `Phantom_Recovered_Autosave_PENDING_VISUAL_CHECK.blend`

Independent backup: `/Users/shaumikmondal/.codex/visualizations/2026/09/09/01a0846e-0399-76e1-9285-5c7c7fc1d15c/phantom-recovery-20260912/Phantom_Reference_Manual_57123_autosave.blend`

Size: 3066319 bytes. Modified 2026-09-12 20:27:51 PDT. SHA256: `c6aa5a41168093d84244a81ec1ed451ce5abe284d4fdd442865059d21c489b5d`.

Zstandard integrity check passed. Both backup copies were verified to match. Read-only inspection found the late-pass objects `95 Gold - shoulder outer return covers`, `96 Black - shoulder brass band fasteners`, `Shoulder Softbox - rear`, and `Verification - Shoulder Close Hero`. This confirms recent work survives, but does not by itself prove every Pass74 edit is present.

All 14 generated supplementary references were also copied into the independent backup directory. They are generated construction studies, not actual-model renders. The original construction guide remains the design authority.

## Last known saved work before directory loss

The Sept9 Pass74 editable file was `checkpoints/Phantom_Reference_Manual.blend`, paired with `Phantom_Shoulders_Pass74_Inner_Fastener_Clearance.blend`. Its then-verified SHA256 was `54186e7dba7fe8df93e5012e15d6ed5aa81ada140b132ba62a093340e33d892d`. These original files have not yet been located.

Pass74 raised the four innermost heads in object96 from Z7.74 to Z7.80; the remaining 12 heads stayed unchanged. Pass72 shortened object95 in Y by 0.96, producing depth approximately1.267, centerY0.065405, front approximately-0.569 and rear approximately0.699. Pass70 moved object95 and the selected outer end of object06 inward by X0.10 on the right, mirrored to the left. These are recovery validation targets, not newly performed edits.

Last verified Sept9 actual render: `Phantom_Shoulders_Rear_Pass74.png`, 2000x1600, 128 Cycles samples; SHA256 `c78368141e3711d293b2bfe8481338db3ef92103099c774eb1ec8ab62e445e49`. That image file has not yet been recovered. It showed a washed-out viewer-left outer shoulder corner and a pale, blocky backpack. Hero71 predates the Pass72 cover clearance and Pass73/74 fasteners. Current side, underside, inner mount and hero verification remain necessary.

The temporary publication clone `/private/tmp/prototype-imagine-publish.tZXdIa/repo` is partial/damaged. Its main ref records `93eb9017122360cc03003f23caef1d5df4c62fac`. Its surviving canonical model is older Pass30 (SHA256 `31f46aa9597fd724430bc8a6e0d54f6addcae42b2e660cfbb6dd5fd4fc15f050`); do not resume that model over the late-pass recovery.

## Rules and remaining modeling work

All Blender modeling, materials, lighting, camera setup, and rendering must use computer control through Blender UI. No Python or Blender scripts. Filesystem tools may verify, back up, and document. Preserve approved torso and helmet. Work in assembly order: cannons, shoulders, backpack, combined fit. Generated references must be critiqued against the original guide; never present them as actual renders.

Cannon51 was retained with open round bores and five verified high-resolution views before loss. Shoulder74 was unfinished: inspect pale outer corner by selecting its actual object, verify object95 overlap from oblique angles, inspect guard mount tabs from a genuine inner angle, and regenerate current multi-view evidence. Backpack remains third: tapered housing, recessed grille and exhaust depth, mechanical supports; identify the two gray discs beside exhausts before deciding whether to retain or remove them. Do not claim AAA quality or completion without evidence.

## Live recovery in progress

Computer control reconnected on Sept12. Blender is running with the mech visible and the old missing canonical path in its title. The live scene has unsaved changes. A separate live recovery save is being made before inspection. Do not close Blender until that save is verified.

## Recovery verified — latest status, supersedes in-progress notes above

The full published repository was successfully cloned to `/Users/shaumikmondal/programming/prototype-imagination/recovered_published_repository`. HEAD is exactly93eb9017122360cc03003f23caef1d5df4c62fac; clean status and Git integrity verification passed. The earlier attempt to archive the damaged local Git object database failed because a tree was missing; its zero-byte output was not a usable backup. Fresh clone is the valid source. Published Godot files and original guide were restored with non-overwriting copies, protecting the recovered canonical model and approved torso root file.

Live Blender save and autosave are both separately preserved. UI checks confirmed the four innermost object96 heads at median(-.14,.067001,7.8), and object95 at mesh median(2.8228,.065405,7.9531), Ydimension~1.27. This matches the documented Pass70/72/74 late changes. No geometry changes were made during recovery.

Final editable: `../checkpoints/Phantom_Reference_Manual.blend`.
Matching checkpoint: `../checkpoints/Phantom_Recovery_20260912_Verified.blend`.
Matching external backup: `/Users/shaumikmondal/.codex/visualizations/2026/09/09/01a0846e-0399-76e1-9285-5c7c7fc1d15c/phantom-recovery-20260912/Phantom_Recovery_20260912_Verified.blend`.
All three SHA256 `00aac2039a65410a373e7b313f75c1f49a96685f086eadb7ccda5809d75798ee`. Compressed-file integrity check passed. The initial unmodified live recovery and initial autosave copies remain separately preserved. Final save has existing side verification camera active; no unsaved geometry.

Retained Rear74 RenderResult exported and inspected: `../renders/Phantom_Shoulders_Rear_Pass74_Recovered.png`,2000x1600, SHA256 `c78368141e3711d293b2bfe8481338db3ef92103099c774eb1ec8ab62e445e49`, EXACT match to Sept9 saved image.
New actual side render: `../renders/Phantom_Assemblies_Side_Recovery_20260912.png`,2000x1600/128Cycles, completed1m49.83s, SHA256 `1eb6acb8e85d95d07a4e10eff96b9fe189957bee6a33ccfd0a871868b7641235`. Exported and viewed, then backed up outside workspace. No render pending. Latest RenderResult remains this side image.

Both images are actual Blender renders, not generated references. The side view shows retained cannon panel/recess construction, a thick rectangular shoulder profile with long front/rear brass edges, broad dark support areas, and a pale bulky backpack with faceted exhaust outer walls. These remain model-quality issues requiring correction. Other unpublished intermediate checkpoints and recent renders have not been recovered; their absence does not imply the current geometry was lost. Continue modeling from the final editable file, never from restored Pass30.
