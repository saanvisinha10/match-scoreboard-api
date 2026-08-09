from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import MatchScoreboardResponse
from services import calculate_scoreboard

app = FastAPI(
    title="Sports Utility API",
    description="Live Match Scoreboard & Cricket Microservice",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["Health Check"])
def root():
    return {"message": "API is live"}

@app.get("/health", tags=["Health Check"])
def health():
    return {"status": "ok"}

@app.get("/scoreboard/{match_id}", response_model=MatchScoreboardResponse, tags=["Scoreboard"])
def get_match_scoreboard(match_id: str):
    result = calculate_scoreboard(match_id)
    if not result:
        raise HTTPException(status_code=404, detail=f"Match '{match_id}' not found.")
    return result
