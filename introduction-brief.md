# Introduction Brief — The Analytical Language Engine

*A self-contained briefing for generating an introductory essay. Needs no other context.*

**Suggested handoff prompt:** "Using the brief below, write a ~600-word essay
introducing this project to a general, curious audience — accurate and
non-hyperbolic, warm and literate, explaining both what it is and why it matters.
Don't over-quote the brief; synthesize it."

---

**What it is.** A free, interactive web page that shows how a Large Language Model
(LLM) turns a prompt into text — reimagined as a Victorian brass machine, in the
manner of Charles Babbage's never-completed Analytical Engine. It is a *working*
model, not an animation: real probability arithmetic runs live in the browser and
drives everything you see. Its self-deprecating class-name is an **ILM —
Infinitesimal Language Model** — the honest counterpart to the Large.

**Where.** Live at https://candc3d.github.io/brassllm/ · source at
github.com/CandC3D/brassllm · a companion "About" page explains the mathematics.
Devised by **Christopher Horrocks** and constructed by **Claude** (an engine of the
very kind depicted). Styled throughout as the wares of "Messrs. Horrocks & Claude,
Purveyors of Analytical Language Engines, Oldham, Lancs., © 2026."

**How it works, honestly.** Under the brass, it is an **n-gram Markov model**: it
counts how often words followed one another across a built-in library of **79
sentences** (a ~231-word catalogue), blending trigram, bigram, and unigram evidence
by interpolation (weights 0.72 / 0.21 / 0.07) with graceful back-off. It reshapes
those odds by **temperature** (q ∝ P^(1/T)) and draws the next word by **weighted
lottery** — exactly the sampling mathematics a real model uses; only the *source* of
the probabilities differs. The engine is candid about this: on-screen plaques pair
each conceit with a plain "In truth —" explanation, and a table states plainly which
stages are genuinely computed (tokenisation, the probability gauges, temperature,
sampling) versus honestly illustrative (the embeddings, attention, and layer
"refinement").

**The eight stations** (the LLM pipeline, made mechanical):

- **I · The Card Reader** — the prompt arrives as a punched card. The machine
  receives marks, not meaning.
- **II · The Type-Sorting Works** — *tokenisation*. A Linotype-style pin-reader reads
  the card and releases numbered brass "slugs" into a composed line; the 24-slot rack
  is the *context window*. A pull-out "Type Drawer" beneath the station displays the
  model's entire closed vocabulary, sortable by number, alphabet, frequency, or
  meaning-district.
- **III · The Ledger of Meanings** — *embeddings*. Each token becomes a vertical
  column of eight dials; position is meaning (ENGINE and GEARS set alike; FOG differs).
- **IV · The Linkage of Regards** — *attention*. Two "heads" shown as linkages: a
  nickel (silver) recency head above, a copper affinity head below; thickness is regard.
- **V · The Grand Mill** — *layers & training*. A ball rolls serpentine down six
  pretended floors (of ~100), bars rising in its wake as the token's numbers are
  refined — spelling → grammar → phrase → sense → intent → judgment.
- **VI · The Manometer Wall** — the *probability distribution*. Live gauge tubes for
  the seven strongest candidates, with "all others" pooled — the model's true output
  at each step.
- **VII · The Governor & Lottery Drum** — *temperature & sampling*. A boiler lever
  runs from frost to fever; a decelerating pawl draws the winning word.
- **VIII · The Endless Crank** — the *autoregressive loop*. The chosen word is struck
  onto ticker-tape, fed back into the rack, and the whole engine turns again — until
  it draws the **stop token (∎)** and rests.

**How you use it.** Type a prompt (or take a ready-punched card), then "Begin the
Demonstration." A paced tour walks station to station — it waits at each by default,
advancing when you press *Proceed*, or you can let it run itself. Thereafter "Turn
the Crank" mints one word at a time, or "Run the Engine" writes until it stops. Move
the boiler lever and the gauges re-compute instantly. Hover any dotted term for a
plain-English definition. An optional synthesized "foley" track (off by default) lets
you *hear* the works — including the mill playing each column's settings as a little
melody, and the lottery's decelerating clicks.

**Particulars.** A single self-contained HTML file (~90 KB). No dependencies, no
build step, no server, no logins, no cookies, no tracking; works offline and on
mobile. All sound is synthesized live via the Web Audio API; all animation is
SVG/CSS. It respects reduced-motion preferences, its tooltips are keyboard-accessible,
and it ships with a proper social-preview card and favicons.

**Flourishes worth a mention.** The footer carries a mock Victorian correspondence
with full Fermi arithmetic in the margins: a full-scale brass LLM built at one
counting-column per parameter would **cover Wales** and mint about *one word per
season*; a "Mr. E. Scrooge" asks whether pauper treadwheels could replace the boiler
(they cannot — and cost thirty times more than coal). It's whimsy in service of
conveying real scale.

**Why it matters (angles for the essay).** It demystifies a technology people find by
turns magical and menacing, by making the invisible mechanism visible and
*touchable*. Its guiding virtue is honesty — it never pretends to be more than it is,
and its candour about what's real versus illustrative is itself a lesson about how to
talk about these systems. And its closing image is the thesis: a small counting-engine
and a hundred-billion-parameter model share the same pipeline — *"the difference
between a music box and an orchestra: both can play the same tune, just at
different scales."*
