# Build the seven folio blocks (const CORPUS ... CORPUS_ALL) for index.html from corpus_verse.txt.
#   powershell -File make_corpus_blocks.ps1        -> writes corpus_blocks.js beside it
# The folio membership below is the schooling lever's fixed choice; the seventh takes the rest.
$ErrorActionPreference='Stop'
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
$lines = Get-Content (Join-Path $here 'corpus_verse.txt') -Encoding UTF8
$son = @{}; $cur = 0
foreach($l in $lines){
  if($l -match '^#(\d+)$'){ $cur=[int]$matches[1]; $son[$cur]=New-Object System.Collections.Generic.List[string]; continue }
  if($cur -ne 0){ $son[$cur].Add($l) }
}
$D = [char]0x2014
$folios = @(
  @{name='CORPUS';    ids=@(18,151,14,130,116); head='/* the first folio ' + $D + ' sonnets 18, 151, 14, 130, 116.  All seven folios are cut by rule from the Gutenberg text (#1041) by normalise.py: verse lines kept, every point its own sort, the printer''s quotes struck, elisions kept */'},
  @{name='CORPUS_B';  ids=@(12,30,65,73,127);   head='/* the second folio ' + $D + ' sonnets 12, 30, 65, 73, 127 */'},
  @{name='CORPUS_C';  ids=@(29,33,60,97,147);   head='/* the third folio ' + $D + ' sonnets 29, 33, 60, 97, 147 */'},
  @{name='CORPUS_D';  ids=@(55,64,71,106,129);  head='/* the fourth folio ' + $D + ' sonnets 55, 64, 71, 106, 129 */'},
  @{name='CORPUS_E';  ids=@(1,15,27,66,87);     head='/* the fifth folio ' + $D + ' sonnets 1, 15, 27, 66, 87 */'},
  @{name='CORPUS_F';  ids=@(2,19,94,110,138);   head='/* the sixth folio ' + $D + ' sonnets 2, 19, 94, 110, 138 */'}
)
$used = @(); foreach($f in $folios){ $used += $f.ids }
$rest = @(); foreach($k in ($son.Keys | Sort-Object)){ if($used -notcontains $k){ $rest += $k } }
$folios += @{name='CORPUS_ALL'; ids=$rest; head='/* the seventh folio ' + $D + ' the remaining 124 sonnets, the whole sequence of 1609 */'}
$sb = New-Object System.Text.StringBuilder
foreach($f in $folios){
  [void]$sb.Append($f.head + "`n" + 'const ' + $f.name + '=`' + "`n")
  foreach($id in $f.ids){ [void]$sb.Append("# $id`n"); foreach($l in $son[$id]){ [void]$sb.Append($l + "`n") } }
  [void]$sb.Append('`;' + "`n")
}
[IO.File]::WriteAllText((Join-Path $here 'corpus_blocks.js'), $sb.ToString(), (New-Object System.Text.UTF8Encoding($false)))
"sonnets: $($son.Count)  seventh folio: $($rest.Count)  chars: $($sb.Length)"
