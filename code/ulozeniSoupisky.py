import requests

# URL zápisu o utkání; bez "sport=fotbal" IS přesměruje na úvodní stránku
URL= "https://is.fotbal.cz/public/zapasy/zapis-o-utkani-report.aspx?sport=fotbal&zapas=1f5b0cd1-a424-4df5-8c7d-fc0c5b78040d"

# Stažení stránky
odpoved = requests.get(URL)
# Stav kód - 200ok
print("Stav. kód: ", odpoved.status_code)

# uložení html do souboru
with open("../soupiska/zapis.html", "w", encoding="utf-8") as f:
    f.write(odpoved.text)


print("Uloženo do zapis.html")

