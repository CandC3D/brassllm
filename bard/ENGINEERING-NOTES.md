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

## Current measured state — SUPERSEDED 2026-08-19, see "The rhyme scheme, mended" below

~~fidelity ~77% · derailment ~14% · rhyme ~76% · mean line 8.8 words~~ → after the fellowship recut and
with the Subject Cam standing: fidelity ~68–72 · **rhyme pairs ~86%, roughly a third of sheets fully
clean and another third one miss short** · line closes ~33% rhyme, ~18% engine's own ⏎.

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

## The ornaments, 2026-08-18

Victorian vegetal trim on the brass of **both** engines — see `ornaments/README.md` for the
full placement table. Chris outlined the glyphs (Adorn Ornaments / Frames / Banners) in
Illustrator; the sheet was cut into `ornaments/svg/*.svg`; both pages carry an inline
`<symbol>` sprite (~72 KB) directly after `<div class="cabinet">`, struck with
`<svg class="orn" viewBox="0 0 W H"><use href="#o-…"/></svg>`. Masthead spandrels, a scroll
rule under the title, gilt feathers flanking every station name, a finial between desk and
works, bookplate curls on the plaques (CSS data URI), a rule over the colophon; the Bard's
appendix wears a ribbon cartouche (banner-a, a stretched band, banner-d) round *The Sonnet Press*.

Traps: (1) the outer `<svg>` must carry `viewBox="0 0 W H"` — without it there is no aspect
ratio, and copying the symbol's own offset viewBox puts the drawing outside the window;
(2) everything shared is outside the Bard's grafts and comes from the parent on resync — edit
both files identically; the press pieces are inside the press graft, whose start marker in
`resync_from_ale.py` now reads `<div class="orn-div press-div"` so the finial before the
appendix survives; (3) `ornaments/make_sprite.ps1` regenerates the sprite/URI/proof — paste by hand.

## The tape and the sprocket roller, 2026-08-18

Station VIII redrawn in both engines. The mangle is now a sprocket roller seen from above, fixed at the
right end of the FIRST row; the tape issues from under it right-to-left, newest word at the roller, and
older rows travel downward. The roller's pin rings sit at the ENDS of the roller on the tape's own hole
gauge (16px, phase measured — see the CSS comment) and turn only while a word feeds through
(`.mangle.feed`, set in `stampAction`), turning right-to-left.

**The layout trick, so nobody "fixes" it:** CSS cannot break lines from the END of a text, and that is
what a tape hanging from a printer needs (last row full and anchored at the roller, first row the
partial one). So `#tapewrap` is mirrored with `transform:rotateY(180deg)`, words are PREPENDED to
`#tape` (`insertBefore(sp, firstChild)`), and every `.stamp` is mirrored back. Consequences: DOM order
is newest-first (`ENGINE.tape` reverses it); every transform in the stamp/thud/inkin keyframes must keep
`rotateY(180deg)` or the word flips for a frame; the stamper is appended to `.tapeworks` (unmirrored),
not `#tapewrap`. Wrapping still works — that was the point; a single scrolling strip was tried and rejected.

`.claude/serve.ps1` + `.claude/launch.json`: a PowerShell static server so the browser pane can run the
page live (file:// snapshots strip scripts). No Python/Node needed.

## The Subject Cam, 2026-08-18

A sixth cam on the press, at Chris's request (after Maillardet's automaton, whose cams held each poem to
its subject). **What it reads:** the card's full words (`subjectOf`: not STOPW, not `SUBJ_AUX`, not points,
must be a sort the wheels have counted). **What it knows:** `coocc` only — the shared-verse-line counts the
Attention station reads; the subject's *company* (`companyOf`) is every sort with a shared line, plus the
subject words themselves. **What it does:** at every draw where the drum offers any company, scale the
company up to `SUBJECT_SHARE` of the drum's remaining mass (same lever pattern as ROADS_SHARE; done on the
un-renormalised q so the `cut` bookkeeping holds). It never adds a sort; with an unknown card it idles and
the tally says so. Applied after the Concord strike and before the Rhyme Cam, so the rhyme goal's half-drum
still wins the last word.

**Revised the same day after Chris's samples** (*shall* five times in one sheet): the small words and
SUBJ_AUX are excluded from the company as well as the subject; and the share is scaled by company size,
`SUBJECT_SHARE * min(1, company.size/SUBJECT_FULL)` (0.20, 100). Reason, measured: an unscaled fifth on a
one-word subject with 17 fellows cost fidelity 75 -> 60 for on-subject 5 -> 33; a flat cap on the multiplier
(3-6x) did nearly nothing, 10x held half as well as the scaled share. Final (12 sheets, seed 7, tier 4,
T=0.85, all cams; off -> on, fidelity in brackets): compare-thee 5->9 (75->74) · summer-day 21->37 (75->67) ·
mistress'-eyes 28->44 (75->69) · count-the-clock 8->13 (75->76) · love 39->49 (75->72). Rhyme within noise.
The tally reports subject words, tilted/offered draws, and on-subject count. `press_harness.js` re-synced
(cams.subject, subject{} block: share, full, companySize, tilted, tiltDraws, onSubjectPct).
## Legibility of small text on brass, 2026-08-18

Chris flagged the masthead fine print and the desk's option labels as hard to read. Measured (canvas
sample of the plate's own 168° gradient under each element, WCAG contrast): `.masthead .sub2` **2.03:1**,
`.opts label` **2.55:1**, `.masthead .sub` 3.27, `.ophelp` 3.90 — all short of 4.5.

Two causes: (1) `.plate label` carries the engraved light halo, which smears text below ~14px, and
(2) the plate's mid-band is bright (≈rgb(140,108,43)), where **even pure black reaches only 4.29:1** —
ink alone cannot fix it. So: new `--engrave-deep: #1a1204` for small text; halo removed from `.opts label`;
sizes up (sub2 13→14, opts 13→14, ophelp 13.5→14, deskl 11.5→12.5, boilerchip 12→12.5, and in the Bard
schooll 11→12.5, rlab 9.5→10.5, folmarks 9.5→10.5); and a **polished-brass panel** (a ~20% warm-white
wash with an inset top highlight) behind the three blocks that sit on the darkest band — the masthead
fine print, `.ophelp`, and `.opts`. Now: sub 4.78 · sub2 5.53 · ophelp 7.93 · opts 5.35 · deskl 5.99 ·
legend 4.80.

**Workstation trap (bit me three times):** in a PowerShell replacement string, segments after a
`` "`r`n" `` escape are silently dropped in this environment — the earlier `#tapewrap` rule, the mangle
comment and these two rules were all truncated to their first line, leaving unclosed CSS. Build newlines
as `$NL=[string][char]13+[string][char]10` instead, and always assert `{` vs `}` counts after writing.

## The Concord Cam, second edition (home machine, 2026-08-18)

Chris asked for subject–verb–object agreement; three options were laid out (A: number/valency tables from the wheels; A+B with the object-wanted rule; C: a subject–predicate tracker across the line) and he chose A+B by his two tests — keeps the model true to itself without pretending, and is what a 19th-century brass engineer might attempt. Built: `NUM`/`VAL`/`VFORM` in `buildParts()`, rules F and G in `concordStrike`, transitive-verb-last added to `unsatisfied()`. Coverage thin by design (40 t-verbs, 434 plurals at tier 4). Measured seed 7 / 20 sheets / tier 4: number violations 3→0, fidelity 74.1→72.4, rhyme 57.9→60.7. C (the tracker) was deliberately NOT built — it is a grammar, not a cam. `press_harness.js` needs no change (it calls concordStrike). The rule chip and the plaque's Concord paragraph carry the second edition; strike-mass tally unchanged.

## Two more traps, met on the home machine (2026-08-18)

- **`strip_quotes` in normalise.py struck closing elisions** — *th' executor* → bare `th`, *th' inviting* likewise — because it exempted only possessive-plural `s'`. Now exempts the short elision heads (`ELIDE_TAIL`: th, o, t, i, y, wi, gi, ha, ne). Also `re-survey` was hyphen-split into an orphan `re`; now `re-` prefixes are joined before the split. Three corpus lines changed; sorts 3,216, wheels 36,580.
- **On a machine WITH Python, the PowerShell chain still runs under PowerShell 5.1** and read the BOM-less UTF-8 `corpus_verse.txt` as ANSI: one em-dash (Sonnet 17) came through as U+FFFD, and `splice_corpora.ps1` wrote the corpus block with LF into a CRLF file. Both caught by diffing before commit (`git diff | grep '^[-+]'` should show only the intended lines; `grep -c $'ï¿½'` should be 0; check CRLF/LF counts). Fixed by hand this once. If the chain must run here again, write `corpus_verse.txt` with a UTF-8 BOM, or splice with Python `newline=''`.
- The goal-first Rhyme Cam's ✗s are **not** lonely goals: only 3 of 1,020 line-final words lack any rhyme fellow (*her, both, growth*). The misses are unreachable goals — no counted road within the measure — which is the disclosed limit, not a defect. Do not 'fix' by filtering goals to fellowed words.

## The Addressee Cam (the seventh), 2026-08-19

Chris's brief: a seventh cam "invented in a fit of pique at the nonsensical outputs", forcing the poem to
one of Shakespeare's three addressees, interlocking with the Subject Cam — the Victorians' last attempt to
get a masterpiece out of the machine.

**What it is told** (the only external fact): which sonnets belong to whom — Fair Youth 1–126, Dark Lady
127–152, Rival Poet 78–86, the Rival group held out of the Youth's so the three are disjoint; 153–154
excluded. This is a fact of the printed book, of the same kind as the rhyme scheme, which the press already
uses. **What it counts for itself:** the vocabulary. `addresseeWords(key)` tallies content words inside and
outside the group and keeps those with count ≥ `ADDR_MIN` (2) and a likelihood ratio ≥ `ADDR_LIFT` (1.6),
i.e. oftener there than elsewhere. Nothing about who these people were enters the machine — and it finds,
unaided, *muse / verse / pen / taught / dumb / ignorance* for the Rival Poet, *summer / buds / eternal /
shade / grow'st* for the Youth, *conscience / faults / soul / proud / poor* for the Dark Lady.

**The interlock:** with the Subject Cam also thrown, the target narrows to `company ∩ addressee` when that
holds ≥ 12 words, else the addressee's set alone; the tally reports which. Both cams then tilt in turn, so
they compound. Lever `ADDR_SHARE` = 0.22, scaled by set size against `ADDR_FULL` = 90 — the same bargain,
and the same scaling fix, as the Subject Cam.

**Measured** (harness, 10 sheets, seed 11, tier 4, T = 0.85, all cams; `addressee.onAddresseePct` = share
of the sheet's full words distinctive to the chosen voice):

| card | cam | fidelity | on-addressee |
|---|---|---|---|
| *my mistress' eyes* | off | 72.4 | — |
| | Dark Lady | 66.3 | **23.9** |
| | Fair Youth | 63.9 | 17.2 |
| | Rival Poet | 65.9 | 11.8 |
| *shall i compare thee to a summer day* | off | 67.7 | — |
| | Fair Youth | 64.6 | **24.4** |
| | Dark Lady | 64.1 | 15.3 |

The matched voice always scores highest, which is the cam working; the mismatched voice still tilts hard,
which is the cam not knowing it is wrong. Cost 3–6 points of quotation; rhyme within noise.

**By schooling** (sonnets read / distinctive words): notch 0 — dark 4/26, youth 11/19, rival **0/0**;
notch 1 — 6/46, 34/35, 0/0; notch 2 — 6/48, 74/26, 0/0; notch 3 — 6/46, 100/93, 9/71; notch 4 — 26/170,
117/273, 9/73. Two teaching results fell out of this and are on the plaque: **the Rival Poet does not exist
for the engine below 115 sonnets** (the cam idles and says so), and **the Fair Youth's vocabulary shrinks**
from 35 words at 40 sonnets to 26 at 80 — by then 74 of 80 sonnets are his, so there is nothing left to be
distinctive against. A word is only distinctive compared with something.

The cam is **off by default**: it is the odd one out, it costs quotation, and the argument is stronger when
the visitor throws it themselves. UI: chip in the rule-book plus a three-stud `fieldset.addrsel` selector,
dead metal (`opacity .42`) until the cam is thrown; seventh disc on the camshaft, one dwell of a quarter
turn. All of it sits inside the resync's grafted press regions (JS 4702–5279, CSS 674–738), so
`resync_from_ale.py` carries it — checked, not assumed.

### The echo, and "no second helping" (same day, from Chris's sample)

Chris's Fair Youth sheet repeated *day arising* three times and *summer's* four. I assumed the cam was
hammering single words and nearly "fixed" that — but measuring first showed **single-word echo was not
worse with the cam on** (4.30 per 100 content words off, 3.73 on). The real regression was in **phrases**:
bigram repetition ran **0.76 per 100 with the cam off and 2.16 with the Fair Youth thrown**, with a phrase
appearing three times in a sheet. A small tilt-set keeps steering back onto the same few high-probability
roads.

Fix: **a word the cam has already laid on the sheet drops out of its tilt-set** (`laid`, per sheet).
Nothing is forbidden — the wheels may draw it again, and do — the cam simply stops pushing the same word
twice. Measured after (12 sheets, seed 23, tier 4, T = 0.85):

| arm | fidelity | on-addressee | word-echo /100 | phrase-echo /100 | worst phrase |
|---|---|---|---|---|---|
| summer's day, cam off | 68.4 | — | 4.30 | 0.76 | 2× |
| …Fair Youth, before | 67.4 | 21.0 | 3.73 | **2.16** | **3×** |
| …Fair Youth, after | 67.5 | 22.5 | 2.23 | **0.95** | 2× |
| mistress' eyes, cam off | 66.4 | — | 3.73 | 0.81 | 2× |
| …Dark Lady, after | 63.6 | 25.0 | 2.47 | 1.22 | 2× |

The excess phrase-echo is gone at no cost to the cam's hold (21.0 → 22.5) or to quotation. `press_harness.js`
now reports `echo{per100Words,typesPerSheet,worst,worstWord}` so this stays measurable.

**Not done, and deliberately:** the card's own words are not seeded into `laid`, so the cam may still push a
word the card supplied (*summer's* recurs in the sample sheet — drawn by the wheels, not pushed). Worth a
measurement if it ever grates.

**Workstation trap, again:** `Rep 'a'+$NL+'b' (…)` in PowerShell does NOT concatenate in argument position —
it silently matched and replaced the wrong text, deleting `if(isWordId(id)){…}` and leaving
`parts.join(+' '+)`, which broke the whole page. Always parenthesise: `Rep ('a'+$NL+'b') (…)`, or use the
Edit tool for anything multi-line.

**Layout, at Chris's direction:** the bank above is the six cams (a tidy 3×2), and the seventh stands
below them in its own bordered box together with its three studs — the cam centred, a hairline divider,
then the caption on its own line and the three studs in a single centred row. The `<fieldset>` became a
`div.addrsel` holding `div.addrrow[role=radiogroup]`, because a fieldset with a legend will not lay out
as a centred flex column. Only the studs dim when the cam is up; the cam itself stays lit, being the
thing you throw. **No more cams are planned** — the bank is closed at seven.

## The rhyme scheme, mended — the fellowship and the closing squeeze, 2026-08-19

Chris: "my main concern is that the rhyme scheme is broken in almost every generated text." True by
arithmetic: at the measured ~50–75% per pair, seven pairs a sheet means a clean sheet is somewhere
between 1-in-8 and 1-in-16,000. Measured before touching anything (40 sheets, 4 cards, 280 pairs,
seeds 31/38/45/52): **50.4% of pairs passed, 0 clean sheets in 40.**

**Diagnosis first — the split that decided everything.** Of 139 missed pairs, only **14 (10%) were
goalless** (no rhyme-fellow in the drum at all); **125 (90%) had a fellow and never landed it.** So it
was the walk, not the vocabulary.

**The Macbeth question (asked and answered).** Chris proposed feeding Macbeth to the engine for extra
rhymes; extended to The Taming of the Shrew and Twelfth Night, and (Chris's catch) A Lover's Complaint —
which is NOT in the corpus (Gutenberg №1041 is the sonnets alone) despite sharing the 1609 quarto.
Line-final vocabularies: Macbeth 1,200 / Shrew 1,192 / Twelfth Night 988 / ALC 278. Of the 11 distinct
goalless words (thou ×3, world ×2, putt'st, firm, poor, praises, wrinkles, winter, shall, off, broad),
Macbeth covers 2, Shrew 2, Twelfth Night 1, ALC 0, **all four together 3**. Ceiling of the whole idea:
~4 of 139 misses. **Rejected on the numbers** — recorded on the plaque as "What would not have fixed it."
Play texts live in `bard/_plays/` (gitignored, regenerable: PG 1533/1508/1526 + ALC sliced from PG 100).

**The recut, in two moves** (both engine and harness):
1. **The fellowship** (replaces steps 1–3 as proposed — steering at the whole class subsumes reachable-goal
   choice and goal re-drawing). `drawGoal` → `rhymeFellows(target)`: ALL rhyme-fellows in the drum, tiered
   (LINE_FINALS members; whole catalogue as fallback). `roads` = `fellowRoads(fell)`, one pass over the
   bigram book checking the smaller side. The boost goes to every fellow one counted road from the current
   word, not to one chosen goal. A ✗ is still known before the line's first word (fellowship empty).
   Alone this bought only 50.4 → 53.9% — because a fellow stood one road away at only ~23% of closing
   draws (harness `rhymeCam.boosts`: 80 in 1,201 draws). The walk needed force, not just breadth.
2. **The closing squeeze**: the cam bears down as the measure runs out. Roads share raised to
   max(ROADS_SHARE, 0.75) from `words >= MAXW-3`; the fellows' boost raised from 0.5 to **0.92** from
   `words >= MAXW-2`. Variant sweep (same 280 pairs; fid = mean fidelity):
   V1 squeeze@-2/.6, boost .85@-1 → 70.7% / 6 clean / fid 69.8 · V2 @-3/.6, .85@-2 → 76.4 / 5 / 69.1 ·
   V3 @-2/.75, .92@-1 → 76.8 / 7 / 70.2 · **V4 @-3/.75, .92@-2 → 85.7 / 14 / 68.8 (chosen)** ·
   V5 @-2/.85, .97@-1 → 81.4 / 9 / 69.2 · V6 @-4/.75, .95@-2 → 87.9 / 16 / 67.5 (curve flat: rejected).

**Result: pairs 50.4% → 85.7%; clean sheets 0 → 14 of 40, one-miss another 15; cost ~1.5 points of
quotation.** First live run on the page: a clean sheet (5 true + 2 licence, 0 ✗). Exhibit text updated:
Rhyme Cam chip, "How the Rhyme Cam works" (now tells the recut story with the numbers), new "What would
not have fixed it" marginalia, ROADS_SHARE comment (the old single-goal sweep figures are labelled as
predating the fellowship; the lever now matters little — the squeeze governs).

**For the future:** the remaining ~14% of missed pairs are roughly half goalless (irreducible without
new vocabulary that measurement says no play supplies) and half lines that close early by `term`/dangle
or genuinely cannot thread a road in time. Do not chase 100%: Shakespeare's own licences are marked with
an asterisk, and a press that never missed would out-rhyme the Bard — the occasional honest ✗ is part of
the exhibit's argument.

---

## Index of 2026-08-19 (one day's work, in order — for whoever reads this next)

1. **The Addressee Cam** (§ above): seventh cam, off by default. Told only the quarto's division
   (Youth 1–126, Dark Lady 127–152, Rival 78–86); counts each voice's vocabulary itself by likelihood
   ratio; interlocks with the Subject Cam (intersection when ≥12 words survive). Its two teaching facts:
   the Rival Poet does not exist below 115 sonnets, and the Youth's vocabulary *shrinks* at notch 2
   because there is nothing left to be distinctive against.
2. **"No second helping"** (§ above): Chris's sample sheet echoed phrases; measurement showed the cam
   tripled *bigram* echo (word echo was fine — the first hypothesis was wrong, measure before fixing).
   A word the cam has laid drops out of its tilt-set. Echo back to baseline, hold undiminished.
3. **Rule-book layout**: six cams in the bank, the seventh centred in its own bordered box with its
   three studs (caption on its own line, studs in one row). The bank is **closed at seven** — Chris.
4. **The rhyme investigation** (§ above): "scheme broken in almost every sheet" → measured 50.4% of
   pairs, 0/40 clean. Split the misses: 90% had a fellow and couldn't reach it. Macbeth/Shrew/Twelfth
   Night/A Lover's Complaint measured as vocabulary donors: 3 of 11 goalless words covered, ceiling
   ~4 of 139 misses — **rejected on the numbers**, recorded on the plaque as the Professor's
   instructive failure.
5. **The fellowship + closing squeeze** (§ above): Rhyme Cam steers at every fellow, bearing down as
   the measure runs out (0.75 roads / 0.92 boost in the last words). **Pairs 50.4 → 85.7%, clean
   sheets 0 → 14/40**, ~1.5 points of quotation. Harness re-synced; exhibit text updated with the
   real numbers, including the honest account of the failed single-goal design it replaces.

Constants to know: `ROADS_SHARE` (mid-line, now minor) · squeeze 0.75 from `MAXW-3` and boost 0.92 from
`MAXW-2` (in the cam code, engine + harness, keep them identical) · `ADDR_SHARE`/`ADDR_FULL` 0.22/90 ·
`SUBJECT_SHARE`/`SUBJECT_FULL` 0.20/100 · `ADDR_LIFT`/`ADDR_MIN` 1.6/2.
