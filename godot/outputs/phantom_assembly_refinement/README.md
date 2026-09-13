# Phantom assembly refinement — recovered September 12

Work is unfinished. Resume the late-pass model from [checkpoints/Phantom_Reference_Manual.blend](checkpoints/Phantom_Reference_Manual.blend) or the repository's [canonical model](../Phantom_Reference_Manual.blend), which are identical. Pass30 is superseded. On the original Mac workspace, the root `outputs/Phantom_Reference_Manual.blend` remains the older approved torso file; use the refinement checkpoint path there.

The workspace directory was absent when work resumed on September12; its disappearance has not been explained. The full published repository was freshly downloaded to `/Users/shaumikmondal/programming/prototype-imagination/recovered_published_repository` and verified at commit `93eb9017122360cc03003f23caef1d5df4c62fac`, with clean status and successful Git integrity verification. Published Godot files were restored without overwriting recovery files. The root `outputs/Phantom_Reference_Manual.blend` was restored from the approved torso checkpoint, preserving the original local-file distinction.

## Recovered recent work

- Live Blender scene saved through its UI as [Phantom_Live_Recovery_20260912.blend](checkpoints/Phantom_Live_Recovery_20260912.blend), with a second backup outside this workspace.
- Separately secured autosave in [recovery_20260912](recovery_20260912/RECOVERY_NOTES.md), also backed up outside this workspace.
- UI validation confirmed object96's four innermost shoulder fasteners have median(-0.14,0.067001,7.8), matching the last documented Pass74 correction.
- UI validation confirmed object95's Y dimension approximately1.27 and mesh median(2.8228,0.065405,7.9531), matching the shortened and inward-seated return covers from Pass70/72.
- The retained actual rear render was exported, inspected, and verified to have exactly the same SHA256 as the saved Sept9 Pass74 image.
- All14 generated supplementary references survived and were backed up. They remain construction studies, never actual-model verification.

## Actual model evidence

[Recovered Pass74 rear render](renders/Phantom_Shoulders_Rear_Pass74_Recovered.png), 2000x1600,128Cycles samples. SHA256 `c78368141e3711d293b2bfe8481338db3ef92103099c774eb1ec8ab62e445e49`.

![Actual recovered rear render](renders/Phantom_Shoulders_Rear_Pass74_Recovered.png)

[New actual side render](renders/Phantom_Assemblies_Side_Recovery_20260912.png), rendered from the recovered model at2000x1600/128Cycles samples, exported and visually inspected. SHA256 `1eb6acb8e85d95d07a4e10eff96b9fe189957bee6a33ccfd0a871868b7641235`. Older published renders through Pass29 are historical evidence, not verification of current shoulder/cannon geometry. Unpublished intermediate checkpoints31–74 and most corresponding renders have not been recovered; don't imply otherwise.

Latest editable and matching [verified recovery checkpoint](checkpoints/Phantom_Recovery_20260912_Verified.blend) share SHA256 `00aac2039a65410a373e7b313f75c1f49a96685f086eadb7ccda5809d75798ee`. A third matching copy exists outside this workspace. Blender's resource-packing command reported no new files to pack. No geometry, material, light or camera-transform edits were made during this recovery; the existing side camera was activated for the new render.

## Next modeling work

Continue UI-only modeling and rendering. Preserve approved torso and helmet. Cannon51 refinements were retained; shoulder74 still needs correction of the pale outer tip, oblique inspection of return-cover transitions, and inner/underside mount checks. The backpack remains too pale and blocky, with the two discs beside the exhausts still requiring identification. Continue assembly comparisons against the [original guide](../phantom_mech_revision6/construction_guide.png), then regenerate front, side, rear, hero, and necessary close-ups. No AAA/final claim is justified.

Read the final recovery section of [RESUME_NOTES.md](RESUME_NOTES.md) and [RECOVERY_NOTES.md](recovery_20260912/RECOVERY_NOTES.md). Older published sections describe superseded work through Pass30.

## Remote checkpoint practice

The user wants recoverable work pushed to GitHub during refinement. After each meaningful saved pass, publish a versioned editable checkpoint, the current canonical model, available verified renders, and updated restart notes. Verify the remote commit before continuing substantial work. A local save or a prepared commit alone is not a remote backup. Keep failed experiments and generated references clearly labeled; do not claim missing images are current verification.

This recovery publication includes the original autosave, the first live recovery save, the validated final checkpoint, two actual renders, all14 generated supplementary references, and restart notes. [SHA256SUMS.txt](recovery_20260912/SHA256SUMS.txt) records model and image checksums relative to the repository root.
