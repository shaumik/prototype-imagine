# Phantom assembly refinement — Pass79, unfinished checkpoint

Current saved model: [Phantom_Shoulders_Pass79_Traced_Root_Roof.blend](checkpoints/Phantom_Shoulders_Pass79_Traced_Root_Roof.blend). Direct reference tracing corrected the shoulder cap slope in Pass78. Pass79 positively identified the rough projecting roof surface as the internal foundation, then lowered only its two upper root corners beneath the cap. The traced cap itself was preserved.

Actual [hero79](renders/Phantom_Shoulders_Hero_Pass79.png), [rear79](renders/Phantom_Shoulders_Rear_Pass79.png) and [side79](renders/Phantom_Shoulders_Side_Pass79.png) verify the continuous roof, clean wing faces and depth taper at 2000 × 1600, Cycles 128 samples. Read [PASS79_NOTES.md](PASS79_NOTES.md) for precise changes, evidence, hashes and remaining work. Both canonical publication paths match the versioned79 checkpoint. The model remains unfinished: the backpack is pale, broad and slab-like; its gray discs require identification, and its rear and side silhouette need comparison with the original guide and generated Study20.

## Historical Pass78 checkpoint

Current saved model: [Phantom_Shoulders_Pass78_Mount_Verification.blend](checkpoints/Phantom_Shoulders_Pass78_Mount_Verification.blend), matching both canonical publication paths. The user requested direct reference-overlay tracing. This exposed and corrected the shoulder root cap's flat, overly high inner roof contour. The wing now follows the brass fascia with a narrow seam. Actual [hero78](renders/Phantom_Shoulders_Hero_Pass78.png) verifies the current shape at2000x1600/128Cycles, but exposes a rough cap roof transition that must be rebuilt. This is a recoverable work checkpoint, not a finished model.

[Inner mount78](renders/Phantom_Shoulders_Inner_Mounts_Pass78.png) shows a solid guard bridge, heavily shadowed, with only the closest tab visible. [Rear trial78](renders/Phantom_Shoulders_Rear_Pass78_TrialA.png) is explicitly PRE-TRACE geometry; it does not verify the latest cap. Read [PASS78_NOTES.md](PASS78_NOTES.md) for exact geometry, reference alignment, control recovery and remaining work. Next: reconstruct the cap roof cleanly, render current hero/rear/side, then refine the pale bulky backpack using original-guide overlays and generated Study20 (known contradictions documented).

## Historical Pass77 checkpoint

Current saved model: [Phantom_Shoulders_Pass77_Continuous_Armor.blend](checkpoints/Phantom_Shoulders_Pass77_Continuous_Armor.blend), matching the canonical checkpoint. The shoulders now have continuous tapered wing shells, sloped root caps and corrected planar faces. Actual [hero77](renders/Phantom_Shoulders_Hero_Pass77.png) and [side77](renders/Phantom_Shoulders_Side_Pass77.png) are exported and verified at2000x1600/128Cycles. See [PASS77_NOTES.md](PASS77_NOTES.md) for retained geometry, rejected TrialA, hashes and remaining differences. Root detail, inner/underside verification and backpack refinement remain unfinished.

The Mac lock interruption was resolved after the user unlocked it. Live interrupted geometry was saved separately before editing; the earlier interruption notes below are historical.

## Historical Pass76 checkpoint

Latest geometry checkpoint: [Phantom_Shoulders_Pass76_Tapered_Shell.blend](checkpoints/Phantom_Shoulders_Pass76_Tapered_Shell.blend), matching current canonical on publication. See [PASS76_NOTES.md](PASS76_NOTES.md). Coherent outer depth taper and thinner front/rear brass fascia are verified in actual [hero76](renders/Phantom_Shoulders_Hero_Pass76.png) and [side76](renders/Phantom_Shoulders_Side_Pass76.png), both2000x1600/128Cycles. The upper shell and root remain boxy and require substantial reshaping toward the generated reference. Work remains unfinished.

## Pass77 interrupted by Mac lock

The live Blender scene contains unsaved shoulder-shell reconstruction. Read [the interruption notes](interrupted_pass77_20260913/INTERRUPTED_PASS77_NOTES.md) before resuming: save the live scene separately immediately after unlock. A recent autosave is preserved in that folder but has not been opened or visually verified. Both canonical models remain the verified Pass76 checkpoint. There is no actual Pass77 render yet.

## Historical Pass75 checkpoint

Pass75 corrects the washed-out exposed shoulder returns using a separate material and object-specific fill. See [PASS75_NOTES.md](PASS75_NOTES.md) for diagnosis, failed trials and current verification. The model's geometry remains the recovered late-pass geometry: shoulders are still boxy in depth, brass edges too thick, and the backpack pale and bulky. The generated studies have not yet been adequately translated into those forms. No finished-quality claim is warranted.

New actual front and hero baselines are `renders/Phantom_Assemblies_Front_PrePass75.png` and `renders/Phantom_Assemblies_Hero_PrePass75.png`. New Pass75 side and rear evidence belongs to this material/light pass; all are 2000 × 1600 with 128 Cycles samples. TrialA/TrialB files are labeled experiments. Generated construction studies15–17 and their critiques remain separately labeled in `supplementary_references`.

At Pass75 publication, [checkpoints/Phantom_Reference_Manual.blend](checkpoints/Phantom_Reference_Manual.blend) matched versioned `Phantom_Shoulders_Pass75_Exposed_Return_Finish.blend`; Pass76 has since superseded it. The local root torso file remains untouched. Read the latest section of [RESUME_NOTES.md](RESUME_NOTES.md), then the historical recovery details below.

## September12 recovery history

Work is unfinished. Resume the late-pass model from [checkpoints/Phantom_Reference_Manual.blend](checkpoints/Phantom_Reference_Manual.blend), not Pass30 and not the root outputs model.

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

## GitHub backup verified

[Recovery commit3c85a55](https://github.com/shaumik/prototype-imagine/commit/3c85a551911d47acaee6ecba24f2f83754a8425e) is published on main. Both repository canonical models are current; the local root outputs model remains approved torso00. All22 published model/image files were downloaded back from GitHub and matched their SHA256 checksums. The publication also includes restart notes and the original autosave.

Push and verify each meaningful saved refinement pass as work proceeds. Local saves alone do not satisfy the user's checkpoint-backup priority.
