# Highway Phantom — Pit Stop Edition

A two-stage car-window action runner. The original illustrated Phantom runner, roadside parallax, and red-light boss framing remain.

## Play

- Arrow keys: move; Up: jump / double jump (triple jump with Phantom Wings).
- Z: buster. X: blade combo. Up + X: rising slash. Down + X: aerial pogo.
- Shift: dash. C: spend a full Flow meter for a seven-second combat burst.
- Escape: pause. Touch controls and fullscreen are available.

## Demo loop

The Long Way Home lasts 60 seconds before the Signal Warden stop. Harbor Afterglow lasts 64 seconds before the Harbor Sentinel stop. Both have authored encounter and platforming beats. Guards resist normal buster shots; blade, dash, support, and powered shots provide alternatives. Boss fan bursts, low waves, and high sweeps telegraph before firing. Normal buster shots deal reduced damage while the boss core is closed; each attack opens the core for 1.2 seconds.

Kills, parries, and route pickups earn scrap. A stage clear grants at least 180 scrap, plus a performance bonus. At the pit stop, selecting a part previews it; buying deducts the displayed price and equips it. Swapping owned equipment costs nothing. The selected preview is never automatically purchased when leaving the shop.

Purchased equipment and unspent scrap carry into stage two and retries. Scrap earned during a failed stage is rolled back to the stage entry balance. Storm Halo and Phantom Wings last until the pit stop. Other temporary powers retain their displayed timers or hit counts. All temporary powers clear when the stage ends. The final pit stop can refit the runner for another two-stage ride; there is no cross-session save.

## Local development

Run `npm run dev -- --port 4187`, then visit the local server. Static source and deployed assets live in `dist/`. There are no runtime package dependencies. `npm run build` validates JavaScript syntax, module imports, UI bindings, image assets, and hosting metadata. `npm test` runs the gameplay suite, including an automated mixed-action completion of both levels with shop purchases between them.

`/qa` exists only on the local development server and exposes the existing development fixtures. QA helpers are not packaged for production.

## Validation limits

Automated progression and combat checks do not establish subjective fun, animation quality, or investor readiness. This edition preserves the existing runner animation; it adds combat feedback, visible temporary effects, shop previews, equipment progression, encounter pacing, and audio rhythm. Browser playtesting requires separate authorization in this environment and has not been performed for this edition.
