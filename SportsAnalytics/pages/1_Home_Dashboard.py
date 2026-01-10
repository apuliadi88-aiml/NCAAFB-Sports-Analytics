import streamlit as st
import pandas as pd
from db_connection import run_query

st.title("Home Dashboard")

col1, col2, col3 = st.columns(3)

with col1:
    teams_count = run_query("SELECT COUNT(*) FROM teams").iloc[0, 0]
    st.metric("Teams", teams_count)

with col2:
    players_count = run_query("SELECT COUNT(*) FROM players").iloc[0, 0]
    st.metric("Players", players_count)

with col3:
    seasons_count = run_query("SELECT COUNT(*) FROM seasons").iloc[0, 0]
    st.metric("Seasons", seasons_count)

st.subheader("📋 Teams and conferences")
df = pd.DataFrame(
    run_query("""
        SELECT t.team_name as team_name, c.name as conference_name
        FROM teams t
        JOIN conferences c ON t.conference_id = c.conference_id
        ORDER BY c.name, t.team_name
    """)
)
df_renamed = df.rename(columns={"team_name": "Team Name", "conference_name": "Conference Name"})    
st.dataframe(df_renamed)

st.subheader("📋 Active Players")
df = pd.DataFrame(
    run_query("SELECT first_name , last_name, position, status FROM players WHERE status = 'ACT'")
)
df_renamed = df.rename(columns={"first_name": "First Name", "last_name": "Last Name", "position": "Position", "status": "Status"})
st.dataframe(df_renamed)

st.subheader("📋 Seasons Overview")
df = pd.DataFrame(
    run_query("SELECT year, status FROM seasons ORDER BY year DESC")
)
df_renamed = df.rename(columns={"year": "Year", "status": "Status"})
st.dataframe(df_renamed)