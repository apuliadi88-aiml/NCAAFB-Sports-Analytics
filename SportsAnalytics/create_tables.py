from load import create_table_postgres
from config import ENGINE
from create_table_queries import *


create_table_postgres(COACHES_QUERY, ENGINE)
create_table_postgres(VENUES_QUERY, ENGINE)
create_table_postgres(DIVISIONS_QUERY, ENGINE)
create_table_postgres(CONFERENCES_QUERY, ENGINE)
create_table_postgres(TEAMS_QUERY, ENGINE)
create_table_postgres(SEASONS_QUERY, ENGINE)
create_table_postgres(PLAYERS_QUERY, ENGINE)
create_table_postgres(PLAYER_STATISTICS_QUERY, ENGINE)
create_table_postgres(RANKINGS_QUERY, ENGINE)
