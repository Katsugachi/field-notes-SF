#!/usr/bin/env python3
"""Assemble the standalone Field Notes HTML file.

Reads the original fonts, icon, and demo photos, plus the source template,
and writes a single self-contained index.html.
"""
from __future__ import annotations

import base64
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / "field-notes.src.html"
OUT = ROOT / "index.html"
FONT_DIR = ROOT / "fonts"
SAMPLE_META = ROOT / "samples" / "library.json"
# Prefer downscaled copies when present (built next to this script).
SAMPLE_DIR_SMALL = Path("/tmp/fn-assets/samples")
SAMPLE_DIR_FULL = ROOT / "samples" / "library"
ICON = Path("/tmp/fn-assets/icon.png")
if not ICON.exists():
    ICON = ROOT / "icon.png"
FAVICON = Path("/tmp/fn-assets/favicon-32.png")
if not FAVICON.exists():
    FAVICON = ICON


def b64(path: Path) -> str:
    return base64.b64encode(path.read_bytes()).decode("ascii")


def font_css() -> str:
    # 400/500 files in this repo are byte-identical; reuse the 400 files.
    faces = [
        ("EB Garamond", "italic", 400, FONT_DIR / "EBGaramond-400-italic.woff2"),
        ("EB Garamond", "italic", 500, FONT_DIR / "EBGaramond-400-italic.woff2"),
        ("EB Garamond", "normal", 400, FONT_DIR / "EBGaramond-400-normal.woff2"),
        ("EB Garamond", "normal", 500, FONT_DIR / "EBGaramond-400-normal.woff2"),
        ("Inter", "normal", 400, FONT_DIR / "Inter-400-normal.woff2"),
        ("Inter", "normal", 500, FONT_DIR / "Inter-400-normal.woff2"),
    ]
    urange = (
        "U+0000-00FF, U+0131, U+0152-0153, U+02BB-02BC, U+02C6, U+02DA, "
        "U+02DC, U+0304, U+0308, U+0329, U+2000-206F, U+20AC, U+2122, "
        "U+2191, U+2193, U+2212, U+2215, U+FEFF, U+FFFD"
    )
    parts = []
    for family, style, weight, path in faces:
        data = b64(path)
        parts.append(
            f"@font-face{{font-family:'{family}';font-style:{style};font-weight:{weight};"
            f"font-display:swap;src:url(data:font/woff2;base64,{data}) format('woff2');"
            f"unicode-range:{urange};}}"
        )
    return "\n".join(parts)


def seed_js() -> str:
    meta = json.loads(SAMPLE_META.read_text())
    sample_dir = SAMPLE_DIR_SMALL if SAMPLE_DIR_SMALL.exists() else SAMPLE_DIR_FULL
    out = []
    for item in meta:
        img = sample_dir / item["file"]
        if not img.exists():
            img = SAMPLE_DIR_FULL / item["file"]
        data = b64(img)
        rec = dict(item)
        rec["dataURL"] = f"data:image/jpeg;base64,{data}"
        out.append(rec)
    return json.dumps(out, separators=(",", ":"))


def main() -> int:
    if not SRC.exists():
        print(f"missing template: {SRC}", file=sys.stderr)
        return 1
    html = SRC.read_text(encoding="utf-8")
    html = html.replace("/*@@FONT_CSS@@*/", font_css())
    html = html.replace("@@FAVICON@@", b64(FAVICON))
    html = html.replace("@@APPICON@@", b64(ICON))
    html = html.replace("/*@@SEED@@*/[]", seed_js())
    OUT.write_text(html, encoding="utf-8")
    size = OUT.stat().st_size
    print(f"wrote {OUT} ({size:,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
