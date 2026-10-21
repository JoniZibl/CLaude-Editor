# Generates index.html for the "Which hat are you?" reel (1080x1920, 15 s).
import math, pathlib
HERE = pathlib.Path(__file__).parent
B0, P = -0.0146, 60 / 139.67       # beat grid of "GLOSS" (measured, first beat ~0 s)
b = lambda k: round(B0 + k * P, 3)
HATS = [f"img/hats/h{i:02d}.png" for i in range(30) if i != 7]   # 29 hats
CROWN, VIKING, TIGER = "img/hats/h03.png", "img/hats/h04.png", "img/hats/h16.png"

# Hat swap times: 1/beat, then 1/2 beat, then 1/4 beat
swaps = [b(k) for k in range(5, 9)] + [b(9 + k / 2) for k in range(8)] + [b(13 + k / 4) for k in range(20)]

def char(cid, hats, x, y, s):
    import json as _j; fit = _j.load(open(HERE / "hatfit.json"))
    imgs = "".join(f'<img class="hat" id="{cid}h{k}" src="{h.replace('/hats/', '/hatfit/')}" style="left:{fit[h][0]}px;top:{fit[h][1]}px;width:{fit[h][2]}px;height:{fit[h][3]}px" />' for k, h in enumerate(hats))
    return (f'<div class="char" id="{cid}" style="left:{x}px;top:{y}px;transform:scale({s})"><div class="bob" id="{cid}b">'
            f'<img class="stick" src="img/stick.png" /><img class="body" src="img/body.png" />{imgs}</div></div>')

def rays(id):
    tri = lambda a: f'0,0 {round(1400*math.cos(math.radians(a-3)))},{round(1400*math.sin(math.radians(a-3)))} {round(1400*math.cos(math.radians(a+3)))},{round(1400*math.sin(math.radians(a+3)))}'
    return f'<svg class="rays" id="{id}" viewBox="-1000 -1000 2000 2000">' + "".join(f'<polygon points="{tri(a)}" />' for a in range(0, 360, 20)) + "</svg>"

roulette = [CROWN if i == len(swaps) - 1 else HATS[i % len(HATS)] for i in range(len(swaps))]
tiles = "".join(f'<img class="tile" src="{HATS[(r*6+c)*7 % len(HATS)]}" style="left:{c*180+20}px;top:{r*180+150}px" />' for r in range(9) for c in range(6))
L = [(0, 0), (110, 140), (30, 260), (140, 420), (60, 560), (170, 700), (40, 860), (130, 1080)]
R = [(2400 - a, b_) for a, b_ in [(120, 1080), (30, 900), (150, 760), (50, 600), (160, 430), (40, 280), (130, 120), (20, 0)]]
pts = " ".join(f"{a},{c}" for a, c in L + R)

js = f"""
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const seen = {{}};
      const ft = (sel, from, to, t) => {{ to.immediateRender = !seen[sel]; seen[sel] = true; tl.fromTo(sel, from, to, t); }};
      const shake = (sel, t, a) => tl.to(sel, {{ x: a, y: -a * 0.6, duration: 0.04, ease: "sine.inOut", yoyo: true, repeat: 5 }}, t);
      const flash = (t, p) => ft("#flash", {{ opacity: p }}, {{ opacity: 0, duration: 0.35, ease: "expo.out" }}, t);
      const slam = (sel, t) => ft(sel, {{ scale: 2.4, opacity: 0, rotation: -8 }}, {{ scale: 1, opacity: 1, rotation: 0, duration: 0.38, ease: "power4.in" }}, t - 0.38);
      const B = k => {B0} + k * {P};
      const swaps = {swaps};
      // 1 Hook: hatless rider bobbing on the beat, question mark, headline slam
      ft("#c1", {{ y: 900 }}, {{ y: 0, duration: 0.6, ease: "power3.out" }}, 0);
      tl.to("#c1b", {{ y: -70, duration: {P/2:.3f}, ease: "power2.out", yoyo: true, repeat: 33 }}, 0);
      ft("#q", {{ scale: 0, rotation: -30 }}, {{ scale: 1, rotation: 0, duration: 0.4, ease: "back.out(3)" }}, B(2));
      tl.to("#q", {{ rotation: 12, duration: {P:.3f}, ease: "sine.inOut", yoyo: true, repeat: 3 }}, B(3));
      tl.to("#q", {{ scale: 0, duration: 0.2, ease: "power2.in" }}, B(5) - 0.2);
      slam("#h1", B(1)); shake("#shk", B(1), 12); flash(B(1), 0.4);
      tl.to("#h1", {{ y: -40, opacity: 0, duration: 0.25, ease: "power2.in" }}, B(5) - 0.25);
      // 2 Hat roulette: swap on the beat, accelerating; counter climbs; camera pushes in
      swaps.forEach((t, i) => {{
        if (i > 0) tl.set("#c1h" + (i - 1), {{ opacity: 0 }}, t);
        const gap = i < swaps.length - 1 ? swaps[i + 1] - t : 0.3;
        ft("#c1h" + i, {{ opacity: 0, scale: 0.4 }}, {{ opacity: 1, scale: 1, duration: Math.min(0.16, gap * 0.8), ease: "back.out(3)" }}, t);
      }});
      ft("#cam", {{ scale: 1 }}, {{ scale: 1.22, duration: B(18) - B(5), ease: "power2.in" }}, B(5));
      ft("#counter", {{ opacity: 0, y: 60 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, B(5));
      const cnt = {{ v: 1 }};
      ft(cnt, {{ v: 1 }}, {{ v: 190, duration: B(18) - B(5), ease: "power2.in", onUpdate: () => {{ document.getElementById("cnum").textContent = String(Math.round(cnt.v)).padStart(3, "0"); }} }}, B(5));
      // crown lands: big hit
      shake("#shk", B(18), 18); flash(B(18), 0.6);
      ft("#ray1", {{ opacity: 0, rotation: 0 }}, {{ opacity: 0.22, rotation: 30, duration: 1.2, ease: "sine.inOut" }}, B(18));
      ft("#legend", {{ scale: 0, rotation: 10 }}, {{ scale: 1, rotation: -4, duration: 0.35, ease: "back.out(3)" }}, B(18.5));
      // 3 Hat wall
      ft(".tile", {{ scale: 0, rotation: 30 }}, {{ scale: 1, rotation: 0, duration: 0.35, ease: "back.out(2.5)", stagger: {{ each: 0.012, from: "center", grid: [9, 6] }} }}, B(20));
      ft("#wallbox", {{ scaleY: 0 }}, {{ scaleY: 1, duration: 0.3, ease: "expo.out" }}, B(22) - 0.3);
      slam("#h3", B(22)); shake("#shk", B(22), 14); flash(B(22), 0.45);
      ft("#h3b", {{ x: -1100 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, B(23));
      tl.to("#wall", {{ scale: 1.08, duration: B(26) - B(20), ease: "sine.inOut" }}, B(20));
      // 4 Three looks
      [0, 1, 2].forEach(k => {{
        ft("#c" + (k + 2), {{ y: 1200 }}, {{ y: 0, duration: 0.45, ease: "power3.out" }}, B(26 + k) - 0.2);
        tl.to("#c" + (k + 2) + "b", {{ y: -50, duration: {P/2:.3f}, ease: "power2.out", yoyo: true, repeat: 7 - 2 * k }}, B(27 + k));
      }});
      slam("#h4", B(29)); shake("#shk", B(29), 10); flash(B(29), 0.35);
      ft("#h4b", {{ x: 1100 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, B(30));
      // 5 Outro
      ft("#logo", {{ y: -900, scale: 1.6 }}, {{ y: 0, scale: 1, duration: 0.35, ease: "power4.in" }}, B(31) - 0.35);
      tl.to("#logo", {{ scaleY: 0.86, scaleX: 1.08, duration: 0.1, ease: "power2.out", yoyo: true, repeat: 1 }}, B(31));
      shake("#shk", B(31), 14); flash(B(31), 0.6);
      ft("#ray5", {{ opacity: 0, rotation: 0 }}, {{ opacity: 0.2, rotation: 30, duration: 1.6, ease: "sine.inOut" }}, B(31));
      ft("#play", {{ scale: 0 }}, {{ scale: 1, duration: 0.4, ease: "back.out(2.5)" }}, B(32));
      tl.to("#play", {{ scale: 1.1, duration: {P/2:.3f}, ease: "sine.inOut", yoyo: true, repeat: 3 }}, B(33));
      ft("#h5", {{ x: -1100 }}, {{ x: 0, duration: 0.4, ease: "power3.out" }}, B(33));
      // Jagged wipes into scene 4 and the outro
      [B(26), B(31)].forEach(c => {{
        ft("#wipe", {{ x: 1080 }}, {{ x: -260, duration: 0.25, ease: "power3.in" }}, c - 0.25);
        tl.to("#wipe", {{ x: -1700, duration: 0.4, ease: "expo.out" }}, c);
      }});
      window.__timelines["main"] = tl;
      tl.seek(0);
"""

S1 = b(26); S2 = b(31)
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
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Exo2", sans-serif; font-weight: 900; font-style: italic; text-transform: uppercase; }}
      .scene {{ position: absolute; inset: 0; overflow: hidden; }}
      .sky {{ background: linear-gradient(180deg, #66806a 0%, #9aa766 55%, #c9b84a 100%); }}
      #shk {{ position: absolute; inset: 0; }}
      .hills {{ position: absolute; left: 0; bottom: 0; width: 1080px; height: 900px; }}
      .sun {{ position: absolute; width: 220px; height: 220px; border-radius: 50%; background: #f4c63d; box-shadow: 0 0 120px 40px rgba(244,198,61,.35); }}
      .ground {{ position: absolute; left: 0; top: 1500px; width: 1080px; height: 420px; background: #1b1d1d; }}
      .ground::before {{ content: ""; position: absolute; left: 0; top: -18px; width: 1080px; height: 30px; background: #2f8a55; border-radius: 0 0 8px 8px; }}
      .char {{ position: absolute; width: 330px; height: 380px; transform-origin: 0 0; }}
      .bob {{ position: absolute; inset: 0; }}
      .stick {{ position: absolute; left: 10px; top: 49px; }}
      .body {{ position: absolute; left: 0; top: 0; }}
      .hat {{ position: absolute; opacity: 0; transform-origin: 50% 100%; }}
      .head {{ font-size: 150px; line-height: .92; letter-spacing: -2px; text-align: center; position: absolute; left: 0; width: 1080px; }}
      .w {{ color: #fbfbf7; }}
      .y {{ background: linear-gradient(180deg, #ffd400, #ff9a00); -webkit-background-clip: text; background-clip: text; color: transparent; }}
      .bar {{ display: inline-block; padding: 10px 36px 6px; font-size: 64px; transform: rotate(-4deg) skewX(-6deg); }}
      .red {{ background: #c3202f; color: #fff; }}
      .teal {{ background: #0b9396; color: #111; }}
      #q {{ position: absolute; left: 640px; top: 470px; font-size: 220px; color: #fff; text-shadow: 0 8px 0 rgba(0,0,0,.25); }}
      #counter {{ position: absolute; left: 0; top: 1580px; width: 1080px; text-align: center; opacity: 0; }}
      #counter .bar {{ font-size: 72px; }}
      #c2 .hat, #c3 .hat, #c4 .hat {{ opacity: 1; }}
      #legend {{ position: absolute; left: 0; top: 330px; width: 1080px; text-align: center; transform: scale(0); }}
      #legend .bar {{ font-size: 96px; }}
      #cam {{ position: absolute; inset: 0; transform-origin: 540px 760px; }}
      #wall {{ position: absolute; inset: 0; background: #0f1418; }}
      .tile {{ position: absolute; width: 140px; height: 140px; }}
      #wallbox {{ position: absolute; left: 0; top: 640px; width: 1080px; height: 560px; background: rgba(11,12,12,.88); }}
      .rays {{ position: absolute; left: -460px; top: -300px; width: 2000px; height: 2000px; fill: #fff; opacity: 0; }}
      #logo {{ position: absolute; left: 90px; top: 520px; width: 900px; }}
      #play {{ position: absolute; left: 330px; top: 1000px; width: 420px; filter: drop-shadow(0 12px 24px rgba(0,0,0,.45)); }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 60; pointer-events: none; }}
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,.4) 100%); z-index: 40; pointer-events: none; }}
      #wipe {{ position: absolute; left: 0; top: 0; width: 1600px; height: 1920px; z-index: 50; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="15" data-width="1080" data-height="1920">
      <div id="shk" class="clip" data-start="0" data-duration="15" data-track-index="0">
        <div id="sA" class="clip scene sky" data-start="0" data-duration="{b(20)}" data-track-index="1">
          <div id="cam">
            <div class="sun" style="left:120px;top:880px"></div>
            <svg class="hills" viewBox="0 0 1080 900" preserveAspectRatio="none"><polygon fill="#58735e" points="0,900 0,560 140,380 260,560 400,300 560,560 700,420 860,560 980,340 1080,480 1080,900" /><polygon fill="#2f6b4a" points="0,900 0,700 90,560 180,700 330,520 470,720 640,600 780,720 900,560 1080,740 1080,900" /></svg>
            {rays("ray1")}
            <div class="ground"></div>
            {char("c1", roulette, 160, 640, 2.2)}
            <div id="q">?</div>
          </div>
          <div class="head" id="h1" style="top:240px"><span class="w">WHICH HAT</span><br><span class="y">ARE YOU?</span></div>
          <div id="counter"><span class="bar red">HAT #<span id="cnum">001</span></span></div>
          <div id="legend"><span class="bar teal">LEGENDARY!</span></div>
        </div>
        <div id="sB" class="clip scene" data-start="{b(20)}" data-duration="{round(S1-b(20),3)}" data-track-index="1">
          <div id="wall">{tiles}</div>
          <div id="wallbox"></div>
          <div class="head" id="h3" style="top:700px"><span class="y" style="font-size:230px">240+</span><br><span class="w">COSMETICS.</span></div>
          <div class="head" id="h3b" style="top:1060px"><span class="bar red">HUNDREDS OF HATS.</span></div>
        </div>
        <div id="sC" class="clip scene sky" data-start="{S1}" data-duration="{round(S2-S1,3)}" data-track-index="1">
          <svg class="hills" viewBox="0 0 1080 900" preserveAspectRatio="none"><polygon fill="#58735e" points="0,900 0,560 140,380 260,560 400,300 560,560 700,420 860,560 980,340 1080,480 1080,900" /><polygon fill="#2f6b4a" points="0,900 0,700 90,560 180,700 330,520 470,720 640,600 780,720 900,560 1080,740 1080,900" /></svg>
          <div class="ground"></div>
          {char("c2", [VIKING], -60, 900, 1.6)}
          {char("c3", [CROWN], 270, 870, 1.6)}
          {char("c4", [TIGER], 600, 900, 1.6)}
          <div class="head" id="h4" style="top:250px"><span class="w">FIND YOUR</span><br><span class="y">STYLE.</span></div>
          <div class="head" id="h4b" style="top:560px"><span class="bar teal">190+ HATS TO UNLOCK</span></div>
        </div>
        <div id="sD" class="clip scene" data-start="{S2}" data-duration="{round(15-S2,3)}" data-track-index="1" style="background: radial-gradient(circle at 50% 40%, #8a9a74, #4e6352 75%)">
          {rays("ray5")}
          <img id="logo" src="img/logo.png" />
          <img id="play" src="img/play.png" />
          <div class="head" id="h5" style="top:1300px"><span class="bar red" style="font-size:80px">PLAY NOW.</span></div>
        </div>
      </div>
      <div id="vig" class="clip" data-start="0" data-duration="15" data-track-index="3"></div>
      <div id="flash" class="clip" data-start="0" data-duration="15" data-track-index="4"></div>
      <svg id="wipe" class="clip" data-start="0" data-duration="15" data-track-index="2" viewBox="0 0 2400 1080" preserveAspectRatio="none"><polygon points="{pts}" fill="#0b0c0c" /></svg>
    </div>
    <script>{js}    </script>
  </body>
</html>
'''
(HERE / "index.html").write_text(html)
print("swaps", len(swaps), "beats S1", S1, "S2", S2)
