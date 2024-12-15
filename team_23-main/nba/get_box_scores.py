import pandas
import time

from nba_api.stats.endpoints import BoxScoreTraditionalV3
from google.cloud import bigquery
from loguru import logger


def get_boxscores(demo_mode="No") -> pandas.DataFrame:

    if demo_mode == "Yes":
        distinct_game_ids = ["21800001", "21800007"]

    else:
        client = bigquery.Client()
        logger.info("BigQuery Client initialized.")

        # Define BigQuery query
        # Get distinct list of Game IDs
        get_distinct_game_ids_query = """
            SELECT 
                DISTINCT NBA_GAME_ID
            FROM 
                `team-23-mj-6242.team_23_dataset.nba_pbp_sorted`
        """

        get_distinct_game_ids_query_job = client.query(
            get_distinct_game_ids_query
        )

        distinct_game_ids_frame = (
            get_distinct_game_ids_query_job.to_dataframe()
        )

        distinct_game_ids = list(distinct_game_ids_frame["NBA_GAME_ID"])

    list_playerstats_frames = []
    list_teamstats_frames = []

    i = 0

    for game_id in distinct_game_ids:

        i += 1

        logger.info(f"Game {i} of {len(distinct_game_ids)}.")

        time.sleep(2)

        # Ensure game_id has two zeroes in front
        game_id = "00" + str(game_id)

        try:

            # Fetch the boxscore data
            boxscore_data = BoxScoreTraditionalV3(game_id=game_id)

            # Convert the data to a pandas DataFrame
            player_stats = boxscore_data.player_stats.get_data_frame()
            team_stats = boxscore_data.team_stats.get_data_frame()
            list_playerstats_frames.append(player_stats)
            list_teamstats_frames.append(team_stats)

        except Exception:
            logger.error("Invalid game_id or API error, skipping.")
            continue

    combined_team_stats_frame = pandas.concat(list_teamstats_frames)

    combined_player_stats_frame = pandas.concat(list_playerstats_frames)

    return combined_team_stats_frame, combined_player_stats_frame


if __name__ == "__main__":
    combined_nba_team_stats_frame, combined_nba_player_stats_frame = (
        get_boxscores()
    )
    combined_nba_team_stats_frame.to_csv("combined_nba_team_stats_frame.csv")
    combined_nba_player_stats_frame.to_csv(
        "combined_nba_player_stats_frame.csv"
    )
