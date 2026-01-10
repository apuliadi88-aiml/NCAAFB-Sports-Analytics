Project Overview:
A Python-based ETL pipeline to extract, transform, and load sports data into PostgreSQL, with a streamlit application to perform analytic queries on NCAAFB sports data(teams, players,rankings, etc.)

Project Structure:
SportsAnalytics/
│
├── config.py        # Database credentials, API keys,API endpoints, constants
├── main.py          # Orchestrates ETL pipeline
├── utils.py         # Helper functions for API limit handling
├── create_tables_queries.py # Contains queries to create tables
├── create_tables.py # Connects to database and creates tables
├── db_connection.py # Create db connection to extract data for streamlit application
├── extract_and_transform.py # Extracts raw data from API endpoints,cleans & transforms data
├── load.py          # Loads data into PostgreSQL tables, and creates css files
├── sports_analytics_app.py # Streamlit application for performing analysis of NCAAFB Sports data
├── pages/           # Folder containing pages of the streamlit application analyzing different tables of sports data
├── data/            # Contains back up data as csv files loaded from API endpoints after running main.py
└── README.md        # Project documentation

Setup:
1. Clone the repo:
2. Create and activate virtual environment:
3. Install dependencies:     
    Python ≥ 3.10
    pandas
    SQLAlchemy
    psycopg2-binary
    requests
4. Setup PostgreSQL database:
5. Update config.py with database credentials and API keys.

Run Pipeline:
1.Run full ETL pipeline
  python3 main.py
2. Or run individual modules for testing
  python3 extract_and_transform.py
  python3 create_tables.py
  python3 load.py
3.Run streamlit app to perform analytics
  streamlit run sports_analytics_app.py





