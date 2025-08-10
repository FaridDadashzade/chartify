import requests
from bs4 import BeautifulSoup

def get_youtube_chart(country_code="tr"):
    url = f"https://kworb.net/youtube/insights/{country_code}.html"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "weeklytable"})
    if not table:
        return []
    rows = table.find("tbody").find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 8:  
            pos = cols[0].get_text(strip=True)
            change = cols[1].get_text(strip=True)
            artist_title = cols[2].get_text(strip=True)
            weeks = cols[3].get_text(strip=True)
            peak = cols[4].get_text(strip=True)
            peak_info = cols[5].get_text(strip=True)
            streams = cols[6].get_text(strip=True)
            streams_change = cols[7].get_text(strip=True)
            if " - " in artist_title:
                artist, title = artist_title.split(" - ", 1)
            else:
                artist, title = artist_title, ""
            data.append({
                "position": int(pos),
                "change": change,
                "artist": artist.strip(),
                "title": title.strip(),
                "weeks": int(weeks) if weeks.isdigit() else 0,
                "peak": int(peak) if peak.isdigit() else 0,
                "peak_info": peak_info,
                "streams": streams,
                "streams_change": streams_change
            })
    return data