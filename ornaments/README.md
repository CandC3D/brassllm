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
| `feather-left/right` | gilt flanks on every station name | either side of `h2.stname` in `.sthead`; hidden ≤560px |
| `finial` | divider between the desk and Station I; again before the appendix (Bard) | `.orn-div` between plates |
| `rule-dot` | the colophon's rule | `.orn-rule` above `<p class="colophon">` |
| `curl-small` | bookplate curls, two corners of every paper plaque | CSS `.plaque::before/::after`, data URI baked in the stylesheet |
| `banner-a` + `banner-d` | ribbon cartouche round *The Sonnet Press* (Bard only): a is the left end, d the right, and a stretched two-rule band (inline `<svg preserveAspectRatio="none">`, rules at y 17.7–19.5 and 37.6–39.3 → 19.1–20.9 and 38.9–40.7 of 58.4, measured at the cut edges) runs under the lettering | `.cartouche` in the press `.sthead`, in place of the feathers |

Unused for now, kept for later: `leaf`, `swirl-small`, `swoosh-single`, `swoosh-double`,
`feather-upright`, `rule-diamonds`, `banner-b`, `banner-c` (b is another right end, but its cut edge is buried under its own foliage, so d was used).

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
