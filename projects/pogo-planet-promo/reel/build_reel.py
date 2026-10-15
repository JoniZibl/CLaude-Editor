# Generates reel/index.html (1080x1920) from the landscape scene assets.
import math, pathlib
HERE = pathlib.Path(__file__).parent
SC = 0.967
FOC = {1: (803, 100), 2: (803, 150), 3: (803, 0), 4: (760, 100), 5: (803, 240), 6: (780, 250)}
TS = {1: (740, 745), 2: (744, 626), 3: (881, 658), 4: (788, 612), 5: (781, 713), 6: (740, 657)}

def tpos(i):
    w, h = TS[i]; s = min(520 / h, 940 / w)
    return s, (1080 - w * s) / 2, 230 + (520 - h * s) / 2

def scene(i, inner):
    x0, y0 = FOC[i]; s, tx, ty = tpos(i); w, h = TS[i]
    return f'''
      <div id="s{i}" class="clip scene" data-start="{2.5*i}" data-duration="2.5" data-track-index="1">
        <div class="shake" id="sh{i}">
          <div class="game"><div class="cam" id="cam{i}"><div class="stage" style="transform: translate({-x0*SC:.0f}px,{-y0*SC:.0f}px) scale({SC})">{inner}</div></div></div>
          <svg class="edge" viewBox="0 0 1080 120" preserveAspectRatio="none"><polygon points="0,0 1080,0 1080,40 940,90 820,30 690,100 560,45 430,110 300,40 170,95 0,35" /></svg>
          <img class="txt" id="t{i}" src="img/t{i}.png" style="left:{tx:.0f}px;top:{ty:.0f}px;width:{w*s:.0f}px;height:{h*s:.0f}px" />
        </div>
        <div class="flash" id="fl{i}"></div>
      </div>'''

ring = lambda id, x, y, c='': f'<div class="ring {c}" id="{id}" style="left:{x}px;top:{y}px"></div>'
S = {}
S[1] = '<img class="bg" src="img/s1_bg.png" />' + ring('r1', 1470, 920) + '<img class="sp" id="jump1" src="img/sp_jumper.png" style="left:1172px;top:296px" />'
S[2] = '<img class="bg" src="img/s2_bg.png" />' + ring('r2a', 1040, 1000, 'teal') + ring('r2b', 1665, 990, 'red') + '<img class="sp" id="fox" src="img/sp_fox.png" style="left:1044px;top:232px" /><img class="sp" id="horse" src="img/sp_horse.png" style="left:1540px;top:384px" />'
S[3] = '<img class="bg" src="img/s3_bg.png" />' + ''.join(f'<img class="sp btn" src="img/btn{k}.png" style="left:1152px;top:{y}px" />' for k, y in enumerate([322, 437, 553, 668, 784, 898]))
S[4] = '<img class="bg" src="img/s4_bg.png" /><img class="sp" id="jump4" src="img/sp_jumper.png" style="left:1148px;top:300px" /><div id="hl" style="left:797px;top:1000px"></div>'
S[5] = '<img class="bg" src="img/s5_bg.png" />' + ''.join(f'<img class="sp hat" src="img/hat{r*3+c}.png" style="left:{x}px;top:{y}px" />' for r, y in enumerate([400, 535, 668, 800, 930]) for c, x in enumerate([1465, 1600, 1732]))
P = ["0px 0px, 1250px 0px, 1106px 1440px, 0px 1440px", "1250px 0px, 1630px 0px, 1457px 1440px, 1106px 1440px", "1630px 0px, 1920px 0px, 1920px 1440px, 1457px 1440px"]
S[6] = ''.join(f'<img class="bg stripe" id="st{k}" src="img/s6_bg.png" style="clip-path: polygon({p})" />' for k, p in enumerate(P))

def rays(id):
    tri = lambda a: f'0,0 {round(1400*math.cos(math.radians(a-3)))},{round(1400*math.sin(math.radians(a-3)))} {round(1400*math.cos(math.radians(a+3)))},{round(1400*math.sin(math.radians(a+3)))}'
    return f'<svg class="rays" id="{id}" viewBox="-1000 -1000 2000 2000">' + ''.join(f'<polygon points="{tri(a)}" />' for a in range(0, 360, 20)) + '</svg>'

L = [(0, 0), (110, 140), (30, 260), (140, 420), (60, 560), (170, 700), (40, 860), (130, 1080)]
R = [(2400 - a, b) for a, b in [(120, 1080), (30, 900), (150, 760), (50, 600), (160, 430), (40, 280), (130, 120), (20, 0)]]
pts = " ".join(f"{a},{b}" for a, b in L + R)

# Reuse the landscape timeline, adapting the wipe travel and logo drop distances
src = (HERE.parent / "compositions" / "index.html").read_text()
js = src.split("<script>\n", 1)[1].split("    </script>", 1)[0]
js = js.replace('{ x: 1920 }, { x: -240,', '{ x: 1080 }, { x: -260,').replace('{ x: -2500, duration: 0.4', '{ x: -1700, duration: 0.4')
js = js.replace('ft("#logo0", { y: -700', 'ft("#logo0", { y: -900').replace('ft("#logo7", { y: -800', 'ft("#logo7", { y: -1000')

html = f'''<!doctype html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=1080, height=1920" />
    <script src="gsap.min.js"></script>
    <style>
      * {{ margin: 0; padding: 0; box-sizing: border-box; }}
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b0c0c; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; background: #0b0c0c; }}
      .scene {{ position: absolute; inset: 0; overflow: hidden; background: #0b0c0c; }}
      .shake {{ position: absolute; inset: 0; }}
      .game {{ position: absolute; left: 0; top: 760px; width: 1080px; height: 1160px; overflow: hidden; }}
      .cam {{ position: absolute; inset: 0; }}
      .stage {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1440px; transform-origin: 0 0; }}
      .bg {{ position: absolute; left: 0; top: 0; width: 1920px; height: 1440px; }}
      .edge {{ position: absolute; left: 0; top: 740px; width: 1080px; height: 120px; fill: #0b0c0c; }}
      .sp, .txt {{ position: absolute; }}
      .flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; pointer-events: none; }}
      .ring {{ position: absolute; width: 300px; height: 300px; margin: -150px 0 0 -150px; border-radius: 50%; border: 16px solid #fff; opacity: 0; }}
      .ring.teal {{ border-color: #0bb3b6; }}
      .ring.red {{ border-color: #e0283a; }}
      #hl {{ position: absolute; width: 780px; height: 48px; border-radius: 12px; border: 6px solid #fff; box-shadow: 0 0 40px 10px rgba(255,214,0,.8); opacity: 0; }}
      #m0 {{ position: absolute; left: -585px; top: 700px; width: 2234px; -webkit-mask-image: linear-gradient(transparent 0, #000 220px); mask-image: linear-gradient(transparent 0, #000 220px); }}
      #m7 {{ position: absolute; inset: 0; width: 1080px; height: 1920px; object-fit: cover; }}
      .rays {{ position: absolute; left: -460px; top: -540px; width: 2000px; height: 2000px; fill: #fff; opacity: 0; }}
      #logo0 {{ position: absolute; left: 90px; top: 300px; width: 900px; }}
      #logo7 {{ position: absolute; left: 70px; top: 480px; width: 940px; }}
      #play {{ position: absolute; left: 340px; top: 1000px; width: 400px; filter: drop-shadow(0 12px 24px rgba(0,0,0,.45)); }}
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 60%, rgba(0,0,0,.4) 100%); z-index: 40; pointer-events: none; }}
      #wipe {{ position: absolute; left: 0; top: 0; width: 1600px; height: 1920px; z-index: 50; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="20" data-width="1080" data-height="1920">
      <div id="s0" class="clip scene" data-start="0" data-duration="2.5" data-track-index="1" style="background: linear-gradient(#5f7a63, #7c8c6c)">
        <div class="shake" id="sh0"><img id="m0" src="img/menu_nologo.png" />{rays("ray0")}<img id="logo0" src="img/logo.png" /></div>
        <div class="flash" id="fl0"></div>
      </div>{"".join(scene(i, S[i]) for i in range(1, 7))}
      <div id="s7" class="clip scene" data-start="17.5" data-duration="2.5" data-track-index="1" style="background: radial-gradient(circle at 50% 40%, #8a9a74, #4e6352 75%)">
        <div class="shake" id="sh7"><div id="m7"></div>{rays("ray7")}<img id="logo7" src="img/logo.png" /><img id="play" src="img/play.png" /></div>
        <div class="flash" id="fl7"></div>
      </div>
      <div id="vig" class="clip" data-start="0" data-duration="20" data-track-index="3"></div>
      <svg id="wipe" class="clip" data-start="0" data-duration="20" data-track-index="2" viewBox="0 0 2400 1080" preserveAspectRatio="none"><polygon points="{pts}" fill="#0b0c0c" /></svg>
    </div>
    <script>
{js}    </script>
  </body>
</html>
'''
(HERE / "index.html").write_text(html)
