# Attribution — słowniki PocketBook (Blumek Labs)

Pliki w katalogu [`dictionaries/`](dictionaries/) (format PocketBook SDIC `.dic`) zawierają **treść leksykalną** pochodzącą z otwartych projektów.

## Licencja treści słowników

**Creative Commons Attribution–ShareAlike (CC BY-SA)** — zgodnie z licencjami źródeł poniżej.

Przy dalszej dystrybucji plików `.dic` lub istotnych fragmentów haseł:

1. Podaj atrybucję źródeł (Wiktionary / Kaikki / FreeDict — jak poniżej).
2. Zachowaj warunki ShareAlike, jeśli wymagane przez CC BY-SA upstream.
3. Dopisz, że pakiet skompilował **Blumek Labs**  
   ([strona](https://blumeklabs.github.io/) · [repo](https://github.com/blumeklabs/blumeklabs.github.io)).

Pełny tekst CC BY-SA 4.0: https://creativecommons.org/licenses/by-sa/4.0/

## Źródła (co poszło do którego typu danych)

| Źródło | Co wzięliśmy | Licencja (typowo) |
|--------|----------------|-------------------|
| [Wiktionary](https://www.wiktionary.org/) via [Kaikki.org](https://kaikki.org/) / [wiktextract](https://github.com/tatuylonen/wiktextract) | Hasła, tłumaczenia, formy odmiany (EN, DE oraz dane z angielskiego / niemieckiego dumpa) | **CC BY-SA** |
| [plwiktionary](https://pl.wiktionary.org/) via Kaikki | Polskie definicje/glossy dla haseł DE i EN; tłumaczenia PL↔DE / PL↔EN; formy PL | **CC BY-SA** |
| [FreeDict](https://freedict.org/) + WikDict | Pary `deu-pol`, `pol-deu`, `eng-pol`, `pol-eng` (StarDict) | **CC BY-SA** (oraz warunki podane w pakietach FreeDict) |

Konkretne wydania FreeDict użyte przy budowie m.in.:

- `freedict-deu-pol` / `freedict-pol-deu` (WikDict, 2025.11.23)
- `freedict-eng-pol` (Piotrowski+Saloni / FreeDict 0.2.1)
- `freedict-pol-eng` (WikDict, 2025.11.23)

## Co jest pracą Blumek Labs (nie „treścią CC słów”)

- pipeline kompilacji i łączenia źródeł,
- dodanie form odmiany pod lookup na czytniku,
- konwersja do natywnego formatu PocketBook `.dic` (SDIC),
- branding / credits w pakiecie,
- ta strona portfolio.

Strona i kod packaging: zobacz [`LICENSE`](LICENSE) (MIT + notice o danych CC).

## Repozytorium

Kod strony, pliki `.dic`, checksumy i ta atrybucja:

**https://github.com/blumeklabs/blumeklabs.github.io**
