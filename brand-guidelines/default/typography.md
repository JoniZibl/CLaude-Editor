# Typography — default (Platzhalter)

- **Display:** Space Grotesk (600/700) — Headlines, Untertitel, Callouts
- **Data:** JetBrains Mono (400/600) — Zahlen, Dateinamen, Statusmeldungen

```html
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
```

```css
:root {
  --font-display: "Space Grotesk", system-ui, sans-serif;
  --font-data: "JetBrains Mono", ui-monospace, monospace;
}
```

Skala (1080p): Headline 96px · Sub 56px · Untertitel 64px (Shorts 72px) · Label 32px.
Keine Banned Fonts (siehe `docs/motion-philosophy.md`).
