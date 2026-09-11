#!/usr/bin/env bash
# Rebuild all official .dic packs with hybrid-D inflection policy.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PBDT="${PBDT:-/tmp/pbdt-bin}"
WORK="${WORK:-/tmp/dict-prod}"
DICT_DIR="$ROOT/dictionaries"
SCRIPT="$ROOT/scripts/apply_hybrid_d_inflections.py"

if [[ ! -x "$PBDT" ]]; then
  echo "pbdt not found at $PBDT" >&2
  exit 1
fi

mkdir -p "$WORK/meta" "$WORK/xdxf" "$WORK/out"

# stem|lang|title
PACKS='
Angielsko-Polski|en|Angielsko-Polski
Polsko-Angielski|pl|Polsko-Angielski
Niemiecko-Polski|de|Niemiecko-Polski
Polsko-Niemiecki|pl|Polsko-Niemiecki
Francusko-Polski|fr|Francusko-Polski
Polsko-Francuski|pl|Polsko-Francuski
Hiszpansko-Polski|es|Hiszpańsko-Polski
Polsko-Hiszpanski|pl|Polsko-Hiszpański
'

echo "$PACKS" | while IFS='|' read -r stem lang title; do
  [[ -z "${stem:-}" ]] && continue
  src="$DICT_DIR/${stem}.dic"
  echo "==== $stem ($lang) → $title ===="
  meta="$WORK/meta/$stem"
  mkdir -p "$meta"
  "$PBDT" extract-meta "$src" "$meta"
  "$PBDT" convert "$src" "$WORK/xdxf/${stem}.xdxf"
  python3 "$SCRIPT" \
    --src-xdxf "$WORK/xdxf/${stem}.xdxf" \
    --dst-xdxf "$WORK/xdxf/${stem}.hybrid-d.xdxf" \
    --lang "$lang" \
    --title "$title"
  "$PBDT" convert \
    "$WORK/xdxf/${stem}.hybrid-d.xdxf" \
    "$WORK/out/${stem}.dic" \
    --meta-dir "$meta"
  python3 -c "from pathlib import Path; p=Path('$WORK/out/${stem}.dic'); t=p.read_bytes()[0x40:0x80].split(b'\\0',1)[0].decode('utf-8'); print('title:', repr(t), 'size:', round(p.stat().st_size/1e6,2), 'MB')"
done

echo "==== installing into repo ===="
cp -f "$WORK/out/"*.dic "$DICT_DIR/"
(cd "$DICT_DIR" && shasum -a 256 *.dic | sort -k2 > SHA256SUMS)
ls -lah "$DICT_DIR"
echo DONE
