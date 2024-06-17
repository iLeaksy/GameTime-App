from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

games = [
    {"name": "Fortnite", "size_gb": 90},
    {"name": "Minecraft", "size_gb": 1},
    {"name": "Call of Duty: Warzone", "size_gb": 175},
    {"name": "League of Legends", "size_gb": 9},
    {"name": "Valorant", "size_gb": 20},
    {"name": "Apex Legends", "size_gb": 68},
    {"name": "Among Us", "size_gb": 0.25},
    {"name": "Counter-Strike: Global Offensive", "size_gb": 20},
    {"name": "Genshin Impact", "size_gb": 30},
    {"name": "PUBG", "size_gb": 30},
    {"name": "Overwatch", "size_gb": 30},
    {"name": "Grand Theft Auto V", "size_gb": 94},
    {"name": "The Witcher 3: Wild Hunt", "size_gb": 50},
    {"name": "Red Dead Redemption 2", "size_gb": 150},
    {"name": "Cyberpunk 2077", "size_gb": 70},
    {"name": "Rocket League", "size_gb": 20},
    {"name": "FIFA 21", "size_gb": 50},
    {"name": "Fall Guys", "size_gb": 2},
    {"name": "Assassin's Creed Valhalla", "size_gb": 50},
    {"name": "Destiny 2", "size_gb": 105},
    {"name": "Battlefield V", "size_gb": 90},
    {"name": "Rainbow Six Siege", "size_gb": 61},
    {"name": "Madden NFL 21", "size_gb": 50},
    {"name": "NBA 2K21", "size_gb": 121},
    {"name": "The Sims 4", "size_gb": 40}
]

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
    return render_template('index.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    download_speed = float(data['downloadSpeed'])

    results = []
    for game in games:
        time = calculate_download_time(game["size_gb"], download_speed)
        results.append({"name": game["name"], "size_gb": game["size_gb"], "time": time})

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
