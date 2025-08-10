import requests
from bs4 import BeautifulSoup

def get_itunes_chart(country_code="az"):
    url = f"https://kworb.net/charts/itunes/{country_code}.html"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "simpletable"})
    if not table:
        table = soup.find("table", {"class": "sortable"})
    if not table:
        return []
    rows = table.find("tbody").find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) == 3:
            pos = cols[0].get_text(strip=True)
            change = cols[1].get_text(strip=True)
            artist_title = cols[2].get_text(strip=True)
        elif len(cols) == 2:
            pos = cols[0].get_text(strip=True)
            change = "" 
            artist_title = cols[1].get_text(strip=True)
        else:
            continue 
        if " - " in artist_title:
            artist, title = artist_title.split(" - ", 1)
        else:
            artist, title = artist_title, ""
        data.append({
            "position": int(pos),
            "change": change,
            "artist": artist.strip(),
            "title": title.strip()
        })
    return data