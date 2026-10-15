# Colors — default (Platzhalter)

> Generischer Platzhalter. Ersetze die Werte durch deine Brand (oder lass Claude eine Claude-Design-ZIP hier entpacken).

| Token          | Hex       | Verwendung                                  |
|----------------|-----------|---------------------------------------------|
| `--bg`         | `#F6F4EF` | Hintergrund (warmes Off-White)              |
| `--ink`        | `#14141A` | Primärtext, Linien                          |
| `--accent`     | `#FF5A1F` | Akzent: Marker, Highlights, Schlüsselwörter |
| `--accent-dim` | `#FFD9C7` | Akzent-Flächen, Marker-Hintergrund          |
| `--muted`      | `#8A8A94` | Sekundärtext, Hilfslinien                   |

```css
:root {
  --bg: #F6F4EF;
  --ink: #14141A;
  --accent: #FF5A1F;
  --accent-dim: #FFD9C7;
  --muted: #8A8A94;
}
```

Regeln: maximal eine Akzentfarbe pro Szene. Text auf `--accent` immer in `--ink`.
