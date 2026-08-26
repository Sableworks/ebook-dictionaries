# Blumek Labs

- **GitHub Pages:** https://blumeklabs.github.io/
- **Repository:** https://github.com/blumeklabs/blumeklabs.github.io

## PocketBook dictionaries

Ready-to-use PocketBook SDIC `.dic` files (Verse and similar devices).

| File | Direction | Approx. size |
|------|-----------|--------------|
| [`dictionaries/Niemiecko-Polski.dic`](dictionaries/Niemiecko-Polski.dic) | DE → PL | ~290k entries |
| [`dictionaries/Polsko-Niemiecki.dic`](dictionaries/Polsko-Niemiecki.dic) | PL → DE | ~330k entries |
| [`dictionaries/Angielsko-Polski.dic`](dictionaries/Angielsko-Polski.dic) | EN → PL | ~232k entries |
| [`dictionaries/Polsko-Angielski.dic`](dictionaries/Polsko-Angielski.dic) | PL → EN | ~425k entries |

Checksums: [`dictionaries/SHA256SUMS`](dictionaries/SHA256SUMS).

**Lexical content license: [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)** — full sources in [`ATTRIBUTION.md`](ATTRIBUTION.md).

### Install

1. Copy `.dic` files into `system/dictionaries` on the device (hidden folder).
2. Disconnect USB and select the dictionary in the reader.

Search `blumek` / `credits` inside the dictionary for the pack signature.

## Data sources

**Lexical content (CC BY-SA):**

- [Wiktionary](https://www.wiktionary.org/) via [Kaikki.org](https://kaikki.org/) / [wiktextract](https://github.com/tatuylonen/wiktextract)
- [Polish Wiktionary](https://pl.wiktionary.org/) via Kaikki
- [FreeDict](https://freedict.org/) + WikDict (`deu-pol`, `pol-deu`, `eng-pol`, `pol-eng`)

**PocketBook packaging** — Blumek Labs (pipeline, inflection forms, SDIC, branding).

This is **not** commercial publisher dictionary content.

## License

- Dictionary content (`.dic`): **CC BY-SA** — see [`ATTRIBUTION.md`](ATTRIBUTION.md)
- Site & Blumek Labs packaging: [`LICENSE`](LICENSE) (MIT + CC data notice)

## Support

[GitHub Sponsors](https://github.com/sponsors/blumeklabs) (or another donate link on the site).
