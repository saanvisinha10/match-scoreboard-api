from pydantic import BaseModel
from typing import Optional, List

class BallEvent(BaseModel):
    over_ball: str          # e.g. "12.4"
    striker: str
    bowler: str
    runs: int
    is_wicket: bool = False

class TopBatter(BaseModel):
    name: str
    runs: int
    balls: int
    strike_rate: float

class TopBowler(BaseModel):
    name: str
    overs: float
    runs_conceded: int
    wickets: int
    economy: float

class MatchScoreboardResponse(BaseModel):
    match_id: str
    venue: str
    has_active_innings: bool
    status_message: str
    innings_number: Optional[int] = None
    batting_team: Optional[str] = None
    bowling_team: Optional[str] = None
    score: Optional[int] = None
    wickets: Optional[int] = None
    overs: Optional[float] = None
    run_rate: Optional[float] = None
    top_batter: Optional[TopBatter] = None
    top_bowler: Optional[TopBowler] = None
    recent_balls: List[str] = []
