#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Extract every plaque passage from both engines into copy/COPY-EDIT.md for line-editing.
Re-run any time either page has been edited; then edit COPY-EDIT.md; then apply_copy.py --write."""
import re, os, io
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FILES=[('ALE',os.path.join(ROOT,'analytical-language-engine.html')),('BARD',os.path.join(ROOT,'bard','index.html'))]
PAT=re.compile(r'<section[^>]*id="([^"]+)"|<footer class="honesty">|<p class="(conceit|truth|fine|sub|sub2|ophelp)"[^>]*>(.*?)</p>|<div class="mnote" id="([^"]+)">([^<]*)</div>|<div class="mcap">([^<]*)</div>|<span class="camrule">(.*?)</span>|<div class="rbnote">([^<]*)</div>',re.S)
def scan(s):
    items=[]; sec=None
    for m in PAT.finditer(s):
        if m.group(0).startswith('<section'): sec=m.group(1); continue
        if m.group(0).startswith('<footer'): sec='footer'; continue
        if m.group(2): items.append((sec,m.group(2),m.group(3)))
        elif m.group(4): items.append((sec,'mnote#'+m.group(4),m.group(5)))
        elif m.group(6): items.append((sec,'mcap',m.group(6)))
        elif m.group(7): items.append((sec,'camrule',m.group(7)))
        elif m.group(8): items.append((sec,'rbnote',m.group(8)))
    return items
out=io.open(os.path.join(ROOT,'copy','COPY-EDIT.md'),'w',encoding='utf-8',newline='\n')
out.write("# The Analytical Engines — copy for line-editing\n\n")
out.write("Edit the text between the `>>>` and `<<<` markers only. Keep the inline `<b>`, `<i>`, `<a>`, `<span>` tags where they are (they carry the glossary tooltips and links) — reword around them freely. Delete a block's text entirely to leave the original untouched. Blank spans like `<span id=\"vN2\">—</span>` are live counters; leave them. Then run `python copy/apply_copy.py --write`.\n\n")
for tag,path in FILES:
    s=io.open(path,encoding='utf-8',newline='').read(); items=scan(s); cur=None
    out.write(f"\n\n# ═══════════════ {tag} ═══════════════\n")
    for i,(sec,kind,html) in enumerate(items):
        if sec!=cur: cur=sec; out.write(f"\n\n## {tag} · {cur or 'masthead/desk'}\n")
        words=len(re.findall(r"[A-Za-z’']+",re.sub(r'<[^>]+>','',html)))
        out.write(f"\n### {tag}-{i:03d} · {kind} · {words}w\n>>>\n{html.strip().replace(chr(13)+chr(10),chr(10))}\n<<<\n")
    print(tag,len(items),'passages')
out.close(); print('wrote copy/COPY-EDIT.md')
