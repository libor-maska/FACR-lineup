from bs4 import BeautifulSoup
from pathlib import Path

ZAPIS = Path(__file__).parent.parent / "data" / "zapis.html"

# otevřít zapis.html soubor
with open(ZAPIS, encoding="utf-8") as f:
    html = f.read()

# parser pro čtení html jako stromu
soup = BeautifulSoup(html, "html.parser")

def zpracuj_radky(radek):
    bunky = radek.find_all("td")

    dres = bunky[0].get_text(strip=True)

    cele_jmeno = list(bunky[1].stripped_strings)[0]
    prijmeni, jmeno = cele_jmeno.rsplit(" ", 1)

    id_a_rocnik = bunky[2].get_text(strip=True)
    facr_id = id_a_rocnik.split(",")[0]

    return {"prijmeni": prijmeni, "jmeno": jmeno, "facr_id": facr_id, "dres": dres}
    


# DOMÁCÍ
# najít a vypsat nadpis Domácí
nadpis = soup.find(string="Hráči domácí")
print("Nadpis: ", nadpis)

# najít a vypsat další tabulku za nadpisem Domácí
tabulka = nadpis.find_next("table")
for radek in tabulka.find_all("tr"):
    if not radek.find_all("td"):
        continue
    hrac = zpracuj_radky(radek)
    print(hrac)


# HOSTÉ
nadpis = soup.find(string="Hráči hosté")
print("Nadpis: ", nadpis)

tabulka = nadpis.find_next("table")
for radek in tabulka.find_all("tr"):
    if not radek.find_all("td"):
        continue
    hrac = zpracuj_radky(radek)
    print(hrac)

# Domácí / Hosté <- <h2>
# Tabulka <- <table style="width:100%">
# Hráč <- <tr> (4 <td>)