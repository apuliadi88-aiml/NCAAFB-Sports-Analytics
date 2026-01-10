import streamlit as st
import pandas as pd
from db_connection import run_query

st.title("Coaches Table")
coaches_query = """
    SELECT
        c.coach_id,
        c.full_name AS coach_fullname,
        c.position AS coach_position,
        c.team_id,
        t.team_name
    FROM coaches c
    JOIN teams t ON c.team_id = t.team_id
"""

df = run_query(coaches_query)
st.dataframe(df)

# Search coaches by name or team
st.subheader("Search Coaches by Team or Name")
search_input = st.text_input("Enter Coach Name or Team Name to Search")
if search_input:
    search_query = coaches_query + " WHERE c.full_name ILIKE %s OR t.team_name ILIKE %s"
    search_param = f"%{search_input}%"
    df_search = run_query(search_query, (search_param, search_param))
    st.dataframe(df_search)

# Filter coaches based on position
st.subheader("Filter Coaches by Position")
position = st.selectbox(
    label="Select Coach Position",
    options=["All"] + run_query("SELECT DISTINCT position FROM coaches")["position"].tolist()
)
if position != "All":
    query = coaches_query + " WHERE c.position = %s"
    df_position = run_query(query, (position,))
else:
    df_position = run_query(coaches_query)
st.dataframe(df_position)