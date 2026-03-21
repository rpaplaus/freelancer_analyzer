from apify_client import ApifyClient
from typing import List
from scraper.models import RawJob
from config.settings import settings
from datetime import datetime

def fetch_upwork_jobs(query: str = "python") -> List[RawJob]:
    """
    Uses the official Apify Client to run a dedicated Upwork Scraper Actor.
    This entirely bypasses local Cloudflare blocks by running remotely.
    """
    if not settings.APIFY_API_KEY:
        print("APIFY_API_KEY is not set. Skipping Apify Upwork scrape.")
        return []

    client = ApifyClient(settings.APIFY_API_KEY)
    
    run_input = {
        "queries": [query],
        "maxItems": 20
    }
    
    raw_jobs = []
    actor_id = getattr(settings, "APIFY_ACTOR_ID", "jupri/upwork-scraper")
    
    print(f"Triggering Apify Actor [{actor_id}] remotely on Apify Cloud...")
    try:
        run = client.actor(actor_id).call(run_input=run_input)
        print("Apify run completed. Fetching results...")
        
        import json
        is_first = True
        
        for item in client.dataset(run["defaultDatasetId"]).iterate_items():
            if is_first:
                try:
                    with open("apify_debug.json", "w", encoding="utf-8") as f:
                        json.dump(item, f, indent=2)
                    print("\n📸 [DEBUG] Salvei a estrutura bruta do primeiro Job em apify_debug.json para inspecao.")
                except Exception as e:
                    print(f"Failed to dump debug json: {e}")
                is_first = False
                
            title = item.get("title") or item.get("jobTitle") or "Unknown"
            url = item.get("url", "")
            description = item.get("description") or item.get("snippet", "")
            
            client_country = item.get("clientLocation", "")
            if not client_country and isinstance(item.get("client"), dict):
                client_country = item.get("client", {}).get("country", "")
                
            raw_budget = str(item.get("budget", "0")).replace("$", "").replace(",", "").replace("k", "000").strip()
            budget_val = float(raw_budget) if raw_budget.replace(".", "", 1).isdigit() else None
            
            posted_dt = None
            if item.get("absoluteDate"):
                try:
                    posted_dt = datetime.fromisoformat(item.get("absoluteDate").replace("Z", "+00:00"))
                except:
                    pass
                    
            raw_jobs.append(RawJob(
                platform="upwork",
                external_id=str(item.get("id", item.get("jobId", url))),
                title=title,
                description=description[:800],
                url=url,
                posted_at=posted_dt,
                budget_min=budget_val,
                budget_max=budget_val,
                hourly=(item.get("jobType", "") == "Hourly"),
                skills=item.get("tags", []) if isinstance(item.get("tags"), list) else [],
                client_country=client_country,
                client_total_spent=float(item.get("clientTotalSpent", 0)) if item.get("clientTotalSpent") else None,
                client_rating=float(item.get("clientRating", 0)) if item.get("clientRating") else None,
                client_total_hires=1 if item.get("hasHired") else 0,
                proposals=item.get("proposals", 0) if isinstance(item.get("proposals"), int) else 0
            ))
            
    except Exception as e:
        print(f"Apify Client Error: {e}")
        
    return raw_jobs
