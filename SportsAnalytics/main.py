# main.py
import pandas as pd
from extract_and_transform import (
    fetch_rankings,
    fetch_teams,
    fetch_team_roster,
    fetch_seasons,
    fetch_player_stats
)
from load import (
    save_to_csv, 
    save_to_postgres
)
from config import ENGINE  # SQLAlchemy engine

# ------------------------------
# 1. Rankings
# ------------------------------
print("Fetching Rankings...")
df_rankings = fetch_rankings()
save_to_csv(df_rankings, "rankings.csv")
save_to_postgres(df_rankings, "rankings", ENGINE)
print(f"Rankings saved: {df_rankings.shape[0]} rows")

# ------------------------------
# 2. Teams
# ------------------------------
print("Fetching Teams...")
# Assuming fetch_teams returns a DataFrame
df_teams = fetch_teams()  
save_to_csv(df_teams, "teams.csv")
save_to_postgres(df_teams, "teams", ENGINE)
print(f"Teams saved: {df_teams.shape[0]} rows")

# ------------------------------
# 3. Team Rosters
# ------------------------------
all_teams = []
all_players = []
all_coaches = []
all_venues = []
all_divisions = []
all_conferences = []

for team_id in df_teams["id"]:
    (
        df_team,
        df_players,
        df_coaches,
        df_venues,
        df_divisions,
        df_conferences
    ) = fetch_team_roster(team_id)
    
    if not df_team.empty:
        all_teams.append(df_team)
    if not df_players.empty:
        all_players.append(df_players)
    if not df_coaches.empty:
        all_coaches.append(df_coaches)
    if not df_venues.empty:
        all_venues.append(df_venues)
    if not df_divisions.empty:
        all_divisions.append(df_divisions)
    if not df_conferences.empty:
        all_conferences.append(df_conferences)

# Concatenate all DataFrames into final ones
df_teams_roster = pd.concat(all_teams, ignore_index=True)
df_players = pd.concat(all_players, ignore_index=True)
df_coaches = pd.concat(all_coaches, ignore_index=True)
df_venues = pd.concat(all_venues, ignore_index=True)
df_divisions = pd.concat(all_divisions, ignore_index=True)
df_conferences = pd.concat(all_conferences, ignore_index=True)

save_to_csv(df_teams_roster, "team_roster.csv")
save_to_csv(df_players, "players.csv")
save_to_csv(df_coaches, "coaches.csv")
save_to_csv(df_venues, "venues.csv")
save_to_csv(df_divisions, "divisions.csv")
save_to_csv(df_conferences, "conferences.csv")

save_to_postgres(df_venues, "venues", ENGINE)
save_to_postgres(df_divisions, "divisions", ENGINE)
save_to_postgres(df_conferences, "conferences", ENGINE)
save_to_postgres(df_teams_roster, "teams", ENGINE)
save_to_postgres(df_players, "players", ENGINE)
save_to_postgres(df_coaches, "coaches", ENGINE)

print("Team roster, players, coaches, venues, divisions, conferences saved.")

# ------------------------------
# 4. Seasons
# ------------------------------
print("Fetching Seasons...")
df_seasons = fetch_seasons()
save_to_csv(df_seasons, "seasons.csv")
save_to_postgres(df_seasons, "seasons", ENGINE)
print(f"Seasons saved: {df_seasons.shape[0]} rows")

# ------------------------------
# 5. Player Statistics
# ------------------------------
print("Fetching Player Statistics...")
all_player_stats = []

for season in df_seasons["year"]:
    for team_id in df_teams["id"]:
        df_stats = fetch_player_stats(team_id, season)
        if df_stats is not None and not df_stats.empty:
            all_player_stats.append(df_stats)

df_player_stats = pd.concat(all_player_stats, ignore_index=True)
save_to_csv(df_player_stats, "player_statistics.csv")
save_to_postgres(df_player_stats, "player_statistics", ENGINE)
print(f"Player statistics saved: {df_player_stats.shape[0]} rows")

