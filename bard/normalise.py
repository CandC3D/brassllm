"""Normalise the Sonnets of 1609 (Gutenberg #1041) into the Bard's corpus format.

CANONICAL SPEC.  This is the reference implementation and the one to edit.
A PowerShell transcription, normalise.ps1, exists only because the workstation
where the 2026 revisions were made had no Python; if you change the rules here,
change them there too, or delete it.

Since the verse-line revision the unit of a corpus line is a VERSE LINE, not a
sentence.  Sentence boundaries survive as their own points inside the line; the
engine is given the line breaks as tokens by buildModel, so line shape is learned
rather than imposed by the Measure Cam.

  usage:  python normalise.py            # sample sonnets, to the terminal
          python normalise.py --all      # every sonnet, '# N' marker then its lines
"""
import re, sys

def r2i(r):
    v={'I':1,'V':5,'X':10,'L':50,'C':100}; t=0
    for i,c in enumerate(r): t+= -v[c] if i+1<len(r) and v[c]<v[r[i+1]] else v[c]
    return t

def load(path='sonnets.txt'):
    txt=open(path,encoding='utf-8').read()
    blocks=re.split(r"\n([IVXLC]+)\n",txt); son={}
    for i in range(1,len(blocks)-1,2):
        n=r2i(blocks[i]); b=blocks[i+1].strip().split("\n\n")[0]
        if 1<=n<=154 and n not in son: son[n]=b
    return son

# a straight quote that opens or closes a word is the printer's quotation mark and is struck;
# the same character between letters, or ending a word after a vowel-less stem, is an elision
# and is kept: o'er, lov'd, beauty's, wights', 'gainst, 'tis, th'
ELIDE_HEAD = ("tis","twas","twixt","gainst","greeing","scap'd","fore","mongst","neath","gan")
def strip_quotes(w):
    core=w
    # closing: a trailing quote is possessive-plural (wights') only after s
    if core.endswith("'") and not core[:-1].endswith('s'): core=core[:-1]
    # opening: a leading quote is an elision only for the known heads
    if core.startswith("'"):
        rest=core[1:]
        if not any(rest.startswith(h) for h in ELIDE_HEAD): core=rest
    return core

def normalise(body):
    s=body
    s=s.replace('’',"'").replace('‘',"'").replace('“','').replace('”','')
    s=s.replace('—',' , ').replace('–',' , ')      # the em-dash is not a sort; it reads as a comma
    s=s.lower()
    s=re.sub(r'(\w)-(\w)',r'\1 \2',s)                        # hyphenated compounds split
    s=re.sub(r'[()\[\]]',' ',s)
    s=re.sub(r'\bo\s*!','o ,',s)                             # 'O!' is an interjection, not a sentence end
    out=[]
    for raw in s.split('\n'):
        l=raw.strip()
        if not l: continue
        l=re.sub(r'\s*([,;:.?!])\s*',r' \1 ',l)              # every point stands as its own sort
        words=[strip_quotes(w) for w in l.split()]
        l=' '.join(w for w in words if w)
        l=re.sub(r'\s+',' ',l).strip()
        if l: out.append(l)
    return out

if __name__=='__main__':
    son=load()
    if '--all' in sys.argv:
        for n in sorted(son):
            print('#%d'%n)
            for l in normalise(son[n]): print(l)
    else:
        for n in (18,130,99,126,145):
            print('==',n); [print(l) for l in normalise(son[n])]
