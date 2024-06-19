import os
import json
import re
from flask import Flask, request, jsonify, render_template
import requests
from bs4 import BeautifulSoup
import html

app = Flask(__name__)

STEAM_MOST_PLAYED_URL = "https://api.steampowered.com/ISteamChartsService/GetMostPlayedGames/v1/"
STEAM_APPDETAILS_URL = "https://store.steampowered.com/api/appdetails?appids="
CACHE_FILE = 'most_played_games_cache.json'
GAME_LIMIT = 25

# Load game details cache from file
if os.path.exists(CACHE_FILE):
    with open(CACHE_FILE, 'r') as f:
        game_details_cache = json.load(f)
else:
    game_details_cache = {}

def fetch_most_played_games():
    if not game_details_cache:
        try:
            response = requests.get(STEAM_MOST_PLAYED_URL)
            response.raise_for_status()
            data = response.json()
            games = data["response"]["ranks"][:GAME_LIMIT]
            for game in games:
                appid = game["appid"]
                # Fetch game details to get the name
                details = fetch_game_details(appid)
                game_details_cache[appid] = {
                    "appid": appid,
                    "name": details.get("name", "Unknown Game")
                }
            # Save to cache file
            with open(CACHE_FILE, 'w') as f:
                json.dump(game_details_cache, f)
        except requests.RequestException as e:
            print(f"Error fetching most played games: {e}")
            return []
    return list(game_details_cache.values())

def fetch_game_details(appid):
    if appid in game_details_cache and ('size_gb' in game_details_cache[appid] or 'pc_requirements' in game_details_cache[appid]):
        return game_details_cache[appid]

    try:
        response = requests.get(f"{STEAM_APPDETAILS_URL}{appid}")
        response.raise_for_status()
        data = response.json()
        if data[str(appid)]["success"]:
            game_data = data[str(appid)]["data"]
            pc_requirements = game_data.get("pc_requirements", {})
            size_gb = None
            if "minimum" in pc_requirements:
                storage_match = re.search(r"Storage:\s*(\d+\.?\d*)\s*GB", pc_requirements["minimum"])
                if storage_match:
                    size_gb = float(storage_match.group(1))
            pc_requirements_text = html.unescape(pc_requirements.get('minimum', ''))
            game_details_cache[appid] = {
                "appid": appid,
                "name": game_data.get("name", "Unknown Game"),
                "size_gb": size_gb,
                "pc_requirements": pc_requirements_text
            }
            # Save updated cache
            with open(CACHE_FILE, 'w') as f:
                json.dump(game_details_cache, f)
            print(f"Fetched and cached details for appid {appid}: {game_details_cache[appid]}")
            return game_details_cache[appid]
        else:
            print(f"Failed to fetch details for appid {appid}: {data}")
        return {"appid": appid, "name": "Unknown Game", "size_gb": None, "pc_requirements": None}
    except requests.RequestException as e:
        print(f"Error fetching game details for appid {appid}: {e}")
        return {"appid": appid, "name": "Unknown Game", "size_gb": None, "pc_requirements": None}

def calculate_download_time(size_gb, speed_mbps):
    size_bits = size_gb * 8 * 1024 * 1024 * 1024
    speed_bps = speed_mbps * 1024 * 1024
    time_seconds = size_bits / speed_bps

    if time_seconds < 60:
        return f"{int(time_seconds)} seconds"
    elif time_seconds < 3600:
        minutes = int(time_seconds // 60)
        seconds = int(time_seconds % 60)
        return f"{minutes} minutes {seconds} seconds"
    elif time_seconds < 86400:
        hours = int(time_seconds // 3600)
        minutes = int((time_seconds % 3600) // 60)
        return f"{hours} hours {minutes} minutes"
    else:
        days = int(time_seconds // 86400)
        hours = int((time_seconds % 86400) // 3600)
        return f"{days} days {hours} hours"

@app.route('/')
def index():
    games = fetch_most_played_games()
    return render_template('index.html', games=games)


@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    download_speed = float(data['downloadSpeed'])
    search_query = data.get('searchQuery', '').lower()

    games = fetch_most_played_games()

    if search_query:
        games = [game for game in games if search_query in game['name'].lower()]

    results = []
    for game in games:
        size_gb = game.get("size_gb")
        if size_gb is None:
            game_details = fetch_game_details(game["appid"])
            size_gb = game_details.get("size_gb")
            pc_requirements = game_details.get("pc_requirements", "")
            results.append({"name": game["name"], "pc_requirements": pc_requirements})
        if size_gb:
            time = calculate_download_time(size_gb, download_speed)
            results.append({"name": game["name"], "size_gb": size_gb, "time": time})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
