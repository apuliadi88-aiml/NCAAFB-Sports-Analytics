import streamlit as st
import pandas as pd
from db_connection import run_query

st.title("Rankings Viewer")
st.subheader("All Rankings")
rankings_query = """
    SELECT
        r.ranking_id,
        r.season_year,
        r.week,
        t.team_name AS team_name,
        r.rank,
        r.points,
        r.fp_votes,
        r.wins,
        r.losses,
        r.ties
    FROM rankings r
    JOIN teams t ON r.team_id = t.team_id
    """
df = run_query(rankings_query)
st.dataframe(df)

# Filter rankings based on season year
season_year = st.selectbox(
    label="Filter by Season Year",
    options=["All"] + run_query("SELECT DISTINCT season_year FROM rankings")["season_year"].tolist()
)
if season_year != "All":
    query = rankings_query + " WHERE r.season_year = %s"
    df_season_year = run_query(query, (season_year,))
else:
    df_season_year = run_query(rankings_query)

# Filter rankings based on week
week = st.selectbox(
    label="Filter by Week",
    options=["All"] + run_query("SELECT DISTINCT week FROM rankings ORDER BY week")["week"].tolist()
)
if week != "All":
    query = rankings_query + " WHERE r.week = %s"
    df_week = run_query(query, (week,))
else:
    df_week = run_query(rankings_query)

# Filter rankings based on range of ranks
rank_range = st.slider(
    label="Filter by Rank Range",
    min_value=1,
    max_value=25,
    value=(1, 25)
)
query = rankings_query + " WHERE r.rank BETWEEN %s AND %s"
df_rank_range = run_query(query, rank_range)

# Combine filters
df = pd.merge(df_season_year, df_week, how='inner', on='ranking_id')
df = pd.merge(df, df_rank_range, how='inner', on='ranking_id')
st.dataframe(df)


# Search rankings by team name
st.subheader("Search Rankings")
search_team = st.text_input("Enter Team Name to Search")
if search_team:
    search_query = rankings_query + " WHERE t.team_name ILIKE %s"
    search_param = f"%{search_team}%"
    df_search = run_query(search_query, (search_param,))
    st.dataframe(df_search)
