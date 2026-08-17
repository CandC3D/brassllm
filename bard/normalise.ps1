# Transcription of normalise.py for workstations without Python. normalise.py is the CANONICAL spec —
# if the rules change there, change them here, or delete this file.
#   usage:  powershell -File normalise.ps1 -Source sonnets.txt -All > corpus.txt
param([string]$Source='sonnets.txt', [switch]$All, [int[]]$Sample=@(18,130,99,126,145))

$ELIDE_HEAD = @('tis','twas','twixt','gainst','greeing',"scap'd",'fore','mongst','neath','gan')

function ConvertTo-Int([string]$r){
  $v=@{'I'=1;'V'=5;'X'=10;'L'=50;'C'=100}; $t=0
  for($i=0;$i -lt $r.Length;$i++){
    if($i+1 -lt $r.Length -and $v[[string]$r[$i]] -lt $v[[string]$r[$i+1]]){ $t -= $v[[string]$r[$i]] } else { $t += $v[[string]$r[$i]] }
  }
  return $t
}

function Import-Sonnets([string]$path){
  $txt = Get-Content $path -Raw -Encoding UTF8
  $txt = $txt -replace "`r`n","`n"
  $blocks = [regex]::Split($txt, "`n([IVXLC]+)`n")
  $son = @{}
  for($i=1; $i -lt $blocks.Count-1; $i+=2){
    $n = ConvertTo-Int $blocks[$i]
    $b = ($blocks[$i+1].Trim() -split "`n`n")[0]
    if($n -ge 1 -and $n -le 154 -and -not $son.ContainsKey($n)){ $son[$n]=$b }
  }
  return $son
}

function Remove-QuoteMark([string]$w){
  $core = $w
  if($core.EndsWith("'") -and -not $core.Substring(0,$core.Length-1).EndsWith('s')){ $core = $core.Substring(0,$core.Length-1) }
  if($core.StartsWith("'")){
    $rest = $core.Substring(1)
    $isElide = $false
    foreach($h in $ELIDE_HEAD){ if($rest.StartsWith($h)){ $isElide = $true; break } }
    if(-not $isElide){ $core = $rest }
  }
  return $core
}

function ConvertTo-CorpusLines([string]$body){
  $s = $body -replace [char]0x2019,"'" -replace [char]0x2018,"'" -replace [char]0x201C,'' -replace [char]0x201D,''
  $s = $s -replace [char]0x2014,(' '+[char]0x2014+' ') -replace [char]0x2013,(' '+[char]0x2014+' ')
  $s = $s.ToLower()
  $s = [regex]::Replace($s, '(\w)-(\w)', '$1 $2')
  $s = [regex]::Replace($s, '[()\[\]]', ' ')
  $s = [regex]::Replace($s, '\bo\s*!', 'o ,')
  $out = New-Object System.Collections.Generic.List[string]
  foreach($raw in ($s -split "`n")){
    $l = $raw.Trim()
    if(-not $l){ continue }
    $l = [regex]::Replace($l, ('\s*([,;:.?!' + [char]0x2014 + '])\s*'), ' $1 ')
    $words = @()
    foreach($w in ($l -split '\s+')){ $c = Remove-QuoteMark $w; if($c){ $words += $c } }
    $l = ($words -join ' ')
    $l = [regex]::Replace($l, '\s+', ' ').Trim()
    if($l){ $out.Add($l) }
  }
  return $out
}

$son = Import-Sonnets $Source
if($All){
  foreach($n in ($son.Keys | Sort-Object)){
    "#$n"
    ConvertTo-CorpusLines $son[$n] | ForEach-Object { $_ }
  }
} else {
  foreach($n in $Sample){ "== $n"; ConvertTo-CorpusLines $son[$n] | ForEach-Object { $_ } }
}
