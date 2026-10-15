# Video-Editing-Workflow (Referenz für Claude)

Die vollständigen Regeln (Cut-Standards, Padding, Bundle-Pipeline) stehen in `SETUP.md`. Hier der Ablauf in Kurzform.

## A. Edit-Workflow (mit Rohvideo)

1. **Input:** `raw/<projekt>/<datei>.mp4`. Projektordner `projects/<projekt>/` aus `projects/example/` anlegen.
2. **Transkription** (ElevenLabs Scribe, wortgenau, gecacht):
   ```bash
   uv run --project ./video-use python ./video-use/helpers/transcribe.py raw/<projekt>/<datei>.mp4 --edit-dir projects/<projekt>
   uv run --project ./video-use python ./video-use/helpers/pack_transcripts.py --edit-dir projects/<projekt> --silence-threshold 0.4
   ```
3. **Versprecher-Detection:** Silence-Map (`silencedetect=noise=-30dB:duration=0.25`) gegen Wort-Marker abgleichen, verdächtige Slices isoliert re-scriben.
4. **Cut-Plan auf Deutsch** (Plain Language): welche Takes bleiben, welche fliegen, Padding pro Range → **auf OK warten**.
5. **EDL** `projects/<projekt>/edl.json` mit `_padding_params`, dann rendern:
   ```bash
   uv run --project ./video-use python ./video-use/helpers/render.py projects/<projekt>/edl.json -o projects/<projekt>/clips/edited.mp4
   ```
   Letztes Wort per Sub-Slice re-scriben, Range-End = echter Word-End + 600–700 ms.
6. **Checkpoint — HTML-Quelle fragen:** Claude Design (claude.ai) oder Direkt Hyperframes. Nur bei Hyperframes nach der Brand fragen.
7. **Storyboard** (Beats, Anchor-Wörter, Animation-Typen) → **auf OK warten**.
8. **Compositions** in `projects/<projekt>/compositions/` bauen — eine pro Szene, unabhängige Szenen parallel per Sub-Agent.
9. **Preview:** `npx hyperframes preview` (Studio auf `localhost:3002`).
10. **Final-Render:** `projects/<projekt>/renders/final.mp4` (1920×1080/30 fps, Shorts 1080×1920).
11. **Self-Eval:** `video-use/helpers/timeline_view.py` auf den Render, Frames prüfen, erst dann zeigen.

## B. Pure-Animation-Workflow (ohne Rohvideo)

Ab Schritt 7: Briefing → Storyboard → OK → Compositions → Preview → Render → Self-Eval.
Voiceover über ElevenLabs TTS (Key aus `.env`), Musik/Sounds gemischt nach den Pegeln in `docs/motion-philosophy.md`.

## C. Claude-Design-Bundle

Nur Transkript exportieren (`output_transcript.md` + `.json`), aktiv auf das Bundle warten, dann eigene Puppeteer+FFmpeg-Pipeline — **nicht** `hyperframes preview/render`. Details: `SETUP.md`, Abschnitt "Claude-Design HTML auf Cut-Video legen + rendern".

## Beispiel-Prompts
Siehe `docs/prompt-examples.md` (Showreel, Short aus Rohaufnahme, Werbespot, Erklärvideo).
