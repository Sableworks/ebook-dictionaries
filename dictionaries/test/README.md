# Temporary EN→PL inflection test packs

**Not an official release.** These files are for side-by-side PocketBook testing only.
After you pick A or D, they should be removed and replaced by updated production dictionaries.

Official `dictionaries/Angielsko-Polski.dic` is unchanged.

## Files

| File | On-device title | Size | Idea |
|------|----------------|------|------|
| [`Angielsko-Polski-Test-A.dic`](Angielsko-Polski-Test-A.dic) | `Angielsko-Polski · Test-A` | ~5.1 MB | Keep every word form; add a short Polish gloss under `forma → lemma` |
| [`Angielsko-Polski-Test-D.dic`](Angielsko-Polski-Test-D.dic) | `Angielsko-Polski · Test-D` | ~3.9 MB | Drop regular forms (`-ed/-ing/-s` …) so the reader can stem to the lemma; keep irregulars / special cases |

## Install (PocketBook)

1. Copy **one or both** `.dic` files into `system/dictionaries` (hidden folder).
2. Keep the normal `Angielsko-Polski.dic` installed if you want a baseline comparison.
3. In the dictionary list you should see titles ending with **Test-A** / **Test-D**.
4. While reading, long-press the same words in each pack (e.g. `attuned`, `books`, `went`, `children`).

### What you should see

**Test-A — `attuned`**
```text
forma → attune
czas. stroić, zestrajać, dostrajać
```

**Test-D — `attuned`**
- No exact `attuned` entry.
- Device stemming should open **`attune`** with the full lemma definition.
- Needs working English morphology on the device (Hunspell / language support). If stemming fails, the word may show as not found — that is useful feedback for choosing A vs D.

**Both — `went` / `children` / `better`**
- Still have their own richer entries (not bare redirects).

## Rebuild (optional)

```bash
# Requires pbdt (https://codeberg.org/datyoma/pbdt)
pbdt convert dictionaries/Angielsko-Polski.dic /tmp/en-pl.xdxf
pbdt extract-meta dictionaries/Angielsko-Polski.dic /tmp/meta-en
python3 scripts/build_en_pl_inflection_tests.py   # edit paths inside if needed
pbdt convert /tmp/en-pl-test-a.xdxf dictionaries/test/Angielsko-Polski-Test-A.dic --meta-dir /tmp/meta-en
pbdt convert /tmp/en-pl-test-d.xdxf dictionaries/test/Angielsko-Polski-Test-D.dic --meta-dir /tmp/meta-en
```

Lexical content remains **CC BY-SA** (Wiktionary / FreeDict). Packaging: Sableworks.
