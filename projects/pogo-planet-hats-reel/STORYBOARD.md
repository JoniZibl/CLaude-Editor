# Pogo Planet — Reel „Hats“ (Storyboard v1, wartet auf Freigabe)

Feature: **Cosmetics / Hüte** – in Figma liegen 190 einzelne Hut-Grafiken (`PogoHut…`).

- Format: 1080×1920, 60 fps, 15 s · Safe Areas: oben 220 px, unten 380 px frei
- Look: wie Reel 1 (Schwarz, gezackte Kanten, gelb-orange Headline, rot/türkise Balken)
- Musik: „mal_schauen.mp3“, Hut-Wechsel auf dem Beat · SFX: Pop pro Hut, Whoosh, Aufprall

| # | Zeit | Inhalt | Text | Animation |
|---|------|--------|------|-----------|
| 1 | 0–2 s | Hook: Figur ohne Hut, Fragezeichen über dem Kopf | WHICH HAT ARE YOU? | Text knallt rein (power4), Figur wippt (sine.inOut) |
| 2 | 2–8 s | Hut-Roulette: Hut auf dem Kopf wechselt im Takt, erst langsam, dann immer schneller (~25 Hüte) | Zähler unten: 1 → 190 | Jeder Hut ploppt auf (back.out), Kamera zoomt langsam rein (power2.out) |
| 3 | 8–11 s | Hut-Wand: 40+ Hüte füllen in Wellen den Bildschirm | 240+ COSMETICS. | Stagger-Pop (back.out, 30 ms), Headline-Slam mit Shake + Blitz |
| 4 | 11–13,5 s | 3 Lieblings-Looks nebeneinander (z. B. Wikinger, Kürbis, Ritter) | FIND YOUR STYLE. | Figuren springen nacheinander rein (power3.out), Balken gleiten rein |
| 5 | 13,5–15 s | Logo + Play-Button | PLAY NOW. | Logo-Drop mit Strahlen, Button pulsiert (sine.inOut) |
