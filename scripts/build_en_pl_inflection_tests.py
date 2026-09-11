#!/usr/bin/env python3
"""Build Test-A and Test-D XDXF variants from Angielsko-Polski export."""

from __future__ import annotations

import html
import re
import xml.sax.saxutils as xu
from pathlib import Path

SRC = Path("/tmp/dict-work/en-pl.xdxf")
OUT_A = Path("/tmp/dict-work/en-pl-test-a.xdxf")
OUT_D = Path("/tmp/dict-work/en-pl-test-d.xdxf")

AR_RE = re.compile(r"<ar><k>(.*?)</k><def>(.*?)</def></ar>", re.S)
FORMA_RE = re.compile(r"^\s*<i>forma</i>\s*→\s*(.+?)\s*$", re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

# Prefer Polish gloss lines that look like real definitions.
POS_HINT = re.compile(
    r"(czas\.|rzecz\.|przym\.|przysł\.|spójn\.|przyim\.|zaim\.|"
    r"wykrz\.|licz\.|skr\.|nazwa|zwrot|lm od:)",
    re.I,
)


def unescape_key(k: str) -> str:
    return html.unescape(k)


def plain_text(s: str) -> str:
    s = html.unescape(s)
    s = TAG_RE.sub(" ", s)
    s = WS_RE.sub(" ", s).strip()
    return s


def split_senses(def_html: str) -> list[str]:
    # Split on bullet / br boundaries used in these packs.
    parts = re.split(r"(?:•|<br\s*/?>)", def_html)
    out = []
    for p in parts:
        t = plain_text(p)
        if t:
            out.append(t)
    return out


SKIP_SENSE = re.compile(
    r"^(?:"
    r"noun|verb|adjective|adverb|pronoun|preposition|conjunction|interjection|"
    r"proper noun|numeral|particle|determiner|phrase|"
    r"v phras|usage:?.*"
    r")$",
    re.I,
)
# Only skip pronunciation-looking lines (must contain IPA marks or be /.../).
IPA_ONLY = re.compile(
    r"^(?:"
    r"/[^/]*/|"
    r"[\[\(]?[ˈˌɪʊəɛɔʌθðŋʃʒːʹ′″.A-Za-z\s]*[ˈˌɪʊəɛɔʌθðŋʃʒː][ˈˌɪʊəɛɔʌθðŋʃʒːʹ′″.A-Za-z\s]*[\]\)]?"
    r")$"
)


def short_gloss(def_html: str, max_len: int = 110) -> str:
    senses = split_senses(def_html)
    picked: list[str] = []
    for s in senses:
        if len(s) < 2:
            continue
        if SKIP_SENSE.match(s) or IPA_ONLY.match(s):
            continue
        if s.lower().startswith("usage:"):
            continue
        useful = bool(POS_HINT.search(s)) or any(
            ch.isalpha() and ord(ch) > 127 for ch in s
        )
        if useful:
            picked.append(s)
        elif not picked and re.search(r"[A-Za-ząćęłńóśźżĄĆĘŁŃÓŚŹŻ]", s) and len(s) > 3:
            picked.append(s)
        if len(picked) >= 2:
            break
    if not picked:
        return ""
    gloss = "; ".join(picked)
    gloss = WS_RE.sub(" ", gloss).strip(" ;")
    if len(gloss) > max_len:
        cut = gloss[: max_len - 1]
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        gloss = cut.rstrip(";,.") + "…"
    return gloss


def lemma_candidates(target: str) -> list[str]:
    # "forties, 40s" / "go / wend" style — try left-to-right.
    parts = re.split(r"\s*(?:,|/|;)\s*", target.strip())
    return [p.strip() for p in parts if p.strip()]


def resolve_lemma(
    target: str,
    by_key: dict[str, str],
    forma_only: dict[str, str],
    max_hops: int = 4,
) -> str | None:
    for cand in lemma_candidates(target):
        hops = 0
        cur = cand
        seen = set()
        while cur in forma_only and hops < max_hops and cur not in seen:
            seen.add(cur)
            nxts = lemma_candidates(forma_only[cur])
            if not nxts:
                break
            cur = nxts[0]
            hops += 1
        if cur in by_key and cur not in forma_only:
            return cur
        if cur in by_key:
            return cur
    return None


def is_regular_english_form(form: str, lemma: str) -> bool:
    """True if form looks like a regular inflection of lemma (EN)."""
    f = form.lower()
    l = lemma.lower()
    if not f.isascii() or not l.isascii():
        # apostrophe words etc. — still try ascii-ish compare
        pass
    if f == l:
        return True

    vowels = set("aeiou")

    def consonant_doubling_stem(word: str) -> str | None:
        # stop -> stopp(ed/ing): CVC ending, stress-agnostic heuristic
        if len(word) < 3:
            return None
        a, b, c = word[-3], word[-2], word[-1]
        if a not in vowels and b in vowels and c not in vowels and c not in "wxy":
            return word + c
        return None

    candidates_true = []

    # -s / -es / -ies
    if l + "s" == f or l + "es" == f:
        return True
    if l.endswith("y") and len(l) > 1 and l[-2] not in vowels and l[:-1] + "ies" == f:
        return True
    if l.endswith(("s", "x", "z", "ch", "sh")) and l + "es" == f:
        return True

    # -ed / -d / -ied
    if l.endswith("e") and l + "d" == f:
        return True
    if l + "ed" == f:
        return True
    if l.endswith("y") and len(l) > 1 and l[-2] not in vowels and l[:-1] + "ied" == f:
        return True
    dbl = consonant_doubling_stem(l)
    if dbl and dbl + "ed" == f:
        return True

    # -ing
    if l + "ing" == f:
        return True
    if l.endswith("e") and not l.endswith("ee") and l[:-1] + "ing" == f:
        return True
    if l.endswith("ie") and l[:-2] + "ying" == f:
        return True
    if dbl and dbl + "ing" == f:
        return True

    # -er / -est / -ly / -ness (adjective-ish regular)
    if l + "er" == f or l + "est" == f or l + "ly" == f or l + "ness" == f:
        return True
    if l.endswith("e") and (l[:-1] + "er" == f or l[:-1] + "est" == f):
        return True
    if l.endswith("y") and len(l) > 1 and l[-2] not in vowels:
        if l[:-1] + "ier" == f or l[:-1] + "iest" == f or l[:-1] + "ily" == f:
            return True
    if dbl and (dbl + "er" == f or dbl + "est" == f):
        return True

    return False


def write_xdxf(path: Path, full_name: str, articles: list[tuple[str, str]]) -> None:
    # Keep keys/defs as already-escaped XML fragments from source where possible.
    with path.open("w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write('<xdxf lang_from="ENG" lang_to="POL" format="visual">\n')
        fh.write(f"<full_name>{xu.escape(full_name)}</full_name>\n")
        for k_xml, d_xml in articles:
            fh.write(f"<ar><k>{k_xml}</k><def>{d_xml}</def></ar>\n")
        fh.write("</xdxf>\n")


def main() -> None:
    raw = SRC.read_text("utf-8")
    pairs = AR_RE.findall(raw)
    print(f"loaded {len(pairs)} articles")

    # Map unescaped key -> def html (first wins); also preserve original key xml
    by_key: dict[str, str] = {}
    key_xml: dict[str, str] = {}
    forma_only: dict[str, str] = {}
    order: list[str] = []

    for k_xml, d_xml in pairs:
        k = unescape_key(k_xml)
        if k not in by_key:
            by_key[k] = d_xml
            key_xml[k] = k_xml
            order.append(k)
        m = FORMA_RE.match(html.unescape(d_xml))
        if m:
            forma_only[k] = m.group(1).strip()

    # --- Test A: enrich pure forma stubs with short gloss ---
    articles_a: list[tuple[str, str]] = []
    enriched = 0
    unresolved = 0
    for k in order:
        d = by_key[k]
        m = FORMA_RE.match(html.unescape(d))
        if not m:
            articles_a.append((key_xml[k], d))
            continue
        target = m.group(1).strip()
        lemma = resolve_lemma(target, by_key, forma_only)
        if not lemma:
            articles_a.append((key_xml[k], d))
            unresolved += 1
            continue
        gloss = short_gloss(by_key[lemma])
        if not gloss or gloss.lower().startswith("forma →"):
            articles_a.append((key_xml[k], d))
            unresolved += 1
            continue
        # Keep original forma line (normalized) + gloss
        # Escape gloss for XML text (no tags)
        new_def = f"<i>forma</i> → {xu.escape(target)}<br/>{xu.escape(gloss)}"
        articles_a.append((key_xml[k], new_def))
        enriched += 1

    write_xdxf(OUT_A, "Angielsko-Polski · Test-A", articles_a)
    print(f"Test-A: {len(articles_a)} entries, enriched={enriched}, unresolved={unresolved} -> {OUT_A}")

    # --- Test D: drop regular forma stubs; keep irregulars (+ gloss if bare) ---
    articles_d: list[tuple[str, str]] = []
    dropped = 0
    kept_irreg = 0
    kept_irreg_enriched = 0
    for k in order:
        d = by_key[k]
        m = FORMA_RE.match(html.unescape(d))
        if not m:
            articles_d.append((key_xml[k], d))
            continue
        target = m.group(1).strip()
        # Regular if ANY primary lemma candidate matches regular morphology
        cands = lemma_candidates(target)
        primary = cands[0] if cands else ""
        # Also resolve through one hop for forms pointing at other forms
        resolved = resolve_lemma(target, by_key, forma_only) or primary
        regular = False
        for cand in [primary, resolved]:
            if cand and is_regular_english_form(k, cand):
                regular = True
                break
        # If form→form chain like attunings→attuning, treat as regular if either hop is
        if not regular and primary in forma_only:
            hop = lemma_candidates(forma_only[primary])
            if hop and is_regular_english_form(k, hop[0]):
                regular = True

        if regular:
            dropped += 1
            continue

        # Keep irregular / alias stub; add gloss when possible
        kept_irreg += 1
        lemma = resolve_lemma(target, by_key, forma_only)
        if lemma:
            gloss = short_gloss(by_key[lemma])
            if gloss and not gloss.lower().startswith("forma →"):
                new_def = f"<i>forma</i> → {xu.escape(target)}<br/>{xu.escape(gloss)}"
                articles_d.append((key_xml[k], new_def))
                kept_irreg_enriched += 1
                continue
        articles_d.append((key_xml[k], d))

    write_xdxf(OUT_D, "Angielsko-Polski · Test-D", articles_d)
    print(
        f"Test-D: {len(articles_d)} entries, dropped_regular={dropped}, "
        f"kept_irreg={kept_irreg}, enriched={kept_irreg_enriched} -> {OUT_D}"
    )

    # Spot-check expected UX words
    for label, arts in (("A", articles_a), ("D", articles_d)):
        m = {unescape_key(k): d for k, d in arts}
        print(f"-- spot {label} --")
        for w in ("attuned", "attune", "books", "went", "children", "better", "running", "mice"):
            if w in m:
                print(f"  {w}: {plain_text(m[w])[:140]}")
            else:
                print(f"  {w}: <ABSENT — stemming should hit lemma>")


if __name__ == "__main__":
    main()
