import requests

URL= "https://is.fotbal.cz/public/zapasy/zapis-o-utkani-report.aspx?sport=fotbal&zapas=1f5b0cd1-a424-4df5-8c7d-fc0c5b78040d"

odpoved = requests.get(URL)
print("Stav. kód: ", odpoved.status_code)

with open("zapis.html", "w", encoding="utf-8") as f:
    f.write(odpoved.text)

print("Uloženo do zapis.html")

