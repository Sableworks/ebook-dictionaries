# Blumek Labs

- **Strona (GitHub Pages):** https://blumeklabs.github.io/
- **Repozytorium:** https://github.com/blumeklabs/blumeklabs.github.io

## PocketBook dictionaries

Gotowe słowniki `.dic` (format SDIC) pod PocketBook Verse i pokrewne.

| Plik | Kierunek | Orientacyjna wielkość |
|------|----------|------------------------|
| [`dictionaries/Niemiecko-Polski.dic`](dictionaries/Niemiecko-Polski.dic) | DE → PL | ~290k haseł |
| [`dictionaries/Polsko-Niemiecki.dic`](dictionaries/Polsko-Niemiecki.dic) | PL → DE | ~330k haseł |
| [`dictionaries/Angielsko-Polski.dic`](dictionaries/Angielsko-Polski.dic) | EN → PL | ~232k haseł |
| [`dictionaries/Polsko-Angielski.dic`](dictionaries/Polsko-Angielski.dic) | PL → EN | ~425k haseł |

Checksumy: [`dictionaries/SHA256SUMS`](dictionaries/SHA256SUMS).

**Licencja treści haseł w `.dic`: [CC BY-SA](https://creativecommons.org/licenses/by-sa/4.0/)** — pełne źródła w [`ATTRIBUTION.md`](ATTRIBUTION.md).

### Instalacja

1. Skopiuj `.dic` do `system/dictionaries` na urządzeniu (folder ukryty).
2. Odłącz USB i wybierz słownik w czytniku.

W słowniku wyszukaj `blumek` / `credits`, żeby zobaczyć podpis pakietu.

## Źródła danych

**Treść leksykalna (CC BY-SA):**

- [Wiktionary](https://www.wiktionary.org/) via [Kaikki.org](https://kaikki.org/) / [wiktextract](https://github.com/tatuylonen/wiktextract)
- [plwiktionary](https://pl.wiktionary.org/) via Kaikki
- [FreeDict](https://freedict.org/) + WikDict (`deu-pol`, `pol-deu`, `eng-pol`, `pol-eng`)

**Kompilacja / packaging PocketBook** — Blumek Labs (pipeline, formy odmiany, SDIC, branding).

To **nie** jest treść z komercyjnych słowników wydawniczych.

## Licencja

- Treść słowników (`.dic`): **CC BY-SA** — zobacz [`ATTRIBUTION.md`](ATTRIBUTION.md)
- Strona i packaging Blumek Labs: [`LICENSE`](LICENSE) (MIT + notice o danych CC)

## Support

[GitHub Sponsors](https://github.com/sponsors/blumeklabs) (albo inny link donate na stronie).
