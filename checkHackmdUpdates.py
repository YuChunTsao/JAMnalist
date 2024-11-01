import os
import json
import requests
from datetime import datetime, timedelta
from discord_webhook import DiscordWebhook, DiscordEmbed

HACKMD_API_KEY = os.environ['HACKMD_API_KEY']
DISCORD_WEBHOOK_URL = os.environ['DISCORD_WEBHOOK_URL']
LAST_CHECK_FILE = 'last_check.json'

def get_hackmd_notes():
    url = "https://api.hackmd.io/v1/teams/JAM4Polkadot/notes"
    headers = {"Authorization": f"Bearer {HACKMD_API_KEY}"}
    response = requests.get(url, headers=headers)
    return response.json()

def load_last_check():
    if os.path.exists(LAST_CHECK_FILE):
        with open(LAST_CHECK_FILE, 'r') as f:
            return json.load(f)
    return {"last_check": datetime.now().isoformat()}

def save_last_check(last_check):
    with open(LAST_CHECK_FILE, 'w') as f:
        json.dump(last_check, f)

def check_updates():
    last_check = load_last_check()
    last_check_time = datetime.fromisoformat(last_check['last_check'])
    notes = get_hackmd_notes()
    
    updated_notes = []
    for note in notes:
        updated_at = datetime.fromisoformat(note['publishedAt'])
        if updated_at > last_check_time:
            updated_notes.append(note)
    
    save_last_check({"last_check": datetime.now().isoformat()})
    return updated_notes

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
    
    embed = DiscordEmbed(title="HackMD 更新通知", color=242424)
    
    for category in ['on-going', 'commit', 'issues']:
        if categories[category]:
            embed.add_embed_field(
                name=f"{category.capitalize()} 文章",
                value="\n".join([f"- [{note['title']}]({note['url']})" for note in categories[category]]),
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
