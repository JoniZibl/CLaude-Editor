# Generates index.html for the "Change your life" meme reel (1080x1920, 11 s).
import json, math, pathlib
HERE = pathlib.Path(__file__).parent
FIT = json.load(open(HERE / "hatfit.json"))
FEET = (95, 300)
END = 11.0
CUTS = [1.5, 2.5, 3.5, 4.5, 5.5]            # epic montage cuts
FREEZE, PUNCH, AGAIN = 6.5, 7.3, 9.0
HATS = [i for i in range(30) if i != 7]
ROUL = [HATS[(k * 7) % len(HATS)] for k in range(12)]   # hats flashing in cut 2

def hat_img(i, cid, k, vis=False):
    l, t, w, h = FIT[f"img/hats/h{i:02d}.png"]
    return f'<img class="hat" id="{cid}h{k}" src="img/hatfit/h{i:02d}.png" style="left:{l}px;top:{t}px;width:{w}px;height:{h}px;opacity:{1 if vis else 0}" />'

def char(cid, x, y, s, hats, vis_first=True):
    imgs = "".join(hat_img(i, cid, k, vis_first and k == 0) for k, i in enumerate(hats))
    return (f'<div class="char" id="{cid}" style="left:{x}px;top:{y}px"><div class="bob" id="{cid}b"><div style="position:absolute;transform:scale({s});transform-origin:0 0">'
            f'<div style="position:absolute;left:{-FEET[0]}px;top:{-FEET[1]}px;width:330px;height:380px">'
            f'<img src="img/stick.png" style="position:absolute;left:10px;top:49px" /><img src="img/body.png" style="position:absolute;left:0;top:0" />{imgs}'
            f'</div></div></div></div>')

def rays(id):
    tri = lambda a: f'0,0 {round(1400*math.cos(math.radians(a-3)))},{round(1400*math.sin(math.radians(a-3)))} {round(1400*math.cos(math.radians(a+3)))},{round(1400*math.sin(math.radians(a+3)))}'
    return f'<svg class="rays" id="{id}" viewBox="-1000 -1000 2000 2000">' + "".join(f'<polygon points="{tri(a)}" />' for a in range(0, 360, 20)) + "</svg>"

SKY = '''<div class="sky"></div><div class="sun"></div>
        <svg class="hills" viewBox="0 0 1080 900" preserveAspectRatio="none"><polygon fill="#58735e" points="0,900 0,560 140,380 260,560 400,300 560,560 700,420 860,560 980,340 1080,480 1080,900" /><polygon fill="#2f6b4a" points="0,900 0,700 90,560 180,700 330,520 470,720 640,600 780,720 900,560 1080,740 1080,900" /></svg>
        <div class="ground"></div>'''

def cap(i, white, yellow):
    return f'<div class="cap" id="cap{i}"><span class="w">{white}</span> <span class="y">{yellow}</span></div>'

scenes = f'''
      <div class="scene" id="m1"><div class="cam" id="cam1">{SKY}<div class="ring" id="ring1"></div>{char("r1", 520, 1500, 1.5, [29])}</div>{cap(1, "ONE", "TAP.")}</div>
      <div class="scene" id="m2"><div class="cam" id="cam2">{SKY}{char("r2", 330, 1700, 2.6, ROUL, False)}</div>{cap(2, "190+", "HATS.")}</div>
      <div class="scene" id="m3"><div class="cam" id="cam3"><div class="gold"></div>{rays("ray3")}{char("r3", 330, 1700, 2.6, [3])}</div>{cap(3, "", "LEGENDARY!")}</div>
      <div class="scene" id="m4"><div class="cam" id="cam4"><img id="boss" src="img/bosses.png" /></div>{cap(4, "EPIC", "BOSSES.")}</div>
      <div class="scene" id="m5"><div class="cam" id="cam5">{SKY}<div id="dark5"></div>
        {"".join(f'<img class="wped" id="wp{k}" src="img/ped_{n}.png" style="left:{40 + k * 255}px" />' for k, n in enumerate(["easy", "normal", "hard", "insane"]))}
        {char("r5", 560, 1050, 1.1, [29])}</div>{cap(5, "4", "WORLDS.")}</div>'''

js = f"""
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const seen = {{}};
      const ft = (sel, from, to, t) => {{ to.immediateRender = !seen[sel]; seen[sel] = true; tl.fromTo(sel, from, to, t); }};
      const shake = (t, a, n) => tl.to("#shk", {{ x: a, y: -a * 0.6, duration: 0.035, ease: "sine.inOut", yoyo: true, repeat: n || 5 }}, t);
      const flash = (t, p) => tl.fromTo("#flash", {{ opacity: p }}, {{ opacity: 0, duration: 0.3, ease: "expo.out", immediateRender: false }}, t);
      const show = (id, a, b) => {{ tl.set(id, {{ opacity: 1 }}, a); tl.set(id, {{ opacity: 0 }}, b); }};
      // 1 Trailer intro: word by word
      [["#t1", 0.15], ["#t2", 0.65], ["#t3", 1.05]].forEach(([id, t]) => ft(id, {{ opacity: 0, scale: 1.25, filter: "blur(10px)" }}, {{ opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.35, ease: "power3.out" }}, t));
      ft("#intro", {{ scale: 1 }}, {{ scale: 1.08, duration: 1.5, ease: "sine.inOut" }}, 0);
      tl.set("#intro", {{ opacity: 0 }}, {CUTS[0]});
      // 2 Epic montage, one cut per second
      const C = {CUTS};
      ["#m1", "#m2", "#m3", "#m4", "#m5"].forEach((id, i) => {{
        show(id, C[i], i < 4 ? C[i + 1] : {PUNCH});
        ft("#cam" + (i + 1), {{ scale: 1.22 }}, {{ scale: 1.0, duration: 0.95, ease: "power2.out" }}, C[i]);
        ft("#cap" + (i + 1), {{ scale: 2.2, opacity: 0, rotation: -6 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: 0.22, ease: "power4.in" }}, C[i] + 0.05);
        flash(C[i], 0.55); shake(C[i] + 0.27, 14);
      }});
      // cut 1: slow-motion tap + jump
      ft("#ring1", {{ scale: 0.3, opacity: 1 }}, {{ scale: 1.6, opacity: 0, duration: 0.6, ease: "expo.out" }}, C[0] + 0.05);
      ft("#r1", {{ x: -200, y: 0, rotation: -10 }}, {{ x: 80, y: -520, rotation: 8, duration: 1.0, ease: "power2.out" }}, C[0]);
      // cut 2: hats flash on the head
      {json.dumps(ROUL)}.forEach((_, k) => {{ const t = C[1] + 0.04 + k * 0.075; if (k) tl.set("#r2h" + (k - 1), {{ opacity: 0 }}, t); tl.set("#r2h" + k, {{ opacity: 1 }}, t); }});
      // cut 3: crown, golden rays
      ft("#ray3", {{ opacity: 0, rotation: 0 }}, {{ opacity: 0.35, rotation: 25, duration: 1.0, ease: "sine.inOut" }}, C[2]);
      ft("#r3h0", {{ y: -260, scale: 1.4 }}, {{ y: 0, scale: 1, duration: 0.3, ease: "back.out(2)" }}, C[2]);
      // cut 4: bosses slam
      ft("#boss", {{ y: -900 }}, {{ y: 0, duration: 0.25, ease: "expo.in" }}, C[3]);
      shake(C[3] + 0.25, 24, 7);
      // cut 5: four worlds slam in, darker each
      [0, 1, 2, 3].forEach(k => ft("#wp" + k, {{ y: 900 }}, {{ y: 0, duration: 0.22, ease: "power4.out" }}, C[4] + 0.08 + k * 0.16));
      ft("#dark5", {{ opacity: 0 }}, {{ opacity: 0.6, duration: 0.7, ease: "power2.in" }}, C[4] + 0.1);
      ft("#r5", {{ y: 0 }}, {{ y: -420, duration: 0.5, ease: "power2.out" }}, C[4] + 0.45);
      // 3 Freeze: colour drains, record scratch
      ft("#shk", {{ filter: "grayscale(0) brightness(1)" }}, {{ filter: "grayscale(1) brightness(0.8)", duration: 0.35, ease: "power2.out" }}, {FREEZE});
      tl.set("#shk", {{ filter: "grayscale(0) brightness(1)" }}, {PUNCH});
      ft("#bars", {{ opacity: 1 }}, {{ opacity: 0, duration: 0.01, ease: "power1.out" }}, {PUNCH});
      // 4 Punchline on white
      show("#punch", {PUNCH}, {AGAIN});
      ft("#pt", {{ opacity: 0, scale: 0.92 }}, {{ opacity: 1, scale: 1, duration: 0.18, ease: "power2.out" }}, {PUNCH + 0.35});
      // 5 ...then you play again
      show("#again", {AGAIN}, {END});
      ft("#r6", {{ y: 900 }}, {{ y: 0, duration: 0.4, ease: "back.out(1.6)" }}, {AGAIN});
      tl.to("#r6b", {{ y: -70, duration: 0.25, ease: "sine.inOut", yoyo: true, repeat: 7 }}, {AGAIN + 0.4});
      ft("#a1", {{ scale: 2.2, opacity: 0, rotation: -6 }}, {{ scale: 1, opacity: 1, rotation: -3, duration: 0.25, ease: "power4.in" }}, {AGAIN + 0.1});
      shake({AGAIN + 0.35}, 10); flash({AGAIN + 0.35}, 0.4);
      ft("#logo", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {AGAIN + 0.8});
      ft("#cta", {{ x: -1100 }}, {{ x: 0, duration: 0.35, ease: "power3.out" }}, {AGAIN + 1.1});
      // loop seam into the black opening
      ft("#loopfade", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.25, ease: "power2.in" }}, {END - 0.25});
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
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #000; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #000; font-family: "Exo2", sans-serif; font-weight: 900; font-style: italic; text-transform: uppercase; }}
      #shk {{ position: absolute; inset: 0; }}
      .scene {{ position: absolute; inset: 0; overflow: hidden; opacity: 0; }}
      .cam {{ position: absolute; inset: 0; transform-origin: 540px 1000px; }}
      .sky {{ position: absolute; inset: 0; background: linear-gradient(180deg, #66806a 0%, #9aa766 55%, #c9b84a 100%); }}
      .sun {{ position: absolute; left: 700px; top: 700px; width: 240px; height: 240px; border-radius: 50%; background: #f4c63d; box-shadow: 0 0 120px 40px rgba(244,198,61,.35); }}
      .hills {{ position: absolute; left: 0; bottom: 0; width: 1080px; height: 900px; }}
      .ground {{ position: absolute; left: 0; top: 1500px; width: 1080px; height: 420px; background: #17191a; }}
      .ground::before {{ content: ""; position: absolute; left: 0; top: -16px; width: 100%; height: 26px; background: #2f8a55; border-radius: 0 0 8px 8px; }}
      .char {{ position: absolute; }}
      .bob {{ position: absolute; left: 0; top: 0; }}
      .hat {{ position: absolute; }}
      .ring {{ position: absolute; left: 690px; top: 1250px; width: 260px; height: 260px; border-radius: 50%; border: 16px solid #fff; opacity: 0; }}
      .gold {{ position: absolute; inset: 0; background: radial-gradient(circle at 50% 45%, #ffd75e, #c98a12 55%, #4a2f06 100%); }}
      .rays {{ position: absolute; left: -460px; top: -100px; width: 2000px; height: 2000px; fill: #fff6c8; opacity: 0; }}
      #boss {{ position: absolute; left: -796px; top: 260px; width: 1960px; height: 1470px; }}
      #dark5 {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 70%, rgba(40,4,8,.3), rgba(10,2,4,.95) 80%); opacity: 0; }}
      .wped {{ position: absolute; top: 1080px; width: 240px; height: 337px; }}
      .cap {{ position: absolute; left: 0; width: 1080px; top: 330px; text-align: center; font-size: 150px; line-height: 1; }}
      .cap .w, #a1 .w {{ text-shadow: 0 10px 0 rgba(0,0,0,.45); }}
      .w {{ color: #fbfbf7; }}
      .y {{ background: linear-gradient(180deg, #ffe14d, #ffa600); -webkit-background-clip: text; background-clip: text; color: transparent; text-shadow: none; filter: drop-shadow(0 10px 0 rgba(0,0,0,.45)); }}
      #intro {{ position: absolute; inset: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 18px; transform-origin: 540px 960px; }}
      #intro div {{ font-size: 110px; color: #fbfbf7; letter-spacing: 4px; font-style: normal; }}
      #t3 {{ font-size: 150px !important; color: #ffc400 !important; }}
      #bars {{ position: absolute; inset: 0; pointer-events: none; z-index: 20; }}
      #bars::before, #bars::after {{ content: ""; position: absolute; left: 0; width: 1080px; height: 200px; background: #000; }}
      #bars::before {{ top: 0; }} #bars::after {{ bottom: 0; }}
      #punch {{ position: absolute; inset: 0; background: #f4f2ec; opacity: 0; z-index: 45; display: flex; align-items: center; justify-content: center; }}
      #pt {{ font-size: 58px; color: #222; text-transform: lowercase; font-style: normal; letter-spacing: 1px; }}
      #again {{ position: absolute; inset: 0; opacity: 0; z-index: 26; overflow: hidden; }}
      #a1 {{ position: absolute; left: 0; width: 1080px; top: 300px; text-align: center; font-size: 120px; line-height: 1; }}
      #logo {{ position: absolute; left: 300px; top: 620px; width: 480px; }}
      #cta {{ position: absolute; left: 0; width: 1080px; top: 860px; text-align: center; }}
      .bar {{ display: inline-block; padding: 10px 36px 6px; font-size: 76px; transform: rotate(-4deg) skewX(-6deg); background: #c3202f; color: #fff; }}
      #loopfade {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 70; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 60; }}
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.45) 100%); z-index: 40; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <div id="shk" class="clip" data-start="0" data-duration="{END}" data-track-index="0">
        <div id="intro"><div id="t1">THIS GAME</div><div id="t2">WILL CHANGE</div><div id="t3">YOUR LIFE.</div></div>
        {scenes}
        <div id="bars"></div>
      </div>
      <div id="punch" class="clip" data-start="0" data-duration="{END}" data-track-index="1"><div id="pt">for like 10 minutes.</div></div>
      <div id="again" class="clip" data-start="0" data-duration="{END}" data-track-index="2">
        {SKY}
        {char("r6", 560, 1500, 1.3, [3])}
        <div id="a1"><span class="w">...THEN YOU</span><br><span class="y">PLAY AGAIN.</span></div>
        <img id="logo" src="img/logo.png" />
        <div id="cta"><span class="bar">PLAY NOW.</span></div>
      </div>
      <div id="vig" class="clip" data-start="0" data-duration="{END}" data-track-index="3"></div>
      <div id="flash" class="clip" data-start="0" data-duration="{END}" data-track-index="4"></div>
      <div id="loopfade" class="clip" data-start="0" data-duration="{END}" data-track-index="5"></div>
    </div>
    <script>{js}    </script>
  </body>
</html>
'''
(HERE / "index.html").write_text(html)
