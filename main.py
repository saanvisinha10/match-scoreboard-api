from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from schemas import ScoreboardRequest, MatchScoreboardResponse
from services import calculate_scoreboard

app = FastAPI(
    title="Match Scoreboard API - Phase 2",
    description="Live Match Scoreboard & Cricket Microservice accepting real-time dynamic ball stream payloads.",
    version="2.0.0"
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
    return {"message": "Phase 2 Match Scoreboard API is live"}

@app.get("/health", tags=["Health Check"])
def health():
    return {"status": "ok"}

@app.post("/scoreboard", response_model=MatchScoreboardResponse, tags=["Scoreboard"])
def get_match_scoreboard(payload: ScoreboardRequest):
    try:
        return calculate_scoreboard(payload)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
