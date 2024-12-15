import duckdb
import pandas

nba_pbp = pandas.read_csv(
    "nba/source_files/all_nba_teams_play_by_play_frame.csv"
)

# Initialize in-memory DuckDB connection
conn = duckdb.connect(database=":memory:")

# Register the Pandas DataFrame as a DuckDB table
conn.register("nba_pbp", nba_pbp)

# Apply duckdb transformation and create new dataframe
nba_pbp_with_crit_times = conn.execute(
    """
    SELECT 
       GAME_ID, 
       EVENTNUM,
       EVENTMSGTYPE,
       EVENTMSGACTIONTYPE, 
       PERIOD, 
       WCTIMESTRING,
       PCTIMESTRING,
       LAG(PCTIMESTRING) OVER (PARTITION BY GAME_ID, PERIOD ORDER BY EVENTNUM) AS lag_pctimestring, 
       HOMEDESCRIPTION, 
       NEUTRALDESCRIPTION, 
       VISITORDESCRIPTION, 
       SCORE,
       SCOREMARGIN,
       game_date, 
       visitor_team, 
       home_team
    FROM
        nba_pbp
     ORDER BY
        GAME_ID, EVENTNUM
"""
).fetchdf()

nba_pbp_with_crit_times["dt_pctimestring"] = pandas.to_datetime(
    nba_pbp_with_crit_times["PCTIMESTRING"], format="%M:%S"
)
nba_pbp_with_crit_times["dt_lag_pctimestring"] = pandas.to_datetime(
    nba_pbp_with_crit_times["lag_pctimestring"], format="%M:%S"
)

# Calculate the difference in seconds - Between each event,
# partitioned by GAME_ID and PERIOD
nba_pbp_with_crit_times["time_difference_seconds"] = (
    nba_pbp_with_crit_times["dt_lag_pctimestring"]
    - nba_pbp_with_crit_times["dt_pctimestring"]
).dt.total_seconds()
