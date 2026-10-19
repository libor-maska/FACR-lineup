from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import sys

# Stránka přehledu soutěží isFAČR
URL_PREHLED = "https://is.fotbal.cz/public/souteze/prehled-soutezi.aspx?sport=fotbal"

# Rozloží číslo utkání a získá soutěž a kolo
def rozloz_id_zapasu(cislo_utkani):
    soutez = cislo_utkani[0:10]
    kolo = int(cislo_utkani[10:12])

    return soutez, kolo


# Najde soutěž podle čísla soutěže a vrátí URL detailu
def najdi_soutez(soutez):
    # GET formulář
    odpoved = requests.get(URL_PREHLED)
    soup = BeautifulSoup(odpoved.text, "html.parser")

    # Skrytá .NET pole
    data = {}
    for pole in soup.find_all("input", type="hidden"):
        data[pole["name"]] = pole.get("value", "")

    # Vyplnit číslo soutěže a "Hledat"
    data["ctl00$MainContent$txtSearchCislo"] = soutez
    data["__EVENTTARGET"] = "ctl00$MainContent$btnSearch"

    # POST
    odpoved = requests.post(URL_PREHLED, data=data)
    vysledek = BeautifulSoup(odpoved.text, "html.parser")

    # Najít detail ve výsledcích
    for odkaz in vysledek.find_all("a", href=True):
        if "detail-souteze" in odkaz["href"]:
            return odkaz["href"]

    return None


# Najde a vrátí URL zápisu
def najdi_zapis(url_souteze, kolo, cislo_utkani):
    odpoved = requests.get(url_souteze)
    soup = BeautifulSoup(odpoved.text, "html.parser")

    # Nadpis kola
    nadpis = None
    for h2 in soup.find_all("h2"):
        if h2.get_text(strip=True).startswith(str(kolo) + ". kolo"):
            nadpis = h2
            break # Nalezeno

    if nadpis is None:
        return None

    # Tabulka zápisů pod nadpisem
    tabulka = nadpis.find_next("table")

    # Hledaný zápas
    for odkaz in tabulka.find_all("a", href=True):
        if "zapis-o-utkani" not in odkaz["href"]:
            continue
        url_zapisu = urljoin(url_souteze, odkaz["href"]) + "&sport=fotbal"
        zapis = requests.get(url_zapisu)

        if cislo_utkani in zapis.text:
            return url_zapisu

    return None


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


# vypíše tabulku hráčů týmu
def vypis_tabulku(nazev, hraci):
    print(f"\n== {nazev} ==")
    print(f"{'Příjmení':<20} {'Jméno':<12} {'FAČR ID':<10} {'Dres':>4}")
    for hrac in hraci:
        print(f"{hrac['prijmeni']:<20} {hrac['jmeno']:<12} {hrac['facr_id']:<10} {hrac['dres']:>4}")


def main():
    # Kontrola a načtení čísla utkání z argumentu
    if len(sys.argv) != 2 or len(sys.argv[1]) != 14:
        sys.exit("Zadej platné číslo utkání")   
    cislo_utkani = sys.argv[1]

    # Rozložení
    soutez, kolo = rozloz_id_zapasu(cislo_utkani)

    odkaz = najdi_soutez(soutez)
    if odkaz is None:
        sys.exit("Soutěž " + soutez + " nenalezena")

    # Získat URL zápisu
    url_souteze = urljoin(URL_PREHLED, odkaz)
    url_zapisu = najdi_zapis(url_souteze, kolo, cislo_utkani)

    if url_zapisu is None:
        sys.exit("Zápas " + cislo_utkani + " nenalezen")

    # html zápisu
    zapis = requests.get(url_zapisu)
    soup = BeautifulSoup(zapis.text, "html.parser")

    domaci = najdi_hrace(soup, "Hráči domácí")
    hoste = najdi_hrace(soup, "Hráči hosté")

    vypis_tabulku("Domácí", domaci)
    vypis_tabulku("Hosté", hoste)


if __name__ == "__main__":
    main()

