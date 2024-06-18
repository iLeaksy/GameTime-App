import requests
from bs4 import BeautifulSoup
import re
import html

# Function to fetch game details from Steam API
def fetch_game_details(appid):
    print(f"Fetching details for AppID: {appid}")
    url = f"https://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        print(f"API request successful for AppID: {appid}")
        data = response.json()
        if str(appid) in data and data[str(appid)]['success']:
            print(f"Data found for AppID: {appid}")
            game_data = data[str(appid)]['data']
            name = game_data.get('name', 'Unknown Game')
            pc_requirements = game_data.get('pc_requirements', {})
            size_gb = extract_storage_requirement(pc_requirements)
            if size_gb is None:
                pc_requirements_text = html.unescape(pc_requirements.get('minimum', ''))
                return {
                    'appid': appid,
                    'name': name,
                    'pc_requirements': pc_requirements_text
                }
            else:
                return {
                    'appid': appid,
                    'name': name,
                    'size_gb': size_gb
                }
    print(f"No data found for AppID: {appid}")
    return {
        'appid': appid,
        'name': 'Unknown Game',
        'pc_requirements': None
    }

# Function to extract storage requirement from pc_requirements
def extract_storage_requirement(pc_requirements):
    minimum_requirements_html = pc_requirements.get('minimum', '')
    decoded_html = html.unescape(minimum_requirements_html)
    soup = BeautifulSoup(decoded_html, 'html.parser')
    
    # Find the <li> element that contains 'Storage:'
    storage_li = soup.find('li', string=re.compile('Storage:'))
    if storage_li:
        # Extract the storage size using regex
        storage_text = storage_li.get_text()
        match = re.search(r'Storage:\s*([\d\.]+)\s*GB', storage_text, re.IGNORECASE)
        if match:
            return float(match.group(1))
    return None

# List of appids to fetch details for
appids = [730, 570, 578080, 431960, 2923300, 1172470, 1203220, 1245620, 271590, 1938090, 
          1085660, 2977660, 236390, 553850, 359550, 2784840, 381210, 413150, 252490, 
          105600, 289070, 1086940, 2195250, 582010, 2016590]

# Fetch details for each appid and store in a list
game_details_list = []
for appid in appids:
    game_details = fetch_game_details(appid)
    game_details_list.append(game_details)

# Print or process the fetched game details
print("\nFetched Game Details:")
for game in game_details_list:
    if 'size_gb' in game:
        print(f"AppID: {game['appid']}, Name: {game['name']}, Size (GB): {game['size_gb']}")
    else:
        print(f"AppID: {game['appid']}, Name: {game['name']}, PC Requirements: {game['pc_requirements']}")
