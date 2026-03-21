import requests
from typing import List
from scraper.models import RawJob
from datetime import datetime

def fetch_remoteok_jobs(query: str = "python") -> List[RawJob]:
    """
    RemoteOK has a public JSON API, allowing resilient aggregation without scraping HTML.
    """
    url = f"https://remoteok.com/api?tag={query}"
    headers = {"User-Agent": "FreelancerAnalyzerBot"}
    raw_jobs = []
    
    try:
        resp = requests.get(url, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            # First element is usually a legal disclaimer on RemoteOK API, subsequent items are jobs
            if len(data) > 1:
                for item in data[1:]:
                    raw_jobs.append(RawJob(
                        platform="remoteok",
                        external_id=str(item.get("id")),
                        title=item.get("position", "Unknown"),
                        description=item.get("description", ""),
                        url=item.get("url", ""),
                        posted_at=datetime.fromisoformat(item.get("date").replace("Z", "+00:00")) if item.get("date") else datetime.utcnow(),
                        budget_max=float(item.get("salary_max", 0)) if item.get("salary_max") else None,
                        budget_min=float(item.get("salary_min", 0)) if item.get("salary_min") else None,
                        client_country=item.get("location", "")
                    ))
    except Exception as e:
        print(f"RemoteOK API Error: {e}")
        
    return raw_jobs
