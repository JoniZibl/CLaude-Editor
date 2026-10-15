#!/usr/bin/env bash
# Idempotentes Setup: Dependencies, video-use, Skill-Links, Headless-Chrome, .env-Sync.
# Sicher mehrfach ausführbar — überspringt, was schon da ist.
set -euo pipefail
cd "$(dirname "$0")/.."

[ -d node_modules/hyperframes ] || npm install --no-audit --no-fund

if [ ! -d video-use/.git ]; then
  git clone --depth 1 https://github.com/browser-use/video-use ./video-use
fi
[ -d video-use/.venv ] || (cd video-use && uv sync)

mkdir -p .claude/skills
for p in node_modules/hyperframes/dist/skills/*/; do
  ln -sfn "$(pwd)/$p" ".claude/skills/$(basename "$p")"
done
ln -sfn "$(pwd)/video-use" .claude/skills/video-use

npx --no-install hyperframes browser ensure >/dev/null 2>&1 || echo "Hinweis: 'npx hyperframes browser ensure' fehlgeschlagen" >&2

# .env anlegen bzw. Projekt-Root -> video-use syncen (Root ist Wahrheit)
[ -f .env ] || printf 'ELEVENLABS_API_KEY=\n' > .env
key=$(grep -E '^ELEVENLABS_API_KEY=' .env | head -1 | cut -d= -f2- || true)
# Cloud-Sessions: Key aus Environment-Variable übernehmen, falls .env leer
if [ -z "$key" ] && [ -n "${ELEVENLABS_API_KEY:-}" ]; then
  key="$ELEVENLABS_API_KEY"
  grep -v '^ELEVENLABS_API_KEY=' .env > .env.tmp || true
  { printf 'ELEVENLABS_API_KEY=%s\n' "$key"; cat .env.tmp; } > .env && rm -f .env.tmp
fi
printf 'ELEVENLABS_API_KEY=%s\n' "$key" > video-use/.env
chmod 600 .env video-use/.env
