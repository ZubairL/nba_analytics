from google.cloud import bigquery
from pandas_gbq import to_gbq
import pandas as pd
import os

project_id = "team-23-mj-6242"
dataset_id = "team_23_dataset"

file_dict = {
    "wnba-pbp-2019-2024": "./wnba_pbp_2013-24.csv",
    "wnba-teambox-2019-2024": "./wnba_teambox_2013-24.csv",
    "wnba-schedule-2019-2024-v2": "./wnba_schedule_2013-24.csv",
}


def clear_bq_tables():
    client = bigquery.Client()
    query1 = """
            DELETE 
            FROM `team-23-mj-6242.team_23_dataset.wnba-pbp-2019-2024`
            WHERE true
            """

    query2 = """
            DELETE 
            FROM `team-23-mj-6242.team_23_dataset.wnba-teambox-2019-2024`
            WHERE true
            """

    query3 = """
            DELETE 
            FROM `team-23-mj-6242.team_23_dataset.wnba-schedule-2019-2024-v2`
            WHERE true
            """

    querylist = [query1, query2, query3]

    for query in querylist:
        query_job = client.query(query)


def append_data_tobq(file_dict, project_id, dataset_id):
    for t, f in file_dict.items():
        # Import new season data from csv
        new_data = pd.read_csv(f, dtype={"season": "int64"})
        new_data_filter = new_data[new_data["season"] > 2012]

        if "pbp" in t:
            new_data_filter = new_data_filter.astype(str)
        elif "teambox" in t:
            new_data_filter = new_data_filter.astype(
                {
                    "game_id": "int64",
                    "season": "int64",
                    "season_type": "int64",
                    "game_date": "datetime64[ns]",
                    "game_date_time": "datetime64[ns]",
                    "team_id": "int64",
                    "team_uid": "str",
                    "team_slug": "str",
                    "team_location": "str",
                    "team_name": "str",
                    "team_abbreviation": "str",
                    "team_display_name": "str",
                    "team_short_display_name": "str",
                    "team_color": "str",
                    "team_alternate_color": "str",
                    "team_logo": "str",
                    "team_home_away": "str",
                    "team_score": "int64",
                    "team_winner": "boolean",
                    "assists": "int64",
                    "blocks": "int64",
                    "defensive_rebounds": "int64",
                    "field_goal_pct": float,
                    "field_goals_made": "int64",
                    "field_goals_attempted": "int64",
                    "flagrant_fouls": "int64",
                    "fouls": "int64",
                    "free_throw_pct": float,
                    "free_throws_made": "int64",
                    "free_throws_attempted": "int64",
                    "largest_lead": "str",
                    "offensive_rebounds": "int64",
                    "steals": "int64",
                    "team_turnovers": "int64",
                    "technical_fouls": "int64",
                    "three_point_field_goal_pct": float,
                    "three_point_field_goals_made": "int64",
                    "three_point_field_goals_attempted": "int64",
                    "total_rebounds": "int64",
                    "total_technical_fouls": "int64",
                    "total_turnovers": "int64",
                    "turnovers": "int64",
                    "opponent_team_id": "int64",
                    "opponent_team_uid": "str",
                    "opponent_team_slug": "str",
                    "opponent_team_location": "str",
                    "opponent_team_name": "str",
                    "opponent_team_abbreviation": "str",
                    "opponent_team_display_name": "str",
                    "opponent_team_short_display_name": "str",
                    "opponent_team_color": "str",
                    "opponent_team_alternate_color": "str",
                    "opponent_team_logo": "str",
                    "opponent_team_score": "int64",
                    "fast_break_points": "str",
                    "points_in_paint": "str",
                    "turnover_points": "str",
                }
            )
        elif "schedule" in t:
            new_data_filter.drop(
                ["broadcast", "highlights"], axis=1, inplace=True
            )

            new_data_filter = new_data_filter.astype(
                {
                    "id": "int64",
                    "uid": "str",
                    "date": "datetime64[ns, UTC]",
                    "attendance": "int64",
                    "time_valid": "boolean",
                    "neutral_site": "boolean",
                    "conference_competition": "boolean",
                    "recent": "boolean",
                    "start_date": "datetime64[ns, UTC]",
                    "notes_type": "str",
                    "notes_headline": "str",
                    "type_id": "int64",
                    "type_abbreviation": "str",
                    "venue_id": "int64",
                    "venue_full_name": "str",
                    "venue_address_city": "str",
                    "venue_address_state": "str",
                    "venue_capacity": "str",
                    "venue_indoor": "boolean",
                    "status_clock": "int64",
                    "status_display_clock": "str",
                    "status_period": "int64",
                    "status_type_id": "int64",
                    "status_type_name": "str",
                    "status_type_state": "str",
                    "status_type_completed": "boolean",
                    "status_type_description": "str",
                    "status_type_detail": "str",
                    "status_type_short_detail": "str",
                    "format_regulation_periods": "int64",
                    "home_id": "int64",
                    "home_uid": "str",
                    "home_location": "str",
                    "home_name": "str",
                    "home_abbreviation": "str",
                    "home_display_name": "str",
                    "home_short_display_name": "str",
                    "home_color": "str",
                    "home_alternate_color": "str",
                    "home_is_active": "boolean",
                    "home_venue_id": "str",
                    "home_logo": "str",
                    "home_score": "int64",
                    "home_winner": "str",
                    "away_id": "int64",
                    "away_uid": "str",
                    "away_location": "str",
                    "away_name": "str",
                    "away_abbreviation": "str",
                    "away_display_name": "str",
                    "away_short_display_name": "str",
                    "away_is_active": "boolean",
                    "away_score": "int64",
                    "away_winner": "str",
                    "game_id": "int64",
                    "season": "int64",
                    "season_type": "int64",
                    "away_color": "str",
                    "away_alternate_color": "str",
                    "away_venue_id": "str",
                    "away_logo": "str",
                    "status_type_alt_detail": "str",
                    "game_json": "boolean",
                    "game_json_url": "str",
                    "game_date_time": "str",
                    "game_date": "datetime64[ns]",
                    "PBP": "boolean",
                    "team_box": "boolean",
                    "player_box": "boolean",
                    "play_by_play_available": "str",
                    "broadcast_market": "str",
                    "broadcast_name": "str",
                    "home_linescores": "str",
                    "home_records": "str",
                    "away_linescores": "str",
                    "away_records": "str",
                }
            )

        # Set up BigQuery client
        client = bigquery.Client()

        # Specify the table ID
        table_id = dataset_id + "." + t

        # Append the DataFrame to the BigQuery table
        new_data_filter.to_gbq(
            table_id, project_id=project_id, if_exists="append"
        )


if __name__ == "__main__":
    clear_bq_tables()
    append_data_tobq(file_dict, project_id, dataset_id)
