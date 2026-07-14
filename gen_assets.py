#!/usr/bin/env python3
"""Generate social-preview and favicon assets for the Analytical Language Engine, in brass."""
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = r"C:\Users\chorr\Documents\Analytical-Language-Engine"
FONTS = r"C:\Windows\Fonts"

# --- palette (from the page) ---
WOOD_D=(20,12,7); WOOD_M=(58,39,23); WOOD_G=(74,50,28)
BRASS_HI=(242,217,142); BRASS=(201,162,75); BRASS_M=(168,130,58)
BRASS_LO=(107,83,32); BRASS_D=(69,51,16)
COPPER=(207,154,98); CREAM=(238,227,200); LIGHTINK=(233,220,184)

def font(name,size): return ImageFont.truetype(f"{FONTS}\\{name}",size)

def gear_pts(cx,cy,r,teeth,root=0.76):
    N=teeth*4; pts=[]
    for i in range(N):
        a=i/N*2*math.pi
        rr=r if (i%4<2) else r*root
        pts.append((cx+math.cos(a)*rr, cy+math.sin(a)*rr))
    return pts

def draw_gear(d,cx,cy,r,teeth,body=BRASS,inner=BRASS_M,hub=BRASS_D,
              rim=BRASS_LO,hole=WOOD_D,spokes=True,glow=None):
    d.polygon(gear_pts(cx,cy,r,teeth),fill=body,outline=rim,width=max(1,int(r*0.02)))
    d.ellipse([cx-r*0.62,cy-r*0.62,cx+r*0.62,cy+r*0.62],fill=inner)
    if spokes:
        for k in range(6):
            a=k/6*2*math.pi
            d.line([cx,cy,cx+math.cos(a)*r*0.6,cy+math.sin(a)*r*0.6],
                   fill=hub,width=max(2,int(r*0.09)))
    d.ellipse([cx-r*0.4,cy-r*0.4,cx+r*0.4,cy+r*0.4],fill=hub)
    if glow:
        d.ellipse([cx-r*0.2,cy-r*0.2,cx+r*0.2,cy+r*0.2],fill=glow)
    d.ellipse([cx-r*0.13,cy-r*0.13,cx+r*0.13,cy+r*0.13],fill=hole)

def fit(d,text,path,start,track,maxw):
    size=start
    while size>10:
        f=font(path,size)
        w=sum(d.textlength(c,font=f) for c in text)+track*(len(text)-1)
        if w<=maxw: return f
        size-=2
    return font(path,size)

def tracked(d,cx,y,text,fnt,fill,track,shadow=None):
    ws=[d.textlength(ch,font=fnt) for ch in text]
    total=sum(ws)+track*(len(text)-1)
    x=cx-total/2
    for ch,w in zip(text,ws):
        if shadow:
            d.text((x+shadow[2],y+shadow[3]),ch,font=fnt,fill=shadow[:3],anchor="lm")
        d.text((x,y),ch,font=fnt,fill=fill,anchor="lm")
        x+=w+track

def radial_alpha(size,cx,cy,inner_r,outer_r,inv=False):
    """L image: opaque(255) toward edges by default (vignette overlay)."""
    m=Image.new("L",size,0); md=ImageDraw.Draw(m)
    steps=60
    for i in range(steps,-1,-1):
        t=i/steps
        rr=inner_r+(outer_r-inner_r)*t
        val=int(255*t)
        md.ellipse([cx-rr,cy-rr,cx+rr,cy+rr],fill=val)
    m=m.filter(ImageFilter.GaussianBlur(size[0]//40))
    if not inv:
        m=Image.eval(m,lambda v:255-v)
    return m

# ============================================================ OG IMAGE
def make_og():
    S=2; W,H=1200*S,630*S
    img=Image.new("RGB",(W,H),WOOD_D); d=ImageDraw.Draw(img,"RGBA")
    # warm top-centre glow
    glow=Image.new("L",(W,H),0); gd=ImageDraw.Draw(glow)
    gd.ellipse([W*0.2,-H*0.5,W*0.8,H*0.75],fill=255)
    glow=glow.filter(ImageFilter.GaussianBlur(160*S))
    warm=Image.new("RGB",(W,H),WOOD_G); img=Image.composite(warm,img,glow); d=ImageDraw.Draw(img,"RGBA")
    # faint vertical grain
    for x in range(0,W,7*S):
        d.line([x,0,x,H],fill=(0,0,0,26),width=S)
    # decorative gears (behind)
    draw_gear(d,110*S,560*S,255*S,12,body=(150,120,55),inner=(120,95,44),
              hub=(70,52,20),rim=BRASS_D,spokes=True)
    draw_gear(d,1120*S,70*S,150*S,10,body=(150,120,55),inner=(120,95,44),
              hub=(70,52,20),rim=BRASS_D,spokes=True)
    draw_gear(d,1150*S,610*S,120*S,9,body=(140,112,52),inner=(112,88,40),
              hub=(66,48,18),rim=BRASS_D,spokes=True)
    # vignette to sink the gears & frame the text
    vig=radial_alpha((W,H),W//2,H//2,W*0.28,W*0.72)
    black=Image.new("RGB",(W,H),(10,7,3))
    img=Image.composite(black,img,vig); d=ImageDraw.Draw(img,"RGBA")
    # brass border + screws
    inset=34*S; d.rounded_rectangle([inset,inset,W-inset,H-inset],
        radius=22*S,outline=BRASS,width=5*S)
    for sx,sy in [(inset,inset),(W-inset,inset),(inset,H-inset),(W-inset,H-inset)]:
        d.ellipse([sx-9*S,sy-9*S,sx+9*S,sy+9*S],fill=BRASS_M,outline=BRASS_D,width=S)
        d.ellipse([sx-3*S,sy-3*S,sx+3*S,sy+3*S],fill=BRASS_HI)
    cx=W//2
    # ornament gear
    draw_gear(d,cx,150*S,26*S,8,body=BRASS,inner=BRASS_M,hub=BRASS_D,
              rim=BRASS_LO,spokes=False,glow=BRASS_HI)
    # title (auto-fit both lines to the safe width, longer line governs)
    safe=1000*S; ttrack=9*S
    tf=fit(d,"LANGUAGE ENGINE","georgiab.ttf",90*S,ttrack,safe)
    tracked(d,cx,256*S,"THE ANALYTICAL",tf,BRASS_HI,ttrack,shadow=(50,34,10,0,3*S))
    tracked(d,cx,358*S,"LANGUAGE ENGINE",tf,BRASS_HI,ttrack,shadow=(50,34,10,0,3*S))
    # rule
    rw=560*S
    d.line([cx-rw//2,420*S,cx+rw//2,420*S],fill=BRASS_M,width=2*S)
    for ex in (cx-rw//2,cx+rw//2):
        d.ellipse([ex-4*S,420*S-4*S,ex+4*S,420*S+4*S],fill=BRASS)
    # subtitle (auto-fit)
    sub="How a Large Language Model works, rendered in brass after Mr. Babbage"
    sf=fit(d,sub,"georgiai.ttf",34*S,1*S,1040*S)
    tracked(d,cx,470*S,sub,sf,CREAM,1*S)
    # ILM badge (pill)
    bf=font("georgia.ttf",23*S)
    label="AN  INFINITESIMAL  LANGUAGE  MODEL"
    tw=sum(d.textlength(c,font=bf) for c in label)+3*S*(len(label)-1)
    bx0,bx1=cx-tw/2-26*S,cx+tw/2+26*S; by=524*S
    d.rounded_rectangle([bx0,by-24*S,bx1,by+24*S],radius=24*S,outline=BRASS_LO,width=2*S)
    tracked(d,cx,by,label,bf,BRASS,3*S)
    img=img.resize((1200,630),Image.LANCZOS)
    img.save(f"{OUT}\\og-image.png",optimize=True)
    print("og-image.png", img.size)

# ============================================================ ICON
def icon_master(px):
    S=3; W=px*S
    img=Image.new("RGB",(W,W),(24,16,9)); d=ImageDraw.Draw(img,"RGBA")
    # warm centre glow
    g=Image.new("L",(W,W),0); gd=ImageDraw.Draw(g)
    gd.ellipse([W*0.12,W*0.12,W*0.88,W*0.88],fill=255)
    g=g.filter(ImageFilter.GaussianBlur(W//9))
    warm=Image.new("RGB",(W,W),(60,40,20)); img=Image.composite(warm,img,g)
    d=ImageDraw.Draw(img,"RGBA")
    c=W/2; r=W*0.40
    # glow behind gear hub
    hb=Image.new("L",(W,W),0); hd=ImageDraw.Draw(hb)
    hd.ellipse([c-r*0.5,c-r*0.5,c+r*0.5,c+r*0.5],fill=255)
    hb=hb.filter(ImageFilter.GaussianBlur(W//12))
    hg=Image.new("RGB",(W,W),(120,90,40)); img=Image.composite(hg,img,hb)
    d=ImageDraw.Draw(img,"RGBA")
    draw_gear(d,c,c,r,10,body=BRASS,inner=BRASS_M,hub=BRASS_D,rim=BRASS_LO,
              spokes=True,glow=(150,116,52))
    # bright center
    d.ellipse([c-r*0.1,c-r*0.1,c+r*0.1,c+r*0.1],fill=BRASS_HI)
    return img.resize((px,px),Image.LANCZOS)

def make_icons():
    master=icon_master(512)
    master.save(f"{OUT}\\icon-512.png",optimize=True)
    for sz,name in [(192,"icon-192.png"),(180,"apple-touch-icon.png"),
                    (32,"favicon-32.png"),(16,"favicon-16.png")]:
        icon_master(sz).save(f"{OUT}\\{name}",optimize=True)
        print(name,"ok")
    # multi-size ico
    master.save(f"{OUT}\\favicon.ico",sizes=[(16,16),(32,32),(48,48)])
    print("favicon.ico ok")

make_og()
make_icons()
print("done")
