#!/usr/bin/env python3
"""Apply hybrid D inflection policy to Sableworks PocketBook dictionaries.

Policy (Test-D, production):
- Drop pure ``forma → lemma`` stubs that look like regular inflections of the
  source-language lemma (device stemming / Hunspell / LemmaGen should resolve).
- Keep irregulars, aliases, and any non-stub morphological articles.
- Enrich kept bare forma stubs with a short lemma gloss when available.
- On-device title = language pair only (no Sableworks / Test suffix).
  Packaging credit stays in searchable headwords (sable / credits / license).
"""

from __future__ import annotations

import html
import re
import xml.sax.saxutils as xu
from pathlib import Path

AR_RE = re.compile(r"<ar><k>(.*?)</k><def>(.*?)</def></ar>", re.S)
FORMA_RE = re.compile(r"^\s*<i>forma</i>\s*→\s*(.+?)\s*$", re.S)
TAG_RE = re.compile(r"<[^>]+>")
WS_RE = re.compile(r"\s+")

POS_HINT = re.compile(
    r"(czas\.|rzecz\.|przym\.|przysł\.|spójn\.|przyim\.|zaim\.|"
    r"wykrz\.|licz\.|skr\.|nazwa|zwrot|lm od:|"
    r"adv_phrase|prep_phrase|noun|verb|adj)",
    re.I,
)
SKIP_SENSE = re.compile(
    r"^(?:"
    r"noun|verb|adjective|adverb|pronoun|preposition|conjunction|interjection|"
    r"proper noun|numeral|particle|determiner|phrase|v phras|usage:?.*"
    r")$",
    re.I,
)
IPA_ONLY = re.compile(
    r"^(?:"
    r"/[^/]*/|"
    r"[\[\(]?[ˈˌɪʊəɛɔʌθðŋʃʒːʹ′″.A-Za-z\s]*[ˈˌɪʊəɛɔʌθðŋʃʒː]"
    r"[ˈˌɪʊəɛɔʌθðŋʃʒːʹ′″.A-Za-z\s]*[\]\)]?"
    r")$"
)

# filename stem -> (source lang code, display title)
PACKS = {
    "Angielsko-Polski": ("en", "Angielsko-Polski"),
    "Polsko-Angielski": ("pl", "Polsko-Angielski"),
    "Niemiecko-Polski": ("de", "Niemiecko-Polski"),
    "Polsko-Niemiecki": ("pl", "Polsko-Niemiecki"),
    "Francusko-Polski": ("fr", "Francusko-Polski"),
    "Polsko-Francuski": ("pl", "Polsko-Francuski"),
    "Hiszpansko-Polski": ("es", "Hiszpańsko-Polski"),
    "Polsko-Hiszpanski": ("pl", "Polsko-Hiszpański"),
}


def unescape_key(k: str) -> str:
    return html.unescape(k)


def plain_text(s: str) -> str:
    s = html.unescape(s)
    s = TAG_RE.sub(" ", s)
    return WS_RE.sub(" ", s).strip()


def split_senses(def_html: str) -> list[str]:
    parts = re.split(r"(?:•|<br\s*/?>)", def_html)
    out = []
    for p in parts:
        t = plain_text(p)
        if t:
            out.append(t)
    return out


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
    gloss = WS_RE.sub(" ", "; ".join(picked)).strip(" ;")
    if len(gloss) > max_len:
        cut = gloss[: max_len - 1]
        if " " in cut:
            cut = cut.rsplit(" ", 1)[0]
        gloss = cut.rstrip(";,.") + "…"
    return gloss


def lemma_candidates(target: str) -> list[str]:
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
        seen: set[str] = set()
        while cur in forma_only and hops < max_hops and cur not in seen:
            seen.add(cur)
            nxts = lemma_candidates(forma_only[cur])
            if not nxts:
                break
            cur = nxts[0]
            hops += 1
        if cur in by_key:
            return cur
    return None


def _fold(s: str) -> str:
    return s.casefold()


def _cvc_double(word: str) -> str | None:
    if len(word) < 3:
        return None
    a, b, c = word[-3], word[-2], word[-1]
    vowels = set("aeiouäöüáéíóúàèìòùâêîôû")
    if a not in vowels and b in vowels and c not in vowels and c not in "wxy":
        return word + c
    return None


def is_regular_en(form: str, lemma: str) -> bool:
    f, l = _fold(form), _fold(lemma)
    if f == l:
        return True
    vowels = set("aeiou")
    if l + "s" == f or l + "es" == f:
        return True
    if l.endswith("y") and len(l) > 1 and l[-2] not in vowels and l[:-1] + "ies" == f:
        return True
    if l.endswith("e") and l + "d" == f:
        return True
    if l + "ed" == f:
        return True
    if l.endswith("y") and len(l) > 1 and l[-2] not in vowels and l[:-1] + "ied" == f:
        return True
    dbl = _cvc_double(l)
    if dbl and dbl + "ed" == f:
        return True
    if l + "ing" == f:
        return True
    if l.endswith("e") and not l.endswith("ee") and l[:-1] + "ing" == f:
        return True
    if l.endswith("ie") and l[:-2] + "ying" == f:
        return True
    if dbl and dbl + "ing" == f:
        return True
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


def is_regular_de(form: str, lemma: str) -> bool:
    f, l = _fold(form), _fold(lemma)
    if f == l:
        return True
    # strip ge- ... -t participle when stem matches
    if f.startswith("ge") and f.endswith("t") and len(f) > 3:
        stem = f[2:-1]
        if stem == l or stem == l.rstrip("en") or stem + "en" == l or stem + "e" == l:
            return True
    suffixes = (
        "em",
        "en",
        "er",
        "es",
        "e",
        "s",
        "n",
        "st",
        "t",
        "te",
        "ten",
        "test",
        "tet",
        "end",
        "ende",
        "enden",
        "ender",
        "endes",
    )
    for suf in sorted(suffixes, key=len, reverse=True):
        if f == l + suf:
            return True
        if l.endswith("en") and f == l[:-2] + suf:
            return True
        if l.endswith("e") and f == l[:-1] + suf:
            return True
    # umlaut plurals are NOT treated as regular here
    return False


def is_regular_fr(form: str, lemma: str) -> bool:
    f, l = _fold(form), _fold(lemma)
    if f == l:
        return True
    suffixes = (
        "issements",
        "issement",
        "ations",
        "ation",
        "ments",
        "ment",
        "aient",
        "ions",
        "iez",
        "ais",
        "ait",
        "ant",
        "ent",
        "ons",
        "ez",
        "es",
        "ée",
        "és",
        "ées",
        "é",
        "e",
        "s",
        "x",
    )
    for suf in suffixes:
        if f == l + suf:
            return True
        if l.endswith("e") and f == l[:-1] + suf:
            return True
        if l.endswith("er") and f == l[:-2] + suf:
            return True
        if l.endswith("re") and f == l[:-2] + suf:
            return True
        if l.endswith("ir") and f == l[:-2] + suf:
            return True
    # -aux / -eaux plurals kept (not regular strip)
    return False


def is_regular_es(form: str, lemma: str) -> bool:
    f, l = _fold(form), _fold(lemma)
    if f == l:
        return True
    suffixes = (
        "ábamos",
        "ábamos",
        "aremos",
        "arían",
        "eremos",
        "iremos",
        "ando",
        "iendo",
        "ados",
        "adas",
        "idos",
        "idas",
        "amos",
        "áis",
        "emos",
        "éis",
        "imos",
        "ís",
        "aba",
        "ado",
        "ada",
        "ido",
        "ida",
        "aré",
        "ará",
        "ía",
        "ían",
        "es",
        "os",
        "as",
        "an",
        "en",
        "ó",
        "é",
        "í",
        "o",
        "a",
        "e",
        "s",
        "n",
    )
    # dedupe while preserving longer-first by sorting
    for suf in sorted(set(suffixes), key=len, reverse=True):
        if f == l + suf:
            return True
        if l.endswith("ar") and f == l[:-2] + suf:
            return True
        if l.endswith("er") and f == l[:-2] + suf:
            return True
        if l.endswith("ir") and f == l[:-2] + suf:
            return True
        if l.endswith("o") and f == l[:-1] + suf:
            return True
        if l.endswith("a") and f == l[:-1] + suf:
            return True
        if l.endswith("e") and f == l[:-1] + suf:
            return True
    return False


def is_regular_pl(form: str, lemma: str) -> bool:
    f, l = _fold(form), _fold(lemma)
    if f == l:
        return True
    suffixes = (
        "ami",
        "ach",
        "owi",
        "owie",
        "ów",
        "om",
        "em",
        "ie",
        "ią",
        "ię",
        "ią",
        "ysz",
        "isz",
        "ymy",
        "imy",
        "icie",
        "ycie",
        "łby",
        "łaby",
        "łoby",
        "liby",
        "łyby",
        "cie",
        "cie",
        "my",
        "cie",
        "ła",
        "ło",
        "li",
        "ły",
        "łem",
        "łeś",
        "łeś",
        "ł",
        "ą",
        "ę",
        "u",
        "y",
        "i",
        "e",
        "a",
        "o",
        "ów",
    )
    for suf in sorted(set(suffixes), key=len, reverse=True):
        if f == l + suf:
            return True
        # soft stem drops
        for end in ("a", "o", "e", "y", "i", "ć", "ąć", "eć", "ić", "yć", "ować", "ać"):
            if l.endswith(end) and f == l[: -len(end)] + suf:
                return True
            if l.endswith(end) and f == l[: -len(end)] + end[0] + suf and len(end) > 1:
                # weak heuristic; skip
                pass
    # past participle / adjectival -ny/-na/-ne from -ć verbs often irregular-ish; keep if not simple
    if l.endswith("ć"):
        stem = l[:-1]
        for suf in ("ł", "ła", "ło", "li", "ły", "łem", "łeś", "łam", "łaś"):
            if f == stem + suf:
                return True
    return False


REGULAR = {
    "en": is_regular_en,
    "de": is_regular_de,
    "fr": is_regular_fr,
    "es": is_regular_es,
    "pl": is_regular_pl,
}


def is_regular(lang: str, form: str, lemma: str) -> bool:
    fn = REGULAR.get(lang, is_regular_en)
    return fn(form, lemma)


def transform_xdxf(src: Path, dst: Path, lang: str, title: str) -> dict:
    raw = src.read_text("utf-8")
    pairs = AR_RE.findall(raw)
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

    out: list[tuple[str, str]] = []
    dropped = kept_irreg = enriched = 0

    for k in order:
        d = by_key[k]
        m = FORMA_RE.match(html.unescape(d))
        if not m:
            out.append((key_xml[k], d))
            continue

        target = m.group(1).strip()
        cands = lemma_candidates(target)
        primary = cands[0] if cands else ""
        resolved = resolve_lemma(target, by_key, forma_only) or primary

        regular = False
        for cand in [primary, resolved]:
            if cand and is_regular(lang, k, cand):
                regular = True
                break
        if not regular and primary in forma_only:
            hop = lemma_candidates(forma_only[primary])
            if hop and is_regular(lang, k, hop[0]):
                regular = True

        if regular:
            dropped += 1
            continue

        kept_irreg += 1
        lemma = resolve_lemma(target, by_key, forma_only)
        if lemma:
            gloss = short_gloss(by_key[lemma])
            if gloss and not gloss.lower().startswith("forma →"):
                new_def = f"<i>forma</i> → {xu.escape(target)}<br/>{xu.escape(gloss)}"
                out.append((key_xml[k], new_def))
                enriched += 1
                continue
        out.append((key_xml[k], d))

    with dst.open("w", encoding="utf-8") as fh:
        fh.write('<?xml version="1.0" encoding="UTF-8"?>\n')
        fh.write(f'<xdxf lang_from="" lang_to="" format="visual">\n')
        fh.write(f"<full_name>{xu.escape(title)}</full_name>\n")
        for k_xml, d_xml in out:
            fh.write(f"<ar><k>{k_xml}</k><def>{d_xml}</def></ar>\n")
        fh.write("</xdxf>\n")

    return {
        "src_entries": len(pairs),
        "out_entries": len(out),
        "dropped": dropped,
        "kept_irreg": kept_irreg,
        "enriched": enriched,
        "title": title,
    }


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--src-xdxf", type=Path, required=True)
    ap.add_argument("--dst-xdxf", type=Path, required=True)
    ap.add_argument("--lang", required=True, choices=sorted(REGULAR))
    ap.add_argument("--title", required=True)
    args = ap.parse_args()
    stats = transform_xdxf(args.src_xdxf, args.dst_xdxf, args.lang, args.title)
    print(stats)


if __name__ == "__main__":
    main()
