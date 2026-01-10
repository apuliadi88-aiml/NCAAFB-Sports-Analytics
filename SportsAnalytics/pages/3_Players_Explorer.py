import streamlit as st
import pandas as pd
from db_connection import run_query

st.title("Players Explorer")

st.subheader("All Players")

players_query = """
    SELECT
        p.player_id,
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
    """

df = run_query(players_query)
st.dataframe(df)

st.subheader("Filter Players")
# Filter players based on position
position = st.selectbox(
    label="Filter by Position",
    options=["All"] + run_query("SELECT DISTINCT position FROM players")["position"].tolist()
)

if position != "All":
    query = players_query + " WHERE p.position = %s"
    df_position = run_query(query, (position,))
else:
    df_position = run_query(players_query)

# Filter players based on status

status = st.selectbox(
    label="Filter by Status",
    options=["All"] + run_query("SELECT DISTINCT status FROM players")["status"].tolist()
)
if status != "All":
    query = players_query + " WHERE p.status = %s"
    df_status = run_query(query, (status,))
else:
    df_status = run_query(players_query)

#Filter players based on eligibility
eligibility = st.selectbox(
    label="Filter by Eligibility",
    options=["All"] + run_query("SELECT DISTINCT eligibility FROM players")["eligibility"].tolist()
)
if eligibility != "All":
    query = players_query + " WHERE p.eligibility = %s"
    df_eligibility = run_query(query, (eligibility,))
else:
    df_eligibility = run_query(players_query)

# Combine filters
df = pd.merge(df_position, df_status, on="player_id")
df = pd.merge(df, df_eligibility, on="player_id")
st.subheader("Filtered Players")
st.dataframe(df)

st.subheader("Search Players")
# Search by player name or team name
player_search = st.text_input("Search player by player name or team name")

df = run_query(players_query)
if player_search:
    players_query += " WHERE t.team_name ILIKE %s OR p.first_name ILIKE %s OR p.last_name ILIKE %s"
    search_param = f"%{player_search}%"
    df = run_query(players_query, (search_param, search_param, search_param))

st.dataframe(df)

