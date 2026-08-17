# Replace the seven corpus constants in index.html with the ones in corpus_blocks.js.
# The constants are NOT contiguous in the page -- the counting-engine definitions sit between the fourth
# folio and the fifth -- so each is replaced in place, by name, and nothing between them is touched.
# Backs up to index.html.bak. Asserts loudly rather than guessing.
$ErrorActionPreference='Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$page = Join-Path $here 'index.html'
$html = [IO.File]::ReadAllText($page, [Text.Encoding]::UTF8)
$blocks = [IO.File]::ReadAllText((Join-Path $here 'corpus_blocks.js'), [Text.Encoding]::UTF8)
$names = @('CORPUS','CORPUS_B','CORPUS_C','CORPUS_D','CORPUS_E','CORPUS_F','CORPUS_ALL')

# pull each new body out of corpus_blocks.js
$new = @{}
foreach($n in $names){
  $open = 'const ' + $n + '=`'
  $i = $blocks.IndexOf($open); if($i -lt 0){ throw "blocks: $n not found" }
  $i += $open.Length
  $j = $blocks.IndexOf('`;', $i); if($j -lt 0){ throw "blocks: $n unterminated" }
  $new[$n] = $blocks.Substring($i, $j - $i)
}

[IO.File]::WriteAllText((Join-Path $here 'index.html.bak'), $html, (New-Object System.Text.UTF8Encoding($false)))
$before = $html.Length
foreach($n in $names){
  $open = 'const ' + $n + '=`'
  $i = $html.IndexOf($open); if($i -lt 0){ throw "page: $n not found" }
  if($html.IndexOf($open, $i + 1) -ge 0){ throw "page: $n appears twice" }
  $s = $i + $open.Length
  $e = $html.IndexOf('`;', $s); if($e -lt 0){ throw "page: $n unterminated" }
  $html = $html.Substring(0, $s) + $new[$n] + $html.Substring($e)
}
if(-not $html.Contains("const FIN='")){ throw 'the counting-engine definitions were lost -- aborting' }
if(([regex]::Matches($html,'const CORPUS')).Count -ne 7){ throw 'corpus count wrong after splice' }
[IO.File]::WriteAllText($page, $html, (New-Object System.Text.UTF8Encoding($false)))
"page $before -> $($html.Length)"
