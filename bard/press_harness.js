/* press_harness.js — headless harness for the Sonnet Press (bard/index.html).
   USAGE: open bard/index.html in a browser, paste this whole file into the devtools console, then e.g.
     ABE_HARNESS.run({sheets:30, tier:4, seed:5})                 // the press as it stands
     ABE_HARNESS.run({sheets:30, tier:4, seed:5, keep:2})         // ... and keep two sheets as specimens
     ABE_HARNESS.run({sheets:30, tier:4, seed:5, cams:{comma:1,measure:0,rhyme:1,volta:1,concord:1}})
     ABE_HARNESS.vocabFacts(4)                                    // sorts, wheels, line lengths, rhyme classes

   It drives the page's own buildModel / rawDist / applyTemp / sample / drawOpener / rhymes / concordStrike /
   unsatisfied / inCorpus; only composeSonnet is re-implemented, without the DOM, animation and audio.
   Math.random is replaced by a seeded PRNG for the duration of a run, so a seed reproduces a sheet exactly.

   IT DUPLICATES composeSonnet AND WILL DRIFT.  Re-sync it by hand whenever the press changes, or its figures
   will be confidently wrong.  Last synced: the fellowship Rhyme Cam with the closing squeeze (rhymeFellows /
   fellowRoads / squeeze 0.75 from MAXW-3 / fellow boost 0.92 from MAXW-2), 2026-08-19.
   subject.onSubjectPct = share of the sheet's full words that share a sonnet line with a card word, scored with the cam
   on OR off, so the two can be compared.

   ABE_HARNESS.validateRhymer(tier) scores rhymes() against every authentic pair the scheme names at that
   schooling, plus non-rhyming controls — run it after any change to rhymeKey, NORHYME, EYE_RHYMES or buildLicence.

   Reported: fidelity (share of words standing in quoted runs of three or more, the concordance's own measure),
   derailment (share of draws with no trigram context), rhymeRate ((true+eye) / lines having a partner),
   meanWords, drawnMarkPct (lines ending on a point the engine actually drew), and the line-closing causes —
   lend (the engine proposed the line-break), rhyme, term, cap (the measure's ceiling), fin, open. */
(function(){
  function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }
  function hasTri(ctx){ const b=ctx[ctx.length-1], a=ctx.length>1?ctx[ctx.length-2]:undefined; return a!==undefined && !!tri.get(a+','+b); }

  function compose(C,T,st,prompt){
    const MINW=C.measure?6:1, MAXW=C.measure?10:12;
    const subject=C.subject?subjectOf(tokenize(prompt)):[], company=C.subject?companyOf(subject):new Set();
    const addr=C.addressee?addresseeWords(C.addressee):{set:new Set(),sonnets:0};
    let addrSet=addr.set;
    const laid=new Set();   /* no second helping: see index.html */
    if(addr.set.size&&company.size){ const both=new Set([...company].filter(id=>addr.set.has(id))); if(both.size>=12) addrSet=both; }
    const lastWords=[], sheet=[];
    const rhymeTarget=ln=>{ if(!C.rhyme) return null; const L=SCHEME[ln]; const j=SCHEME.indexOf(L); return (j<ln&&lastWords[j])?lastWords[j]:null; };
    for(let ln=0;ln<14;ln++){
      let ctx;
      if(ln===0){ ctx=tokenize(prompt); }
      else {
        let o;
        if(C.volta&&ln===8){
          const cands=OPENERS.filter(e=>VOLTA_WORDS.includes(vocabArr[e[0]]));
          if(cands.length){ let Z=0; const w=cands.map(e=>{Z+=e[1];return e[1];}); let r=Math.random()*Z;
            o=cands[cands.length-1][0]; for(let i=0;i<w.length;i++){ r-=w[i]; if(r<=0){ o=cands[i][0]; break; } } }
        }
        if(o===undefined) o=drawOpener(T);
        ctx=[o];
      }
      let words=ctx.filter(isWordId).length, ended=false, lastWord=null, cause=null;
      const target=rhymeTarget(ln);
      const fell=(C.rhyme&&target)?rhymeFellows(target):[];
      const goal=fell.length?1:null;
      const FELLOWS=goal?new Set(fell):null;
      const roads=goal?fellowRoads(fell):null;
      let draws=0;
      while(words<MAXW&&draws++<MAXW*3){   /* bounded in draws: the held-open line could otherwise spin on commas */
        st.draws++; if(!hasTri(ctx)) st.noTri++;
        const q=applyTemp(rawDist(ctx),T);
        let cut=0;
        if(C.comma){
          if(words<4){ TERM_IDS.forEach(id=>{cut+=q[id];q[id]=0;}); }
          if(words<2){ SOFT_IDS.forEach(id=>{cut+=q[id];q[id]=0;}); }
        }
        if(words<MINW){ cut+=q[FINID]; q[FINID]=0; if(C.measure){ cut+=q[LENDID]; q[LENDID]=0; TERM_IDS.forEach(id=>{cut+=q[id];q[id]=0;}); } }
        if(C.comma&&ln===13&&words>=MINW){
          SOFT_IDS.forEach(id=>{ cut+=q[id]; q[id]=0; });
          if(goal===null&&words>=MINW+2&&!unsatisfied(ctx)){
            let tm=0; TERM_IDS.forEach(id=>{ tm+=q[id]; });
            if(tm>1e-9&&tm<0.5){ const boost=0.5/tm, rest=0.5/(1-tm); for(let i=0;i<q.length;i++) q[i]*=TERM_IDS.has(i)?boost:rest; cut=0; }
          }
        }
        if(C.concord){ const m=concordStrike(q,ctx); if(m>1e-9){ cut+=m; st.struck++; } }
        if(C.subject&&company.size){ let T=0, sm=0; for(let i=0;i<q.length;i++){ T+=q[i]; if(q[i]>0&&company.has(i)) sm+=q[i]; }
          if(sm>1e-9){ st.tiltDraws++; const sh=SUBJECT_SHARE*Math.min(1,company.size/SUBJECT_FULL); if(sm<sh*T){ const b=sh*T/sm, r=(T-sh*T)/(T-sm); for(let i=0;i<q.length;i++) q[i]*=company.has(i)?b:r; st.tilted++; } } }
        if(C.addressee&&addrSet.size){ let T=0, am=0; for(let i=0;i<q.length;i++){ T+=q[i]; if(q[i]>0&&addrSet.has(i)&&!laid.has(i)) am+=q[i]; }
          if(am>1e-9){ st.aDraws++; const sh=ADDR_SHARE*Math.min(1,addrSet.size/ADDR_FULL); if(am<sh*T){ const b=sh*T/am, r=(T-sh*T)/(T-am); for(let i=0;i<q.length;i++) q[i]*=(addrSet.has(i)&&!laid.has(i))?b:r; st.aTilted++; } } }
        /* the fellowship rhyme cam: hold open, favour roads to ANY fellow, squeeze as the ceiling nears */
        if(goal!==null){
          cut+=q[LENDID]; q[LENDID]=0; cut+=q[FINID]; q[FINID]=0;
          TERM_IDS.forEach(id=>{ cut+=q[id]; q[id]=0; });
          if(SOFT_IDS.has(ctx[ctx.length-1])) SOFT_IDS.forEach(id=>{ cut+=q[id]; q[id]=0; });
          if(cut>1e-9&&cut<1){ const z=1-cut; for(let i=0;i<q.length;i++) q[i]/=z; cut=0; }
          if(words>=MINW-2){
            const share=(words>=MAXW-3)?Math.max(ROADS_SHARE,0.75):ROADS_SHARE;   /* the closing squeeze */
            let rm=0; for(let i=0;i<q.length;i++) if(q[i]>0&&roads.has(i)) rm+=q[i];
            if(share>0&&rm>1e-9&&rm<share){ const b=share/rm, r=(1-share)/(1-rm); for(let i=0;i<q.length;i++) q[i]*=roads.has(i)?b:r; }
          }
          const biL=bi.get(ctx[ctx.length-1]);
          if(words>=MINW-1&&biL){
            const gshare=(words>=MAXW-2)?0.92:0.5;
            let gm=0; for(const g of fell){ if(q[g]>0&&biL.m.has(g)) gm+=q[g]; }
            if(gm>1e-9){ st.boosts++; st.massSum+=gm;
              if(gm<gshare){ const b=gshare/gm, r=(1-gshare)/(1-gm); for(let i=0;i<q.length;i++) q[i]*=(FELLOWS.has(i)&&biL.m.has(i))?b:r; } }
          }
        }
        if(cut>1e-9&&cut<1){ const z=1-cut; for(let i=0;i<q.length;i++) q[i]/=z; }
        const id=sample(q);
        if(id===FINID){ ended=true; cause='fin'; break; }
        if(id===LENDID){ ended=true; cause='lend'; break; }
        ctx.push(id);
        if(isWordId(id)){ words++; lastWord=vocabArr[id]; laid.add(id); }
        if(TERM_IDS.has(id)){ ended=true; cause='term'; break; }
        if(target&&words>=MINW&&lastWord&&rhymes(lastWord,target)&&!DANGLE.has(lastWord)&&!unsatisfied(ctx)){ ended=true; cause='rhyme'; break; }
      }
      if(!ended) cause='cap';
      const openT=()=>!!(lastWord&&(DANGLE.has(lastWord)||unsatisfied(ctx)));
      let extra=0; const dangled=!ended&&openT();
      while(!ended&&extra<3&&openT()){
        st.draws++; if(!hasTri(ctx)) st.noTri++;
        const q=applyTemp(rawDist(ctx),T); q[FINID]=0; q[LENDID]=0; TERM_IDS.forEach(id=>{q[id]=0;}); SOFT_IDS.forEach(id=>{q[id]=0;});
        if(C.concord) concordStrike(q,ctx);
        let Z=0; for(let i=0;i<q.length;i++) Z+=q[i]; if(Z<=1e-9) break; for(let i=0;i<q.length;i++) q[i]/=Z;
        const id=sample(q); ctx.push(id); if(isWordId(id)){ words++; lastWord=vocabArr[id]; }
        extra++;
      }
      if(dangled) cause=openT()?'open':'cap-after-dangle';
      const toks=ctx.map(id=>vocabArr[id]);
      lastWords[ln]=lastWord;
      if(C.rhyme&&target){ const r=lastWord?rhymes(lastWord,target):null;
        if(r==='true') st.hits++; else if(r==='eye') st.eyes++; else st.misses++; }
      st.lines++; st.lw+=words; st.cause[cause]=(st.cause[cause]||0)+1;
      const last=ctx[ctx.length-1];
      if(TERM_IDS.has(last)||SOFT_IDS.has(last)) st.drawnMark++;
      /* on-subject: full words of the line that keep the subject's company (scored even with the cam off, against the card's company) */
      for(const id of ctx){ if(isWordId(id)&&!STOPW.has(vocabArr[id])&&!PUNCT.has(vocabArr[id])){ st.cw++; if(st.company.has(id)) st.onSubj++; if(st.addrScore.has(id)) st.onAddr++; } }
      sheet.push({toks,cause});
    }
    /* echo: how often the sheet says the same full word again and again — the pathology a small tilt-set invites */
    { const m=new Map();
      for(const L of sheet) for(const w of L.toks){ if(PUNCT.has(w)||STOPW.has(w)||SUBJ_AUX.has(w)||w===FIN||w===LEND) continue; m.set(w,(m.get(w)||0)+1); }
      for(const [w,n] of m){ if(n>=3){ st.echoExtra+=n-2; st.echoTypes++; } if(n>st.echoWorst){ st.echoWorst=n; st.echoWord=w; } } }
    return sheet;
  }

  function fid(sheet,st){
    for(const L of sheet){
      const words=L.toks.filter(w=>!PUNCT.has(w)&&w!==FIN&&w!==LEND);
      let i=0;
      while(i<words.length){
        let best=null;
        for(let j=words.length;j-i>=CONC_MIN;j--){ if(inCorpus(words.slice(i,j))){ best={to:j-1,n:j-i}; break; } }
        if(best){ st.quoted+=best.n; i=best.to+1; } else i++;
      }
      st.words+=words.length;
    }
  }

  window.ABE_HARNESS={
    run(opts){
      const o=Object.assign({sheets:30,tier:4,T:S.T,seed:1,prompt:'shall i compare thee',
        cams:{comma:1,measure:1,rhyme:1,volta:1,concord:1,subject:1,addressee:0},keep:0},opts||{});   /* cams.addressee is '' or 'dark'|'youth'|'rival' */
      if(FOLIO!==o.tier) buildModel(o.tier);
      const st={draws:0,noTri:0,lines:0,words:0,quoted:0,hits:0,eyes:0,misses:0,cause:{},lw:0,drawnMark:0,struck:0,boosts:0,massSum:0,tilted:0,tiltDraws:0,cw:0,onSubj:0,aTilted:0,aDraws:0,onAddr:0,echoExtra:0,echoTypes:0,echoWorst:0,echoWord:null,company:companyOf(subjectOf(tokenize(o.prompt))),addrScore:(o.cams.addressee?addresseeWords(o.cams.addressee).set:new Set())};
      const saved=Math.random, spec=[];
      try{
        for(let s=0;s<o.sheets;s++){
          Math.random=mulberry32(o.seed*1000003+s*7919+1);
          const sh=compose(o.cams,o.T,st,o.prompt);
          fid(sh,st);
          if(s<o.keep) spec.push(sh.map(L=>L.toks.join(' ')+'   <'+L.cause+'>'));
        }
      } finally { Math.random=saved; }
      const tl=st.hits+st.eyes+st.misses;
      return {
        cfg:{sheets:o.sheets,tier:o.tier,T:o.T,seed:o.seed,sorts:BASE_N,wheels:WHEELS,verseLines:LINES.length},
        fidelity:+(100*st.quoted/st.words).toFixed(1),
        derailment:+(100*st.noTri/st.draws).toFixed(1),
        rhymeRate:tl?+(100*(st.hits+st.eyes)/tl).toFixed(1):null, hits:st.hits, eyes:st.eyes, misses:st.misses,
        meanWords:+(st.lw/st.lines).toFixed(1),
        drawnMarkPct:+(100*st.drawnMark/st.lines).toFixed(1),
        cause:Object.fromEntries(Object.entries(st.cause).map(([k,v])=>[k,+(100*v/st.lines).toFixed(1)])),
        rhymeCam:{boosts:st.boosts, meanNaturalMassPct:st.boosts?+(100*st.massSum/st.boosts).toFixed(2):null},
        subject:{share:SUBJECT_SHARE, full:SUBJECT_FULL, companySize:st.company.size, tilted:st.tilted, tiltDraws:st.tiltDraws, onSubjectPct:st.cw?+(100*st.onSubj/st.cw).toFixed(1):null},
        echo:{per100Words:+(100*st.echoExtra/Math.max(1,st.cw)).toFixed(2), typesPerSheet:+(st.echoTypes/o.sheets).toFixed(2), worst:st.echoWorst, worstWord:st.echoWord},
        addressee:{who:o.cams.addressee||null, share:ADDR_SHARE, words:st.addrScore.size, tilted:st.aTilted, tiltDraws:st.aDraws, onAddresseePct:st.cw?+(100*st.onAddr/st.cw).toFixed(1):null},
        lines:st.lines, draws:st.draws, specimens:spec
      };
    },
    validateRhymer(tier){
      if(tier===undefined) tier=FOLIOS.length-1;
      if(FOLIO!==tier) buildModel(tier);
      const bySon=new Map();
      LINES.forEach((l,i)=>{ const s=LINE_SONNET[i]; if(!bySon.has(s)) bySon.set(s,[]); bySon.get(s).push(l); });
      const finals=lines=>lines.map(l=>{ const ws=l.split(/\s+/); for(let k=ws.length-1;k>=0;k--){ if(!PUNCT.has(ws[k])) return ws[k]; } return null; });
      const PAIRS=[[0,2],[1,3],[4,6],[5,7],[8,10],[9,11],[12,13]], CTRL=[[0,1],[4,5],[8,9]];
      const auth=[], ctrl=[];
      for(const lines of bySon.values()){ if(lines.length!==14) continue; const f=finals(lines);
        for(const [a,b] of PAIRS){ if(f[a]&&f[b]&&f[a]!==f[b]) auth.push([f[a],f[b]]); }
        for(const [a,b] of CTRL){ if(f[a]&&f[b]&&f[a]!==f[b]) ctrl.push([f[a],f[b]]); } }
      let t=0,e=0,fails=[]; for(const [a,b] of auth){ const r=rhymes(a,b); if(r==='true')t++; else if(r==='eye')e++; else fails.push(a+'/'+b); }
      let phon=0; for(const [a,b] of auth){ if(rhymes(a,b,true)) phon++; }
      let fp=[]; for(const [a,b] of ctrl){ if(rhymes(a,b)) fp.push(a+'/'+b); }
      return {authentic:auth.length, trueByPhonetics:t, byLicence:e, fails,
        passPct:+(100*(t+e)/auth.length).toFixed(1), phoneticOnlyPct:+(100*phon/auth.length).toFixed(1),
        licencePairs:LIC_PAIRS, licenceWords:LICENCE.size,
        controls:ctrl.length, falsePositives:fp};
    },
    vocabFacts(tier){
      if(FOLIO!==tier) buildModel(tier);
      const ee=[]; for(let i=0;i<vocabArr.length;i++){ if(!isWordId(i)) continue; if(rhymeKey(vocabArr[i])==='ee') ee.push(vocabArr[i]); }
      const lens=LINES.map(l=>l.split(/\s+/).filter(w=>!PUNCT.has(w)).length).sort((a,b)=>a-b);
      return {sorts:BASE_N, wheels:WHEELS, verseLines:LINES.length,
        lineEnds:uniC[LENDID], sentenceEnds:uniC[FINID],
        lineWords:{min:lens[0], median:lens[lens.length>>1], mean:+(lens.reduce((a,b)=>a+b,0)/lens.length).toFixed(1), max:lens[lens.length-1]},
        points:vocabArr.filter(w=>PUNCT.has(w)), soft:[...SOFT_IDS].map(i=>vocabArr[i]), term:[...TERM_IDS].map(i=>vocabArr[i]),
        eeClass:{size:ee.length, pctVocab:+(100*ee.length/BASE_N).toFixed(1), endingY:ee.filter(w=>/y$/.test(w)).length},
        quoteEdgeSorts:vocabArr.filter(w=>/^'|'$/.test(w)),
        openersDistinct:OPENERS.length};
    }
  };
  return 'harness installed';
})()
