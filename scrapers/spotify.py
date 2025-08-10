import requests
from bs4 import BeautifulSoup

def get_spotify_chart(country_code="tr"):
    url = f"https://kworb.net/spotify/country/{country_code}_daily.html"
    response = requests.get(url)
    response.encoding = "utf-8"
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", {"id": "spotifydaily"})
    if not table:
        return []
    rows = table.find("tbody").find_all("tr")
    data = []
    for row in rows:
        cols = row.find_all("td")
        if len(cols) >= 11: 
            pos = cols[0].get_text(strip=True)
            change = cols[1].get_text(strip=True)
            artist_title_div = cols[2].find("div")
            if artist_title_div:
                artist_links = artist_title_div.find_all("a")
                if len(artist_links) >= 2:
                    artist = artist_links[0].get_text(strip=True)
                    title = artist_links[1].get_text(strip=True)
                    featuring = []
                    for a in artist_links[2:]:
                        if 'w/' in a.previous_sibling:
                            featuring.append(a.get_text(strip=True))
                    if featuring:
                        artist += " (feat. " + ", ".join(featuring) + ")"
                else:
                    artist = artist_title_div.get_text(strip=True)
                    title = ""
            else:
                artist = cols[2].get_text(strip=True)
                title = ""
            weeks = cols[3].get_text(strip=True)
            peak = cols[4].get_text(strip=True)
            peak_info = cols[5].get_text(strip=True)
            streams = cols[6].get_text(strip=True)
            streams_change = cols[7].get_text(strip=True)
            total_streams = cols[9].get_text(strip=True)
            data.append({
                "position": int(pos),
                "change": change,
                "artist": artist,
                "title": title,
                "weeks": int(weeks) if weeks.isdigit() else 0,
                "peak": int(peak) if peak.isdigit() else 0,
                "peak_info": peak_info,
                "daily_streams": int(streams.replace(",", "")) if streams.replace(",", "").isdigit() else 0,
                "streams_change": streams_change,
                "total_streams": int(total_streams.replace(",", "")) if total_streams.replace(",", "").isdigit() else 0
            })
    return data