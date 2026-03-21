from pydantic import BaseModel, HttpUrl
from typing import List, Optional
from datetime import datetime

class RawJob(BaseModel):
    platform: str
    external_id: str
    title: str
    description: str
    url: str
    posted_at: datetime
    
    # Optional fields depending on platform
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    hourly: Optional[bool] = None
    category: Optional[str] = None
    skills: List[str] = []
    
    # Client info
    client_external_id: Optional[str] = None
    client_country: Optional[str] = None
    client_rating: Optional[float] = None
    client_payment_verified: Optional[bool] = None
    client_total_spent: Optional[float] = None
    client_total_hires: Optional[int] = None
    
    # Stats
    proposals: Optional[int] = None
