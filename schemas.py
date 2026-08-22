from pydantic import BaseModel, Field
from typing import Optional, List

class BallEventInput(BaseModel):
    over_ball: str = Field(..., description="Over and ball delivery number, e.g., '0.1'")
    striker: str = Field(..., description="Name of the facing batter")
    bowler: str = Field(..., description="Name of the bowler")
    runs: int = Field(..., ge=0, description="Runs scored off the bat")
    is_wicket: bool = Field(default=False, description="Whether a dismissal occurred")

class ScoreboardRequest(BaseModel):
    match_id: str = Field(..., description="Unique match identifier")
    venue: str = Field(..., description="Match venue location")
    batting_team: str = Field(..., description="Name of the batting team")
    bowling_team: str = Field(..., description="Name of the bowling team")
    has_active_innings: bool = Field(default=True, description="State of the active innings")
    innings_number: Optional[int] = Field(default=1, description="Current innings number")
    ball_events: List[BallEventInput] = Field(default_factory=list, description="Array of delivery logs")

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
