# Sableworks — free offline e-reader dictionaries

- **Site:** https://sableworks.github.io/ebook-dictionaries/
- **Repository:** https://github.com/Sableworks/ebook-dictionaries
- **Support:** https://ko-fi.com/sableworks

Created by **Mateusz Blumensztajn** / **Sableworks**.

Free **German↔Polish** and **English↔Polish** bilingual dictionaries in **`.dic`** format for ebook / e-ink readers — offline long-press lookup while reading, with common word forms included.

**Lexical content is [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)** (Wiktionary / FreeDict and related open sources). See [`ATTRIBUTION.md`](ATTRIBUTION.md).

Built and tested on **PocketBook** (e.g. Verse). Other devices that accept the same `.dic` packs can use them too.

## Downloads

| File | Direction | Approx. size |
|------|-----------|--------------|
| [`dictionaries/Niemiecko-Polski.dic`](dictionaries/Niemiecko-Polski.dic) | German → Polish | ~290k entries |
| [`dictionaries/Polsko-Niemiecki.dic`](dictionaries/Polsko-Niemiecki.dic) | Polish → German | ~330k entries |
| [`dictionaries/Angielsko-Polski.dic`](dictionaries/Angielsko-Polski.dic) | English → Polish | ~232k entries |
| [`dictionaries/Polsko-Angielski.dic`](dictionaries/Polsko-Angielski.dic) | Polish → English | ~425k entries |

Checksums: [`dictionaries/SHA256SUMS`](dictionaries/SHA256SUMS).

### Install (PocketBook example)

1. Copy `.dic` files into `system/dictionaries` (hidden folder).
2. Disconnect USB and select the dictionary in the reader.

Search `sable`, `credits`, or `license` inside a dictionary for the pack signature.

## Data sources

**Lexical content (CC BY-SA):**

- [Wiktionary](https://www.wiktionary.org/) via [Kaikki.org](https://kaikki.org/) / [wiktextract](https://github.com/tatuylonen/wiktextract)
- [Polish Wiktionary](https://pl.wiktionary.org/) via Kaikki
- [FreeDict](https://freedict.org/) + WikDict (`deu-pol`, `pol-deu`, `eng-pol`, `pol-eng`)

**Compilation & e-reader packaging** — Sableworks (Mateusz Blumensztajn).

## License

- Dictionary content (`.dic`): **CC BY-SA** — [`ATTRIBUTION.md`](ATTRIBUTION.md)
- Site & packaging code: [`LICENSE`](LICENSE) (MIT + CC data notice)

## Support

[ko-fi.com/sableworks](https://ko-fi.com/sableworks)
