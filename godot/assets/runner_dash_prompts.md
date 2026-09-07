# Dash sprite sheet

Generated with the built-in image-generation tool, using assets/runner_pixel.png as the character and pixel-style reference. Saved asset: assets/runner_dash_pixel.png.

Use case: stylized-concept. Asset type: production PIXEL ART dash animation atlas for an existing side-scrolling action game.
Input image is CHARACTER AND PIXEL-STYLE REFERENCE. Match this exact blue armored runner, dark navy outlines, cyan visor, short orange scarf, forward integrated arm cannon, and green/white saber in the rear hand. Same helmet and armor proportions. Preserve the clean flat pixel-art style. NO painting, realistic metal, gradients, airbrush, blur, dithering, or soft outlines.

Create TWELVE different successive dash poses on a uniform 4-COLUMN by 3-ROW grid, ideally 1536x1152 (384x384 cells). All characters fully SIDE-ON facing RIGHT. Strict consistent character size: the same head is about 55 output pixels tall in every cell, and a standing body would be about 220 output pixels tall. Clear 4x4 square pixel clusters. Each character must fit completely within its cell with generous blank margins, including scarf, boots, saber and cannon. No sprite overlaps a neighboring cell.

Rows 1 and 2: an EIGHT-FRAME GROUND DASH sequence, read left-to-right:
1. Enter dash from running: slight forward lean, knees beginning to bend, cannon forward.
2. Push off strongly: torso leans further, one boot presses off ground, rear leg begins extending back.
3. Accelerating: body low and streamlined, chest forward, both legs swept backward, cannon aimed horizontally RIGHT.
4. FULL BOOST: unmistakable low horizontal dash silhouette, torso almost horizontal, bent legs trailing LEFT, orange scarf streams straight LEFT.
5. FULL BOOST continuation: same low silhouette, subtle alternate trailing-leg and scarf position. No standing or running here.
6. Release boost: chest starts to rise, leading knee unfolds toward the next step.
7. Recover stride: body rises further, leading boot reaches down for contact, rear leg bends.
8. Return to run: close to the reference running pose, upright forward lean, planted leading foot.

Row 3: FOUR AIR DASH recovery poses:
9. Air dash launch: airborne knees tucked, pitching forward from the reference jump proportions, cannon level right.
10. Air boost: streamlined horizontal airborne pose, legs folded back together, no grounded contact.
11. Air dash release: torso coming upright, both knees folding UNDER the hips.
12. Return to airborne: upright compact jump-apex pose, knees tucked under torso, cannon right. Do not plant a foot or extend a landing leg in these last two cells.

Motion must progress smoothly between poses. Keep the weapons attached: integrated cannon aimed RIGHT throughout, saber trails left behind, no attack swing. Draw only the runner, NO exhaust, afterimages, speed lines or glow clouds; the engine adds effects.
Ground frames: imaginary floor at local y=330, hip near x=175. The torso naturally lowers as the runner leans into boost. Air frames: center the torso and let feet tuck naturally. Keep same scale, never shrink the low dash pose just because it is wider.
Perfectly uniform flat solid MAGENTA #FF00FF background throughout, including all limb gaps, for runtime chroma keying. NO transparent checkerboard, shadows, scene, text, numbers, borders, visible grid, logos or labels.
