from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.routes_jobs import router as jobs_router

app = FastAPI(title="Freelancer Analyzer API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(jobs_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "freelancer-analyzer"}
