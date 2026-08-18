# serve.ps1 -- a tiny static file server for previewing the exhibit on a workstation with no Python/Node.
# Usage: powershell -File .claude/serve.ps1 [-Port 8765]
param([int]$Port=8765)
$root=Split-Path -Parent $PSScriptRoot
$l=New-Object System.Net.HttpListener; $l.Prefixes.Add("http://localhost:$Port/"); $l.Start()
"serving $root on http://localhost:$Port/"
$types=@{'.html'='text/html; charset=utf-8';'.svg'='image/svg+xml';'.png'='image/png';'.ico'='image/x-icon';'.js'='text/javascript';'.css'='text/css';'.md'='text/plain; charset=utf-8';'.json'='application/json';'.webmanifest'='application/manifest+json'}
while($l.IsListening){
  $c=$l.GetContext(); $rq=$c.Request; $rs=$c.Response
  try{
    $path=[Uri]::UnescapeDataString($rq.Url.AbsolutePath); if($path.EndsWith('/')){ $path+='index.html' }
    $file=Join-Path $root ($path.TrimStart('/') -replace '/','\')
    if(Test-Path $file -PathType Leaf){
      $b=[IO.File]::ReadAllBytes($file); $ext=[IO.Path]::GetExtension($file).ToLower()
      $rs.ContentType=$(if($types.ContainsKey($ext)){$types[$ext]}else{'application/octet-stream'})
      $rs.Headers['Cache-Control']='no-store'
      $rs.ContentLength64=$b.Length; $rs.OutputStream.Write($b,0,$b.Length)
    } else { $rs.StatusCode=404 }
  } catch { $rs.StatusCode=500 } finally { $rs.Close() }
}
