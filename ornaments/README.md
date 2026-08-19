# The ornaments

Victorian vegetal trim for the brass of both engines, added 2026-08-18.

## Where they came from

Chris set the glyphs in Illustrator from the **Adorn** family (Ornaments / Frames / Banners),
converted them to outlines, and exported one sheet: `src/sheet.svg` (491×407, 21 paths). Twenty
of those paths were cut out by bounding box into `svg/*.svg` — one path per file, `fill="currentColor"`,
tight viewBox — and named for what they are. (Path 8 on the sheet duplicated path 4 and was dropped.)
Earlier per-glyph exports were `<text>` elements referencing the fonts and were useless off-machine;
if you ever re-export, *Type ▸ Create Outlines* first, or set *Fonts: convert to outlines* in the SVG dialog.

## What is placed where (both pages unless noted)

| ornament | role | how |
|---|---|---|
| `corner-tl/tr/bl/br` | masthead spandrels, inboard of the screws | `<svg class="orn corner …">` in `.masthead`; hidden ≤700px |
| `rule-scroll` | the rule under the title (replaces the 2px gradient) | inside `.masthead .rule` |
| `feather-right` ×2, one mirrored | gilt flanks on every station name, 22px, plumes outward | either side of `h2.stname` in `.sthead`; hidden ≤560px |
| `finial` | divider between the desk and Station I; again before the appendix (Bard) | `.orn-div` between plates |
| `rule-dot` | the colophon's rule | `.orn-rule` above `<p class="colophon">` |
| `curl-small` | bookplate curls, two corners of every paper plaque | CSS `.plaque::before/::after`, data URI baked in the stylesheet |
| `banner-a` + `banner-d` | ribbon cartouche round *The Sonnet Press* (Bard only): a is the left end, d the right, and a stretched two-rule band (inline `<svg preserveAspectRatio="none">`, rules at y 17.7–19.5 and 37.6–39.3 → 19.1–20.9 and 38.9–40.7 of 58.4, measured at the cut edges) runs under the lettering | `.cartouche` in the press `.sthead`, in place of the feathers |

Unused for now, kept for later: `leaf`, `swirl-small`, `swoosh-single`, `swoosh-double`,
`feather-left`, `feather-upright`, `rule-diamonds`, `banner-b`, `banner-c` (b is another right end, but its cut edge is buried under its own foliage, so d was used).

## How they are struck

One inline `<svg style="display:none">` sprite of `<symbol id="o-…">` sits directly after
`<div class="cabinet">` in each page (~72 KB, from `sprite.html`); every placement is
`<svg class="orn" viewBox="0 0 W H"><use href="#o-name"/></svg>`. Colour comes from `currentColor`,
so the plate's `--engrave` ink and the drop-shadow highlight the portraits use make them read as
cut into the brass; the japanned station bands use the gilt of their lining instead.

**The outer `<svg>` must carry `viewBox="0 0 W H"`.** Without one it has no aspect ratio and falls
to 300×150; and the symbols' own viewBoxes have offset origins (they were cut from a sheet), so
copying those onto the outer element puts the drawing outside the window. `make_sprite.ps1`
prints the numbers.

## Regenerating

```
powershell -File ornaments/make_sprite.ps1     # sprite.html, curl.uri.txt, proof.html from svg/*.svg
```
Then paste the sprite block over the one in each page by hand. Open `proof.html` to see every
ornament on brass and on paper.

## The resync

The ornament CSS, the sprite and every shared placement live *outside* the Bard's grafted regions,
so `resync_from_ale.py` carries them from the parent. The Bard-only pieces (press cartouche, the
finial before the appendix) sit inside the press graft — the graft's start marker was moved to
`<div class="orn-div press-div"` for exactly that reason. Edit both pages identically for anything shared.

## Later placements (2026-08-18, same day)

| ornament | role | how |
|---|---|---|
| `swirl-small` | the masthead fleuron, in place of the typographic ❦ | inside `.masthead > .orn`, 20px |
| `swoosh-single` | the Bard's desk band, in place of its ❦ | `.deskband .dband`, 11px gilt |
| `rule-diamonds` | the divider above every plaque's fine print (replacing a dotted border), and the head-rule under the fair-copy sheet's title | CSS mask on `.plaque .fine::before` and `#sheet .stitle::after`, painted in `currentColor` so it takes the plaque's own ink; the data URI lives in `--orn-diamonds` on `:root` |

The little polished panels (`.ophelp`, `.opts`, `.masthead .sub2`) are **riveted**: `--rivet-l` / `--rivet-r`
on `:root` are domed-brass radial gradients (highlight, body, dark rim) laid as the first two background
layers, one each side, vertically centred; the panels carry 24px side padding to clear them.

Still unused: `leaf`, `swoosh-double`, `feather-upright`, `feather-left`, `banner-b`, `banner-c`.

## The manicule and the engine rail (2026-08-19)

| ornament | role | how |
|---|---|---|
| `hand-right` | the printer's pointing hand, at the left of the buttons that *do* something: **Begin the Demonstration** (both engines) and **Set the Press Running** (Bard) | `<svg class="orn manicule">` inside `.btn`; `.btn:has(.manicule)` becomes an inline-flex row with a 9px gap |
| `hand-up` | cut and kept, not yet placed | — |

**The engine rail** (`.engrail`) sits on the masthead plate between the fine print and the station
legend, so a visitor can change engines or step behind the page without hunting for the foot of it.
It is built as one more riveted panel and holds two sections divided by a brass line: *Choose the Engine*
(Babbage -> Language Engine, Shakespeare -> Bard Engine) and *Behind the Page* (Lady Lovelace ->
`educators.html`, Markov -> `about.html`).

Each switch is a 46px brass disc carrying an engraved face, filtered to sepia and multiplied into the
brass so it reads as struck rather than pasted on. The engine you are looking at is **pushed in**:
`.eswitch.on` drops 2px, darkens, and takes an inset shadow instead of a dome, its label goes bold, and
it is a `<span>` (not a link) with `aria-current="page"` - the others stand proud and are `<a>`.
Paths differ per page (plain names and `bard/…` from the root, `../…` from the Bard), so this block is
**not** identical between the two files; everything else about the rail is. Below 480px the rail stacks
and the division turns from a wall into a floor.

**Markov** (`portrait-markov.svg`) is unlike the other portraits: dark line-work on an **opaque white
card**, not dark-on-transparent. `mix-blend-mode: multiply` is what makes it usable - white multiplies
to nothing, so the card vanishes into the brass and only the engraving remains. It must therefore NOT
take the other discs' `brightness(.42)`, which would grey the card and wash out the whole disc: class
`.card` gives it `sepia(1) saturate(.6) contrast(1.5) brightness(1.05)` and `transform: scale(1.35)`,
the engraving sitting small inside wide margins. The same portrait stands beside the title on
`about.html`, as Shakespeare does on the Bard, with the same multiply treatment.
## The sub-pages, and the nickel rims (2026-08-19)

`about.html` (the mathematics) and `educators.html` now carry the engines' own plate treatment: four
screws (`.screws`, corner radial-gradients over the brass), acanthus spandrels at the corners, and the
scroll rule beneath the title. They take `sprite-lite.html` (~34 KB: the four corners and `rule-scroll`
only) rather than the full case, pasted after `<div class="wrap">`. `make_sprite.ps1` builds it alongside
the big one.

A portrait stands beside each title as Shakespeare does on the Bard: **Markov** on the mathematics page,
**Lady Lovelace** on the educators' page. They need *different* treatments and this matters —

* Lovelace is a head-and-shoulders engraving on clear ground, so she takes the engines' masthead
  treatment (the plate's ink, raised highlight, no blend) and no crop.
* Markov is half-length on an opaque white card, so he keeps `mix-blend-mode: multiply` and is cropped
  to the bust with `object-fit: cover; object-position: 50% 14%`. Measured, not guessed: his ink sits at
  x 98–1061, y 104–1293 of 1121×1403, the head at x 340–884, y 104–604 — sampled by drawing the SVG to a
  canvas and scanning for dark pixels. Uncropped at title height his head reads far smaller than
  Shakespeare's.
* Below 560px the mathematics title stacks with the portrait above it; the forced `<br>` is hidden, and
  it is written `Mathematics <br> Behind` **with spaces** so hiding it does not weld the words together.

**The studs wear a nickel rim** — after the round keys of a classic typewriter. It is a gradient border:
the brass face is a `padding-box` layer, the rim a `linear-gradient(155deg, …)` `border-box` layer on a
3px transparent border, so it lights top-left and darkens bottom-right like turned metal. The pressed
switch keeps the rim but dulls it, and both keep a 1px dark line outside to seat them on the plate.