# FACR-lineup

Vypíše všechny hráče z oficiálního zápisu o utkání na [is.fotbal.cz](https://is.fotbal.cz) (informační systém FAČR). Stačí zadat číslo utkání.

Pro každého hráče vypíše **příjmení, jméno, FAČR ID a číslo dresu**. Nejdřív jsou domácí, potom hosté.

## Ukázka

```
python code/program.py <číslo utkání>
```

```
== Domácí ==
Příjmení             Jméno        FAČR ID    Dres
Svoboda              Petr         XXXXXXXX      1
Novák                Jan          XXXXXXXX      2
...

== Hosté ==
Příjmení             Jméno        FAČR ID    Dres
Dvořák               Tomáš        XXXXXXXX      1
...
```

## Instalace

Python 3

Knihovny:

```bash
pip install -r requirements.txt
```

## Použití

Výpis hráčů do terminálu:

```bash
python code/program.py <číslo utkání>
```

### Kde najít číslo utkání?

Číslo utkání je v zápisu o utkání nebo v detailu zápasu na is.fotbal.cz. Má 14 znaků ve tvaru `RRRRSSSSSSKKZZ`:

| Část | Význam |
|---|---|
| `RRRRSSSSSS` (10 znaků) | ročník + číslo soutěže |
| `KK` (2 číslice) | kolo |
| `ZZ` (2 číslice) | pořadí zápasu v kole |

## Omezení

- Zápis uvádí hráče jako „Příjmení Jméno“. Za jméno se bere poslední slovo a zbytek je příjmení.
- Hráče jde vypsat jen ze zápasů, které už mají zápis.
- Program je určený k osobnímu použití.

## Pomocné soubory
Mezikroky z vývoje, ponechané pro ukázku postupu. Ke spuštění programu nejsou potřeba.

### helpCode/ulozeniSoupisky.py
Program pro uložení soupisky FAČR podle URL soupisky do html.

### helpCode/cteniSoupisky.py
Program pro vypsání hráčů ze soupisky uložené v html.

### helpCode/hledaniZapasu.py
Program pro vyhledání URL adresy konkrétní soupisky.

