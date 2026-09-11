#!/usr/bin/env python3
"""Replace sableworks credit headword with quiet signature ``13``."""

from __future__ import annotations

import hashlib
import re
import subprocess
import xml.sax.saxutils as xu
from pathlib import Path

AR_RE = re.compile(r"<ar><k>(.*?)</k><def>(.*?)</def></ar>", re.S)

CREDITS_HTML = (
    "<b>Made by Sableworks</b><br>"
    "Compiled by Mateusz Blumensztajn (Sableworks)<br>"
    "E-reader dictionary pack (.dic)<br>"
    '<a href="https://sableworks.github.io/ebook-dictionaries/">'
    "https://sableworks.github.io/ebook-dictionaries/</a><br>"
    "<br>"
    "<b>License:</b> lexical content is <b>CC BY-SA</b> "
    "(Wiktionary / FreeDict and related open sources). "
    "Keep upstream attribution when redistributing."
)

TITLES = {
    "Angielsko-Polski": "Angielsko-Polski",
    "Polsko-Angielski": "Polsko-Angielski",
    "Niemiecko-Polski": "Niemiecko-Polski",
    "Polsko-Niemiecki": "Polsko-Niemiecki",
    "Francusko-Polski": "Francusko-Polski",
    "Polsko-Francuski": "Polsko-Francuski",
    "Hiszpansko-Polski": "Hiszpańsko-Polski",
    "Polsko-Hiszpanski": "Polsko-Hiszpański",
}


def transform(src: Path, dst: Path, title: str) -> tuple[bool, bool]:
    raw = src.read_text("utf-8")
    pairs = AR_RE.findall(raw)
    out: list[tuple[str, str]] = []
    removed_sw = False
    has_13 = False
    for k, d in pairs:
        if k == "sableworks":
            removed_sw = True
            continue
        if k == "13":
            has_13 = True
            # Force credit-only signature (no leftover forma stubs)
            out.append((k, f"• {CREDITS_HTML}"))
            continue
        out.append((k, d))
    added_13 = False
    if not has_13:
        out.append(("13", f"• {CREDITS_HTML}"))
        added_13 = True
        # Keep roughly sorted? PocketBook packs are sorted by converter.
    with dst.open("w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<xdxf lang_from="" lang_to="" format="visual">\n')
        fh.write(f"<full_name>{xu.escape(title)}</full_name>\n")
        for k, d in out:
            fh.write(f"<ar><k>{k}</k><def>{d}</def></ar>\n")
        fh.write("</xdxf>\n")
    return removed_sw, added_13


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    dict_dir = root / "dictionaries"
    pbdt = Path("/tmp/pbdt-bin")
    work = Path("/tmp/dict-sig13")
    work.mkdir(parents=True, exist_ok=True)

    for stem, title in TITLES.items():
        src = dict_dir / f"{stem}.dic"
        print(f"==== {stem} ====")
        meta = work / "meta" / stem
        meta.mkdir(parents=True, exist_ok=True)
        xdxf = work / f"{stem}.xdxf"
        fixed = work / f"{stem}.fixed.xdxf"
        out = work / "out" / f"{stem}.dic"
        out.parent.mkdir(parents=True, exist_ok=True)
        subprocess.check_call([str(pbdt), "extract-meta", str(src), str(meta)])
        subprocess.check_call([str(pbdt), "convert", str(src), str(xdxf)])
        removed, added = transform(xdxf, fixed, title)
        print(f"  removed sableworks={removed} added/kept 13={added or True}")
        subprocess.check_call(
            [str(pbdt), "convert", str(fixed), str(out), "--meta-dir", str(meta)]
        )
        src.write_bytes(out.read_bytes())

    lines = []
    for p in sorted(dict_dir.glob("*.dic")):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{h}  {p.name}\n")
    (dict_dir / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")
    print("DONE")


if __name__ == "__main__":
    main()
