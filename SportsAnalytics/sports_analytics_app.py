import streamlit as st

st.set_page_config(
    page_title="NCAAFB Sports Analytics",
    layout="wide"
)

st.title("NCAAFB Sports Analytics Dashboard :football:")

st.markdown("""
Use the sidebar on the left to explore teams, players, rankings, venues, and more.
This application provides insights and analytics on NCAAFB football data. 
Navigate through different sections to analyze various aspects of the sport.
Enjoy your exploration! 
""")

# Check the pages folder for the sidebar contents - Home Dashboard, Teams Explorer, Players Explorer,Seasons_And_Schedule_Viewer, Rankings, Venue_Directory, Coaches_table
