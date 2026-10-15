# Pogo Planet — Promo (Storyboard v1, wartet auf Freigabe)

Quelle: Figma `mNola2cIYKyzEYoXFbZ694`, Seite „PogoPlanet“ (node 1:4).
Referenzen: `assets/ref/` (6 Feature-Grafiken, Hauptmenü, One-Tap-Grafik).

- **Format:** 1920×1080, 30 fps
- **Länge:** 20 s (statt 15 s Default, damit alle 6 Features je ~2,5 s bekommen)
- **Look:** der Pogo-Planet-Stil aus Figma (schwarze, gezackte Fläche, fette kursive Headline in Weiß und Gelb-Orange, rote und türkise Schrägbalken, Szenen in Olivgrün und Sonnengelb). `brand-guidelines/default` ist nur ein Platzhalter und passt nicht zum Spiel.
- **Text:** Englisch, wie in den Store-Grafiken
- **Musik/Sound:** keine (es liegt keine Datei vor)
- **Szenenwechsel:** Die schwarze, gezackte Fläche wischt jedes Mal von links ins Bild (≤ 0,5 s, `expo.out` / `power3.in`).

| # | Zeit | Szene | On-Screen-Text | Animation (Easing) |
|---|------|-------|----------------|--------------------|
| 1 | 0–2,5 s | Hauptmenü-Welt | POGO PLANET | Sonne steigt auf (`sine.inOut`), Logo stempelt ein (`back.out(1.6)`), 5 Strichmännchen hüpfen gestaffelt rein (`power3.out`, 80 ms Stagger) |
| 2 | 2,5–5 s | Gameplay | ONE TAP. CRAZY JUMPS. / EASY TO PLAY. HARD TO MASTER. | Finger tippt, Ring pulsiert (`expo.out`), Figur springt im Bogen (`power3.out` hoch, `power2.in` runter), Balken gleiten rein (`power3.out`) |
| 3 | 5–7,5 s | Multiplayer | PLAY WITH FRIENDS. / ONLINE OR LOCAL. | Zwei Finger tippen abwechselnd, Fuchs und Pferd springen versetzt (`power3.out`/`power2.in`), Ringe poppen (`back.out`) |
| 4 | 7,5–10 s | Map Editor | CREATE YOUR OWN MAPS. / BUILD & TEST. | Editor-Oberfläche fährt rein (`power3.out`), Blöcke ploppen ins Raster (`back.out(1.6)`, 80 ms Stagger), Laterne glimmt (`sine.inOut`) |
| 5 | 10–12,5 s | Leaderboard | CLIMB THE SCOREBOARD / BEAT PLAYERS WORLDWIDE. | Ranking-Tafel fällt rein (`power3.out`), Zeile „Jonny“ klettert von Platz 17 auf 14 (`power3.inOut`), Highlight blitzt (`expo.out`) |
| 6 | 12,5–15 s | Cosmetics | COLLECT 240+ COSMETICS. | Hut-Raster staggert rein (`back.out`, 60 ms), Zähler 0 → 240+ (`power2.out`), Hüte wechseln auf dem Kopf der Figur (`expo.out`) |
| 7 | 15–17,5 s | Bosse | FIGHT EPIC BOSSES. / THE ULTIMATE CHALLENGE. | Drei Bosse krachen nacheinander rein (`power4.in` + `back.out`), Kamera-Shake (`sine.inOut`), Farbstreifen dahinter wischen (`power3.out`) |
| 8 | 17,5–20 s | Outro | POGO PLANET / PLAY NOW. | Logo groß (`back.out(1.6)`), Figur hüpft in der Schleife (`sine.inOut`), „PLAY NOW.“-Balken gleitet rein (`power3.out`), 1 s Ruhe am Ende |

## Umsetzung
- Die Szenen werden mit HTML/GSAP nachgebaut, nicht als Standbilder gezeigt. Figuren, Bosse, Hüte und Plattformen kommen als einzelne Grafiken aus Figma.
- Zum Herunterladen ist `www.figma.com` gesperrt. Die Grafiken kann ich trotzdem über den Figma-Zugang als PNG holen (das hat schon funktioniert).
