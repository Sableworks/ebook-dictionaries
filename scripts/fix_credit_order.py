#!/usr/bin/env python3
"""Move packaging credit block after lexical senses in SDIC packs."""

from __future__ import annotations

import argparse
import re
import subprocess
import xml.sax.saxutils as xu
from pathlib import Path

AR_RE = re.compile(r"<ar><k>(.*?)</k><def>(.*?)</def></ar>", re.S)
# Credit block as injected by branding.CREDITS_HTML (with optional leading bullet)
CREDIT_RE = re.compile(
    r"(?:•\s*)?<b>Made by Sableworks</b>.*?"
    r"Keep upstream attribution when redistributing\.",
    re.S,
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


def reorder_def(def_xml: str) -> tuple[str, bool]:
    m = CREDIT_RE.search(def_xml)
    if not m:
        return def_xml, False
    credit = m.group(0).strip()
    # Normalize credit as a trailing bullet block
    if not credit.startswith("•"):
        credit = "• " + credit
    rest = (def_xml[: m.start()] + def_xml[m.end() :]).strip()
    rest = re.sub(r"^(?:<br\s*/?>)+", "", rest)
    rest = re.sub(r"(?:<br\s*/?>)+$", "", rest)
    rest = rest.strip()
    if not rest:
        # Credit-only entry — leave as a single bullet
        return credit, False
    # Lexical first, credit last
    if rest.endswith("<br/>") or rest.endswith("<br>"):
        new_def = f"{rest}{credit}"
    else:
        new_def = f"{rest}<br/>{credit}"
    return new_def, True


def fix_xdxf(src: Path, dst: Path, title: str) -> int:
    raw = src.read_text("utf-8")
    pairs = AR_RE.findall(raw)
    changed = 0
    with dst.open("w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<xdxf lang_from="" lang_to="" format="visual">\n')
        fh.write(f"<full_name>{xu.escape(title)}</full_name>\n")
        for k, d in pairs:
            new_d, did = reorder_def(d)
            if did:
                changed += 1
            fh.write(f"<ar><k>{k}</k><def>{new_d}</def></ar>\n")
        fh.write("</xdxf>\n")
    return changed


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dict-dir", type=Path, required=True)
    ap.add_argument("--pbdt", type=Path, default=Path("/tmp/pbdt-bin"))
    ap.add_argument("--work", type=Path, default=Path("/tmp/dict-credit-fix"))
    args = ap.parse_args()

    work = args.work
    work.mkdir(parents=True, exist_ok=True)
    pbdt = str(args.pbdt)

    for stem, title in TITLES.items():
        src = args.dict_dir / f"{stem}.dic"
        if not src.exists():
            print(f"skip missing {src}")
            continue
        print(f"==== {stem} ====")
        meta = work / "meta" / stem
        meta.mkdir(parents=True, exist_ok=True)
        xdxf = work / f"{stem}.xdxf"
        fixed = work / f"{stem}.fixed.xdxf"
        out = work / "out" / f"{stem}.dic"
        out.parent.mkdir(parents=True, exist_ok=True)

        subprocess.check_call([pbdt, "extract-meta", str(src), str(meta)])
        subprocess.check_call([pbdt, "convert", str(src), str(xdxf)])
        n = fix_xdxf(xdxf, fixed, title)
        print(f"  reordered credit-after-lexical in {n} entries")
        subprocess.check_call(
            [pbdt, "convert", str(fixed), str(out), "--meta-dir", str(meta)]
        )
        src.write_bytes(out.read_bytes())
        title_bytes = src.read_bytes()[0x40:0x80].split(b"\0", 1)[0]
        print(f"  title={title_bytes.decode('utf-8')!r}")

    # checksums
    import hashlib

    lines = []
    for p in sorted(args.dict_dir.glob("*.dic")):
        h = hashlib.sha256(p.read_bytes()).hexdigest()
        lines.append(f"{h}  {p.name}\n")
    (args.dict_dir / "SHA256SUMS").write_text("".join(lines), encoding="utf-8")
    print("DONE")


if __name__ == "__main__":
    main()
