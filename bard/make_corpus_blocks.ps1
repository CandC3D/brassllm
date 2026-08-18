# Build the folio blocks (const CORPUS ... CORPUS_ALL) for index.html from corpus_verse.txt.
#   powershell -File make_corpus_blocks.ps1        -> writes corpus_blocks.js beside it
# The schooling's five notches hold 15 / 40 / 80 / 115 / 154 sonnets.  The thirty hand-curated
# sonnets of the old seven-notch lever remain the heart of the early notches; each notch then
# fills to its size in numeric order from the sonnets not yet included.
$ErrorActionPreference='Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$lines = Get-Content (Join-Path $here 'corpus_verse.txt') -Encoding UTF8
$son = @{}; $cur = 0
foreach($l in $lines){
  if($l -match '^#(\d+)$'){ $cur=[int]$matches[1]; $son[$cur]=New-Object System.Collections.Generic.List[string]; continue }
  if($cur -ne 0){ $son[$cur].Add($l) }
}
$D = [char]0x2014
$curated15 = @(18,151,14,130,116, 12,30,65,73,127, 29,33,60,97,147)
$curated30 = @(55,64,71,106,129, 1,15,27,66,87, 2,19,94,110,138)
$targets = @(
  @{name='CORPUS';     size=15;  head='/* the first folio ' + $D + ' the fifteen hand-picked sonnets (18, 151, 14, 130, 116; 12, 30, 65, 73, 127; 29, 33, 60, 97, 147).  All folios are cut by rule from the Gutenberg text (#1041) by normalise.py: verse lines kept, every point its own sort, the printer''s quotes struck, elisions kept */'},
  @{name='CORPUS_B';   size=40;  head='/* the second folio ' + $D + ' to forty: the other fifteen curated sonnets (55, 64, 71, 106, 129; 1, 15, 27, 66, 87; 2, 19, 94, 110, 138) and ten more in numeric order */'},
  @{name='CORPUS_C';   size=80;  head='/* the third folio ' + $D + ' to eighty, in numeric order */'},
  @{name='CORPUS_D';   size=115; head='/* the fourth folio ' + $D + ' to one hundred and fifteen, in numeric order */'},
  @{name='CORPUS_ALL'; size=154; head='/* the fifth folio ' + $D + ' the whole sequence of 1609 */'}
)
$included = New-Object System.Collections.Generic.HashSet[int]
$allNums = $son.Keys | Sort-Object
$sb = New-Object System.Text.StringBuilder
foreach($t in $targets){
  $ids = New-Object System.Collections.Generic.List[int]
  if($t.name -eq 'CORPUS'){ foreach($n in $curated15){ $ids.Add($n) } }
  if($t.name -eq 'CORPUS_B'){ foreach($n in $curated30){ $ids.Add($n) } }
  foreach($n in $ids){ [void]$included.Add($n) }
  foreach($n in $allNums){
    if($included.Count -ge $t.size){ break }
    if(-not $included.Contains($n)){ $ids.Add($n); [void]$included.Add($n) }
  }
  [void]$sb.Append($t.head + "`n" + 'const ' + $t.name + '=`' + "`n")
  foreach($id in $ids){ [void]$sb.Append("# $id`n"); foreach($l in $son[$id]){ [void]$sb.Append($l + "`n") } }
  [void]$sb.Append('`;' + "`n")
  "{0}: {1} sonnets this block, {2} cumulative" -f $t.name, $ids.Count, $included.Count
}
if($included.Count -ne 154){ throw "cumulative count $($included.Count), expected 154" }
[IO.File]::WriteAllText((Join-Path $here 'corpus_blocks.js'), $sb.ToString(), (New-Object System.Text.UTF8Encoding($false)))
"chars: $($sb.Length)"
