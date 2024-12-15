import pandas
import time

from nba_api.stats.endpoints import shotchartdetail
from google.cloud import bigquery
from loguru import logger


def get_coordinates(demo_mode="No") -> pandas.DataFrame:

    if demo_mode == "Yes":

        distinct_game_ids_frame = pandas.DataFrame(
            {
                "gameId": ["21800007"],
                "teamId": ["1610612737"],
                "personId": ["1628416"],
            }
        )

    else:

        client = bigquery.Client()
        logger.info("BigQuery Client initialized.")

        # Define BigQuery query
        get_distinct_game_team_person_ids_query = """
            SELECT 
                DISTINCT gameId, teamId, personId
            FROM 
                `team-23-mj-6242.team_23_dataset.nba_player_stats_by_game_id`
        """

        get_distinct_game_team_person_ids_query_job = client.query(
            get_distinct_game_team_person_ids_query
        )

        distinct_game_ids_frame = (
            get_distinct_game_team_person_ids_query_job.to_dataframe()
        )

    distinct_game_ids_frame = distinct_game_ids_frame.sort_values(
        by=["gameId", "teamId", "personId"]
    )

    len_distinct_game_ids_frame = len(distinct_game_ids_frame)

    i = 0

    combined_dataframe = pandas.DataFrame()

    for index, row in distinct_game_ids_frame.iterrows():

        i += 1

        logger.debug(f"{i} of {len_distinct_game_ids_frame}.")

        time.sleep(1)

        team_id = row["teamId"]
        game_id = "00" + str(row["gameId"])
        person_id = row["personId"]

        logger.debug(f"{team_id}-{game_id}-{person_id}")

        try:
            response = shotchartdetail.ShotChartDetail(
                team_id=team_id,
                player_id=person_id,
                game_id_nullable=game_id,
                context_measure_simple="FGA",  # <-- Default is 'PTS' and will only return made shots, but we want all shot attempts
            )
            shot_df = response.get_data_frames()[0]
            logger.debug(shot_df)
            logger.info(
                f"Retrieved {len(shot_df)} shots for game {game_id}, player {person_id}"
            )

            combined_dataframe = pandas.concat([combined_dataframe, shot_df])

            if i % 30000 == 0:
                combined_dataframe.to_csv(f"combined_dataframe_{i}.csv")
                logger.info(f"Checkpoint saved: combined_dataframe_{i}.csv")

        except Exception as e:
            logger.warning(f"Error - {e}")

    return combined_dataframe


if __name__ == "__main__":

    all_coordinates_frame = get_coordinates()
    all_coordinates_frame.to_csv("all_coordinates_frame.csv")

    logger.info("Done!")
