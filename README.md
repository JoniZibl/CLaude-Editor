# KI Video Editing Studio

Rohvideo rein, fertiges Video raus, oder reine Animationsvideos ganz ohne Rohmaterial. Gesteuert per Chat mit Claude Code.

- **[Video-Use](https://github.com/browser-use/video-use):** Transkription (ElevenLabs Scribe), Schnitt, Untertitel, Self-Eval
- **[Hyperframes](https://hyperframes.heygen.com/quickstart):** HTML/GSAP-Motion-Graphics, Render via FFmpeg

## Quickstart

1. **Setup:** In Claude Code *"Setup das Projekt"* sagen, oder selbst `./scripts/setup.sh` ausführen. In Cloud-Sessions läuft das automatisch per SessionStart-Hook.
   Voraussetzungen: Node ≥ 22, Python ≥ 3.11, uv, FFmpeg, Git.
2. **ElevenLabs-Key** in `./.env` eintragen (`ELEVENLABS_API_KEY=…`, Key unter https://elevenlabs.io/app/settings/api-keys). Claude synct ihn nach `./video-use/.env`.
3. **Erstes Video:** Roh-MP4 nach `raw/test/take_001.mp4` legen und sagen:
   > *Edit @raw/test/take_001.mp4 in eine Folge mit Brand default.*

## Struktur

```
raw/                     Rohvideos (gitignored)
projects/<name>/         assets/ clips/ transcripts/ compositions/ previews/ renders/
brand-guidelines/        default/ (Platzhalter) + eigene Sub-Brands
docs/                    motion-philosophy.md, video-editing-workflow.md, prompt-examples.md
video-use/               beim Setup geklont (gitignored)
.claude/skills/          Symlinks: hyperframes, hyperframes-cli, media-use, video-use
scripts/setup.sh         idempotentes Setup
```

## Beispielprompts

- `/video <Briefing>`: Animationsvideo aus einem Briefing, z.B. `/video 20s Promo für unser Tool, hochkant`
- *Edit @raw/<projekt>/<datei>.mp4 in eine Folge.*
- *Mach daraus einen YouTube-Short (1080×1920) mit Split-Layouts und Untertiteln.*
- *Mach ein 30-Sekunden-Promo-Video für unser Produkt mit Brand `brand-guidelines/<name>/`.*
- *Nutze für dieses Projekt die Brand Guidelines aus `brand-guidelines/<deine-brand>/`.*
- Ausführliche Prompts: [`docs/prompt-examples.md`](docs/prompt-examples.md)

## Brand einrichten

Claude-Design-ZIP (claude.ai) in den Projekt-Root legen und Claude Bescheid sagen. Claude entpackt sie nach `brand-guidelines/default/`. Weitere Brands kommen als eigene Ordner in `brand-guidelines/<name>/`.

## Troubleshooting

| Problem | Lösung |
|---|---|
| `ffmpeg: command not found` | FFmpeg installieren und in den PATH aufnehmen (Windows: `winget install Gyan.FFmpeg`, Terminal neu starten). |
| ElevenLabs 401 / Quota erreicht | Key in `.env` prüfen; Free-Tier-Limit erreicht → Plan upgraden oder `OPENAI_API_KEY` als Whisper-Fallback setzen. |
| Studio-Port 3002 belegt | Anderen Prozess beenden oder `npx hyperframes preview --port 3005`. |
| `Chrome Headless Shell is required` | `npx hyperframes browser ensure` |
| `[StaticGuard] Invalid HyperFrame contract` | Claude-Design-Bundle → eigene Bundle-Pipeline nutzen (siehe `SETUP.md`), nicht `hyperframes render`. |
| Speaker-Video "hängt" im Render | Vor dem Render All-Intra konvertieren (`-g 1`), siehe `SETUP.md`. |
| Windows `UnicodeEncodeError` | `$env:PYTHONUTF8 = "1"` setzen. |
