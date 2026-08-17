#!/usr/bin/env python3
"""Generate social-preview and favicon assets for the Analytical BARD Engine — the parent's
brass family look, with a quill laid across the gear.  Run from anywhere; writes into bard/."""
import math, sys, importlib.util
from PIL import Image, ImageDraw, ImageFont, ImageFilter

PARENT = r"C:\Users\chorr\Documents\Analytical-Language-Engine"
OUT    = PARENT + r"\bard"
FONTS  = r"C:\Windows\Fonts"

# reuse the parent's drawing helpers & palette verbatim (do not fork the look)
spec = importlib.util.spec_from_file_location("gen_assets", PARENT + r"\gen_assets.py")
src = open(PARENT + r"\gen_assets.py", encoding="utf-8").read()
src = src.replace("make_og()\nmake_icons()\nprint(\"done\")", "")   # import helpers only
ns = {}; exec(compile(src, "gen_assets.py", "exec"), ns)
gear_pts, draw_gear, fit, tracked, radial_alpha, font = (ns[k] for k in
    ("gear_pts","draw_gear","fit","tracked","radial_alpha","font"))
WOOD_D,WOOD_G,BRASS_HI,BRASS,BRASS_M,BRASS_LO,BRASS_D,CREAM = (ns[k] for k in
    ("WOOD_D","WOOD_G","BRASS_HI","BRASS","BRASS_M","BRASS_LO","BRASS_D","CREAM"))
INK_BLUE=(46,77,123)   # the card's blue ink

def draw_quill(d, x0, y0, L, ang_deg, S, ink=INK_BLUE):
    """A quill from nib (x0,y0) up-right along ang_deg for length L: shaft, barbs, nib, and a drop of ink."""
    a=math.radians(ang_deg); ux,uy=math.cos(a),-math.sin(a)          # along the shaft
    px,py=-uy,ux                                                     # perpendicular
    x1,y1=x0+ux*L,y0+uy*L
    # feather vane: two lobes either side of the upper 65% of the shaft
    vane=[]
    n=26
    for i in range(n+1):
        t=0.32+0.68*i/n; w=L*0.16*math.sin(math.pi*(t-0.32)/0.68)**0.7*(1.0 if i<n else 0.2)
        vane.append((x0+ux*L*t+px*w, y0+uy*L*t+py*w))
    for i in range(n,-1,-1):
        t=0.32+0.68*i/n; w=L*0.11*math.sin(math.pi*(t-0.32)/0.68)**0.7*(1.0 if i<n else 0.2)
        vane.append((x0+ux*L*t-px*w, y0+uy*L*t-py*w))
    d.polygon(vane, fill=(238,227,200), outline=(120,95,50), width=max(1,int(S*1.2)))
    # barbs
    for i in range(1,14):
        t=0.36+0.60*i/14; w=L*0.15*math.sin(math.pi*(t-0.32)/0.68)**0.7
        bx,by=x0+ux*L*t, y0+uy*L*t
        d.line([bx,by, bx+px*w*0.9+ux*L*0.05, by+py*w*0.9+uy*L*0.05], fill=(190,170,125), width=max(1,int(S*0.9)))
        d.line([bx,by, bx-px*w*0.65+ux*L*0.05, by-py*w*0.65+uy*L*0.05], fill=(190,170,125), width=max(1,int(S*0.9)))
    # shaft
    d.line([x0,y0,x1,y1], fill=(120,95,50), width=max(2,int(S*3.4)))
    d.line([x0,y0,x1,y1], fill=(220,200,150), width=max(1,int(S*1.4)))
    # nib
    nl=L*0.11
    d.polygon([(x0,y0),(x0+ux*nl+px*nl*0.28,y0+uy*nl+py*nl*0.28),(x0+ux*nl-px*nl*0.28,y0+uy*nl-py*nl*0.28)],
              fill=BRASS, outline=BRASS_D, width=max(1,int(S)))
    d.line([x0,y0,x0+ux*nl*0.7,y0+uy*nl*0.7], fill=BRASS_D, width=max(1,int(S*0.8)))
    # ink drop just past the nib
    r=L*0.035
    d.ellipse([x0-ux*r*1.2-r, y0-uy*r*1.2-r, x0-ux*r*1.2+r, y0-uy*r*1.2+r], fill=ink)

# ============================================================ OG IMAGE
def make_og():
    S=2; W,H=1200*S,630*S
    img=Image.new("RGB",(W,H),WOOD_D); d=ImageDraw.Draw(img,"RGBA")
    glow=Image.new("L",(W,H),0); gd=ImageDraw.Draw(glow)
    gd.ellipse([W*0.2,-H*0.5,W*0.8,H*0.75],fill=255)
    glow=glow.filter(ImageFilter.GaussianBlur(160*S))
    warm=Image.new("RGB",(W,H),WOOD_G); img=Image.composite(warm,img,glow); d=ImageDraw.Draw(img,"RGBA")
    for x in range(0,W,7*S): d.line([x,0,x,H],fill=(0,0,0,26),width=S)
    draw_gear(d,110*S,560*S,255*S,12,body=(150,120,55),inner=(120,95,44),hub=(70,52,20),rim=BRASS_D,spokes=True)
    draw_gear(d,1120*S,70*S,150*S,10,body=(150,120,55),inner=(120,95,44),hub=(70,52,20),rim=BRASS_D,spokes=True)
    draw_gear(d,1150*S,610*S,120*S,9,body=(140,112,52),inner=(112,88,40),hub=(66,48,18),rim=BRASS_D,spokes=True)
    vig=radial_alpha((W,H),W//2,H//2,W*0.28,W*0.72)
    black=Image.new("RGB",(W,H),(10,7,3)); img=Image.composite(black,img,vig); d=ImageDraw.Draw(img,"RGBA")
    inset=34*S; d.rounded_rectangle([inset,inset,W-inset,H-inset],radius=22*S,outline=BRASS,width=5*S)
    for sx,sy in [(inset,inset),(W-inset,inset),(inset,H-inset),(W-inset,H-inset)]:
        d.ellipse([sx-9*S,sy-9*S,sx+9*S,sy+9*S],fill=BRASS_M,outline=BRASS_D,width=S)
        d.ellipse([sx-3*S,sy-3*S,sx+3*S,sy+3*S],fill=BRASS_HI)
    cx=W//2
    # ornament: gear with a quill laid across it
    draw_gear(d,cx,140*S,26*S,8,body=BRASS,inner=BRASS_M,hub=BRASS_D,rim=BRASS_LO,spokes=False,glow=BRASS_HI)
    draw_quill(d,cx-34*S,166*S,84*S,42,S)
    # title
    safe=1000*S; ttrack=9*S
    tf=fit(d,"THE ANALYTICAL","georgiab.ttf",90*S,ttrack,safe)
    tracked(d,cx,256*S,"THE ANALYTICAL",tf,BRASS_HI,ttrack,shadow=(50,34,10,0,3*S))
    tracked(d,cx,358*S,"BARD ENGINE",tf,BRASS_HI,ttrack,shadow=(50,34,10,0,3*S))
    rw=560*S
    d.line([cx-rw//2,420*S,cx+rw//2,420*S],fill=BRASS_M,width=2*S)
    for ex in (cx-rw//2,cx+rw//2): d.ellipse([ex-4*S,420*S-4*S,ex+4*S,420*S+4*S],fill=BRASS)
    sub="An LLM schooled on nothing but Shakespeare’s Sonnets — the brass engine, re-read"
    sf=fit(d,sub,"georgiai.ttf",34*S,1*S,1040*S)
    tracked(d,cx,470*S,sub,sf,CREAM,1*S)
    bf=font("georgia.ttf",23*S)
    label="A  FINE-TUNE  IN  BRASS  ·  5  TO  20  SONNETS"
    tw=sum(d.textlength(c,font=bf) for c in label)+3*S*(len(label)-1)
    bx0,bx1=cx-tw/2-26*S,cx+tw/2+26*S; by=524*S
    d.rounded_rectangle([bx0,by-24*S,bx1,by+24*S],radius=24*S,outline=BRASS_LO,width=2*S)
    tracked(d,cx,by,label,bf,BRASS,3*S)
    img=img.resize((1200,630),Image.LANCZOS)
    img.save(f"{OUT}\\og-image.png",optimize=True); print("og-image.png",img.size)

# ============================================================ ICON
def icon_master(px):
    S=3; W=px*S
    img=Image.new("RGB",(W,W),(24,16,9)); d=ImageDraw.Draw(img,"RGBA")
    g=Image.new("L",(W,W),0); gd=ImageDraw.Draw(g)
    gd.ellipse([W*0.12,W*0.12,W*0.88,W*0.88],fill=255); g=g.filter(ImageFilter.GaussianBlur(W//9))
    warm=Image.new("RGB",(W,W),(60,40,20)); img=Image.composite(warm,img,g); d=ImageDraw.Draw(img,"RGBA")
    c=W/2; r=W*0.40
    hb=Image.new("L",(W,W),0); hd=ImageDraw.Draw(hb)
    hd.ellipse([c-r*0.5,c-r*0.5,c+r*0.5,c+r*0.5],fill=255); hb=hb.filter(ImageFilter.GaussianBlur(W//12))
    hg=Image.new("RGB",(W,W),(120,90,40)); img=Image.composite(hg,img,hb); d=ImageDraw.Draw(img,"RGBA")
    draw_gear(d,c,c,r,10,body=BRASS,inner=BRASS_M,hub=BRASS_D,rim=BRASS_LO,spokes=True,glow=(150,116,52))
    d.ellipse([c-r*0.1,c-r*0.1,c+r*0.1,c+r*0.1],fill=BRASS_HI)
    # the quill, laid across the gear from lower-left to upper-right
    draw_quill(d, c-r*0.95, c+r*0.95, r*2.05, 45, W/64)
    return img.resize((px,px),Image.LANCZOS)

def make_icons():
    master=icon_master(512); master.save(f"{OUT}\\icon-512.png",optimize=True)
    for sz,name in [(192,"icon-192.png"),(180,"apple-touch-icon.png"),(32,"favicon-32.png"),(16,"favicon-16.png")]:
        icon_master(sz).save(f"{OUT}\\{name}",optimize=True); print(name,"ok")
    master.save(f"{OUT}\\favicon.ico",sizes=[(16,16),(32,32),(48,48)]); print("favicon.ico ok")

# ============================================================ SVG favicon (parent's gear + a quill)
def make_svg():
    svg=open(PARENT+r"\favicon.svg",encoding="utf-8").read()
    quill='''  <!-- the quill: laid across the gear, nib lower-left -->
  <g transform="rotate(-45 32 32)">
    <path d="M32 9 C 27 16, 25 24, 25.5 33 L 32 31 L 38.5 33 C 39 24, 37 16, 32 9 Z" fill="#eee3c8" stroke="#7a6130" stroke-width="0.9"/>
    <path d="M32 12 L 32 50" stroke="#7a6130" stroke-width="2.2" stroke-linecap="round"/>
    <path d="M32 12 L 32 50" stroke="#e8cd85" stroke-width="0.9" stroke-linecap="round"/>
    <path d="M29.6 47.5 L 32 55 L 34.4 47.5 Z" fill="#c9a24b" stroke="#453310" stroke-width="0.7"/>
    <circle cx="32" cy="57.4" r="1.4" fill="#2e4d7b"/>
  </g>
</svg>'''
    assert svg.rstrip().endswith("</svg>")
    svg=svg.rstrip()[:-len("</svg>")]+quill
    open(f"{OUT}\\favicon.svg","w",encoding="utf-8").write(svg); print("favicon.svg ok")

def make_manifest():
    m='''{
  "name": "The Analytical Bard Engine",
  "short_name": "Bard Engine",
  "description": "An LLM schooled on nothing but Shakespeare's Sonnets — the brass engine, re-read.",
  "start_url": "./",
  "scope": "./",
  "display": "standalone",
  "background_color": "#140c07",
  "theme_color": "#1a100a",
  "icons": [
    { "src": "favicon.svg", "type": "image/svg+xml", "sizes": "any" },
    { "src": "icon-192.png", "type": "image/png", "sizes": "192x192" },
    { "src": "icon-512.png", "type": "image/png", "sizes": "512x512" },
    { "src": "apple-touch-icon.png", "type": "image/png", "sizes": "180x180", "purpose": "any" }
  ]
}
'''
    open(f"{OUT}\\site.webmanifest","w",encoding="utf-8").write(m); print("site.webmanifest ok")

make_og(); make_icons(); make_svg(); make_manifest(); print("done")
