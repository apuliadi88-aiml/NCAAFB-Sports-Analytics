import streamlit as st
import pandas as pd
from db_connection import run_query

st.title("Seasons and Schedule Viewer")

st.subheader("All Seasons")

seasons_query = """
    SELECT
        s.season_id,
        s.year,
        s.start_date,
        s.end_date
    FROM seasons s
    """

rankings_query = """
    SELECT
        r.ranking_id,
        r.season_year,
        r.week,
        r.team_id,
        t.team_name AS team_name,
        r.rank,
        r.prev_rank,
        r.points,
        r.fp_votes,
        r.wins,
        r.losses,
        r.ties
    FROM rankings r
    JOIN seasons s ON r.season_year= s.year
    JOIN teams t ON r.team_id = t.team_id
    """ 

df = run_query(seasons_query)
st.dataframe(df)

st.subheader("Filter Seasons")
# Filter seasons based on year
year = st.selectbox(
    label="Filter by Year",
    options=["All"] + run_query("SELECT DISTINCT year FROM seasons")["year"].tolist()
)
if year != "All":
    query = seasons_query + " WHERE s.year = %s"
    df_year = run_query(query, (year,))
else:
    df_year = run_query(seasons_query)

# Filter season based on status
status = st.selectbox(
    label="Filter by Status",
    options=["All"] + run_query("SELECT DISTINCT status FROM seasons")["status"].tolist()
)
if status != "All":
    query = seasons_query + " WHERE s.status = %s"
    df_status = run_query(query, (status,))
else:
    df_status = run_query(seasons_query)

# Combine filters
st.subheader("Filtered Seasons")
df = pd.merge(df_year, df_status, how='inner')
st.dataframe(df)

# Search rankings by season year
st.subheader("Search Seasons")

search_year = st.text_input("Enter Season Year to Search")
if search_year:
    search_query = rankings_query + " WHERE s.year = %s"
    df_search = run_query(search_query, (search_year,))
    st.dataframe(df_search)