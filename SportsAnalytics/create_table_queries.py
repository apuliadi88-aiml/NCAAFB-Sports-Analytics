COACHES_QUERY = """
CREATE TABLE IF NOT EXISTS coaches (
    coach_id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,              
    last_name VARCHAR(100) NOT NULL, 
    full_name VARCHAR(255) GENERATED ALWAYS AS (
        first_name || ' ' || last_name
    ) STORED,
    position VARCHAR(100),
    team_id  UUID NOT NULL,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
"""

VENUES_QUERY = """
CREATE TABLE IF NOT EXISTS venues (
    venue_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    state  VARCHAR(100),
    country VARCHAR(100),
    zip VARCHAR(20),
    address VARCHAR(255),
    capacity INT,
    surface VARCHAR(100),
    roof_type VARCHAR(50),
    latitude DECIMAL,
    longitude DECIMAL
);
"""

DIVISIONS_QUERY = """
CREATE TABLE IF NOT EXISTS divisions (
    division_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    alias VARCHAR(100)
);
"""
CONFERENCES_QUERY = """
CREATE TABLE IF NOT EXISTS conferences (
    conference_id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    alias VARCHAR(100)
);
"""
TEAMS_QUERY = """
CREATE TABLE IF NOT EXISTS teams (
    team_id UUID PRIMARY KEY,
    market VARCHAR(150),
    team_name VARCHAR(150) NOT NULL,
    alias VARCHAR(20),
    founded INT,
    mascot VARCHAR(150),
    fight_song VARCHAR(255),
    championships_won INT,
    conference_id  UUID,
    division_id UUID,
    venue_id  UUID,
    FOREIGN KEY (conference_id) REFERENCES conferences(conference_id),
    FOREIGN KEY (division_id) REFERENCES divisions(division_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id)
);
"""
SEASONS_QUERY = """
CREATE TABLE IF NOT EXISTS seasons (
    season_id UUID PRIMARY KEY,
    year INT NOT NULL,
    start_date DATE,
    end_date DATE,
    status VARCHAR(50),
    type_code  VARCHAR(20)
);
"""

PLAYERS_QUERY = """
CREATE TABLE IF NOT EXISTS players (
    player_id UUID PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    abbr_name VARCHAR(20),
    birth_place VARCHAR(150),
    position VARCHAR(50),
    height INT,
    weight INT,
    status VARCHAR(20),
    eligibility VARCHAR(20),
    team_id UUID,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
"""

PLAYER_STATISTICS_QUERY = """
CREATE TABLE IF NOT EXISTS player_statistics (
    stat_id SERIAL PRIMARY KEY,
    player_id UUID,
    team_id UUID,
    season_id UUID,
    games_played INT,
    games_started INT,
    rushing_yards INT,
    rushing_touchdowns INT,
    receiving_yards INT,
    receiving_touchdowns INT,
    kick_return_yards INT,
    fumbles INT,
    FOREIGN KEY (player_id) REFERENCES players(player_id)
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
    FOREIGN KEY (season_id) REFERENCES seasons(season_id)
);
"""

RANKINGS_QUERY = """
CREATE TABLE IF NOT EXISTSrankings (
    ranking_id SERIAL PRIMARY KEY,
    poll_id UUID NOT NULL,
    poll_name VARCHAR(150),
    season_year int,
    week INT,
    effective_time TIMESTAMP,
    team_id UUID,
    rank INT,
    prev_rank INT,
    points INT,
    fp_votes INT,
    wins INT DEFAULT 0,
    losses INT DEFAULT 0,
    ties INT DEFAULT 0,
    FOREIGN KEY (season_id) REFERENCES seasons(season_id),
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);
"""

SAMPLE_QUERY = """
CREATE TABLE IF NOT EXISTS sample_table (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    value INT
);
"""
