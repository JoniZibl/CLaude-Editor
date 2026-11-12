"""Instagram-style word-pop captions (ASS) for on-camera speakers only.

speaker_0 = off-camera interviewer -> no captions.
Groups of max 3 words, active word highlighted yellow, pop-in per group.
"""
import json, re, sys
from pathlib import Path

SRC = Path(__file__).parent / "transcripts" / "karneval_impfen_v3.json"
OUT = Path(__file__).parent / "captions.ass"
SKIP_SPEAKERS = {"speaker_0"}
FILLERS = {"ähm", "äh", "öhm", "hm", "ähm,", "äh,"}
MAX_WORDS, MAX_CHARS = 3, 16

def ts(t):
    t = max(t, 0)
    h, r = divmod(t, 3600); m, s = divmod(r, 60)
    return f"{int(h)}:{int(m):02d}:{s:05.2f}"

words = [w for w in json.load(open(SRC))["words"] if w.get("type") == "word"]

groups, cur = [], []
for i, w in enumerate(words):
    txt = w["text"].strip()
    if w.get("speaker_id") in SKIP_SPEAKERS:
        if cur: groups.append(cur); cur = []
        continue
    if re.sub(r"[^\wäöüß]", "", txt.lower()) in {f.strip(",") for f in FILLERS}:
        continue
    gap = cur and w["start"] - cur[-1]["end"] > 0.6
    chars = sum(len(x["text"]) + 1 for x in cur) + len(txt)
    spk_change = cur and cur[-1]["speaker_id"] != w["speaker_id"]
    if cur and (len(cur) >= MAX_WORDS or chars > MAX_CHARS or gap or spk_change):
        groups.append(cur); cur = []
    cur.append({"text": txt, "start": w["start"], "end": w["end"], "speaker_id": w["speaker_id"]})
    if re.search(r"[.?!,]$", txt):
        groups.append(cur); cur = []
if cur: groups.append(cur)

YEL, WHITE = r"&H0000E5FF&", r"&H00FFFFFF&"
lines = []
for gi, g in enumerate(groups):
    nxt = groups[gi + 1][0]["start"] if gi + 1 < len(groups) else 1e9
    g_end = min(g[-1]["end"] + 0.35, nxt)
    for wi, w in enumerate(g):
        s = w["start"] if wi else max(w["start"] - 0.05, 0)
        e = g[wi + 1]["start"] if wi + 1 < len(g) else g_end
        parts = []
        for k, x in enumerate(g):
            t = x["text"].upper().rstrip(",.")
            parts.append(f"{{\\c{YEL if k == wi else WHITE}}}{t}")
        pop = r"{\fscx70\fscy70\t(0,110,\fscx108\fscy108)\t(110,190,\fscx100\fscy100)}" if wi == 0 else ""
        lines.append(f"Dialogue: 0,{ts(s)},{ts(e)},Cap,,0,0,0,,{pop}{' '.join(parts)}")

header = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,Inter Display Black,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H64000000,0,0,0,0,100,100,0,0,1,7,4,2,80,80,560,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
"""
OUT.write_text(header + "\n".join(lines) + "\n", encoding="utf-8")
print(f"{len(groups)} groups, {len(lines)} events -> {OUT}")
