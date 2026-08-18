# make_sprite.ps1 -- rebuilds sprite.html (the <symbol> case struck into both pages), the plaque-curl data URI,
# and proof.html (every ornament on brass) from ornaments/svg/*.svg.  ASCII-only source; PS 5.1.
# The sprite is pasted by hand into analytical-language-engine.html and bard/index.html directly after
# <div class="cabinet"> -- it is NOT wired in automatically; run this, then replace the block in each page.
$ErrorActionPreference='Stop'
$dir=Join-Path $PSScriptRoot 'svg'
$enc=New-Object Text.UTF8Encoding($false)

# the symbols the pages actually strike (the rest stay in svg/ for later)
$use=@('corner-tl','corner-tr','corner-bl','corner-br','rule-scroll','feather-left','feather-right','finial','rule-dot','banner-a','banner-d')
$sb=New-Object Text.StringBuilder
[void]$sb.Append('<svg xmlns="http://www.w3.org/2000/svg" style="display:none" aria-hidden="true"><!-- the ornament case: cast once, struck wherever the page wants a flourish (ornaments/svg, from the Adorn sheet) -->')
foreach($n in $use){
  $s=[IO.File]::ReadAllText("$dir\$n.svg"); $vb=[regex]::Match($s,'viewBox="([^"]*)"').Groups[1].Value; $d=[regex]::Match($s,' d="([^"]*)"').Groups[1].Value
  [void]$sb.Append('<symbol id="o-'+$n+'" viewBox="'+$vb+'"><path fill="currentColor" d="'+$d+'"/></symbol>')
}
[void]$sb.Append('</svg>')
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'sprite.html'),$sb.ToString(),$enc)
"sprite.html  $($sb.Length) bytes"

# NOTE for whoever strikes a symbol: the outer <svg class="orn"> MUST carry viewBox="0 0 W H" (W,H from the
# symbol's viewBox) or it has no aspect ratio and falls to 300x150. Several symbols have offset viewBox origins;
# the outer one is always 0 0.

# the plaque curl, as a CSS data URI (used by .plaque::before/::after; ink #8a7550 baked in)
$s=[IO.File]::ReadAllText("$dir\curl-small.svg"); $vb=[regex]::Match($s,'viewBox="([^"]*)"').Groups[1].Value; $d=[regex]::Match($s,' d="([^"]*)"').Groups[1].Value
$svg='<svg xmlns="http://www.w3.org/2000/svg" viewBox="'+$vb+'"><path fill="#8a7550" d="'+$d+'"/></svg>'
$u=$svg.Replace('"',"'").Replace('#','%23').Replace('<','%3C').Replace('>','%3E')
"curl data URI  $($u.Length) bytes  (paste into .plaque::before/::after background)"
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'curl.uri.txt'),"url(`"data:image/svg+xml,$u`")",$enc)

# proof sheet
$pb=New-Object Text.StringBuilder
[void]$pb.Append('<!doctype html><meta charset="utf-8"><title>Ornament proof</title><style>body{background:#191009;font-family:Georgia,serif;padding:20px}.plate{background:linear-gradient(168deg,#d9b563 0%,#b08b3e 36%,#8a6a2a 74%,#a8823a 100%);border-radius:14px;padding:20px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}.c{text-align:center;color:#43310f;font-size:11px;letter-spacing:.1em}.c svg{height:56px;width:auto;max-width:100%;color:#43310f;filter:drop-shadow(0 1px 0 rgba(255,242,196,.55)) drop-shadow(0 -0.5px 0 rgba(0,0,0,.25))}.paper{background:linear-gradient(175deg,#f2e8cf,#e4d5b3);margin-top:20px;border-radius:10px;padding:20px;display:flex;gap:30px;align-items:center;justify-content:center}.paper svg{height:40px;color:#5c4c33}</style><div class="plate">')
Get-ChildItem "$dir\*.svg" | ForEach-Object { [void]$pb.Append('<div class="c">'+[IO.File]::ReadAllText($_.FullName)+'<br>'+$_.BaseName+'</div>') }
[void]$pb.Append('</div><div class="paper">')
foreach($n in 'corner-tl','curl-small','leaf','swirl-small','rule-dot'){ [void]$pb.Append([IO.File]::ReadAllText("$dir\$n.svg")) }
[void]$pb.Append('</div>')
[IO.File]::WriteAllText((Join-Path $PSScriptRoot 'proof.html'),$pb.ToString(),$enc)
"proof.html written"
