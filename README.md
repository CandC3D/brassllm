# The Analytical Language Engine

*Being a candid mechanical account of the Large Language Model — rendered in brass, in the manner of Mr. Charles Babbage.*

An educational, single-file HTML app that shows what happens inside an LLM between prompt and output, staged as a Victorian brass machine. Built July 2026.

## Running it

Double-click `analytical-language-engine.html`. It is fully self-contained — no internet, no install, works in any modern browser.

Hosted copies:

- GitHub Pages: https://candc3d.github.io/analytical-language-engine/
- Claude artifact: https://claude.ai/code/artifact/f0c03be7-7e4f-49c5-ba5d-83f67ae0eae2

## The eight stations

| Station | Mechanism | Real concept |
|---|---|---|
| I | The Card Reader | the prompt (text in, nothing else) |
| II | The Type-Cutting Works | tokenization + context window |
| III | The Ledger of Meanings | embeddings |
| IV | The Linkage of Regards | attention (two heads shown) |
| V | The Grand Mill | layers, parameters, training |
| VI | The Manometer Wall | probability over every token |
| VII | The Governor & Lottery Drum | temperature + sampling |
| VIII | The Endless Crank | autoregressive loop + stop token |

## Presenting

1. Type a few opening words (this small engine continues them — Station I's plaque explains how real chat engines handle whole questions via the transcript trick) or take a ready-punched card, then **Begin the Demonstration**.
2. The tour pauses at every station by default — press *Proceed* (bottom-right chip) to advance at your own pace. Untick **Wait at each station** for a self-running tour.
3. Thereafter **Turn the Crank** for one word at a time, or **Run the Engine** until it draws the stop token ∎.
4. Move the boiler lever (Station VII) mid-run — the gauges reshape instantly. FROST ≈ greedy decoding; FEVERISH ≈ chaos.
5. Append `?fast=1` to the URL for quick-cycling animations (rehearsals, impatient audiences).
6. When a revolution ends, the telegraph chip (bottom-right) grows contextual buttons: **↻ Crank** mints the next word from wherever you stand, and **⇧ To the desk** returns to the top (it appears whenever you've scrolled down and the works are idle).

## What is real, what is theatre

- **Real:** the probabilities. A miniature counting engine (interpolated trigram/bigram/unigram Markov model over the built-in ~80-sentence library) computes every distribution live. Temperature (p^(1/T), renormalised), the weighted-lottery draw, novel-word handling (✶), and the ∎ stop token are all genuine.
- **Theatre, labelled as such:** the attention arcs (recency + co-occurrence affinity, schematic), the six mill floors (whose bars trace the final token's column being revised floor by floor — floor I is the entering pattern from Station III, floor VI the much-revised result), the dial values. The plaques state candidly how the full-sized article differs, and the footer post-scriptum records the famous estimate: built in brass at one counting-column per parameter, a trillion-parameter engine would cover Wales, mint about one word per season, and burn half of 1850 Britain's coal. A post-post-scriptum computes the labour question — pauper treadwheels would buy four days per word at thirty times the price of coal — and declines the scheme, anticipating the Prison Act of 1898 by fifty-five years.

## Editing notes

- Everything is in the one HTML file: CSS, markup, corpus, and JS.
- Line 1 is the entire `<head>` shell and the last line is `</body></html>`; the claude.ai artifact copy is the same file with those two lines stripped (`sed '1d;$d'`).
- The corpus (a JS template string, ~80 lines, pre-spaced punctuation) is what shapes the demo: preset cards were tuned so their contexts branch nicely. Avoid corpus lines ending `<preset-word> .` or that preset will draw early stops.
- `window.ENGINE` exposes state for scripted testing; `?fast=1` sets pacing to 0.12×; `prefers-reduced-motion` is respected.
