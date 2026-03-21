import feedparser
from typing import List
from scraper.models import RawJob
from scraper.parser import parse_upwork_rss

# Example dummy URLs, real ones should come from config
UPWORK_RSS_URLS = [
    "https://www.upwork.com/ab/feed/jobs/rss?q=python",
]

def fetch_upwork_rss() -> List[RawJob]:
    parsed_jobs = []
    for url in UPWORK_RSS_URLS:
        feed = feedparser.parse(url)
        for entry in feed.entries:
            try:
                job = parse_upwork_rss(entry)
                parsed_jobs.append(job)
            except Exception as e:
                print(f"Error parsing RSS entry: {e}")
    return parsed_jobs
