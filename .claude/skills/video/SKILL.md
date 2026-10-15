---
name: video
description: Baut aus einem kurzen Briefing ein Animationsvideo mit Hyperframes (Pure-Animation-Workflow, ohne Rohvideo) — Storyboard auf Deutsch zur Freigabe, dann Compositions, Render und Self-Eval. Aufruf: /video <Briefing>, z.B. "/video 20s Promo für unser Tool, Shorts-Format, Brand default".
argument-hint: <Briefing: Thema, Länge, Format, optional Brand>
---

# /video — Animationsvideo aus einem Briefing

Briefing: $ARGUMENTS

## 0. Vorbereitung
- Lies den `hyperframes`-Skill (`.claude/skills/hyperframes/SKILL.md`) und folge seinem Ablauf für die Compositions.
- Lies `docs/motion-philosophy.md` und **alle** Files der Brand (`brand-guidelines/<name>/`, ohne Angabe `brand-guidelines/default/`).
- Fehlende Angaben sinnvoll annehmen statt nachzufragen. Defaults: 15 s, 1920×1080 @ 30 fps ("Short"/"Reel"/"hochkant" → 1080×1920), Brand `default`, Sprache Deutsch.
- Kein ElevenLabs nötig. Sprecherstimme nur, wenn ein Key in `.env` steht und der Nutzer sie will.

## 1. Storyboard → Freigabe (Pflicht)
Lege `projects/<slug>/` an (Ordnerstruktur wie `projects/example/`). Zeig dem Nutzer auf Deutsch, in Plain Language und kompakt:
- Format, Länge, Brand
- Szenen mit Zeitfenster, Inhalt, On-Screen-Text, Animation und Easing
- Musik/Sound: nur, wenn eine Datei vorliegt
**Dann stoppen und auf OK warten.** Bei Feedback das Storyboard anpassen und erneut vorlegen.

## 2. Bauen
- Projekt anlegen: `HYPERFRAMES_SKIP_SKILLS=1 npx hyperframes init projects/<slug>/compositions --example blank --non-interactive [--resolution portrait]`
- **GSAP lokal:** `cp node_modules/gsap/dist/gsap.min.js projects/<slug>/compositions/` und per `<script src="gsap.min.js">` laden, keine CDN-URLs (jsdelivr/unpkg sind gesperrt). Fonts und Bilder ebenfalls lokal ablegen, wo möglich.
- Unabhängige Szenen parallel per Sub-Agent bauen (eine Szene pro Agent), dann zusammenführen.
- Regeln: niemals `linear`, mindestens 3 Easings pro Szene, keine Banned Fonts, kurzer On-Screen-Text, das echte Ding statt eines Symbols zeigen.
- `npx hyperframes check` im Projektordner ausführen und alle Fehler beheben.

## 3. Render + Self-Eval
- `npx hyperframes render -o ../renders/final.mp4` (im Ordner `compositions/`)
- Self-Eval-Aufruf: `uv run --project ./video-use python ./video-use/helpers/timeline_view.py projects/<slug>/renders/final.mp4 -o projects/<slug>/previews/timeline.png`
- Alternativ Einzelframes per `ffmpeg -ss <t> -frames:v 1` nach `projects/<slug>/previews/`. Die Frames selbst ansehen und auf Lesbarkeit, Safe Areas, Überlappungen, leere Frames und Timing prüfen. Probleme beheben und neu rendern, bevor du dem Nutzer etwas zeigst.

## 4. Abgabe
Kurz auf Deutsch: Pfad `projects/<slug>/renders/final.mp4`, Länge und Format, 2–3 Sätze zum Ergebnis. Dann nach Feedback fragen.
