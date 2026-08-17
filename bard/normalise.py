import re
def r2i(r):
    v={'I':1,'V':5,'X':10,'L':50,'C':100}; t=0
    for i,c in enumerate(r): t+= -v[c] if i+1<len(r) and v[c]<v[r[i+1]] else v[c]
    return t
def load():
    txt=open('sonnets.txt',encoding='utf-8').read()
    blocks=re.split(r"\n([IVXLC]+)\n",txt); son={}
    for i in range(1,len(blocks)-1,2):
        n=r2i(blocks[i]); b=blocks[i+1].strip().split("\n\n")[0]
        if 1<=n<=154 and n not in son: son[n]=b
    return son
def normalise(body):
    s=body.replace('’',"'").replace('‘',"'").replace('“','').replace('”','').replace('—',' , ').replace('–',' , ')
    s=' '.join(l.strip() for l in s.split('\n')).lower()
    s=re.sub(r'(\w)-(\w)',r'\1 \2',s)
    s=re.sub(r'[()]',' ',s)
    s=re.sub(r"\bo\s*!",'o ,',s)                       # 'O!' is an interjection, not a sentence end
    s=re.sub(r'\s*([,])\s*',r' \1 ',s)
    # colon and semicolon are period-strength in this edition: they end a corpus line, rendered as a full stop
    s=re.sub(r'\s*[;:]\s*',' .\n',s)
    s=re.sub(r'\s*([.?!])\s*',r' \1\n',s)
    lines=[]
    for l in s.split('\n'):
        l=re.sub(r'\s+',' ',l).strip()
        if not l: continue
        if l in ('.','?','!'):
            if lines and not re.search(r' [.?!]$',lines[-1]): lines[-1]+=' '+l
            continue
        if not re.search(r' [.?!]$',l): l+=' .'
        lines.append(l)
    out=[]
    for l in lines:
        nw=len([w for w in l.split() if re.search(r"[a-z]",w)])
        if out and nw<4: out[-1]=re.sub(r' [.?!]$','',out[-1])+' , '+l   # too short to stand: fold into the previous
        else: out.append(l)
    return out
if __name__=='__main__':
    son=load()
    for n in (18,130,99,126):
        print('==',n); [print(l) for l in normalise(son[n])]
