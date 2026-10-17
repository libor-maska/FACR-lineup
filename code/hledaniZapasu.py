import requests
from bs4 import BeautifulSoup

URL_SOUTEZE = "https://is.fotbal.cz/public/souteze/prehled-soutezi.aspx?sport=fotbal"

# rozloží číslo zápasu na id soutěže, kolo soutěže a pořadí zápasu
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


def main():
    soutez, kolo, zapas = rozloz_id_zapasu("2026008C1A0906")
    print(soutez, kolo, zapas)

    url = najdi_soutez(soutez)
    print("Detail soutěže: ", url)

if __name__ == "__main__":
    main()