"""Regenerate the Bard from the current ALE and re-apply every Bard delta.
Each transplant is a (start-marker, end-marker) region lifted from the OLD Bard
and grafted over the SAME region in the fresh ALE copy; the rest are targeted
string swaps.  Every step asserts, so a missed anchor fails loudly."""
import re, sys
ALE=r"C:\Users\chorr\Documents\Analytical-Language-Engine\analytical-language-engine.html"
OLD=r"C:\Users\chorr\Documents\Analytical-Bard-Engine\bard-before-sync.html"   # copy the current Bard here before running
OUT=r"C:\Users\chorr\Documents\Analytical-Bard-Engine\analytical-bard-engine.html"
ale=open(ALE,encoding='utf-8').read(); old=open(OLD,encoding='utf-8').read()
new=ale

def region(s,a,b,inclusive_end=True):
    i=s.index(a); j=s.index(b,i)+(len(b) if inclusive_end else 0); return i,j
def graft(a,b,label,inclusive_end=True,b_new=None):
    global new
    oi,oj=region(old,a,b,inclusive_end); ni,nj=region(new,a,b_new or b,inclusive_end)
    new=new[:ni]+old[oi:oj]+new[nj:]; print("grafted",label)
def swap(a,b,label,count=1):
    global new
    assert new.count(a)==count, f"{label}: expected {count} of anchor, found {new.count(a)}"
    new=new.replace(a,b); print("swapped",label)

# DOMAIN NOTE (2026-08-18): the site moved to https://brassllm.com/ — the head-string anchors below quote the
# parent's canonical/og:url and were updated to match. The absolute FILE paths above are the home machine's: leave them.
# ---- head / title / masthead ----
swap('<link rel="canonical" href="https://brassllm.com/"><!-- Google Analytics (GA4) --><script async src="https://www.googletagmanager.com/gtag/js?id=G-G7GXZPF2YR"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){dataLayer.push(arguments);}gtag(\'js\',new Date());gtag(\'config\',\'G-G7GXZPF2YR\');</script><meta name="description" content="See what happens inside a Large Language Model, from prompt to output, staged as a working Victorian brass machine — with live probabilities, station by station.">',
     '<meta name="description" content="An LLM schooled on nothing but Shakespeare\'s Sonnets — the Analytical Bard Engine, a working Victorian brass machine with live probabilities, station by station.">','head:desc/GA')
swap('<meta property="og:title" content="The Analytical Language Engine"><meta property="og:description" content="How an LLM works, from prompt to output — illustrated as a working brass machine, after Mr. Babbage."><meta property="og:url" content="https://brassllm.com/">',
     '<meta property="og:title" content="The Analytical Bard Engine"><meta property="og:description" content="An LLM of the Sonnets — the brass engine re-schooled on Mr. Shakespeare, after Mr. Babbage.">','head:og')
swap('<title>The Analytical Language Engine — how an LLM works, in brass</title>','<title>The Analytical Bard Engine — an LLM of the Sonnets, in brass</title>','title')
swap('<h1>The Analytical Language Engine</h1>','<h1>The Analytical Bard Engine</h1>','h1')
swap('<p class="sub">Being a candid mechanical account of the <b>Large Language Model</b> — what truly happens between your question and its answer — rendered in brass, in the manner of Mr.&nbsp;Charles&nbsp;Babbage.</p>',
     '<p class="sub">Being a candid mechanical account of the <b>Large Language Model</b> — rendered in brass, in the manner of Mr.&nbsp;Charles&nbsp;Babbage, and schooled upon nothing whatever but the Sonnets of Mr.&nbsp;William&nbsp;Shakespeare.</p>','masthead sub')
# legend chip + schooling lever: replace ALE's "loop chip → </header>" with the Bard's "loop chip → schooling → </header>"
oi,oj=region(old,'    <a href="#st8">VIII · The loop</a>','</header>',True)
ni,nj=region(new,'    <a href="#st8">VIII · The loop</a>','</header>',True)
new=new[:ni]+old[oi:oj]+new[nj:]; print("grafted legend+schooling")
# schooling CSS
graft('/* the schooling — a three-notch folio lever on the masthead */','#folcap{font-family:var(--mono);font-size:11px;color:#5b4517;margin-top:2px}','schooling css') if '/* the schooling' in new else None
if '/* the schooling' not in new:
    # insert schooling css after legend focus rule
    a='.legend a:focus-visible{outline:3px solid var(--glow);outline-offset:2px}'
    oi,oj=region(old,'/* the schooling — a three-notch folio lever on the masthead */','#folcap{font-family:var(--mono);font-size:11px;color:#5b4517;margin-top:2px}')
    new=new.replace(a,a+'\n'+old[oi:oj]); print("inserted schooling css")

# ---- desk presets / prompt ----
graft('      <input id="prompt" type="text"','      </div>\n    </div>\n    <div class="deskright">','presets',False)
swap('          <div id="pcText">the engine</div>','          <div id="pcText">shall i compare thee</div>','pcText')
swap('      <div class="mnote">Note how ENGINE and GEARS set their dials nearly alike, while FOG wears a different aspect.</div>',
     '      <div class="mnote">Note how LOVE and EYES set their dials near one another, while SUMMER wears a different aspect.</div>','specimen note')

# ---- station VIII legend & press section & rule-book CSS ----
# press CSS block
a='#tapelegend{margin-top:10px;font-size:12px;color:#c9b787;font-style:italic}'
oi,oj=region(old,'/* the sonnet press — a fair-copy sheet, fourteen lines to completion */','#pressnote b{color:#e6c87d}')
assert '/* the sonnet press' not in new
new=new.replace(a,a+'\n\n'+old[oi:oj]); print("inserted press+rulebook css")
# press section
oi,oj=region(old,'<section class="station plate screws" id="press"','</section>\n\n<footer class="honesty">',False)
new=new.replace('<footer class="honesty">',old[oi:oj]+'<footer class="honesty">',1); print("inserted press section")

# ---- honesty footer: the Bard's own candid note (plaque + button row), up to the colophon ----
graft('<footer class="honesty">','  <p class="colophon">','honesty footer',False)
assert new.count('<section ')==new.count('</section>'), 'unbalanced <section> — a graft ate a closing tag'
# ---- colophon ----
swap('  <p class="colophon">Devised by <b>MESSRS. HORROCKS &amp; CLAUDE</b> (an engine of the very kind depicted)<br>',
     '  <p class="colophon">Devised by <b>MESSRS. HORROCKS &amp; CLAUDE</b> (an engine of the very kind depicted)<br>\n  the verses <b>MR. WILLIAM SHAKESPEARE’S</b>, his Sonnets, MDCIX — the machinery ours<br>','colophon')

# ---- corpus (all four folios) ----
graft('const CORPUS=`','the heaven that leads men to this hell .\n`;','corpora',True,'the clockmaker sleeps . the engine does not .\n`;')
# ---- model build (buildModel/refreshFolio) ----
graft("const FIN='∎', PUNCT=new Set(['.',',',';',':','!','?']);",'const cooGet=','buildModel',False)
# ---- clusters / stopwords / bays / specimens ----
graft('const CLUSTERS={','const clusterOf=','clusters+proto',False)
graft("const STOPW=new Set(","split(' '));",'stopw')
graft("const BAYS=[","[null,'Mortar & points — the small words that bind']];",'bays')
swap("  for(const w of ['engine','gears','fog']) el.specimens.appendChild(dialCol(w,true));","  for(const w of ['love','summer','eyes']) el.specimens.appendChild(dialCol(w,true));",'specimens')
# ---- el registry additions ----
swap("  prompt:$('#prompt'),begin:$('#btnBegin'),crank:$('#btnCrank'),run:$('#btnRun'),reset:$('#btnReset'),",
     "  prompt:$('#prompt'),begin:$('#btnBegin'),crank:$('#btnCrank'),run:$('#btnRun'),reset:$('#btnReset'),\n  sheet:$('#sheet'),pressnote:$('#pressnote'),pressBtn:$('#btnPress'),",'el registry')
# ---- refreshButtons ----
swap("  el.run.disabled=S.finished||!S.started||(S.busy&&!S.running);\n  updateTgButtons();",
     "  el.run.disabled=S.finished||!S.started||(S.busy&&!S.running);\n  el.pressBtn.disabled=S.busy||S.running;\n  updateTgButtons();",'refreshButtons')
# ---- clearWorks additions ----
swap("  telegraph('Idle. Write a card and begin.');\n  FOLEY.bed('hum',false); FOLEY.bed('roll',false);",
     "  telegraph('Idle. Write a card and begin.');\n  el.sheet.innerHTML='<div class=\"stitle\">Sonnet —</div>';\n  el.pressnote.textContent='The press stands ready; your card seeds the first line.';\n  FOLEY.bed('hum',false); FOLEY.bed('roll',false);",'clearWorks')
# ---- press machinery (rhymer + composeSonnet) inserted before doHaltAndClear ----
oi,oj=region(old,'/* ---------------- the sonnet press ---------------- */','async function doHaltAndClear(){',False)
assert new.count('async function doHaltAndClear(){')==1
new=new.replace('async function doHaltAndClear(){',old[oi:oj]+'async function doHaltAndClear(){',1); print("inserted press machinery")
# ---- begin fallback + press button + init ----
swap("  S.prompt=(el.prompt.value.trim()||'the engine'); el.prompt.value=S.prompt;","  S.prompt=(el.prompt.value.trim()||'shall i compare thee'); el.prompt.value=S.prompt;",'begin fallback')
swap("el.crank.addEventListener('click',()=>revolution('quick'));","el.crank.addEventListener('click',()=>revolution('quick'));\nel.pressBtn.addEventListener('click',composeSonnet);",'press button')
graft('function init(){','  buildMill(); buildCrank(); buildSpecimens(); buildTubes(); buildBand(); buildCutter();','init head',False)
# boiler default 0.95
swap('value="0.7" autocomplete="off" aria-label="Temperature lever">','value="0.95" autocomplete="off" aria-label="Temperature lever">','lever default')
swap('BOILER: TEMPERATE (0.70)</button>','BOILER: WARM (0.95)</button>','boiler chip')
swap('<div id="tname">TEMPERATE · T = 0.70</div>','<div id="tname">WARM · T = 0.95</div>','tname')
swap("setTemp(parseFloat(el.lever.value)||0.7);","setTemp(parseFloat(el.lever.value)||0.95);",'setTemp default')

open(OUT,'w',encoding='utf-8',newline='').write(new)
print("WROTE",OUT,len(new))
