/* press_harness.js — headless harness for the Sonnet Press (bard/index.html), per abe_press_brief.md §1.
   USAGE: open bard/index.html in a browser, paste this whole file into the devtools console, then e.g.
     ABE_HARNESS.vocabFacts(6)                                       // sorts, wheels, -ee class, quote-sorts, cools/fools
     ABE_HARNESS.run({sheets:40, tier:6, seed:1})                    // baseline (brief's "factory": notch 6, T 0.95, all cams)
     ABE_HARNESS.run({sheets:30, tier:6, seed:2, mods:{floor:0.02}}) // §6 ablations
   mods: floor (unigram weight), boostCap (max rhyme boost factor), boostLate, noDangleBoost, bigramOnly, carry:'one'|'two'
   Uses the page's own buildModel/rawDist/applyTemp/sample/drawOpener/rhymes/concordStrike/inCorpus; composeSonnet is
   re-implemented without DOM/animation/audio. Math.random is replaced by a seeded PRNG for the duration of a run.
   Metrics: fidelity (words in quoted runs >=3), derailment (draws with no trigram), dashLines (harness em-dash added),
   bareEnds (no terminal mark drawn, incl. line 14's forced stop), rhymeRate ((true+eye)/lines with a target), cause breakdown. */
/* ABE press harness — runs inside bard/index.html, uses the page's own model + cams.
   composeSonnet re-implemented without DOM/animation/audio. */
(function(){
  function mulberry32(a){ return function(){ a|=0; a=a+0x6D2B79F5|0; let t=Math.imul(a^a>>>15,1|a); t=t+Math.imul(t^t>>>7,61|t)^t; return ((t^t>>>14)>>>0)/4294967296; }; }

  /* rawDist with optional floor override (M.floor) — mirrors index.html rawDist exactly otherwise */
  function rawDistM(ctx,M){
    if(M.floor===undefined) return rawDist(ctx);
    const n=vocabArr.length, p=new Float64Array(n);
    const b=ctx[ctx.length-1], a=ctx.length>1?ctx[ctx.length-2]:undefined;
    const triE=(a!==undefined)?tri.get(a+','+b):undefined;
    const biE=bi.get(b);
    const w3=triE?0.72:0, w2=biE?0.21:0, w1=M.floor, W=w3+w2+w1;
    for(let i=0;i<n;i++){ let v=0;
      if(triE) v+=w3*((triE.m.get(i)||0)/triE.t);
      if(biE)  v+=w2*((biE.m.get(i)||0)/biE.t);
      v+=w1*((uniC[i]||0)/uniT); p[i]=v/W; }
    return p;
  }
  function hasTri(ctx){ const b=ctx[ctx.length-1], a=ctx.length>1?ctx[ctx.length-2]:undefined; return a!==undefined && !!tri.get(a+','+b); }

  function compose(C,T,M,st,prompt){
    const MINW=C.measure?6:1, MAXW=C.measure?10:12;
    const lastWords=[]; const sheet=[];
    const rhymeTarget=ln=>{ if(!C.rhyme) return null; const L=SCHEME[ln]; const j=SCHEME.indexOf(L); return (j<ln&&lastWords[j])?lastWords[j]:null; };
    let prevCtx=null;
    for(let ln=0;ln<14;ln++){
      let ctx, start=0;   /* start: index in ctx where this line's own tokens begin */
      if(ln===0){ ctx=tokenize(prompt); }
      else {
        let o;
        if(C.volta&&ln===8){
          const cands=OPENERS.filter(e=>VOLTA_WORDS.includes(vocabArr[e[0]]));
          if(cands.length){ let Z=0; const w=cands.map(e=>{Z+=e[1];return e[1];}); let r=Math.random()*Z;
            o=cands[cands.length-1][0]; for(let i=0;i<w.length;i++){ r-=w[i]; if(r<=0){ o=cands[i][0]; break; } } }
        }
        if(M.carry==='two'&&prevCtx){ ctx=prevCtx.slice(-2); start=ctx.length; }
        else {
          if(o===undefined) o=drawOpener(T);
          st.openers[vocabArr[o]]=(st.openers[vocabArr[o]]||0)+1;
          if(M.carry==='one'&&prevCtx){ ctx=[prevCtx[prevCtx.length-1],o]; start=1; } else { ctx=[o]; }
        }
      }
      let words=ctx.slice(start).filter(isWordId).length, ended=false, lastWord=null, cause=null;
      const target=rhymeTarget(ln);
      const secondDraw = (ln>0);   /* first draw of a non-seed line = the "second word" */
      let drawNo=0;
      while(words<MAXW){
        const tri_ok=hasTri(ctx);
        st.draws++; if(!tri_ok) st.noTri++;
        if(ln>0&&drawNo===0){ st.d2++; if(!tri_ok) st.d2noTri++; if(!bi.get(ctx[ctx.length-1])) st.d2noBi++; }
        drawNo++;
        const q=applyTemp(rawDistM(ctx,M),T);
        let cut=0;
        if(C.comma){
          if(words<4){ TERM_IDS.forEach(id=>{cut+=q[id];q[id]=0;}); }
          if(words<2){ SOFT_IDS.forEach(id=>{cut+=q[id];q[id]=0;}); }
        }
        if(words<MINW){ cut+=q[FINID]; q[FINID]=0; if(C.measure) TERM_IDS.forEach(id=>{cut+=q[id];q[id]=0;}); }
        if(C.comma&&ln===13&&words>=MINW){
          SOFT_IDS.forEach(id=>{ cut+=q[id]; q[id]=0; });
          if(M.legacy||(words>=MINW+2&&!unsatisfied(ctx))){
            let tm=0; TERM_IDS.forEach(id=>{ tm+=q[id]; });
            if(tm>1e-9&&tm<0.5){ const boost=0.5/tm, rest=0.5/(1-tm); for(let i=0;i<q.length;i++) q[i]*=TERM_IDS.has(i)?boost:rest; cut=0; }
          }
        }
        if(C.concord){ const m=concordStrike(q,ctx); if(m>1e-9){ cut+=m; st.struck++; st.strikeMass+=m; } }
        /* rhyme cam */
        let zoneOK = target&&words>=Math.max(MINW-1,3)&&lastWord!==null&&rhymes(lastWord,target)===null;
        if(zoneOK&&M.boostLate&&words<MAXW-1) zoneOK=false;
        if(zoneOK&&M.noDangleBoost&&DANGLE.has(lastWord)) zoneOK=false;
        if(zoneOK){
          /* natural (pre-cam) mass of the rhyming set, for the record: measure on q before renorm of cut */
          let mass=0; const good=[]; const biE=M.bigramOnly?bi.get(ctx[ctx.length-1]):null;
          for(let i=0;i<q.length;i++) if(q[i]>0&&isWordId(i)&&rhymes(vocabArr[i],target)) { if(M.bigramOnly&&!(biE&&biE.m.has(i))) continue; good.push(i); mass+=q[i]; }
          st.boostEvents++;
          if(good.length&&mass>1e-9){
            const massN=mass/(1-cut);   /* natural share among what remains after the cams' cuts */
            let boost=0.5/mass, rest=0.5/(1-mass);
            if(M.boostCap!==undefined&&boost>M.boostCap){ boost=M.boostCap; rest=(1-boost*mass)/(1-mass); }
            st.boosted++; st.candSum+=good.length; st.massSum+=massN; st.factors.push(0.5/massN);
            const G=new Set(good);
            for(let i=0;i<q.length;i++) q[i]*=(G.has(i)?boost:rest); cut=0;
          } else st.noRhyme++;
        }
        if(cut>1e-9&&cut<1){ const z=1-cut; for(let i=0;i<q.length;i++) q[i]/=z; }
        const id=sample(q);
        if(id===FINID){ ended=true; cause='fin'; break; }
        ctx.push(id);
        if(isWordId(id)){ words++; lastWord=vocabArr[id]; }
        if(TERM_IDS.has(id)){ ended=true; cause='term'; break; }
        if(target&&words>=MINW&&lastWord&&rhymes(lastWord,target)){
          if(M.legacy){ const prev=ctx.length>=2?vocabArr[ctx[ctx.length-2]]:''; if(!DANGLE.has(prev)){ ended=true; cause='rhyme'; break; } }
          else if(!DANGLE.has(lastWord)&&!unsatisfied(ctx)){ ended=true; cause='rhyme'; break; }
        }
      }
      if(!ended) cause='cap';
      const openTest=()=>M.legacy?!!(lastWord&&DANGLE.has(lastWord)):!!(lastWord&&(DANGLE.has(lastWord)||unsatisfied(ctx)));
      let extra=0; const dangled = !ended&&openTest();
      while(!ended&&extra<3&&openTest()){
        st.draws++; if(!hasTri(ctx)) st.noTri++;
        const q=applyTemp(rawDistM(ctx,M),T); q[FINID]=0; TERM_IDS.forEach(id=>{q[id]=0;}); SOFT_IDS.forEach(id=>{q[id]=0;});
        if(C.concord) concordStrike(q,ctx);
        let Z=0; for(let i=0;i<q.length;i++) Z+=q[i]; if(Z<=1e-9) break; for(let i=0;i<q.length;i++) q[i]/=Z;
        const id=sample(q); ctx.push(id); if(isWordId(id)){ words++; lastWord=vocabArr[id]; }
        extra++;
      }
      if(dangled){ cause = openTest()?'open':'cap-after-dangle'; }
      let toks=ctx.slice(start).map(id=>vocabArr[id]);
      let tail='';
      const lastIsTerm=TERM_IDS.has(ctx[ctx.length-1]);
      if(!lastIsTerm){
        if(C.comma&&ln===13){ while(toks.length>1&&SOFT_IDS.has(vocabId.get(toks[toks.length-1]))) toks.pop(); toks.push('.'); tail='forced.'; }
        else if(M.legacy) tail='—';
        else if(cause==='rhyme'&&(ln===3||ln===7||ln===11)&&!SOFT_IDS.has(ctx[ctx.length-1])){ toks.push(','); tail=','; }
      }
      lastWords[ln]=lastWord;
      let rr=null;
      if(C.rhyme&&target){ const r=lastWord?rhymes(lastWord,target):null; rr=r||'miss'; if(r==='true') st.hits++; else if(r==='eye') st.eyes++; else st.misses++; }
      /* concord/verbal token check (§8a) */
      const hasVerb=toks.some(w=>{ const id=vocabId.get(w); const t=id!==undefined?PART[id]:'?'; return t==='V'||t==='NV'||t==='X'; });
      if(hasVerb) st.linesWithVerb++;
      st.lines++;
      st.cause[cause]=(st.cause[cause]||0)+1;
      if(tail==='—') st.dash++;
      if(cause==='open') st.open++;
      if(ln===13){ st.l14w+=toks.filter(w=>!PUNCT.has(w)).length; st.l14n++; }
      if(!lastIsTerm) st.bareEnds++;
      sheet.push({toks,tail,cause,rr,ln});
      prevCtx=ctx;
    }
    return sheet;
  }

  /* concordance, as concordSheet does it */
  function fidelity(sheet,st){
    for(const L of sheet){
      const words=L.toks.filter(w=>!PUNCT.has(w)&&w!==FIN);
      let i=0; const runs=[];
      while(i<words.length){
        let best=null;
        for(let j=words.length;j-i>=CONC_MIN;j--){ const hit=inCorpus(words.slice(i,j)); if(hit){ best={from:i,to:j-1,n:j-i}; break; } }
        if(best){ runs.push(best); i=best.to+1; } else i++;
      }
      st.words+=words.length; runs.forEach(r=>{ st.quoted+=r.n; });
    }
  }

  window.ABE_HARNESS={
    run(opts){
      const o=Object.assign({sheets:40,tier:6,T:(typeof PRESS_T!=='undefined'?PRESS_T:0.95),seed:1,prompt:'shall i compare thee',cams:{comma:1,measure:1,rhyme:1,volta:1,concord:1},mods:{},keep:2},opts||{});
      if(FOLIO!==o.tier) buildModel(o.tier);
      const st={draws:0,noTri:0,d2:0,d2noTri:0,d2noBi:0,lines:0,words:0,quoted:0,hits:0,eyes:0,misses:0,boostEvents:0,boosted:0,noRhyme:0,candSum:0,massSum:0,factors:[],struck:0,strikeMass:0,cause:{},dash:0,open:0,l14w:0,l14n:0,bareEnds:0,openers:{},linesWithVerb:0};
      const saved=Math.random; const specimens=[];
      try{
        for(let s=0;s<o.sheets;s++){
          Math.random=mulberry32(o.seed*1000003+s*7919+1);
          const sheet=compose(o.cams,o.T,o.mods,st,o.prompt);
          fidelity(sheet,st);
          if(s<o.keep) specimens.push(sheet.map(L=>L.toks.join(' ')+(L.tail==='—'?' —':'')+(L.rr?'  ['+L.rr+']':'')+'  <'+L.cause+'>'));
        }
      } finally { Math.random=saved; }
      st.factors.sort((a,b)=>a-b);
      const med=st.factors.length?st.factors[Math.floor(st.factors.length/2)]:null;
      const targetLines=st.hits+st.eyes+st.misses;
      const op=Object.entries(st.openers).sort((a,b)=>b[1]-a[1]).slice(0,14).map(([w,n])=>w+' '+(100*n/(st.lines-o.sheets)).toFixed(1)+'%');
      return {
        cfg:{sheets:o.sheets,tier:o.tier,T:o.T,seed:o.seed,mods:o.mods,cams:o.cams,sorts:BASE_N,wheels:WHEELS,corpusLines:LINES.length},
        fidelity:+(100*st.quoted/st.words).toFixed(1),
        derailment:+(100*st.noTri/st.draws).toFixed(1),
        secondDraw:{noTri:+(100*st.d2noTri/st.d2).toFixed(1),noBi:+(100*st.d2noBi/st.d2).toFixed(1)},
        bareEnds:+(100*st.bareEnds/st.lines).toFixed(1), dashLines:+(100*st.dash/st.lines).toFixed(1),
        rhymeRate: targetLines?+(100*(st.hits+st.eyes)/targetLines).toFixed(1):null, hits:st.hits, eyes:st.eyes, misses:st.misses,
        cause:Object.fromEntries(Object.entries(st.cause).map(([k,v])=>[k,+(100*v/st.lines).toFixed(1)])),
        rhymeCam:{events:st.boostEvents,noRhyme:st.noRhyme,meanCands:st.boosted?+(st.candSum/st.boosted).toFixed(1):null,meanNaturalMassPct:st.boosted?+(100*st.massSum/st.boosted).toFixed(2):null,medianBoost:med?Math.round(med):null},
        concord:{struck:st.struck,linesWithVerbPct:+(100*st.linesWithVerb/st.lines).toFixed(1)},
        openLinesPct:+(100*st.open/st.lines).toFixed(1), line14Words:+(st.l14w/Math.max(1,st.l14n)).toFixed(1),
        lines:st.lines, draws:st.draws, openers:op, specimens
      };
    },
    vocabFacts(tier){
      if(FOLIO!==tier) buildModel(tier);
      const ee=[]; for(let i=0;i<vocabArr.length;i++){ const w=vocabArr[i]; if(!isWordId(i)) continue; if(rhymeKey(w)==='ee') ee.push(w); }
      const yEnd=ee.filter(w=>/y$/.test(w)).length;
      const c=id=>uniC[vocabId.get(id)]||0;
      const punct=vocabArr.filter(w=>PUNCT.has(w));
      const quoteSorts=vocabArr.filter(w=>/^'|'$/.test(w)&&!/^o'|s'$/.test(w));
      const foolsRh=vocabArr.filter((w,i)=>isWordId(i)&&rhymes(w,'fools'));
      const lens=LINES.map(l=>l.split(/\s+/).filter(w=>!PUNCT.has(w)).length).sort((a,b)=>a-b);
      const mean=lens.reduce((a,b)=>a+b,0)/lens.length;
      return {sorts:BASE_N,wheels:WHEELS,corpusLines:LINES.length,lineWords:{median:lens[Math.floor(lens.length/2)],mean:+mean.toFixed(1),max:lens[lens.length-1],min:lens[0]},
        punctInDrawer:punct, softIds:[...SOFT_IDS].map(i=>vocabArr[i]), termIds:[...TERM_IDS].map(i=>vocabArr[i]),
        eeClass:{size:ee.length,pctVocab:+(100*ee.length/BASE_N).toFixed(1),endingY:yEnd,sample:ee.slice(0,40)},
        cools:c('cools'),fools:c('fools'),foolsRhymes:foolsRh, quoteSorts, openersDistinct:OPENERS.length};
    }
  };
  return 'harness installed';
})()
