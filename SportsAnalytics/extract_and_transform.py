import pandas as pd
from config import *
from utils import api_get

# Fetch rankings for specified seasons and weeks
def fetch_rankings(seasons=SEASONS, weeks=WEEKS):
    all_rows = []
    for season in seasons:
        for week in weeks:
            url = RANKINGS_URL.format(season=season, week=week)
            data = api_get(url, HEADERS)
            if not data:
                continue
            poll_id = data.get("poll", {}).get("id")
            poll_name = data.get("poll", {}).get("name")
            effective_time = data.get("effective_time")
            rankings = data.get("rankings", [])
            for r in rankings:
                team = r.get("team", {})
                all_rows.append({
                    "poll_id": poll_id,
                    "poll_name": poll_name,
                    "season_year": season,
                    "week": week,
                    "effective_time": effective_time,
                    "team_id": team.get("id"),
                    "rank": r.get("rank"),
                    "prev_rank": r.get("prev_rank"),
                    "points": r.get("points"),
                    "fp_votes": r.get("fp_votes"),
                    "wins": r.get("wins"),
                    "losses": r.get("losses"),
                    "ties": r.get("ties")
                })
    return pd.DataFrame(all_rows)

# Fetch all teams information
def fetch_teams():
    data = api_get(TEAM_URL, HEADERS)
    teams = data.get("teams", [])
    return pd.DataFrame(teams)

# Fetch team roster and related information
def fetch_team_roster(team_id):
    roster_data = api_get(TEAM_ROSTER_URL.format(team_id=team_id), headers=HEADERS)
    if not roster_data:
        return (pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame())

    # -------- Team Info --------
    df_team = pd.DataFrame([{
        "team_id": roster_data.get("id"),
        "market": roster_data.get("market"),
        "team_name": roster_data.get("name"),
        "alias": roster_data.get("alias"),
        "founded": roster_data.get("founded"),
        "mascot": roster_data.get("mascot"),
        "fight_song": roster_data.get("fight_song"),
        "championships_won": roster_data.get("championships_won"),
        "conference_id": roster_data.get("conference", {}).get("id"),
        "division_id": roster_data.get("division", {}).get("id"),
        "venue_id": roster_data.get("venue", {}).get("id")
    }])

    # -------- Venue Info --------
    venue = roster_data.get("venue", {})
    df_venue = pd.DataFrame([{
        "venue_id": venue.get("id"),
        "name": venue.get("name"),
        "city": venue.get("city"),
        "state": venue.get("state"),
        "country": venue.get("country"),
        "zip": venue.get("zip"),
        "address": venue.get("address"),
        "capacity": venue.get("capacity"),
        "surface": venue.get("surface"),
        "roof_type": venue.get("roof_type"),
        "latitude": venue.get("location", {}).get("lat"),
        "longitude": venue.get("location", {}).get("lng")
    }]) if venue else pd.DataFrame()

    # -------- Division Info --------
    division = roster_data.get("division", {})
    df_division = pd.DataFrame([{
        "division_id": division.get("id"),
        "name": division.get("name"),
        "alias": division.get("alias")
    }]) if division else pd.DataFrame()

    # -------- Conference Info --------
    conference = roster_data.get("conference", {})
    df_conference = pd.DataFrame([{
        "conference_id": conference.get("id"),
        "name": conference.get("name"),
        "alias": conference.get("alias")
    }]) if conference else pd.DataFrame()

    # -------- Coaches Info --------
    coaches_list = []
    for coach in roster_data.get("coaches", []):
        coaches_list.append({
            "coach_id": coach.get("id"),
            "first_name": coach.get("first_name"),
            "last_name": coach.get("last_name"),
            "position": coach.get("position"),
            "team_id": roster_data.get("id")
        })
    df_coaches = pd.DataFrame(coaches_list)

    # -------- Players Info --------
    players_list = []
    for player in roster_data.get("players", []):
        players_list.append({
            "player_id": player.get("id"),
            "first_name": player.get("first_name"),
            "last_name": player.get("last_name"),
            "abbr_name": player.get("abbr_name"),
            "birth_place": player.get("birth_place"),
            "position": player.get("position"),
            "height": player.get("height"),
            "weight": player.get("weight"),
            "status": player.get("status"),
            "eligibility": player.get("eligibility"),
            "team_id": roster_data.get("id")
        })
    df_players = pd.DataFrame(players_list)

    return df_team, df_players, df_coaches, df_venue, df_division, df_conference

# Fetch seasons information
def fetch_seasons():
    data = api_get(SEASONS_URL, headers=HEADERS)
    if not data:
        return pd.DataFrame()  # return empty DataFrame if failed

    seasons_list = []
    for season in data.get("seasons", []):
        seasons_list.append({
            "season_id": season.get("id"),
            "year": season.get("year"),
            "start_date": season.get("start_date"),
            "end_date": season.get("end_date"),
            "status": season.get("status"),
            "type_code": season.get("type", {}).get("code")
        })

    return pd.DataFrame(seasons_list)


# Fetch player statistics for a given team and season
def fetch_player_stats(team_id, season):
    url = SEASON_STATISTICS_URL.format(team_id=team_id, season=season)
    data = api_get(url, headers=HEADERS)
    if not data:
        return pd.DataFrame()  # return empty if failed

    rows = []
    for player in data.get("players", []):
        rushing = player.get("rushing", {})
        receiving = player.get("receiving", {})
        kick_returns = player.get("kick_returns", {})
        fumbles = player.get("fumbles", {})

        rows.append({
            "player_id": player.get("id"),
            "team_id": team_id,
            "season_id": data.get("season", {}).get("id"),
            "games_played": player.get("games_played", 0),
            "games_started": player.get("games_started", 0),
            "rushing_yards": rushing.get("yards", 0),
            "rushing_touchdowns": rushing.get("touchdowns", 0),
            "receiving_yards": receiving.get("yards", 0),
            "receiving_touchdowns": receiving.get("touchdowns", 0),
            "kick_return_yards": kick_returns.get("yards", 0),
            "fumbles": fumbles.get("fumbles", 0)
        })

    return pd.DataFrame(rows)

