# Motion-Philosophie

**Modern, hochwertig, clean, dynamisch.** Jede Bewegung hat einen Grund: Sie lenkt den Blick, erklärt etwas oder setzt einen Akzent. Deko-Bewegung fliegt raus.

## Easings
- Reveals / Auftritte: `power3.out`
- Abgänge: `power2.in` / `power3.in`
- Loops, Schweben, Atmen: `sine.inOut`
- Akzente, Pops: `back.out(1.6)` / `expo.out`
- **Niemals `linear`** — außer für mechanische Dinge, die wirklich linear laufen (Progressbar-Füllung, Ticker).
- **Mindestens 3 verschiedene Easings pro Szene.**

## Timing
- **Anchor-Word-Sync:** Die Animation landet **mit** dem Wort, ±100 ms. Basis sind die Wort-Zeitstempel aus `transcripts/master.json`.
- Reveals 0.4–0.8 s, Mikro-Akzente 0.15–0.3 s, Szenenwechsel ≤ 0.5 s.
- Stagger für Listen: 60–120 ms pro Element.
- Ruhe ist ein Werkzeug: nach einem großen Reveal 0.5–1 s halten.

## Komposition
- Eine Hauptaussage pro Bild. Kurzer Text (Dateiname, Regel, Statusmeldung), keine Absätze.
- Das echte Ding statt eines Symbols zeigen: Datei = Blatt mit lesbarem Inhalt, Programm = nachgebaute Oberfläche.
- Safe Areas: 1080p 96 px Rand · Shorts 1080×1920: oben 220 px, unten 380 px frei für Plattform-UI.

## Banned Fonts
Inter, Roboto, Open Sans, Lato, Poppins, Outfit, Sora, Fraunces, Playfair Display, Cormorant Garamond, Syne, Cinzel, Nunito, Source Sans, PT Sans, Arimo.

## Audio
- Stimme vorne (~ -14 LUFS), Musik leise darunter (-36 bis -38 LUFS), konstanter Pegel.
- Sounds nur wo auf dem Bild etwas passiert — dezent, nicht verspielt.
