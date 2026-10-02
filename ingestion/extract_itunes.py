import requests
import json
import time
import os

TERMS = ["business", "technology", "comedy", "true crime", "history"]
OUTPUT_DIR = "data/raw"

def extract_podcasts():
    print("Extracting podcasts from iTunes API...")
    podcasts = []
    for term in TERMS:
        # Search for podcasts by term
        url = f"https://itunes.apple.com/search?term={term}&media=podcast&limit=20"
        response = requests.get(url)
        if response.status_code == 200:
            results = response.json().get("results", [])
            for res in results:
                podcasts.append({
                    "podcast_id": str(res.get("collectionId")),
                    "podcast_name": res.get("collectionName"),
                    "creator_name": res.get("artistName"),
                    "primary_genre": res.get("primaryGenreName"),
                    "release_date": res.get("releaseDate"),
                    "country": res.get("country")
                })
        time.sleep(1) # Be nice to the API
    
    # Deduplicate by podcast_id
    unique_podcasts = {p["podcast_id"]: p for p in podcasts}.values()
    
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(f"{OUTPUT_DIR}/podcasts.json", "w") as f:
        json.dump(list(unique_podcasts), f, indent=2)
    
    return list(unique_podcasts)

def extract_episodes(podcasts):
    print("Extracting episodes for podcasts...")
    episodes = []
    
    # We will simulate multiple episodes per podcast as the lookup API for episodes 
    # can be inconsistent or require RSS parsing which is heavy for a demo.
    # To keep it simple and deterministic for the demo, we generate realistic metadata.
    from faker import Faker
    import random
    from datetime import datetime, timedelta
    
    fake = Faker()
    
    for pod in podcasts:
        num_episodes = random.randint(10, 50)
        for i in range(num_episodes):
            ep_date = fake.date_between(start_date='-1y', end_date='today')
            episodes.append({
                "episode_id": fake.uuid4(),
                "podcast_id": pod["podcast_id"],
                "episode_title": f"Episode {i+1}: {fake.catch_phrase()}",
                "publish_date": ep_date.isoformat(),
                "duration_seconds": random.randint(1200, 7200)
            })
            
    with open(f"{OUTPUT_DIR}/episodes.json", "w") as f:
        json.dump(episodes, f, indent=2)

if __name__ == "__main__":
    pods = extract_podcasts()
    extract_episodes(pods)
    print("Extraction complete.")
