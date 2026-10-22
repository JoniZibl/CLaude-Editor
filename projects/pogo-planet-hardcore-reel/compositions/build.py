# Generates index.html for the "Ultra Hardcore" reel (1080x1920, 12.5 s).
import pathlib
HERE = pathlib.Path(__file__).parent
HAT = (165.2, -12.2, 108.7, 110.7)      # crab hat seat on body.png
FEET = (95, 300)

# level: (key, label, quip, color, start, darkness 0..1, shake px, meter %)
LV = [("easy", "EASY", "chill.", "#3f8f5a", 1.1, 0.0, 0, 25),
      ("normal", "NORMAL", "okay.", "#1f9a92", 2.9, 0.25, 5, 50),
      ("hard", "HARD", "hm.", "#8a3f8f", 4.7, 0.55, 11, 75)]
BLACK, ULTRA, END = 6.6, 7.2, 11.5

def char(id, x, y, s):
    return (f'<div class="char" id="{id}" style="left:{x}px;top:{y}px"><div class="bob" id="{id}b"><div style="position:absolute;transform:scale({s});transform-origin:0 0">'
            f'<div style="position:absolute;left:{-FEET[0]}px;top:{-FEET[1]}px;width:330px;height:380px">'
            f'<img src="img/stick.png" style="position:absolute;left:10px;top:49px" /><img src="img/body.png" style="position:absolute;left:0;top:0" />'
            f'<img src="img/h29.png" style="position:absolute;left:{HAT[0]}px;top:{HAT[1]}px;width:{HAT[2]}px;height:{HAT[3]}px" />'
            f'<div class="sweat" id="{id}sw" style="left:150px;top:30px"></div><div class="sweat" id="{id}sw2" style="left:255px;top:40px"></div>'
            f'</div></div></div></div>')

levels = "".join(f'''
        <div class="lv" id="lv{i}">
          <img class="ped" id="ped{i}" src="img/ped_{k}.png" />
          <div class="wnum" id="wn{i}">WORLD {i + 1}</div>
          <div class="lvname" id="nm{i}" style="color:{c}">{n}</div>
          <div class="quip" id="qp{i}">{q}</div>
        </div>''' for i, (k, n, q, c, *_r) in enumerate(LV))

hearts = "".join(f'<svg class="heart" id="ht{i}" viewBox="0 0 32 29" style="left:{470 + i * 110}px"><path d="M16 29 2.6 15.6A8 8 0 0 1 16 4.3 8 8 0 0 1 29.4 15.6Z" fill="#e0283a" stroke="#fff" stroke-width="2"/></svg>' for i in range(3))

js_levels = "\n".join(f'''
      // level {i}: {n}
      ft("#lv{i}", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.05, ease: "power1.out" }}, {t});
      ft("#ped{i}", {{ y: 700 }}, {{ y: 0, duration: 0.45, ease: "power3.out" }}, {t});
      ft("#wn{i}", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {t + 0.05});
      ft("#nm{i}", {{ scale: 2.6, opacity: 0, rotation: -8 }}, {{ scale: 1, opacity: 1, rotation: -4, duration: 0.3, ease: "power4.in" }}, {t + 0.15});
      ft("#qp{i}", {{ opacity: 0, y: 30 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, {t + 0.7});
      tl.to("#dark", {{ opacity: {d}, duration: 0.4, ease: "power2.out" }}, {t + 0.45});
      tl.to("#meterfill", {{ width: "{m}%", backgroundColor: "{c}", duration: 0.45, ease: "power3.out" }}, {t + 0.45});
      flash({t + 0.45}, {0.25 + 0.1 * i}); {f'shake({t + 0.45}, {s});' if s else ''}
      tl.to("#lv{i}", {{ opacity: 0, duration: 0.12, ease: "power2.in" }}, {(LV[i + 1][4] if i < 2 else BLACK) - 0.12});'''
    for i, (k, n, q, c, t, d, s, m) in enumerate(LV))

js = f"""
      window.__timelines = window.__timelines || {{}};
      const tl = gsap.timeline({{ paused: true }});
      const seen = {{}};
      const ft = (sel, from, to, t) => {{ to.immediateRender = !seen[sel]; seen[sel] = true; tl.fromTo(sel, from, to, t); }};
      const shake = (t, a, n) => tl.to("#shk", {{ x: a, y: -a * 0.6, duration: 0.035, ease: "sine.inOut", yoyo: true, repeat: n || 5 }}, t);
      const flash = (t, p) => tl.fromTo("#flash", {{ opacity: p }}, {{ opacity: 0, duration: 0.3, ease: "expo.out", immediateRender: false }}, t);
      // hook: headline + meter on frame 1
      ft("#h1", {{ scale: 1.8, opacity: 0 }}, {{ scale: 1, opacity: 1, duration: 0.25, ease: "power4.out" }}, 0.02);
      tl.to("#h1", {{ y: -30, opacity: 0, duration: 0.2, ease: "power2.in" }}, 0.95);
      ft("#meter", {{ opacity: 0, y: -40 }}, {{ opacity: 1, y: 0, duration: 0.3, ease: "power3.out" }}, 0.9);
      ft("#c1", {{ y: 600 }}, {{ y: 0, duration: 0.45, ease: "back.out(1.6)" }}, 0.1);
      // the rider bobs faster with every level
      tl.to("#c1b", {{ y: -45, duration: 0.3, ease: "sine.inOut", yoyo: true, repeat: 9 }}, 0.55);
      tl.to("#c1b", {{ y: -55, duration: 0.2, ease: "sine.inOut", yoyo: true, repeat: 9 }}, 3.55);
      tl.to("#c1b", {{ y: -60, duration: 0.12, ease: "sine.inOut", yoyo: true, repeat: 11 }}, 5.55);
      
      ft("#c1sw", {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: 60, duration: 0.7, ease: "power2.in", repeat: 1 }}, 5.0);
      ft("#c1sw2", {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: 60, duration: 0.6, ease: "power2.in", repeat: 1 }}, 5.4);
      {js_levels}
      tl.to("#shk", {{ rotation: 0.8, duration: 0.05, ease: "sine.inOut", yoyo: true, repeat: 15 }}, 5.6);
      // hard cut to black + silence
      ft("#black", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.02, ease: "power1.in" }}, {BLACK});
      tl.set("#meter, #c1", {{ opacity: 0 }}, {BLACK});
      // WORLD 4 · INSANE finale
      ft("#ultra", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.02, ease: "power1.out" }}, {ULTRA});
      ft("#fped", {{ y: 800 }}, {{ y: 0, duration: 0.4, ease: "power4.out" }}, {ULTRA});
      ft("#c2", {{ y: 800 }}, {{ y: 0, duration: 0.4, ease: "power4.out" }}, {ULTRA});
      ft("#fwn", {{ opacity: 0, y: -30 }}, {{ opacity: 1, y: 0, duration: 0.25, ease: "power3.out" }}, {ULTRA + 0.1});
      ft("#u1", {{ scale: 3, opacity: 0, rotation: -10 }}, {{ scale: 1, opacity: 1, rotation: -4, duration: 0.32, ease: "power4.in" }}, {ULTRA + 0.1});
      flash({ULTRA + 0.42}, 0.8); shake({ULTRA + 0.42}, 26, 7);
      ft("#umeter", {{ width: "75%" }}, {{ width: "100%", duration: 0.5, ease: "expo.out" }}, {ULTRA + 0.42});
      ft("#glow", {{ scale: 0.6, opacity: 0.35 }}, {{ scale: 1.15, opacity: 0.95, duration: 0.42, ease: "sine.inOut", yoyo: true, repeat: 5 }}, {ULTRA + 0.42});
      [0.9, 1.75, 2.6].forEach(d => tl.fromTo("#pulse2", {{ opacity: 0.7 }}, {{ opacity: 0, duration: 0.4, ease: "expo.out", immediateRender: false }}, {ULTRA} + d));
      tl.to("#c2b", {{ x: 6, duration: 0.035, ease: "sine.inOut", yoyo: true, repeat: 59 }}, {ULTRA + 0.5});
      ft("#c2sw", {{ opacity: 0, y: 0 }}, {{ opacity: 1, y: 60, duration: 0.5, ease: "power2.in", repeat: 4 }}, {ULTRA + 0.6});
      ft("#u2", {{ opacity: 0, y: 40 }}, {{ opacity: 1, y: 0, duration: 0.35, ease: "power3.out" }}, {ULTRA + 1.6});
      ft("#ulogo", {{ opacity: 0, scale: 0.7 }}, {{ opacity: 1, scale: 1, duration: 0.35, ease: "back.out(2)" }}, {ULTRA + 2.2});
      // loop seam: fade to the bright opening frame
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
      html, body {{ width: 1080px; height: 1920px; overflow: hidden; background: #0b0c0c; }}
      #root {{ position: relative; width: 1080px; height: 1920px; overflow: hidden; font-family: "Exo2", sans-serif; font-weight: 900; font-style: italic; text-transform: uppercase; }}
      #shk {{ position: absolute; inset: -40px; }}
      .sky {{ position: absolute; inset: 0; background: linear-gradient(180deg, #66806a 0%, #9aa766 55%, #c9b84a 100%); }}
      .sun {{ position: absolute; left: 140px; top: 760px; width: 220px; height: 220px; border-radius: 50%; background: #f4c63d; box-shadow: 0 0 120px 40px rgba(244,198,61,.35); }}
      .hills {{ position: absolute; left: 40px; bottom: 40px; width: 1080px; height: 900px; }}
      .ground {{ position: absolute; left: 0; top: 1540px; width: 1160px; height: 500px; background: #17191a; }}
      .ground::before {{ content: ""; position: absolute; left: 0; top: -16px; width: 100%; height: 26px; background: #2f8a55; border-radius: 0 0 8px 8px; }}
      #dark {{ position: absolute; inset: 0; background: radial-gradient(ellipse at 50% 55%, rgba(20,6,10,.55), rgba(5,2,4,.97) 75%); opacity: 0; }}
      #pulse {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(224,40,58,.0) 30%, rgba(224,40,58,.75) 100%); opacity: 0; }}
      .lv {{ position: absolute; inset: 0; opacity: 0; }}
      .ped {{ position: absolute; left: 390px; top: 1300px; width: 380px; height: 534px; }}
      .lvname {{ position: absolute; left: 0; width: 1160px; top: 520px; text-align: center; font-size: 210px; line-height: 1; text-shadow: 0 10px 0 rgba(0,0,0,.55), 0 0 40px rgba(0,0,0,.35); }}
      .wnum {{ position: absolute; left: 0; width: 1160px; top: 450px; text-align: center; font-size: 56px; color: #fbfbf7; letter-spacing: 6px; }}
      #pulse2 {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(224,40,58,0) 30%, rgba(224,40,58,.8) 100%); opacity: 0; }}
      .quip {{ position: absolute; left: 0; width: 1160px; top: 745px; text-align: center; font-size: 64px; color: #fbfbf7; text-transform: lowercase; }}
      .char {{ position: absolute; }}
      .bob {{ position: absolute; left: 0; top: 0; }}
      .sweat {{ position: absolute; width: 22px; height: 30px; background: #9fd8ff; border-radius: 50% 50% 50% 50% / 60% 60% 40% 40%; opacity: 0; }}
      #h1 {{ position: absolute; left: 0; width: 1160px; top: 420px; text-align: center; font-size: 150px; line-height: .92; }}
      .w {{ color: #fbfbf7; }}
      .y {{ background: linear-gradient(180deg, #ffd400, #ff9a00); -webkit-background-clip: text; background-clip: text; color: transparent; }}
      #meter {{ position: absolute; left: 150px; top: 270px; width: 860px; opacity: 0; }}
      #meter .lbl {{ font-size: 40px; color: #fbfbf7; letter-spacing: 3px; margin-bottom: 14px; }}
      .track {{ height: 40px; border-radius: 20px; background: rgba(0,0,0,.45); border: 5px solid #fbfbf7; overflow: hidden; }}
      #meterfill {{ height: 100%; width: 0%; background: #3f8f5a; }}
      #card {{ position: absolute; left: 350px; top: 780px; width: 460px; }}
      #hearts {{ position: absolute; left: 0; top: 0; opacity: 0; }}
      .heart {{ position: absolute; top: 980px; width: 80px; height: 73px; }}
      #black {{ position: absolute; inset: 0; background: #000; opacity: 0; z-index: 30; }}
      #ultra {{ position: absolute; inset: 0; background: #050203; opacity: 0; z-index: 31; }}
      #glow {{ position: absolute; left: 40px; top: 860px; width: 1080px; height: 1080px; border-radius: 50%; background: radial-gradient(circle, rgba(224,40,58,.85), rgba(224,40,58,0) 65%); }}
      #skbox {{ position: absolute; left: 380px; top: 600px; width: 440px; height: 440px; }}
      #sk {{ position: absolute; inset: 0; border-radius: 70px; background: #a3212b; border: 18px solid #6e141c; box-shadow: 0 0 80px rgba(224,40,58,.9); }}
      #sk img {{ position: absolute; left: 95px; top: 75px; width: 214px; height: 259px; }}
      #u1 {{ position: absolute; left: 0; width: 1160px; top: 470px; text-align: center; font-size: 230px; line-height: .92; color: #fbfbf7; text-shadow: 0 0 40px rgba(224,40,58,.9); }}
      #u1 span {{ color: #ff2b3c; }}
      .umeter {{ position: absolute; left: 150px; top: 270px; width: 860px; }}
      .umeter .lbl {{ font-size: 40px; color: #ff2b3c; letter-spacing: 3px; margin-bottom: 14px; }}
      .umeter .track {{ border-color: #ff2b3c; }}
      #umeter {{ height: 100%; background: #ff2b3c; box-shadow: 0 0 30px #ff2b3c; }}
      #u2 {{ position: absolute; left: 0; width: 1160px; top: 740px; text-align: center; }}
      .bar {{ display: inline-block; padding: 12px 40px 8px; font-size: 70px; transform: rotate(-4deg) skewX(-6deg); background: #fbfbf7; color: #0b0c0c; }}
      #ulogo {{ position: absolute; left: 420px; top: 880px; width: 320px; filter: brightness(1.9) saturate(.2); }}
      #loopfade {{ position: absolute; inset: 0; z-index: 70; background: linear-gradient(180deg, #66806a 0%, #9aa766 55%, #c9b84a 100%); opacity: 0; }}
      #flash {{ position: absolute; inset: 0; background: #fff; opacity: 0; z-index: 60; }}
      #vig {{ position: absolute; inset: 0; background: radial-gradient(ellipse at center, rgba(0,0,0,0) 55%, rgba(0,0,0,.45) 100%); z-index: 40; }}
    </style>
  </head>
  <body>
    <div id="root" data-composition-id="main" data-start="0" data-duration="{END}" data-width="1080" data-height="1920">
      <div id="shk" class="clip" data-start="0" data-duration="{END}" data-track-index="0">
        <div class="sky"></div><div class="sun"></div>
        <svg class="hills" viewBox="0 0 1080 900" preserveAspectRatio="none"><polygon fill="#58735e" points="0,900 0,560 140,380 260,560 400,300 560,560 700,420 860,560 980,340 1080,480 1080,900" /><polygon fill="#2f6b4a" points="0,900 0,700 90,560 180,700 330,520 470,720 640,600 780,720 900,560 1080,740 1080,900" /></svg>
        <div class="ground"></div>
        <div id="dark"></div>
        {levels}
        {char("c1", 560, 1315, 0.95)}
        <div id="pulse"></div>
        <div id="meter"><div class="lbl">WORLD</div><div class="track"><div id="meterfill"></div></div></div>
        <div id="h1"><span class="w">HOW FAR</span><br><span class="y">CAN YOU GO?</span></div>
        <div id="black"></div>
        <div id="ultra">
          <div id="glow"></div>
          <div class="umeter"><div class="lbl">WORLD</div><div class="track"><div id="umeter"></div></div></div>
          <img class="ped" id="fped" src="img/ped_insane.png" style="top:1390px; filter: drop-shadow(0 0 40px rgba(224,40,58,.8))" />
          {char("c2", 560, 1405, 0.95)}
          <div id="pulse2"></div>
          <div class="wnum" id="fwn" style="top:400px; color:#ff8a94">WORLD 4</div>
          <div id="u1"><span>INSANE.</span></div>
          <div id="u2"><span class="bar">WHERE WOULD YOU QUIT?</span></div>
          <img id="ulogo" src="img/logo.png" />
        </div>
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
