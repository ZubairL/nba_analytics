import pandas

from typing import Tuple
from google.cloud import bigquery

client = bigquery.Client()


def get_relevant_tables() -> Tuple[pandas.DataFrame, pandas.DataFrame]:

    get_nba_combined_query = """
        SELECT 
            *
        FROM 
            `team-23-mj-6242.team_23_dataset.combined_nba_data`
    """

    get_nba_combined_query_job = client.query(get_nba_combined_query)

    combined_nba_data = get_nba_combined_query_job.to_dataframe()

    get_wnba_combined_query = """
        SELECT 
            *
        FROM 
            `team-23-mj-6242.team_23_dataset.combined_wnba_data`
    """

    get_wnba_combined_query_job = client.query(get_wnba_combined_query)

    combined_wnba_data = get_wnba_combined_query_job.to_dataframe()

    return combined_nba_data, combined_wnba_data


combined_nba_data, combined_wnba_data = get_relevant_tables()

combined_nba_data = combined_nba_data[["SEASON_YEAR", "season_wins"]]
combined_wnba_data = combined_wnba_data[["SEASON", "wins"]]

summary_stats_season_wins_nba = (
    combined_nba_data.groupby(["SEASON_YEAR"])
    .describe()
    .transpose()
    .reset_index()
    .rename(columns={"level_0": "var", "level_1": "measure"})
)

summary_stats_season_wins_wnba = (
    combined_wnba_data.groupby(["SEASON"])
    .describe()
    .transpose()
    .reset_index()
    .rename(columns={"level_0": "var", "level_1": "measure"})
)

summary_stats_season_wins_nba["league"] = "NBA"
summary_stats_season_wins_wnba["league"] = "WNBA"

combined_summary_stats_season_wins = pandas.concat(
    [summary_stats_season_wins_nba, summary_stats_season_wins_wnba]
)

combined_summary_stats_season_wins.drop(["var"], axis=1, inplace=True)

combined_summary_stats_season_wins.to_csv(
    "machine_learning_models/light_gradient_boosting_machine/Metrics/combined_summary_stats_season_wins.csv"
)
