from datetime import datetime
from typing import Optional, List, Dict, Any
from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy import Column
from sqlalchemy.dialects.postgresql import JSONB

# Platforms
class Platform(SQLModel, table=True):
    __tablename__ = "platforms"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    base_url: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    clients: List["Client"] = Relationship(back_populates="platform")
    jobs: List["Job"] = Relationship(back_populates="platform")

# Clients
class Client(SQLModel, table=True):
    __tablename__ = "clients"
    id: Optional[int] = Field(default=None, primary_key=True)
    platform_id: Optional[int] = Field(default=None, foreign_key="platforms.id")
    external_id: Optional[str] = None
    country: Optional[str] = None
    rating: Optional[float] = None
    payment_verified: Optional[bool] = None
    total_spent: Optional[float] = None
    total_hires: Optional[int] = None
    avg_hourly_rate: Optional[float] = None
    jobs_posted: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    platform: Optional[Platform] = Relationship(back_populates="clients")
    jobs: List["Job"] = Relationship(back_populates="client")
    stats: List["ClientStat"] = Relationship(back_populates="client")

# Skills
class Skill(SQLModel, table=True):
    __tablename__ = "skills"
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(unique=True, index=True)

    job_links: List["JobSkillLink"] = Relationship(back_populates="skill")
    trends: List["SkillTrend"] = Relationship(back_populates="skill")

# Job-Skill Many-to-Many
class JobSkillLink(SQLModel, table=True):
    __tablename__ = "job_skills"
    job_id: Optional[int] = Field(default=None, foreign_key="jobs.id", primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skills.id", primary_key=True)

    job: "Job" = Relationship(back_populates="skill_links")
    skill: "Skill" = Relationship(back_populates="job_links")

# Jobs
class Job(SQLModel, table=True):
    __tablename__ = "jobs"
    id: Optional[int] = Field(default=None, primary_key=True)
    platform_id: Optional[int] = Field(default=None, foreign_key="platforms.id", index=True)
    client_id: Optional[int] = Field(default=None, foreign_key="clients.id", index=True)
    external_id: Optional[str] = None
    title: str
    description: str
    category: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    hourly: Optional[bool] = None
    proposals: Optional[int] = None
    experience_level: Optional[str] = None
    duration: Optional[str] = None
    posted_at: Optional[datetime] = Field(default=None, index=True)
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
    url: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

    platform: Optional[Platform] = Relationship(back_populates="jobs")
    client: Optional[Client] = Relationship(back_populates="jobs")
    skill_links: List[JobSkillLink] = Relationship(back_populates="job")
    scores: List["JobScore"] = Relationship(back_populates="job")
    analysis_results: List["AnalysisResult"] = Relationship(back_populates="job")
    stats: List["JobStat"] = Relationship(back_populates="job")

# Job Stats
class JobStat(SQLModel, table=True):
    __tablename__ = "job_stats"
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="jobs.id")
    proposals: Optional[int] = None
    views: Optional[int] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

    job: Optional[Job] = Relationship(back_populates="stats")

# Client Stats
class ClientStat(SQLModel, table=True):
    __tablename__ = "client_stats"
    id: Optional[int] = Field(default=None, primary_key=True)
    client_id: Optional[int] = Field(default=None, foreign_key="clients.id")
    total_spent: Optional[float] = None
    total_hires: Optional[int] = None
    avg_hourly: Optional[float] = None
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

    client: Optional[Client] = Relationship(back_populates="stats")

# Job Scores
class JobScore(SQLModel, table=True):
    __tablename__ = "job_scores"
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="jobs.id")
    budget_score: Optional[float] = None
    client_score: Optional[float] = None
    competition_score: Optional[float] = None
    skill_match_score: Optional[float] = None
    final_score: Optional[float] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    job: Optional[Job] = Relationship(back_populates="scores")

# Skill Trends
class SkillTrend(SQLModel, table=True):
    __tablename__ = "skill_trends"
    id: Optional[int] = Field(default=None, primary_key=True)
    skill_id: Optional[int] = Field(default=None, foreign_key="skills.id")
    date: Optional[datetime] = Field(default=None, index=True)
    job_count: Optional[int] = None
    avg_budget: Optional[float] = None
    trend_score: Optional[float] = None

    skill: Optional[Skill] = Relationship(back_populates="trends")

# Analysis Results
class AnalysisResult(SQLModel, table=True):
    __tablename__ = "analysis_results"
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="jobs.id")
    analysis_type: Optional[str] = None
    result: Dict[str, Any] = Field(default_factory=dict, sa_column=Column(JSONB))
    created_at: datetime = Field(default_factory=datetime.utcnow)

    job: Optional[Job] = Relationship(back_populates="analysis_results")

# Scrape Logs
class ScrapeLog(SQLModel, table=True):
    __tablename__ = "scrape_logs"
    id: Optional[int] = Field(default=None, primary_key=True)
    source: Optional[str] = None
    status: Optional[str] = None
    message: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Proposals (Future)
class Proposal(SQLModel, table=True):
    __tablename__ = "proposals"
    id: Optional[int] = Field(default=None, primary_key=True)
    job_id: Optional[int] = Field(default=None, foreign_key="jobs.id")
    freelancer_country: Optional[str] = None
    rate: Optional[float] = None
    cover_letter: Optional[str] = None
    hired: Optional[bool] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Freelancers (Future)
class Freelancer(SQLModel, table=True):
    __tablename__ = "freelancers"
    id: Optional[int] = Field(default=None, primary_key=True)
    platform_id: Optional[int] = Field(default=None, foreign_key="platforms.id")
    country: Optional[str] = None
    hourly_rate: Optional[float] = None
    success_rate: Optional[float] = None
    total_earned: Optional[float] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
