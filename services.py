from typing import Dict, Any, Optional

# Mock database simulating Khel AI match and ball-event relations
MOCK_DATABASE: Dict[str, Dict[str, Any]] = {
    "match_101": {
        "venue": "M. Chinnaswamy Stadium, Bengaluru",
        "batting_team": "Royal Challengers Bengaluru",
        "bowling_team": "Chennai Super Kings",
        "has_active_innings": True,
        "innings_number": 1,
        "ball_events": [
            {"over_ball": "0.1", "striker": "Virat Kohli", "bowler": "Deepak Chahar", "runs": 4, "is_wicket": False},
            {"over_ball": "0.2", "striker": "Virat Kohli", "bowler": "Deepak Chahar", "runs": 1, "is_wicket": False},
            {"over_ball": "0.3", "striker": "Faf du Plessis", "bowler": "Deepak Chahar", "runs": 0, "is_wicket": False},
            {"over_ball": "0.4", "striker": "Faf du Plessis", "bowler": "Deepak Chahar", "runs": 6, "is_wicket": False},
            {"over_ball": "0.5", "striker": "Faf du Plessis", "bowler": "Deepak Chahar", "runs": 0, "is_wicket": True},
            {"over_ball": "0.6", "striker": "Rajat Patidar", "bowler": "Deepak Chahar", "runs": 1, "is_wicket": False},
            {"over_ball": "1.1", "striker": "Virat Kohli", "bowler": "Maheesh Theekshana", "runs": 6, "is_wicket": False},
            {"over_ball": "1.2", "striker": "Virat Kohli", "bowler": "Maheesh Theekshana", "runs": 2, "is_wicket": False},
        ]
    },
    "match_102": {
        "venue": "Wankhede Stadium, Mumbai",
        "batting_team": "Mumbai Indians",
        "bowling_team": "Kolkata Knight Riders",
        "has_active_innings": False,
        "innings_number": None,
        "ball_events": []
    }
}

def calculate_scoreboard(match_id: str) -> Optional[Dict[str, Any]]:
    match_data = MOCK_DATABASE.get(match_id)
    if not match_data:
        return None

    # Handle edge case: Match exists but no active innings created
    if not match_data["has_active_innings"] or not match_data["ball_events"]:
        return {
            "match_id": match_id,
            "venue": match_data["venue"],
            "has_active_innings": False,
            "status_message": "Match created, but no innings has started yet.",
            "innings_number": None,
            "batting_team": match_data["batting_team"],
            "bowling_team": match_data["bowling_team"],
            "score": 0,
            "wickets": 0,
            "overs": 0.0,
            "run_rate": 0.0,
            "top_batter": None,
            "top_bowler": None,
            "recent_balls": []
        }

    events = match_data["ball_events"]
    total_runs = sum(b["runs"] for b in events)
    total_wickets = sum(1 for b in events if b["is_wicket"])
    total_legal_balls = len(events)
    
    overs_completed = total_legal_balls // 6
    remaining_balls = total_legal_balls % 6
    overs_formatted = float(f"{overs_completed}.{remaining_balls}")
    
    total_overs_decimal = total_legal_balls / 6.0
    run_rate = round(total_runs / total_overs_decimal, 2) if total_overs_decimal > 0 else 0.0

    # Top Batter Calculation
    batters = {}
    for b in events:
        striker = b["striker"]
        if striker not in batters:
            batters[striker] = {"runs": 0, "balls": 0}
        batters[striker]["runs"] += b["runs"]
        batters[striker]["balls"] += 1

    top_batter_name = max(batters, key=lambda k: batters[k]["runs"]) if batters else None
    top_batter_info = None
    if top_batter_name:
        b_data = batters[top_batter_name]
        sr = round((b_data["runs"] / b_data["balls"]) * 100, 2) if b_data["balls"] > 0 else 0.0
        top_batter_info = {
            "name": top_batter_name,
            "runs": b_data["runs"],
            "balls": b_data["balls"],
            "strike_rate": sr
        }

    # Top Bowler Calculation
    bowlers = {}
    for b in events:
        bowler = b["bowler"]
        if bowler not in bowlers:
            bowlers[bowler] = {"runs": 0, "balls": 0, "wickets": 0}
        bowlers[bowler]["runs"] += b["runs"]
        bowlers[bowler]["balls"] += 1
        if b["is_wicket"]:
            bowlers[bowler]["wickets"] += 1

    top_bowler_name = max(bowlers, key=lambda k: (bowlers[k]["wickets"], -bowlers[k]["runs"])) if bowlers else None
    top_bowler_info = None
    if top_bowler_name:
        bw_data = bowlers[top_bowler_name]
        bw_overs_dec = bw_data["balls"] / 6.0
        econ = round(bw_data["runs"] / bw_overs_dec, 2) if bw_overs_dec > 0 else 0.0
        bw_overs_formatted = float(f"{bw_data['balls'] // 6}.{bw_data['balls'] % 6}")
        top_bowler_info = {
            "name": top_bowler_name,
            "overs": bw_overs_formatted,
            "runs_conceded": bw_data["runs"],
            "wickets": bw_data["wickets"],
            "economy": econ
        }

    recent_balls = [f"{b['over_ball']} - {b['runs']} runs" + (" (W)" if b["is_wicket"] else "") for b in events[-6:]]

    return {
        "match_id": match_id,
        "venue": match_data["venue"],
        "has_active_innings": True,
        "status_message": "Live innings in progress",
        "innings_number": match_data["innings_number"],
        "batting_team": match_data["batting_team"],
        "bowling_team": match_data["bowling_team"],
        "score": total_runs,
        "wickets": total_wickets,
        "overs": overs_formatted,
        "run_rate": run_rate,
        "top_batter": top_batter_info,
        "top_bowler": top_bowler_info,
        "recent_balls": recent_balls
    }
