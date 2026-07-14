# Sound Effects Plan — "Let the Works Be Heard"

Status: IMPLEMENTED (July 2026) — all 16 cues live as specified below; FOLEY module in the main HTML.
Verified via FOLEY.log: cue order and exact counts through a full revolution (tick×10 for a 10-char card,
note×48 for 6 floors × 8 bars, thump×5 for 5 drops, etc.); toggle persistence and muted-means-no-AudioContext
both confirmed. This document remains as the design reference.

## Principles

- **No external assets.** Every sound synthesized live via the Web Audio API — keeps the
  single-file, offline, CSP-safe guarantees intact.
- **Off by default.** A brass toggle on the Operator's Desk: *"Let the works be heard (sound)"*.
  Nobody gets surprise audio mid-presentation. Choice persisted in localStorage (`ale-sound`).
- **Quiet and dry.** Master gain ~0.22; every cue short (<400ms) except two barely-audible beds.
  No music. The register is: brass, wood, paper, steam.
- **Throttle/fast-safe.** A per-cue rate limiter (min ~60ms gap per cue name) so `?fast=1`
  or rapid cranking never machine-guns. Mid-run mute ramps master gain over 50ms (no pop).
- **Lazy start.** AudioContext created only on first enable (a user gesture, satisfying
  autoplay policy). While muted every `FOLEY.play()` is a zero-cost no-op.

## Architecture

One IIFE module `FOLEY` (~150 lines), inserted near the top of the script:

- Cached noise buffer; primitives: `click(freq,gain)`, `ping(freq,dur,gain)`,
  `thump(f0,f1,dur)`, `hiss(dur,band,gain)`, `swish(bandFrom,bandTo,dur)`,
  `bed(name,on)` for the two continuous layers.
- `FOLEY.play(name, params)` dispatches from a cue catalog; instrumentation in the app
  is one line per hook.
- `FOLEY.log` — ring buffer of the last ~50 cues played, for automated verification
  (assert the cue sequence of a revolution without ears).
- Mute switch: checkbox in the desk `.opts` row + tiny CSS; `id=chkSound`,
  `autocomplete=off`, default unchecked.

## Cue catalog and hooks

| # | Beat | Sound design | Code hook |
|---|------|--------------|-----------|
| 1 | Works running | brown-noise hum, lowpass ~180Hz, slow LFO wobble, barely audible | `revolution()` start/end, `html.running` |
| 2 | Card feeds (I) | bandpassed noise swish ~1.2kHz falling, 200ms | `phCard` slide-in |
| 3 | Pin column read (II) | 2ms tick + faint 2.2kHz ping; **filter brightness mapped to hole count** of the character | `runCutter` column loop |
| 4 | Slug released (II) | descending zip (drop leg) + brass "shink" (slide-home leg) | `dropChip` |
| 5 | Dials set (III) | tiny clock ticks, random detune, staggered, rate-limited | `setDials` callbacks |
| 6 | Linkage drawn (IV) | short triangle pluck; **pitch inverse to weight** (heavy regard = low note); cap ~10/render | `renderAttn` `draw()` |
| 7 | Ball rolls (V) | soft rumble bed while roll loop runs | `runMill` roll loops |
| 8 | Bar rises (V) | short sine ping, **pitch mapped to bar value 0..1 → ~220–880Hz** — the mill "plays" the column; the figure mutates floor by floor | bar-set line in `runMill` |
| 9 | Floor drop (V) | sine thump 90→60Hz, 120ms | drop loop in `runMill` |
| 10 | Gauges rise (VI) | single rising pressure swell, 600ms (not per-tube) | `phGauges` |
| 11 | Boiler lever (VII) | steam hiss, gain ∝ |ΔT|, 150ms, highpassed | `setTemp` |
| 12 | Lottery pointer (VII) | **decelerating pawl click-train matched to the pointer easing** (~18 clicks, widening gaps), final clunk on landing | `phDraw` |
| 13 | Crank turn (VIII) | low chunk + ratchet triplet, ~250ms | `crankTurn` |
| 14 | Stamper strike (VIII) | 40ms press-whoosh + firm *thock* (120Hz sine + click transient) at the impact moment `stampAction` already sleeps to | `stampAction` |
| 15 | The engine rests (∎) | deeper double-thock + single 880Hz bell, 400ms decay | FIN branch of `phPrint` |
| 16 | Proceed/Begin press | one soft click (other buttons stay silent) | button handlers |

Showpieces: #12 (audible deceleration = suspense of the draw) and #8 (refinement made
audible — six floors, six variations of an eight-note figure).

## Rollout order

1. FOLEY core + mute switch + persistence + log buffer.
2. Stamper, crank, lottery pawl (highest payoff).
3. Mill notes, cutter ticks, slug zips.
4. Ambience beds, gauges, lever hiss, garnish.

## Verification

- Automated: enable via simulated gesture; run a revolution; assert `FOLEY.log` sequence
  (card→ticks→zips→plucks→notes→thumps→swell→pawl-train→clunk→chunk→thock), assert
  no cues while muted, AudioContext state transitions, no console errors.
- Human: final ear pass in the preview at normal pace and `?fast=1`.
