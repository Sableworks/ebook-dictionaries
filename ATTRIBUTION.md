# Attribution — e-reader dictionaries (Blumek Labs)

Files in [`dictionaries/`](dictionaries/) (`.dic` / PocketBook SDIC format for ebook readers) contain **lexical content** from open projects.

## Dictionary content license

**Creative Commons Attribution–ShareAlike (CC BY-SA)** — following the upstream licenses below.

When redistributing the `.dic` files or substantial extracts of their entries:

1. Credit the sources (Wiktionary / Kaikki / FreeDict — as listed below).
2. Keep ShareAlike terms where required by upstream CC BY-SA.
3. Credit that the pack was compiled by **Blumek Labs**  
   ([site](https://blumeklabs.github.io/) · [repo](https://github.com/blumeklabs/blumeklabs.github.io)).

Full CC BY-SA 4.0 text: https://creativecommons.org/licenses/by-sa/4.0/

## Sources

| Source | What we used | Typical license |
|--------|----------------|-----------------|
| [Wiktionary](https://www.wiktionary.org/) via [Kaikki.org](https://kaikki.org/) / [wiktextract](https://github.com/tatuylonen/wiktextract) | Headwords, translations, inflection forms (EN/DE dumps) | **CC BY-SA** |
| [Polish Wiktionary](https://pl.wiktionary.org/) via Kaikki | Polish glosses for DE/EN; PL↔DE / PL↔EN translations; Polish forms | **CC BY-SA** |
| [FreeDict](https://freedict.org/) + WikDict | Pairs `deu-pol`, `pol-deu`, `eng-pol`, `pol-eng` (StarDict) | **CC BY-SA** (plus terms in FreeDict packages) |

FreeDict releases used in the build include:

- `freedict-deu-pol` / `freedict-pol-deu` (WikDict, 2025.11.23)
- `freedict-eng-pol` (Piotrowski+Saloni / FreeDict 0.2.1)
- `freedict-pol-eng` (WikDict, 2025.11.23)

## What is Blumek Labs work (not the CC word data)

- compile / merge pipeline,
- inflection forms for better on-device lookup while reading,
- conversion to e-reader `.dic` (SDIC) packs,
- branding / credits in the pack,
- this portfolio site.

Site and packaging code: see [`LICENSE`](LICENSE) (MIT + notice about CC data).

## Repository

Site code, `.dic` files, checksums, and this attribution:

**https://github.com/blumeklabs/blumeklabs.github.io**
