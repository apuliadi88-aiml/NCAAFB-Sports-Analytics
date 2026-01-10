from sqlalchemy import create_engine, text

# API Configuration
API_KEY = "your_API_KEY"
HEADERS = {
    "accept": "application/json",
    "x-api-key": API_KEY
}

# Database configuration
ENGINE = create_engine('postgresql+psycopg2://postgres:password@localhost:5432/your_database')

# API Endpoints
RANKINGS_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/polls/AP25/{season}/{week}/rankings.json"
TEAM_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/league/teams.json"
TEAM_ROSTER_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/teams/{team_id}/full_roster.json"
SEASONS_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/league/seasons.json"
SEASON_STATISTICS_URL = "https://api.sportradar.com/ncaafb/trial/v7/en/seasons/{season}/REG/teams/{team_id}/statistics.json"

# Constants
SEASONS = [2024, 2025]
WEEKS = [f"{week:02d}" for week in range(1, 22)]
