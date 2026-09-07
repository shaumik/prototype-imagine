# Jump sprite sheet

Generated with the built-in image-generation tool, using `assets/runner_pixel.png` as the character and style reference. Final asset: `assets/runner_jump_pixel.png`.

Use case: stylized-concept. Asset type: production pixel-art JUMP ANIMATION SPRITE SHEET for the existing side-scrolling game.
Input image: STYLE AND CHARACTER REFERENCE ONLY. Match this exact clean blue pixel robot with navy outlines, cobalt armor, sky-blue highlights, cyan helmet visor, short orange scarf, chunky boots, forward integrated arm cannon and green energy saber trailing behind. Keep the same head, proportions, armor and pixel-cluster size. Do not redesign him or return to painted/realistic shading.

Create EIGHT sequential JUMP poses in a precise 4-column by 2-row equal grid. 1536x768 canvas, each cell 384x384. Every pose fully SIDE-ON facing RIGHT. Clean genuine 16-bit pixel art with flat limited-palette shading and stepped square pixel edges. Each character's body would be about 48 pixels tall at native resolution, shown at 4x nearest-neighbor scale. No blur, gradients, painterly textures, 3D metal, or antialiasing.

Frames left-to-right:
TOP ROW:
1. TAKEOFF: body stretching upward from push-off, one leg straight down and the other knee starting to lift.
2. RISING: rear leg begins to fold underneath, leading knee bent forward; torso upright with a slight forward lean.
3. HIGH RISE: both legs gathered closer, rear shin tucked back, leading knee lifted to hip height.
4. APEX: compact tucked midair pose, both knees softly bent, relaxed torso, scarf lifting slightly.
BOTTOM ROW:
5. FALLING: leading shin unfolds DOWNWARD from the knee, rear leg still bent, feet clearly below hips.
6. REACH FOR LANDING: front leg extends downward with toe preparing for contact, rear leg bends back; NOT another running pose.
7. CONTACT / COMPRESSION: grounded weight-bearing landing, leading foot flat, knees bent and pelvis lower as legs absorb impact.
8. RECOVER: knees straightening out of landing into the start of a running stride.

Registration is essential: all eight have the SAME character scale and head/body proportions, BODY centered around local x=190, hip center at local y=220 in the first six AIRBORNE cells. Do NOT line all the FEET up; feet must lift and tuck naturally while hip stays in the same place. For landing frames 7 and 8, register the planted foot on local y=330. The cannon stays attached at chest height and aimed RIGHT in every pose. The rear hand holds the same sharp green/white saber; keep it trailing diagonally backward with slight natural changes, no attack slash or effects. All limbs remain anatomically consistent. Exactly two arms and two legs.

Background MUST be perfectly flat pure solid MAGENTA #FF00FF, including all gaps. This is a chroma-key technical game asset, NOT a transparent/checkerboard presentation. Leave ample blank magenta margin around every sprite, including saber tip, scarf and feet. No sprite may touch a cell boundary or overlap a neighboring cell. No ground, shadows, fog, particle effects, words, numbers, labels, borders, grids or logos.
