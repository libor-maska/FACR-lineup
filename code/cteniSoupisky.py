from bs4 import BeautifulSoup
from pathlib import Path

ZAPIS = Path(__file__).parent.parent / "data" / "zapis.html"

# funkce pro zpracování řádků
# rozdělí řádky na sloupce prijmeni, jmeno, facr_id, dres
def zpracuj_radky(radek):
    bunky = radek.find_all("td")

    dres = bunky[0].get_text(strip=True)

    cele_jmeno = list(bunky[1].stripped_strings)[0]
    prijmeni, jmeno = cele_jmeno.rsplit(" ", 1)

    id_a_rocnik = bunky[2].get_text(strip=True)
    facr_id = id_a_rocnik.split(",")[0]

    return {"prijmeni": prijmeni, "jmeno": jmeno, "facr_id": facr_id, "dres": dres}
    
# najde tabulku pod nadpisem a vrátí seznam hráčů
def najdi_hrace(soup, text_nadpis):
    nadpis = soup.find(string=text_nadpis)
    tabulka = nadpis.find_next("table")

    hraci = []

    for radek in tabulka.find_all("tr"):
        if not radek.find_all("td"):
            continue
        hraci.append(zpracuj_radky(radek))
    return hraci


def vypis_tabulku(nazev, hraci):
    print(f"\n== {nazev} ==")
    print(f"{'Příjmení':<20} {'Jméno':<12} {'FAČR ID':<10} {'Dres':>4}")
    for hrac in hraci:
        print(f"{hrac['prijmeni']:<20} {hrac['jmeno']:<12} {hrac['facr_id']:<10} {hrac['dres']:>4}")


def main():
    # otevřít zapis.html soubor
    with open(ZAPIS, encoding="utf-8") as f:
        html = f.read()

    # parser pro čtení html jako stromu
    soup = BeautifulSoup(html, "html.parser")

    # uloží hráče jako seznam
    domaci = najdi_hrace(soup, "Hráči domácí")
    hoste = najdi_hrace(soup, "Hráči hosté")

    # vypíše hráče 
    vypis_tabulku("Domácí", domaci)
    vypis_tabulku("Hosté", hoste)



if __name__ == "__main__":
    main()