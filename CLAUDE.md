# CLAUDE.md — Arbeitsregeln für das KI Video Editing Studio

Dieses Repo ist ein Video-Studio: **Video-Use** (Schnitt, Transkription via ElevenLabs Scribe, Untertitel) + **Hyperframes** (HTML/GSAP-Motion-Graphics, Render via FFmpeg). Vollständige Regeln und Pipelines: `SETUP.md`. Ablauf: `docs/video-editing-workflow.md`. Stil: `docs/motion-philosophy.md`.

## Setup / Session-Start
- `scripts/setup.sh` ist idempotent und läuft per SessionStart-Hook (`.claude/settings.json`): `npm install`, `video-use` klonen + `uv sync`, Skill-Symlinks in `.claude/skills/`, Headless-Chrome, `.env`-Sync.
- Skills: `hyperframes`, `hyperframes-cli`, `media-use` (aus `node_modules/hyperframes/dist/skills/`), `video-use` (aus `./video-use`). Ab Hyperframes 0.8 ist GSAP Teil des `hyperframes`-Skills — es gibt keinen separaten `gsap`-Skill mehr.
- Nie `npx skills add …` o.ä. verwenden — nur die mitgelieferten Skills aus dem npm-Paket.

## Arbeitsregeln
- **Video-Use first** für Schnitt/Transkription, danach **Hyperframes** für Motion Graphics.
- **Plan-Bestätigung auf Deutsch** (Plain Language) vor jedem Cut und vor jeder Composition. Erst nach OK ausführen.
- Outputs landen unter `projects/<name>/` (Renders in `projects/<name>/renders/`) — niemals im Repo-Root, in `raw/` oder in `video-use/`.
- Video-Use-Helpers immer mit `--edit-dir projects/<name>` aufrufen (sonst schreiben sie nach `<video_parent>/edit/`).
- `.env` nie committen, Keys nie im Chat ausgeben.
- **`.env`-Sync:** Wenn `./.env` und `./video-use/.env` divergieren → syncen; Projekt-Root ist die Wahrheit (`scripts/setup.sh` erledigt das).
- Bei Multi-Scene-Compositions: parallele Sub-Agents (eine Szene pro Agent), wenn die Szenen unabhängig sind.
- Nach jedem Render **Self-Eval** per `timeline_view`-Pattern (`video-use/helpers/timeline_view.py`), bevor eine Preview gezeigt wird.
- Cut-Standards aus `SETUP.md` (Versprecher-Detection, Padding-Tabelle, Re-Scribe des letzten Wortes, `_padding_params` in jeder `edl.json`) sind nicht verhandelbar.
- Nach dem Cut **immer** fragen: Claude Design (claude.ai) oder Direkt Hyperframes? Brand-Frage nur bei Direkt Hyperframes.
- Claude-Design-Bundles **nie** mit `npx hyperframes preview/render` — eigene Puppeteer+FFmpeg-Pipeline, Speaker-Video vorher All-Intra (`-g 1`) nach `assets/speaker.mp4`.

## Brand-Guidelines
- Nennt der Nutzer `brand-guidelines/<name>/`, lies **alle** Files darin (Farben, Fonts, Logos, Tone, ggf. Motion-Overrides) und richte Schnitt, Farben, Typografie, Overlays, Untertitel und Layouts danach aus.
- Ohne Angabe: `brand-guidelines/default/` (aktuell Platzhalter — beim ersten Direkt-Hyperframes-Cut fragen, ob eine echte Brand nachgereicht werden soll).
- Claude-Design-ZIP im Projekt-Root → nach `brand-guidelines/default/` entpacken (Top-Level-Ordner eine Ebene hochziehen, `SKILL.md` muss direkt drin liegen, vorher Backup falls nicht mehr Platzhalter).

## Environment-Hinweise
- **CDN-Blockade (Cloud-Sessions):** `cdn.jsdelivr.net`/`unpkg.com` können per Netzwerk-Policy gesperrt sein → Render schlägt fehl mit `sub_timeline_script_failure`. Lösung: GSAP lokal nutzen — `node_modules/gsap/dist/gsap.min.js` in den Composition-Ordner kopieren und `<script src="gsap.min.js">` referenzieren (gsap ist Dependency in `package.json`). Lokale Assets sind ohnehin deterministischer.
- `hyperframes init` immer mit `HYPERFRAMES_SKIP_SKILLS=1 … --non-interactive` aufrufen (sonst lädt es Skills von GitHub).
- ElevenLabs braucht Zugriff auf `api.elevenlabs.io` — in Cloud-Umgebungen ggf. in den Allowed Domains freigeben.
- Windows: `PYTHONUTF8=1` vor `uv run … video-use/helpers/…`; `grade: null` statt `"auto"`; Junctions statt Symlinks.
- `npx hyperframes doctor`: Docker, whisper-cpp, Kokoro, MusicGen sind optional — kein Fehler.
