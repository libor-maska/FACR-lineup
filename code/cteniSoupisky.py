from bs4 import BeautifulSoup
from pathlib import Path

ZAPIS = Path(__file__).parent.parent / "data" / "zapis.html"

# otevřít zapis.html soubor
with open(ZAPIS, encoding="utf-8") as f:
    html = f.read()

# parser pro čtení html jako stromu
soup = BeautifulSoup(html, "html.parser")

# DOMÁCÍ
# najít a vypsat nadpis Domácí
nadpis = soup.find(string="Hráči domácí")
print("Nadpis: ", nadpis)

# najít a vypsat další tabulku za nadpisem Domácí
tabulka = nadpis.find_next("table")
for radek in tabulka.find_all("tr"):
    print(radek.get_text(" | ", strip=True))


# HOSTÉ
nadpis = soup.find(string="Hráči hosté")
print("Nadpis: ", nadpis)

tabulka = nadpis.find_next("table")
for radek in tabulka.find_all("tr"):
    print(radek.get_text(" | ", strip=True))


# Domácí / Hosté <- <h2>
# Tabulka <- <table style="width:100%">
# Hráč <- <tr> (4 <td>)