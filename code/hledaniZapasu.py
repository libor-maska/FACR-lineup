import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL_SOUTEZE = "https://is.fotbal.cz/public/souteze/prehled-soutezi.aspx?sport=fotbal"

# rozloží číslo zápasu na id soutěže, kolo soutěže a pořadí zápasu
# 1.....10 - ID soutěže
# 11...12 - Kolo
# 13...14 - Pořadí zápasu v kole
def rozloz_id_zapasu(cislo_utkani):
    soutez = cislo_utkani[0:10]
    kolo = int(cislo_utkani[10:12])
    zapas = int(cislo_utkani[12:14])

    return soutez, kolo, zapas

# Najde soutěž podle čísla soutěže a vrátí URL detailu
def najdi_soutez(cislo_souteze):
    # GET formulář
    odpoved = requests.get(URL_SOUTEZE)
    soup = BeautifulSoup(odpoved.text, "html.parser")

    # Skrytá .NET pole
    data = {}
    for pole in soup.find_all("input", type="hidden"):
        data[pole["name"]] = pole.get("value", "")

    # Vyplnit číslo soutěže a "Hledat"
    data["ctl00$MainContent$txtSearchCislo"] = cislo_souteze
    data["__EVENTTARGET"] = "ctl00$MainContent$btnSearch"

    # POST
    odpoved = requests.post(URL_SOUTEZE, data=data)
    vysledek = BeautifulSoup(odpoved.text, "html.parser")

    # Najít detail ve výsledcích
    for odkaz in vysledek.find_all("a", href=True):
        if "detail-souteze" in odkaz["href"]:
            return odkaz["href"]
    
    return None

# Najde zápis
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

    # Tabulka zápasů pod nadpisem
    tabulka = nadpis.find_next("table")

    # Hledaný zápas
    for odkaz in tabulka.find_all("a", href=True):
        if "zapis-o-utkani" not in odkaz["href"]:
            continue
        url_zapisu = urljoin(url_souteze, odkaz["href"])+ "&sport=fotbal"
        zapis = requests.get(url_zapisu)
        if cislo_utkani in zapis.text:
            return url_zapisu

    return None


def main():
    cislo_utkani = "2026008C1A0906"

    soutez, kolo, zapas = rozloz_id_zapasu(cislo_utkani)
    print(soutez, kolo, zapas)

    odkaz = najdi_soutez(soutez) # část odkazu (jen url soutěže)

    url_souteze = urljoin(URL_SOUTEZE, odkaz) # celá adresa

    print("Detail soutěže: ", url_souteze)

    url_zapisu = najdi_zapis(url_souteze, kolo, cislo_utkani)
    print("URL zápisu: ", url_zapisu)

if __name__ == "__main__":
    main()