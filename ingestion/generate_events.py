import json
import random
import os
from faker import Faker
import numpy as np
from datetime import datetime, timedelta
import uuid

OUTPUT_DIR = "data/raw"

def load_json(filename):
    with open(f"{OUTPUT_DIR}/{filename}", "r") as f:
        return json.load(f)

def generate_advertisers(num=50):
    fake = Faker()
    advertisers = []
    for _ in range(num):
        advertisers.append({
            "advertiser_id": fake.uuid4(),
            "advertiser_name": fake.company(),
            "industry": fake.bs()
        })
    with open(f"{OUTPUT_DIR}/advertisers.json", "w") as f:
        json.dump(advertisers, f, indent=2)
    return advertisers

def generate_campaigns(advertisers, podcasts):
    fake = Faker()
    campaigns = []
    for adv in advertisers:
        # Each advertiser runs 1-5 campaigns
        for _ in range(random.randint(1, 5)):
            start_date = fake.date_between(start_date='-6m', end_date='today')
            end_date = start_date + timedelta(days=random.randint(14, 60))
            campaigns.append({
                "campaign_id": fake.uuid4(),
                "advertiser_id": adv["advertiser_id"],
                "campaign_name": f"{adv['advertiser_name']} - {fake.catch_phrase()}",
                "start_date": start_date.isoformat(),
                "end_date": end_date.isoformat(),
                "budget": round(random.uniform(1000, 50000), 2),
                "cpm_rate": round(random.uniform(15, 30), 2)
            })
    with open(f"{OUTPUT_DIR}/campaigns.json", "w") as f:
        json.dump(campaigns, f, indent=2)
    return campaigns

def generate_events(episodes, campaigns):
    fake = Faker()
    downloads = []
    impressions = []
    
    print("Generating downloads and impressions...")
    for ep in episodes:
        # Number of downloads per episode based on a log-normal distribution
        num_downloads = int(np.random.lognormal(mean=5, sigma=1.5))
        
        # Determine if this episode had an ad campaign active
        active_campaigns = random.sample(campaigns, k=random.randint(0, 2))
        
        for i in range(num_downloads):
            dl_id = fake.uuid4()
            dl_time = fake.date_time_between_dates(
                datetime.fromisoformat(ep["publish_date"]), 
                datetime.now()
            )
            
            # Plant defect: Sometimes null listener_id
            listener_id = fake.uuid4() if random.random() > 0.05 else None
            
            downloads.append({
                "download_id": dl_id,
                "episode_id": ep["episode_id"],
                "listener_id": listener_id,
                "download_timestamp": dl_time.isoformat(),
                "user_agent": fake.user_agent(),
                "country": fake.country_code()
            })
            
            # Plant defect: Duplicates
            if random.random() > 0.99:
                downloads.append(downloads[-1])
                
            # Generate impressions
            for camp in active_campaigns:
                camp_start = datetime.fromisoformat(camp["start_date"])
                camp_end = datetime.fromisoformat(camp["end_date"])
                
                # Check if download happened during campaign window
                if camp_start.date() <= dl_time.date() <= camp_end.date():
                    # 80% fill rate
                    if random.random() < 0.8:
                        impressions.append({
                            "impression_id": fake.uuid4(),
                            "download_id": dl_id,
                            "campaign_id": camp["campaign_id"],
                            "impression_timestamp": (dl_time + timedelta(seconds=random.randint(1, 60))).isoformat()
                        })

    with open(f"{OUTPUT_DIR}/downloads.json", "w") as f:
        json.dump(downloads, f, indent=2)
    with open(f"{OUTPUT_DIR}/impressions.json", "w") as f:
        json.dump(impressions, f, indent=2)

def generate_payouts(campaigns, podcasts):
    fake = Faker()
    payouts = []
    print("Generating payouts...")
    for camp in campaigns:
        # Payouts to random podcasts for this campaign
        pods_in_camp = random.sample(podcasts, k=random.randint(1, 5))
        for pod in pods_in_camp:
            amount = round(random.uniform(50, 1000), 2)
            payout_date = datetime.fromisoformat(camp["end_date"]) + timedelta(days=30)
            
            payouts.append({
                "payout_id": fake.uuid4(),
                "campaign_id": camp["campaign_id"],
                "podcast_id": pod["podcast_id"],
                "amount": amount,
                "payout_date": payout_date.isoformat(),
                "status": random.choice(["paid", "pending", "failed"])
            })
            
    with open(f"{OUTPUT_DIR}/payouts.json", "w") as f:
        json.dump(payouts, f, indent=2)

if __name__ == "__main__":
    if not os.path.exists(f"{OUTPUT_DIR}/podcasts.json"):
        print("Please run extract_itunes.py first!")
        exit(1)
        
    podcasts = load_json("podcasts.json")
    episodes = load_json("episodes.json")
    
    advs = generate_advertisers()
    camps = generate_campaigns(advs, podcasts)
    generate_events(episodes, camps)
    generate_payouts(camps, podcasts)
    print("Synthetic events generated.")
