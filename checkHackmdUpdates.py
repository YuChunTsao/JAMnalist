import os
import json
import requests
from datetime import datetime, timezone
from discord_webhook import DiscordWebhook, DiscordEmbed
from dotenv import load_dotenv

load_dotenv()

HACKMD_API_KEY = os.environ["HACKMD_API_KEY"]
# for development, read from .env file
if not HACKMD_API_KEY:
    HACKMD_API_KEY = os.getenv("HACKMD_API_KEY")

DISCORD_WEBHOOK_URL = os.environ["DISCORD_WEBHOOK_URL"]
# for development, read from .env file
if not DISCORD_WEBHOOK_URL:
    DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")

LAST_CHECK_FILE = 'last_check.json'

def timestamp_to_datetime(timestamp_ms):
    return datetime.fromtimestamp(timestamp_ms / 1000.0, tz=timezone.utc)

def get_hackmd_notes():
    url = "https://api.hackmd.io/v1/teams/JAM4Polkadot/notes"
    headers = {"Authorization": f"Bearer {HACKMD_API_KEY}"}

    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Request failed with status code: {response.status_code}")
            return [] 
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return [] 

def check_updates():
    last_check = load_last_check()
    last_check_time = int(last_check['last_check']) 
    notes = get_hackmd_notes()
    
    updated_notes = []
    for note in notes:
        try:
            last_changed_at = note['lastChangedAt'] 
            
            if last_changed_at > last_check_time:
                updated_notes.append(note)
        except (KeyError, ValueError, TypeError) as e:
            print(f"Error processing note: {e}")
            print(f"Note data: {note}")
            continue
    
    # 更新最後檢查時間為當前時間的毫秒時間戳
    current_time = int(datetime.now().timestamp() * 1000)
    save_last_check({"last_check": current_time})
    
    return updated_notes

def load_last_check():
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r') as f:
            data = json.load(f)
            return data
    else:
        initial_data = {"last_check": int(datetime.now().timestamp() * 1000)}
        save_last_check(initial_data)
        return initial_data

def save_last_check(last_check):
    with open(LAST_CHECK_FILE, 'w') as f:
        json.dump(last_check, f)

def categorize_notes(notes):
    categories = {
        'on-going': [],
        'commit': [],
        'issues': [],
        'verified': [],
        'casual': []
    }
    
    for note in notes:
        for tag in note['tags']:
            if tag in categories:
                categories[tag].append(note)
                break
    
    return categories

def send_discord_notification(categories):
    webhook = DiscordWebhook(url=DISCORD_WEBHOOK_URL)
    
    embed = DiscordEmbed(title="HackMD 狀態更新", color="c9e0f0")
    
    for category in ['on-going', 'commit', 'issues']:
        if categories[category]:
            embed.add_embed_field(
                name=f"{category.capitalize()} 文章",
                value="\n".join([f"- [{note['title']}]({note['publishLink']})" for note in categories[category]]),
                inline=False
            )
    
    webhook.add_embed(embed)
    webhook.execute()

def main():
    updated_notes = check_updates()
    if updated_notes:
        categories = categorize_notes(updated_notes)
        send_discord_notification(categories)

if __name__ == "__main__":
    main()
