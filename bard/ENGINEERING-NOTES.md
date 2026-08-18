# Engineering notes — the sonnet press revisions of August 2026

*Written for whoever works on this next, human or engine. It records what was changed, why,
what was measured, and the traps this repository sets for the unwary. The revisions answer
the brief `abe_press_brief.md` (Chris's Downloads, not in the repo); every change below was
authorised by Chris explicitly, one item at a time.*

**Branch:** all of this sits on `press-revisions`. `main` is the pre-revision exhibit.

---

## The problem, in one paragraph

The Bard's corpus was built by joining every line-break and cutting at sentence points, so
the engine's "line" was a sentence — median 16 words, maximum 65 — and the press cut across
it at 6–10 words at a point the engine had no reason to treat as a boundary. Nearly
everything wrong with the sheets flowed from that: an em-dash imposed by the harness on
three lines in four (a mark not even in the type drawer), every line opening as though
beginning a sentence, the second word of every line the least-constrained draw in the
machine, and a Rhyme Cam that dragged ~36 candidates to half the drum (median boost ×4,000)
because it had no line-final distribution to draw on.

## What was changed, in dependency order

1. **Tail marks** (`composeSonnet`): the em-dash is gone. A line cut at the measure or the
   engine's own line-break is left unmarked (enjambment); a rhyme closing lines 4/8/12 takes
   a comma; line 14 takes the full stop. Capitals stay on every line opener (1609 practice).
2. **Concord completion test** (`unsatisfied()`, used by `concordStrike`, the rhyme close,
   the extension loop, and line 14): no stop, ∎ or ⏎ while a determiner/preposition stands
   unsatisfied in the last three tokens or a conjunction stands last.
3. **Line 14**: terminal-mark boost starts two words past the measure and never while the
   phrase is open. (It was cutting the couplet at a mean 6.8 words, sometimes on "to".)
4. **Rhymer hygiene**: no word rhymes against its own possessive (heart/heart's — `rhymeKey`
   strips `'s` so the identity check missed it).
5. ~~**Press boiler**: `PRESS_T = 0.85`.~~ **Reverted 2026-08-18 — do not reintroduce.** A
   press-only temperature constant was added on the strength of Chris saying "0.80 or 0.85 are
   the settings in my experience"; he had authorised a *measurement*, not a second boiler
   hidden inside the press, and said so. There is **one boiler**: `composeSonnet` draws at
   `S.T`, the Station VII lever, exactly as the crank does. The measurement stands and is
   quoted in the marginalia — cooling the lever to 0.85 buys ~5 points of quotation — but the
   reader does the cooling, in plain sight. General lesson for anyone editing this exhibit:
   a constant that quietly changes the machine's behaviour where the visitor cannot see it is
   the exact failure the whole page exists to argue against.
6. **Witten–Bell** in `rawDist`, both in the Bard **and the parent ALE** (see traps): weights
   `T/(T + WB_D·D)`. Textbook `WB_D = 1` measured *worse* (fidelity 76→68) because **85% of
   trigram contexts are singletons** and 1/(1+1) surrenders half their mass; `WB_D = 0.25`
   was set by measurement and beats the old fixed 0.72/0.21/0.07 at every folio.
7. **The verse-line corpus** (the big one): all folios regenerated from Gutenberg #1041
   as verse lines (2,155 at the top notch, 5–11 words, mean 8.2). New sort `⏎` (`LEND`),
   distinct from `∎` (`FIN`). `buildModel` cuts the wheels on the whole sonnet — each verse
   line followed by ⏎, each sentence point by ∎, counting straight through — so trigrams
   cross the line-break (that is what enjambment is). The **Measure Cam is now advisory**:
   with it off, lines still average 6.0 words, 37% closed by the engine's own ⏎. Also carried
   in: em-dash, `;` and `:` survive as sorts (SOFT_IDS is finally real); word-edge straight
   quotes struck, elisions kept ('tis, o'er, beauty's, wights') — the orphan sorts
   ('thou, 'will, 'i / hate') are gone. Registers: **3,216 sorts / 36,582 wheels**.
8. **The rhymer, recut and re-proven**: the old claim was "106 pairs pass". The scheme is
   public, so the 152 regular sonnets *name* 1,060 authentic pairs (1–3, 2–4, 5–7, 6–8,
   9–11, 10–12, 13–14; 99 and 126 excused) — the initial score was 77.5%, and two failures
   were regressions of ours (by/lie, mine/thine refused by an over-broad NORHYME).
   Systematic fixes: the -y split (3+ syllables = weak class `'Y'`, licence-only, ending the
   6%-of-vocab collapse; 1–2 syllables sound as die/eye), heart/art, final s-as-z
   (days/praise), vowel-guarded past-tense stripping (bed/fled/head), young/tongue/song,
   survey/day, gu- as hard g (guest), rhyme/time, deceive/leave, -ence/-ense, you/new/view.
   NORHYME pruned by the Bard's own hand (any word he rhymed on is struck from it). The
   remainder go in the **licence book** (`buildLicence`): union-find over authentic pairs the
   phonetics cannot hear, built at schooling-time so it grows with the folio (~151 pairs /
   219 words at the top notch), returned as `'eye'`. **Final: phonetics 85.8%, with licence
   100% by construction; false positives 4/456 controls (0.9%), all -ing/-est weak tails of
   the kind the Bard himself rhymes.** `ABE_HARNESS.validateRhymer()` re-scores it.
9. **The Rhyme Cam, recut goal-first** (constrained decoding proper): the line's last word
   is chosen *before* the line begins — `drawGoal()` draws a rhyme-fellow of the partner's
   last word from `LINE_FINALS`, the line-end book — and the line walks to it: the cam holds
   the line open (strikes ⏎/∎/terminals) until the rhyme lands, favours successors with a
   counted bigram road to the goal (`goalRoads`, share `ROADS_SHARE`), and gives the goal
   half the drum when the current word has a counted road to it. One word steered, not 36
   catapulted; a ✗ is known from the line's first word when the drum holds no fellow.
   `ROADS_SHARE` is the rhyme-against-sense lever, measured at the full schooling:
   0 → fidelity 81 / rhyme 57; 0.20 → 77 / 73; 0.30 (default) → 77 / 76; 0.35 → 75 / 82.
10. **All exhibit text updated** to match: cam chips, press plaques, schooling plaque,
    marginalia (the boiler, and the withdrawn
    "rises with the schooling" claim), README, about-the-mathematics.md. The free-completion
    boiler sweep was **re-run** under the new engine: the old sharp 0.95 peak and post-1.00
    cliff are gone; the curve is a plateau (product within ~2 points, 0.70–1.05), collapsing
    past ~1.1. The crank keeps 0.95.

## Current measured state (unseeded, ~16–20 sheets, full schooling, all cams, lever at 0.85)

fidelity ~77% · derailment ~14% · rhyme ~76% (three in four at the first notch and the last —
it does **not** climb with the schooling; that old claim is withdrawn) · mean line 8.8 words ·
line closes: ~26% rhyme-goal, ~24% engine's own ⏎, ~8% drawn stop, rest at the ceiling.

## Decisions taken by Chris along the way (do not relitigate)

ONE boiler, no press-side constant (see 5) · Witten–Bell only, no PART-conditioned backoff
(yet) · **no** blanket rhyme-cam restraints from the old §6 ablation table — the goal-first
recut replaced that trade · em-dash kept as a sort of its own · verse-line rebuild as ONE
corpus for the whole machine, not a press-side second corpus · resync script paths point at
his home system and are **not** to be "fixed" · carry-over line context (old §4) rejected —
the ⏎ sort made it moot.

## The traps (read before editing anything)

- **`bard/resync_from_ale.py`** regenerates the Bard from the parent
  `analytical-language-engine.html` and re-applies grafts. `rawDist`/`tokenize` sit
  *outside* the grafted region: a Bard-only change there is silently reverted by the next
  resync. That is why Witten–Bell was made identically in both files. The script's absolute
  paths belong to Chris's home machine; leave them.
- **The seven corpus constants in `index.html` are not contiguous** — the counting-engine
  definitions (`FIN`, `intern`, `bump`) sit between the fourth folio and the fifth. A splice
  that replaces "from `const CORPUS` to the end of `CORPUS_ALL`" eats them. Use
  `splice_corpora.ps1`, which replaces each constant by name and asserts.
- **Never run `sed`/`perl`/byte-oriented tools over `index.html`** — it is UTF-8 with CRLF
  and they will destroy both (this happened; it was reverted from git). Use the Edit tool or
  .NET file APIs with explicit UTF-8.
- **This workstation** (Chris's office machine) has **no Python, no Node** (`python3` is a
  Microsoft Store stub). PowerShell 5.1 is the only scripting runtime — and it reads
  BOM-less `.ps1` files as ANSI, so keep script sources ASCII (build em-dashes with
  `[char]0x2014`). .NET calls in PowerShell resolve relative paths against the *process*
  working directory, not PowerShell's `cd` — always absolute paths.
- **`press_harness.js` duplicates `composeSonnet`** and will drift silently. Re-sync it by
  hand with every press change, or its figures are confidently wrong. Same for the measured
  figures quoted in README/marginalia — they are only as fresh as their last run.
- **Measurement is done in the browser**: open `bard/index.html`, paste `press_harness.js`
  into the console. `ABE_HARNESS.run({sheets,tier,seed})`, `.validateRhymer()`,
  `.vocabFacts()`. The preview pane may serve a cached document after `navigate` — force
  `location.reload()` and check a known-changed global before trusting results.

## The regeneration chain (corpus)

```
python normalise.py --all > corpus_verse.txt        # canonical rules (normalise.ps1 = transcription)
powershell -File make_corpus_blocks.ps1              # groups into the five folios
powershell -File splice_corpora.ps1                  # writes them into index.html, with backup + asserts
```

`sonnets.txt` (Gutenberg #1041), `corpus_verse.txt` and `corpus_blocks.js` are gitignored as
regenerable.

## Still open

- ~~The Concord Cam paragraph in README quotes strike statistics measured before all of this~~ **Re-measured
  2026-08-17 (home machine, harness seed 7, 20 sheets/arm, tier 6, T=0.85): violations 4.7 → 0.0 per sheet,
  fidelity 77.3 → 75.2, rhyme 56.4 → 59.3, ~120 strikes/sheet at 99.5% of draws. README updated; the press
  tally now reports struck mass rather than count.**
- PART-conditioned unigram backoff (the sense-preserving fallback) was explained and
  deliberately deferred, not rejected.
- The schooling interlock table in README was measured with the previous (catapult) rhyme
  cam AND the old seven-notch scale; it needs re-running across the five notches.

## The schooling rescaled, 2026-08-18

The lever went from seven notches (5/10/15/20/25/30/154) to **five: 15 / 40 / 80 / 115 / 154**.
The old scale spent six notches inside the first fifth of the sequence and then leapt from 30
to 154 — four times the library in one step — so the last notch was incomparable with the rest.
Now the registers climb in even strides:

| notch | sonnets | verse lines | sorts | wheels | licence pairs |
|---|---|---|---|---|---|
| 0 | 15 | 210 | 738 | 4,555 | 11 |
| 1 | 40 | 560 | 1,443 | 11,063 | 33 |
| 2 | 80 | 1,120 | 2,168 | 20,482 | 77 |
| 3 | 115 | 1,611 | 2,666 | 28,133 | 116 |
| 4 | 154 | 2,155 | 3,216 | 36,582 | 151 |

The thirty hand-curated sonnets are kept as the first two notches; later notches fill in
numeric order. `CORPUS_E`/`CORPUS_F` were deleted; the constants are now CORPUS, _B, _C, _D,
_ALL, and `FOLIOS.length` drives every clamp (no more hard-coded `Math.min(6, …)`).

**Tier indices shifted**: what was `tier:6` in the harness is now `tier:4`. Anything quoting
"tier 6" from before this date means the full folio and should read 4.

New teaching demos, one per notch, measured (probability of the wanted word at boiler 0.95):
"not marble , nor the gilded" → *monuments* (— / 90 / 90 / 88 / 88); "make war upon this
bloody" → *tyrant* (— / — / 88 / 88 / 88); "wherefore with infection should he" → *live*
(— / 0 / 0 / 92 / 92); "two loves i have of comfort and" → *despair* (— / — / — / 0 / 85).
The 0% entries are the instructive ones: the sort is cut but no road leads to it.
