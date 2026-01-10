import streamlit as st
import pandas as pd
from db_connection import run_query

st.title("Teams Explorer")

conference = st.selectbox(
    label = "Filter by Conference",
    options = ["All"] + run_query("SELECT DISTINCT name FROM conferences")["name"].tolist()
)

#Filter teams based on selected conference
# Create a base query to fetch team details along with conference names
query = """
SELECT
    t.team_id,
    t.market,
    t.team_name,
    t.founded,
    t.mascot,
    t.fight_song,
    t.championships_won,
    c.name AS conference_name,
    v.name AS venue
FROM teams t
LEFT JOIN conferences c ON t.conference_id = c.conference_id
LEFT JOIN venues v ON t.venue_id = v.venue_id
"""
# Apply conference filter if selected
if conference != "All":
    query += " WHERE c.name = %s"           
    df_conference = run_query(query, (conference,))
else:
    df_conference = run_query(query)


# Filter teams based on division
division = st.selectbox(
    label="Filter by Division",
    options=["All"] + run_query("SELECT DISTINCT name FROM divisions")["name"].tolist()
)

query = """
SELECT
    t.team_id,
    t.market,
    t.team_name,
    t.founded,
    t.mascot,
    t.fight_song,
    t.championships_won,
    d.name AS division_name,
    v.name AS venue
FROM teams t
LEFT JOIN divisions d ON t.division_id = d.division_id
LEFT JOIN venues v ON t.venue_id = v.venue_id
"""
if division != "All":
    query += " WHERE d.name = %s"
    df_division = run_query(query, (division,))
else:
    df_division = run_query(query)

df= pd.merge(df_conference, df_division, on="team_id")
st.subheader("Filtered Teams")
st.dataframe(df)

# Search for a team by name or alias
team_name_or_alias = st.text_input("Search Team by name or alias")
query = """
SELECT
    t.team_id,  
    t.market,
    t.team_name,
    t.alias,
    t.founded,
    t.mascot,
    t.fight_song,
    t.championships_won,
    v.name AS venue
FROM teams t
LEFT JOIN venues v ON t.venue_id = v.venue_id
"""
df = run_query(query)
if team_name_or_alias:
    query += " WHERE t.team_name ILIKE %s OR t.alias ILIKE %s"
    search_param = f"%{team_name_or_alias}%"
    df = run_query(query, (search_param, search_param))

st.dataframe(df)

# View team roster by selecting a team
selected_team = st.selectbox(
    label="Select a Team to View Roster",
    options=run_query("SELECT DISTINCT team_name FROM teams")["team_name"].tolist()
)
if selected_team:
    query = """
    SELECT
        p.first_name,
        p.last_name,
        p.position,
        p.eligibility,
        p.status,
        p.abbr_name,
        p.height,
        p.weight,
        p.birth_place,
        t.team_name AS team_name
    FROM players p
    JOIN teams t ON p.team_id = t.team_id
    WHERE t.team_name = %s
    """
    df = run_query(query, (selected_team,))
    st.subheader(f"Roster for {selected_team}")
    st.dataframe(df)