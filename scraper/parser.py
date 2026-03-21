from scraper.models import RawJob
from bs4 import BeautifulSoup
from datetime import datetime
import re

def parse_upwork_rss(entry: dict) -> RawJob:
    title = entry.get("title", "Unknown")
    link = entry.get("link", "")
    published = entry.get("published_parsed")
    posted_at = datetime(*published[:6]) if published else datetime.utcnow()
    
    description_html = entry.get("summary", "") or entry.get("description", "")
    
    budget_min = None
    budget_max = None
    hourly = None
    category = None
    skills = []
    client_country = None

    if description_html:
        soup = BeautifulSoup(description_html, "html.parser")
        text = soup.get_text()
        
        budget_match = re.search(r'Budget\s*:\s*\$?([\d,]+(?:\.\d{2})?)', text, re.IGNORECASE)
        if budget_match:
            val = budget_match.group(1).replace(",", "")
            budget_max = float(val)
            budget_min = float(val)
            hourly = False
            
        hourly_match = re.search(r'Hourly Range\s*:\s*\$?([\d,.]+)\s*-\s*\$?([\d,.]+)', text, re.IGNORECASE)
        if hourly_match:
            budget_min = float(hourly_match.group(1).replace(",", ""))
            budget_max = float(hourly_match.group(2).replace(",", ""))
            hourly = True
            
        category_match = re.search(r'Category\s*:\s*([^\n]+)', text, re.IGNORECASE)
        if category_match:
            category = category_match.group(1).strip()
            
        country_match = re.search(r'Country\s*:\s*([^\n]+)', text, re.IGNORECASE)
        if country_match:
            client_country = country_match.group(1).strip()
            
        skills_match = re.search(r'Skills\s*:\s*([^\n]+)', text, re.IGNORECASE)
        if skills_match:
            skills_raw = skills_match.group(1).strip()
            skills = [s.strip() for s in skills_raw.split(',') if s.strip()]
            
        description_text = text
    else:
        description_text = ""

    return RawJob(
        platform="upwork",
        external_id=entry.get("id", link),
        title=title,
        description=description_text,
        url=link,
        posted_at=posted_at,
        budget_min=budget_min,
        budget_max=budget_max,
        hourly=hourly,
        category=category,
        skills=skills,
        client_country=client_country
    )
