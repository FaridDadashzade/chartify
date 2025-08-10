from flask import Flask, render_template, request
from scrapers.itunes import get_itunes_chart
from scrapers.youtube import get_youtube_chart
from scrapers.shazam import get_shazam_chart
from scrapers.tiktok import get_tiktok_chart
from scrapers.spotify import get_spotify_chart

app = Flask(__name__)

COUNTRIES = {
    "az": "Azerbaijan",
    "tr": "Turkey",
    "us": "United States",
    "uk": "United Kingdom",
    "de": "Germany",
    "fr": "France",
    "ru": "Russia",
    "jp": "Japan"
}

@app.route("/", methods=["GET"])
def index():
    country_code = request.args.get("country", "az")
    itunes_data = get_itunes_chart(country_code)
    youtube_data = get_youtube_chart(country_code)
    shazam_data = get_shazam_chart(country_code)
    tiktok_data = get_tiktok_chart(country_code)
    spotify_data = get_spotify_chart(country_code)
    
    return render_template("index.html",
                           itunes=itunes_data,
                           youtube=youtube_data,
                           shazam=shazam_data,
                           tiktok=tiktok_data,
                           spotify=spotify_data,
                           countries=COUNTRIES,
                           selected_country=country_code)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)