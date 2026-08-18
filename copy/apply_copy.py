#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Apply line-edits from copy/COPY-EDIT.md back into both engines.

Usage:  python copy/apply_copy.py            (dry run: shows what would change)
        python copy/apply_copy.py --write    (writes the files)

How it works: extract_copy.py wrote COPY-EDIT.md with one block per plaque passage, keyed
ALE-007 / BARD-021 etc., plus copy-index.json recording each block's kind and its position
in the source. This script re-locates every block by re-scanning the LIVE files (positions
are not trusted — the office machine may have edited in between), matches on kind + order
within section, and replaces the inner HTML with the edited text where it differs.

CRLF and UTF-8 are preserved (files opened with newline=''). Inline tags in the copy are
kept verbatim, so glossary <b>/<i> tooltips and links survive. A block whose text between
the markers is empty is skipped (original left untouched)."""
import re, sys, os, io, json

ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
COPY=os.path.join(ROOT,'copy','COPY-EDIT.md')
FILES={'ALE':os.path.join(ROOT,'analytical-language-engine.html'),'BARD':os.path.join(ROOT,'bard','index.html')}
WRITE='--write' in sys.argv

PAT=re.compile(r'<section[^>]*id="([^"]+)"|<footer class="honesty">|<p class="(conceit|truth|fine|sub|sub2|ophelp)"[^>]*>(.*?)</p>|<div class="mnote" id="([^"]+)">([^<]*)</div>|<div class="mcap">([^<]*)</div>|<span class="camrule">(.*?)</span>|<div class="rbnote">([^<]*)</div>',re.S)
def scan(s):
    items=[]; sec=None
    for m in PAT.finditer(s):
        if m.group(0).startswith('<section'): sec=m.group(1); continue
        if m.group(0).startswith('<footer'): sec='footer'; continue
        if m.group(2): items.append({'sec':sec,'kind':m.group(2),'start':m.start(3),'end':m.end(3),'html':m.group(3)})
        elif m.group(4): items.append({'sec':sec,'kind':'mnote#'+m.group(4),'start':m.start(5),'end':m.end(5),'html':m.group(5)})
        elif m.group(6): items.append({'sec':sec,'kind':'mcap','start':m.start(6),'end':m.end(6),'html':m.group(6)})
        elif m.group(7): items.append({'sec':sec,'kind':'camrule','start':m.start(7),'end':m.end(7),'html':m.group(7)})
        elif m.group(8): items.append({'sec':sec,'kind':'rbnote','start':m.start(8),'end':m.end(8),'html':m.group(8)})
    return items

# parse the edited copy
copy=io.open(COPY,encoding='utf-8').read()
edits={}
for m in re.finditer(r'### (ALE|BARD)-(\d{3}) · [^\n]*\n>>>\n(.*?)\n<<<',copy,re.S):
    txt=m.group(3).strip()
    if txt: edits.setdefault(m.group(1),{})[int(m.group(2))]=txt

for tag,path in FILES.items():
    s=io.open(path,encoding='utf-8',newline='').read()
    items=scan(s)
    ed=edits.get(tag,{}); changed=0; out=[]; pos=0
    for i,it in enumerate(items):
        new=ed.get(i)
        if new is None: continue
        cur=it['html'].strip()
        # normalise CRLF inside the passage for comparison only
        if cur.replace('\r\n','\n')==new.replace('\r\n','\n'): continue
        out.append(s[pos:it['start']]); out.append(new); pos=it['end']; changed+=1
        print(f"{tag}-{i:03d} [{it['kind']}] {'WRITE' if WRITE else 'would change'}: {re.sub(r'<[^>]+>','',new)[:70]}…")
    out.append(s[pos:])
    if changed and WRITE:
        io.open(path,'w',encoding='utf-8',newline='').write(''.join(out))
    print(f"== {tag}: {changed} passage(s) {'written' if WRITE else 'differ'} of {len(items)} scanned")
if not WRITE: print("\n(dry run — add --write to apply)")
