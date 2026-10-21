# Generates index.html for the "Block-Chaos" reel (1080x1920, 15 s).
import json, pathlib
HERE = pathlib.Path(__file__).parent
P = 60 / 120.19                      # beat of "Clowns" from 0:16.52 (first downbeat at 0 s)
B = lambda k: round(k * P, 3)
HAT = (165.2, -12.2, 108.7, 110.7)   # crab hat seat (body.png coords), from the hats reel fit
CS = 0.6                            # character scale in world units
FEET = (95, 300)                     # stick tip in body.png coords

# World layout (world px). Platforms: (id, left, top, width, height, kind)
PLAT = [("start", -400, 1300, 660, 700, "ground"), ("f1", 330, 1240, 150, 50, "block"), ("f2", 540, 1170, 150, 50, "block"),
        ("f3", 750, 1240, 150, 50, "block"), ("mv", 960, 1100, 170, 50, "block"), ("tm", 1180, 860, 150, 50, "block"), ("ph", 1770, 1180, 160, 120, "block"),
        ("goal", 2020, 1020, 700, 980, "ground")]
ROT = (1500, 1110, 320, 40)
LAND = [(150, 1300), (405, 1240), (615, 1170), (825, 1240), (1045, 1100), (1350, 1090), (1600, 1180)]
OVER = (1130, 1230, 0.42)            # overview camera (centre x, centre y, scale)

def plat(p):
    i, l, t, w, h, k = p
    return f'<div class="plat {k}" id="{i}" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px"></div>'

def label(i, text):
    return f'<div class="pill" id="lb{i}"><span class="ring"></span><span class="pt">{text}</span><span class="arr">&#9660;</span></div>'

char = (f'<div id="ch"><div id="chs"><div id="chsc" style="transform:scale({CS})"><div id="chi" style="left:{-FEET[0]}px;top:{-FEET[1]}px">'
        f'<img src="img/stick.png" style="position:absolute;left:10px;top:49px" /><img src="img/body.png" style="position:absolute;left:0;top:0" />'
        f'<img src="img/h29.png" style="position:absolute;left:{HAT[0]}px;top:{HAT[1]}px;width:{HAT[2]}px;height:{HAT[3]}px" /></div></div></div></div>')

world = ('<div id="grid"></div>' + "".join(plat(p) for p in PLAT) +
         f'<div id="rot" style="left:{ROT[0]-ROT[2]/2}px;top:{ROT[1]-ROT[3]/2}px;width:{ROT[2]}px;height:{ROT[3]}px"></div>'
         f'<div class="pivot" style="left:{ROT[0]-14}px;top:{ROT[1]-14}px"></div>'
         '<div id="sel"><i></i><i></i><i></i><i></i></div><div id="tap"></div>'
         '<div class="flag" style="left:120px;top:1150px"><div class="cloth green"></div></div>'
         '<div class="flag" style="left:2140px;top:870px"><div class="cloth check"></div></div>')

def cam(cx, cy, s):  # world transform that centres (cx, cy) at screen (540, 1080)
    return dict(x=round(540 - s * cx, 1), y=round(1080 - s * cy, 1), scale=s)

O = cam(*OVER)
js = f"""
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const seen = {{}};
      const ft = (sel, from, to, t) => {{ to.immediateRender = !seen[sel]; seen[sel] = true; tl.fromTo(sel, from, to, t); }};
      const P = {P}, B = k => k * P;
      const shake = (t, a) => tl.to("#shk", {{ x: a, y: -a * 0.6, duration: 0.04, ease: "sine.inOut", yoyo: true, repeat: 5 }}, t);
      const flash = (t, p) => ft("#flash", {{ opacity: p }}, {{ opacity: 0, duration: 0.3, ease: "expo.out" }}, t);
      const slam = (sel, t) => ft(sel, {{ scale: 2.3, opacity: 0, rotation: -8 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.36, ease: "power4.in" }}, t - 0.36);
      const pop = (sel, t) => ft(sel, {{ scale: 0, rotation: -12 }}, {{ scale: 1, rotation: 0, duration: 0.32, ease: "back.out(2.6)" }}, t);
      const camTo = (c, t, d, e) => tl.to("#world", {{ x: c.x, y: c.y, scale: c.scale, duration: d, ease: e || "power3.inOut" }}, t);
      const pillIn = (id, t) => ft(id, {{ x: -1400 }}, {{ x: 0, duration: 0.35, ease: "power3.out" }}, t);
      const pillOut = (id, t) => tl.to(id, {{ x: 1400, duration: 0.25, ease: "power2.in" }}, t);
      tl.set("#world", {json.dumps(O)}, 0);
      // 1 Empty level + grid
      ft("#grid", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.5, ease: "power2.out" }}, 0);
      slam("#h1", B(1)); shake(B(1), 12); flash(B(1), 0.35);
      tl.to("#h1", {{ y: -60, opacity: 0, duration: 0.25, ease: "power2.in" }}, B(3) - 0.25);
      // editor selection frame jumps to every block that gets placed
      const sel = (b, t) => {{
        tl.set("#sel", {{ left: b[0] - 14, top: b[1] - 14, width: b[2] + 28, height: b[3] + 28 }}, t);
        ft("#sel", {{ opacity: 0, scale: 1.4 }}, {{ opacity: 1, scale: 1, duration: 0.22, ease: "back.out(2)" }}, t);
      }};
      const hideSel = t => tl.to("#sel", {{ opacity: 0, duration: 0.15, ease: "power2.in" }}, t);
      const ring = (x, y, t) => {{ tl.set("#tap", {{ left: x - 60, top: y - 60 }}, t); ft("#tap", {{ scale: 0.3, opacity: 1 }}, {{ scale: 1.4, opacity: 0, duration: 0.5, ease: "expo.out" }}, t); }};
      // 2 Touch falling blocks (B3-B9)
      camTo({json.dumps(cam(615, 1210, 1.15))}, B(2.4), 0.6);
      pillIn("#lb1", B(3));
      [["#f1", [330, 1240, 150, 50]], ["#f2", [540, 1170, 150, 50]], ["#f3", [750, 1240, 150, 50]]].forEach(([id, bb], i) => {{ pop(id, B(3 + i)); sel(bb, B(3 + i)); }});
      hideSel(B(5.6));
      ring(615, 1170, B(6));
      tl.to("#f2", {{ x: 6, duration: 0.05, ease: "sine.inOut", yoyo: true, repeat: 7 }}, B(6));
      tl.to("#f2", {{ y: 700, rotation: 25, duration: 0.6, ease: "power2.in" }}, B(6.6));
      tl.set("#f2", {{ y: 0, rotation: 0, scale: 0 }}, B(8));
      tl.to("#f2", {{ scale: 1, duration: 0.3, ease: "back.out(2.6)" }}, B(8));
      pillOut("#lb1", B(9) - 0.25);
      // 3 Moving block (B9-B15)
      camTo({json.dumps(cam(1080, 1150, 1.15))}, B(8.6), 0.55);
      pillIn("#lb2", B(9)); pop("#mv", B(9)); sel([960, 1100, 170, 50], B(9)); hideSel(B(10.4));
      tl.to("#mv", {{ x: 140, duration: P, ease: "sine.inOut", yoyo: true, repeat: 7 }}, B(10.5));
      pillOut("#lb2", B(15) - 0.25);
      // 4 Touch moving block (B15-B20)
      camTo({json.dumps(cam(1255, 1000, 1.15))}, B(14.6), 0.55);
      pillIn("#lb5", B(15)); pop("#tm", B(15)); sel([1180, 860, 150, 50], B(15)); hideSel(B(16.4));
      ring(1255, 860, B(17));
      tl.to("#tm", {{ y: -160, duration: 0.6, ease: "power2.inOut" }}, B(17.3));
      tl.to("#tm", {{ y: 0, duration: 0.6, ease: "power2.inOut" }}, B(18.8));
      pillOut("#lb5", B(20) - 0.25);
      // 5 Rotating block, snapping 90 degrees on every beat (B20-B25)
      camTo({json.dumps(cam(1500, 1110, 1.15))}, B(19.6), 0.55);
      pillIn("#lb3", B(20)); pop("#rot", B(20)); sel([1340, 1090, 320, 40], B(20)); hideSel(B(20.8));
      [21, 22, 23, 24].forEach((k, i) => tl.to("#rot", {{ rotation: 90 * (i + 1), duration: 0.28, ease: "back.out(2)" }}, B(k) - 0.1));
      pillOut("#lb3", B(25) - 0.25);
      // 6 Physics block over the death zone (B25-B29), then zoom out
      camTo({json.dumps(cam(1850, 1260, 1.15))}, B(24.6), 0.55);
      pillIn("#lb4", B(25)); pop("#ph", B(25)); sel([1770, 1180, 160, 120], B(25)); hideSel(B(26));
      tl.to("#ph", {{ rotation: 14, duration: 0.3, ease: "power2.in", yoyo: true, repeat: 3 }}, B(26.2));
      pillOut("#lb4", B(28.4));
      camTo({json.dumps(O)}, B(28.6), 0.9);
      // 7 Finished course stays alive on the beat
      [30, 31, 32, 33, 34, 35].forEach((k, i) => tl.to("#rot", {{ rotation: 360 + 90 * (i + 1), duration: 0.28, ease: "back.out(2)" }}, B(k) - 0.1));
      tl.to("#mv", {{ x: 140, duration: P, ease: "sine.inOut", yoyo: true, repeat: 5 }}, B(30));
      tl.to("#tm", {{ y: -160, duration: 0.6, ease: "power2.inOut", yoyo: true, repeat: 1 }}, B(31.5));
      tl.to("#ph", {{ rotation: -12, duration: 0.3, ease: "power2.in", yoyo: true, repeat: 3 }}, B(31));
      ft("#freeze", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.out" }}, B(30.8));
      slam("#h7", B(31)); shake(B(31), 14); flash(B(31), 0.5);
      ft("#lgw", {{ y: -500, scale: 1.4, opacity: 0 }}, {{ y: 0, scale: 1, opacity: 1, duration: 0.35, ease: "power4.in" }}, B(33.5) - 0.35);
      shake(B(33.5), 8);
      ft("#cta", {{ x: -900 }}, {{ x: 0, duration: 0.35, ease: "power3.out" }}, B(34));
      window.__timelines["main"] = tl;
      tl.seek(0);
"""

html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="gsap.min.js"></script>
    <style>
      @font-face {{ font-family: "Exo2"; src: url("fonts/exo-2-latin-900-italic.woff2") format("woff2"); font-weight: 900; font-style: italic; }}
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b0c0c; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Exo2", sans-serif; font-weight: 900; font-style: italic; text-transform: uppercase;
              background: linear-gradient(180deg, #5f7a66 0%, #95a466 55%, #c9b84a 100%); }}
      #shk {{ position: absolute; inset: 0; }}
      .sun {{ position: absolute; left: 700px; top: 640px; width: 230px; height: 230px; border-radius: 50%; background: #f4c63d; box-shadow: 0 0 120px 40px rgba(244,198,61,.35); }}
      .hills {{ position: absolute; left: 0; bottom: 0; width: 1080px; height: 1000px; }}
      #world {{ position: absolute; left: 0; top: 0; width: 10px; height: 10px; transform-origin: 0 0; }}
      #grid {{ position: absolute; left: -600px; top: 500px; width: 3200px; height: 1100px;
              background-image: linear-gradient(rgba(255,255,255,.22) 2px, transparent 2px), linear-gradient(90deg, rgba(255,255,255,.22) 2px, transparent 2px); background-size: 60px 60px; }}
      .plat {{ position: absolute; background: #17191a; }}
      .plat::before {{ content: ""; position: absolute; left: -2px; right: -2px; top: -12px; height: 18px; background: #2f8a55; border-radius: 6px; }}
      .plat.block {{ border-radius: 6px; transform-origin: 50% 100%; background: #17191a; }}
      .plat.block::before {{ display: none; }}
      #ph {{ transform-origin: 50% 100%; }}
      #sel {{ position: absolute; border: 5px dashed #fff; border-radius: 10px; opacity: 0; z-index: 5; }}
      #sel i {{ position: absolute; width: 18px; height: 18px; background: #fff; border-radius: 4px; }}
      #sel i:nth-child(1) {{ left: -12px; top: -12px; }} #sel i:nth-child(2) {{ right: -12px; top: -12px; }} #sel i:nth-child(3) {{ left: -12px; bottom: -12px; }} #sel i:nth-child(4) {{ right: -12px; bottom: -12px; }}
      #tap {{ position: absolute; width: 120px; height: 120px; border-radius: 50%; border: 12px solid #fff; opacity: 0; z-index: 6; }}
      #rot {{ position: absolute; background: #17191a; border-radius: 10px; }}
      .pivot {{ position: absolute; width: 28px; height: 28px; border-radius: 50%; background: #c3202f; border: 5px solid #fff; }}
      #lava {{ position: absolute; left: -2000px; top: 1540px; width: 6000px; height: 3000px; background: linear-gradient(#c3202f 0, #6e0f19 260px, #2a070b 700px); }}
      #lava::before {{ content: ""; position: absolute; left: 0; top: -18px; width: 100%; height: 22px; background: repeating-linear-gradient(90deg, #c3202f 0 40px, transparent 40px 80px); }}
      .flag {{ position: absolute; width: 10px; height: 150px; background: #e9e4d4; border-radius: 4px; }}
      .cloth {{ position: absolute; left: 10px; top: 4px; width: 90px; height: 60px; }}
      .green {{ background: #2f8a55; clip-path: polygon(0 0, 100% 50%, 0 100%); }}
      .check {{ background: repeating-conic-gradient(#111 0 25%, #fff 0 50%) 0 0 / 30px 30px; }}
      #ch {{ position: absolute; left: 0; top: 0; }}
      #chs, #chsc {{ position: absolute; left: 0; top: 0; transform-origin: 0 0; }}
      #chi {{ position: absolute; width: 330px; height: 380px; }}
      .head {{ position: absolute; left: 0; width: 1080px; text-align: center; font-size: 150px; line-height: .92; }}
      .w {{ color: #fbfbf7; }}
      .y {{ background: linear-gradient(180deg, #ffd400, #ff9a00); -webkit-background-clip: text; background-clip: text; color: transparent; }}
      .bar {{ display: inline-block; padding: 10px 36px 6px; font-size: 64px; transform: rotate(-4deg) skewX(-6deg); }}
      .red {{ background: #c3202f; color: #fff; }}
      .teal {{ background: #0b9396; color: #111; }}
      .pill {{ position: absolute; left: 90px; top: 300px; width: 900px; height: 120px; border-radius: 26px; background: #1b2330; display: flex; align-items: center; padding: 0 24px; gap: 26px; box-shadow: 0 14px 0 rgba(0,0,0,.25); }}
      .ring {{ width: 64px; height: 64px; border-radius: 50%; border: 11px solid #fff; flex: none; }}
      .pt {{ color: #fff; font-size: 50px; white-space: nowrap; flex: 1; letter-spacing: 1px; }}
      .arr {{ width: 84px; height: 84px; border-radius: 14px; background: #a81e32; color: #f3dada; font-size: 44px; display: flex; align-items: center; justify-content: center; font-style: normal; flex: none; }}
      #hint {{ position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; opacity: 0; }}
      #freeze {{ position: absolute; inset: 0; background: rgba(10,12,14,.35); opacity: 0; }}
      #logocard {{ position: absolute; left: 200px; top: 1130px; width: 680px; height: 330px; border-radius: 36px; background: #e9e4d2; box-shadow: 0 16px 0 rgba(0,0,0,.3); }}
      #logo {{ position: absolute; left: 260px; top: 1160px; width: 560px; }}
      #lgw {{ position: absolute; inset: 0; }}
      #cta {{ position: absolute; left: 0; width: 1080px; top: 1420px; text-align: center; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 60; }}
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,.4) 100%); z-index: 40; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="18.5" data-width="1080" data-height="1920">
      <div id="shk" class="clip" data-start="0" data-duration="18.5" data-track-index="0">
        <div class="sun"></div>
        <svg class="hills" viewBox="0 0 1080 1000" preserveAspectRatio="none"><polygon fill="#58735e" points="0,1000 0,560 140,380 260,560 400,300 560,560 700,420 860,560 980,340 1080,480 1080,1000" /><polygon fill="#2f6b4a" points="0,1000 0,700 90,560 180,700 330,520 470,720 640,600 780,720 900,560 1080,740 1080,1000" /></svg>
        <div id="world"><div id="lava"></div>{world}</div>
        <div class="head" id="h1" style="top:300px"><span class="w">BUILD THE</span><br><span class="y">WORST LEVEL.</span></div>
        {label(1, "TOUCH FALLING BLOCK")}{label(2, "MOVING BLOCK")}{label(3, "ROTATING BLOCK")}{label(4, "PHYSICS BLOCK")}{label(5, "TOUCH MOVING BLOCK")}
        <div id="freeze"></div>
        <div class="head" id="h7" style="top:330px"><span class="w">CAN YOU</span><br><span class="y">MAKE IT?</span></div>
        <div id="lgw"><div id="logocard"></div><img id="logo" src="img/logo.png" /></div>
        <div id="cta"><span class="bar red" style="font-size:76px">PLAY NOW.</span></div>
      </div>
      <div id="vig" class="clip" data-start="0" data-duration="18.5" data-track-index="3"></div>
      <div id="flash" class="clip" data-start="0" data-duration="18.5" data-track-index="4"></div>
    </div>
    <script>{js}    </script>
  </body>
</html>
'''
(HERE / "index.html").write_text(html)
