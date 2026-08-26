# Blumek Labs — free offline e-reader dictionaries

- **Site:** https://blumeklabs.github.io/
- **Repository:** https://github.com/blumeklabs/blumeklabs.github.io

Free **German↔Polish** and **English↔Polish** bilingual dictionaries in **`.dic`** format for ebook / e-ink readers — offline long-press lookup while reading, with common word forms included.

Built and tested on **PocketBook** (e.g. Verse). Other devices that accept the same `.dic` dictionary packs can use them too.

## Downloads

| File | Direction | Approx. size |
|------|-----------|--------------|
| [`dictionaries/Niemiecko-Polski.dic`](dictionaries/Niemiecko-Polski.dic) | German → Polish | ~290k entries |
| [`dictionaries/Polsko-Niemiecki.dic`](dictionaries/Polsko-Niemiecki.dic) | Polish → German | ~330k entries |
| [`dictionaries/Angielsko-Polski.dic`](dictionaries/Angielsko-Polski.dic) | English → Polish | ~232k entries |
| [`dictionaries/Polsko-Angielski.dic`](dictionaries/Polsko-Angielski.dic) | Polish → English | ~425k entries |

Checksums: [`dictionaries/SHA256SUMS`](dictionaries/SHA256SUMS).

**Lexical content license: [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)** — full sources in [`ATTRIBUTION.md`](ATTRIBUTION.md).

### Install (PocketBook example)

1. Copy `.dic` files into `system/dictionaries` (hidden folder).
2. Disconnect USB and select the dictionary in the reader.

On other e-readers, use that device’s dictionary folder if it supports the same `.dic` packs.

Search `blumek` / `credits` inside a dictionary for the pack signature.

## Why these packs

Stock dictionaries on many readers miss past tenses, plurals, and other forms from real books.
These packs merge open lexical data and add inflection forms so lookups hit more often while you read.

## Data sources

**Lexical content (CC BY-SA):**

- [Wiktionary](https://www.wiktionary.org/) via [Kaikki.org](https://kaikki.org/) / [wiktextract](https://github.com/tatuylonen/wiktextract)
- [Polish Wiktionary](https://pl.wiktionary.org/) via Kaikki
- [FreeDict](https://freedict.org/) + WikDict (`deu-pol`, `pol-deu`, `eng-pol`, `pol-eng`)

**Compilation & e-reader packaging** — Blumek Labs (pipeline, forms, `.dic` / SDIC build, branding).

This is **not** commercial publisher dictionary content.

## License

- Dictionary content (`.dic`): **CC BY-SA** — see [`ATTRIBUTION.md`](ATTRIBUTION.md)
- Site & Blumek Labs packaging: [`LICENSE`](LICENSE) (MIT + CC data notice)

## Support

[GitHub Sponsors](https://github.com/sponsors/blumeklabs) (or another donate link on the site).
