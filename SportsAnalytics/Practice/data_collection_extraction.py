#----------------------------
# Import necessary libraries
#----------------------------

import pandas as pd
import requests
import time
from sqlalchemy import create_engine


#---------------
# Configuration
#---------------

API_KEY = "your_API_KEY"  # Replace with your actual API key
ENGINE = create_engine('postgresql+psycopg2://username:password@localhost:5432/your_database') # Update with your actual database credentials

RANKINGS_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/polls/AP25/{season}/{week}/rankings.json"
TEAM_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/league/teams.json"
TEAM_ROSTER_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/teams/{team_id}/full_roster.json"
SEASONS_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/league/seasons.json"
SEASON_STATISTICS_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/seasons/{season}/REG/teams/{team_id}/statistics.json"

HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

SEASONS = [2024, 2025]
WEEKS = [f"{week:02d}" for week in range(1, 22)]  # 01 → 21


#-------------------------------------------------------------------------------
# RANKINGS DATA EXTRACTION
# Collect RANKINGS DATA for multiple seasons(2024 & 2025) and weeks (1 to 21)
#-------------------------------------------------------------------------------

all_rankings = []

for season in SEASONS:
    for week in WEEKS:
        url = RANKINGS_URL.format(season=season, week=week)
        print(f"Fetching rankings: season={season}, week={week}")

        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            all_rankings.append(response.json())
        else:
            print(
                f"Skipped season={season}, week={week} "
                f"(status={response.status_code})"
            )

        time.sleep(0.5)  # avoid rate limiting


# Process all rankings data into a list of dictionaries
all_rows = []

for rankings_data in all_rankings:  # Loop over all JSON responses
    poll_id = rankings_data.get("poll", {}).get("id")
    poll_name = rankings_data.get("poll", {}).get("name")
    season = rankings_data.get("season")
    week = rankings_data.get("week")
    effective_time = rankings_data.get("effective_time")

    rankings = rankings_data.get("rankings", [])

    for ranking in rankings:
        team = ranking.get("team", {})  # Extract nested team info

        ranking_info = {
            "poll_id": poll_id,
            "poll_name": poll_name,
            "season_year": season,
            "week": week,
            "effective_time": effective_time,
            "team_id": team.get("id"),
            "rank": ranking.get("rank"),
            "prev_rank": ranking.get("prev_rank"),
            "points": ranking.get("points"),
            "fp_votes": ranking.get("fp_votes"),
            "wins": ranking.get("wins"),
            "losses": ranking.get("losses"),
            "ties": ranking.get("ties")
        }

        all_rows.append(ranking_info)

# Convert all rows to a DataFrame
df_rankings = pd.DataFrame(all_rows)


#---------------------------------------------------------------
# TEAMS DATA EXTRACTION
# Import and extract TEAMS DATA from API, creating a DataFrame
#---------------------------------------------------------------

response = requests.get(TEAM_URL, headers=HEADERS)
teams_data = response.json()
teams = teams_data.get("teams",[])
df_teams = pd.DataFrame(teams)


#-----------------------------------------------------------------------------------------------------
# TEAM ROSTER, COACHES, PLAYERS, VENUES, DIVISIONS, CONFERENCES DATA EXTRACTION
# Import and Extract Team Roster, Coaches, Players, Venues, Divisions, and Conferences data from API
#-----------------------------------------------------------------------------------------------------
# Session setup
session = requests.Session()
session.headers.update({
    "accept": "application/json",
    "x-api-key": API_KEY
})

# Function to Extract team roster with retry logic
def extract_team_roster(team_id, session, max_retries=5):
    url = TEAM_ROSTER_URL.format(team_id=team_id)

    for attempt in range(max_retries):
        response = session.get(url,timeout=15)

        # Handling API Rate Limit (429 Error)
        if response.status_code == 429:
            wait = 2 ** attempt
            print(f"429 for team {team_id}. Sleeping {wait}s...")
            time.sleep(wait)
            continue

        # Team not found (404 Error)
        if response.status_code == 404:
            print(f"Team {team_id} not found. Skipping.")
            return None

        response.raise_for_status()
        time.sleep(1)  
        return response.json()

    print(f"Skipped team {team_id} after retries")
    return None

# Storage structures
teams_list = []
coaches_list = []
players_list = []

venues_dict = {}
divisions_dict = {}
conferences_dict = {}

processed_teams = set()

# Data Extraction Loop for all teams
for team_id in df_teams["id"]:
    if team_id in processed_teams:
        continue

    roster_data = extract_team_roster(team_id, session)
    if not roster_data:
        continue

    processed_teams.add(team_id)

    # Team List
    teams_list.append({
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
    })

    # Venue Details
    venue = roster_data.get("venue")
    if venue and venue.get("id") not in venues_dict:
        venues_dict[venue["id"]] = {
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
        }

    # Division Details
    division = roster_data.get("division")
    if division and division.get("id") not in divisions_dict:
        divisions_dict[division["id"]] = {
            "division_id": division.get("id"),
            "name": division.get("name"),
            "alias": division.get("alias")
        }

    # Conference Details
    conference = roster_data.get("conference")
    if conference and conference.get("id") not in conferences_dict:
        conferences_dict[conference["id"]] = {
            "conference_id": conference.get("id"),
            "name": conference.get("name"),
            "alias": conference.get("alias")
        }

    # Coaches List
    for coach in roster_data.get("coaches", []):
        coaches_list.append({
            "coach_id": coach.get("id"),
            "first_name": coach.get("first_name"),
            "last_name": coach.get("last_name"),
            "position": coach.get("position"),
            "team_id": team_id
        })

    # Players List
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
            "team_id": team_id
        })

# Create DataFrames
df_teams_roster = pd.DataFrame(teams_list)
df_venues = pd.DataFrame(venues_dict.values())
df_divisions = pd.DataFrame(divisions_dict.values())
df_conferences = pd.DataFrame(conferences_dict.values())
df_coaches = pd.DataFrame(coaches_list)
df_players = pd.DataFrame(players_list)


#-----------------------------------------------------------------
# SEASONS DATA EXTRACTION
# Import and extract SEASONS DATA from API, creating a DataFrame
#-----------------------------------------------------------------
response = requests.get(SEASONS_URL, headers=HEADERS)

seasons_data = response.json()
seasons_list =[]

seasons = seasons_data.get("seasons", [])
for season in seasons:
    season_info = {
        "season_id": season.get("id"),
        "year": season.get("year"),
        "start_date": season.get("start_date"),
        "end_date": season.get("end_date"),
        "status": season.get("status"),
        "type_code": season.get("type",{}).get("code")    
    }
    seasons_list.append(season_info)
df_seasons = pd.DataFrame(seasons_list)


#----------------------------------------------------------------------------
# PLAYERS SEASON STATISTICS DATA EXTRACTION
# Import and Extract Team Season Statistics for specified seasons(2024,2025)
#----------------------------------------------------------------------------

# Function to fetch team season statistics with retry logic
def fetch_team_season_stats(team_id, season, max_retries=5):
    url = SEASON_STATISTICS_URL.format(season=season, team_id=team_id)

    for attempt in range(max_retries):
        response = requests.get(url, headers=HEADERS)

        if response.status_code == 200:
            return response.json()

        elif response.status_code == 429:
            wait = 2 ** attempt
            print(f"429 sleeping {wait}s (team={team_id}, season={season})")
            time.sleep(wait)

        else:
            print(f"Error {response.status_code} for team {team_id}, season {season}")
            return None

    print(f"Max retries exceeded for team {team_id}, season {season}")
    return None


def extract_player_season_stats(team_json):
    team_id = team_json.get("id")
    season_id = team_json.get("season", {}).get("id")

    rows = []

    for player in team_json.get("players", []):
        rushing = player.get("rushing", {})
        receiving = player.get("receiving", {})
        kick_returns = player.get("kick_returns", {})
        fumbles = player.get("fumbles", {})

        rows.append({
            "player_id": player.get("id"),
            "team_id": team_id,
            "season_id": season_id,
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

all_player_stats = []

for season in SEASONS:
    for team_id in df_teams["id"]:
        print(f"Fetching team={team_id}, season={season}")

        team_json = fetch_team_season_stats(team_id, season)

        if team_json:
            df = extract_player_season_stats(team_json)
            all_player_stats.append(df)

        time.sleep(0.4)

df_player_stats = pd.concat(all_player_stats, ignore_index=True)
print(df_player_stats.shape)


#---------------------------------
# SAVE DATAFRAMES TO CSV FILES
#---------------------------------

df_rankings.to_csv("data/rankings_latest.csv", index=False)
df_teams.to_csv("data/teams.csv", index=False)
df_teams_roster.to_csv("data/team_roster.csv", index=False)
df_venues.to_csv("data/venues.csv", index=False)
df_divisions.to_csv("data/divisions.csv", index=False)
df_conferences.to_csv("data/conferences.csv", index=False)
df_coaches.to_csv("data/coaches.csv", index=False)
df_players.to_csv("data/players.csv", index=False)
df_seasons.to_csv("data/seasons.csv", index=False)
df_player_stats.to_csv("data/player_statistics.csv", index=False)


#---------------------------------------
# SAVE DATAFRAMES TO POSTGRESQL DATABASE
#---------------------------------------
df_venues.to_sql('venues', con=ENGINE, if_exists='append', index=False, method='multi')
df_conferences.to_sql('conferences', con=ENGINE, if_exists='append', index=False, method='multi')
df_divisions.to_sql('divisions', con=ENGINE, if_exists='append', index=False, method='multi')
df_teams_roster.to_sql('teams', con=ENGINE, if_exists='append', index=False, method='multi')
df_coaches.to_sql('coaches', con=ENGINE, if_exists='append', index=False, method='multi')
df_players.to_sql('players', con=ENGINE, if_exists='append', index=False, method='multi')
df_rankings.to_sql('rankings', con=ENGINE, if_exists='append', index=False, method='multi')
df_seasons.to_sql('seasons', con=ENGINE, if_exists='append', index=False, method='multi')
df_player_stats.to_sql('player_statistics', con=ENGINE, if_exists='append', index=False, method='multi')