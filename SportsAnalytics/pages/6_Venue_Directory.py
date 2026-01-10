import streamlit as st
import pandas as pd
from db_connection import run_query

st.title("Venue Directory")
st.subheader("All Venues")

venues_query = """
    SELECT
        venue_id,
        name AS venue_name,
        city,
        state,
        country,
        zip,
        capacity,
        surface,
        roof_type 
   FROM venues
"""

df = run_query(venues_query)
st.dataframe(df)

st.subheader("Filter Venues")
# Filter venues based on state
state = st.selectbox(
    label="Filter by State",
    options=["All"] + run_query("SELECT DISTINCT state FROM venues")["state"].tolist()
)
if state != "All":
    query = venues_query + " WHERE state = %s"
    df_state = run_query(query, (state,))
else:
    df_state = run_query(venues_query)

# Filter venues based on roof type
roof_type = st.selectbox(
    label="Filter by Roof Type",
    options=["All"] + run_query("SELECT DISTINCT roof_type FROM venues")["roof_type"].tolist()
)
if roof_type != "All":
    query = venues_query + " WHERE roof_type = %s"
    df_roof_type = run_query(query, (roof_type,))
else:
    df_roof_type = run_query(venues_query)

# Combine filters
df = pd.merge(df_state, df_roof_type, how='inner', on='venue_id')
st.dataframe(df)    

# Search venues by name
st.subheader("Search Venues")
venue_name = st.text_input("Enter Venue Name to Search")
if venue_name:
    search_query = venues_query + " WHERE name ILIKE %s"
    df_search = run_query(search_query, (f"%{venue_name}%",))
    st.dataframe(df_search)
    

