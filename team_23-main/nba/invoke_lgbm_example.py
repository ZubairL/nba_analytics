import requests

from loguru import logger


def invoke_lgbm_example():

    payload_data = {
        "bigquery_table_name": "team-23-mj-6242.team_23_dataset.combined_nba_data",
        "dependent_var": "season_wins",
        "independent_vars": [
            "AVG_ASSISTS",
            "AVG_DEF_REBOUNDS",
            "AVG_FIELD_GOAL_PCT",
            "AVG_FOULS",
            "AVG_TOT_TURNOVERS",
            "per_jumpshots",
            "per_pts_off_assists",
            "per_secondchance",
        ],
        "what_if_dict": {
            "AVG_ASSISTS": 10,
            "AVG_DEF_REBOUNDS": 10,
            "AVG_FIELD_GOAL_PCT": 10,
            "AVG_FOULS": 10,
            "AVG_TOT_TURNOVERS": 10,
            "per_jumpshots": 10,
            "per_pts_off_assists": 10,
            "per_secondchance": 10,
        },
    }

    logger.info("What-If Dictionary:")

    logger.debug(payload_data["what_if_dict"])

    # LightGBM Model
    url = "https://us-west1-team-23-mj-6242.cloudfunctions.net/train_lgbm"

    # Send the POST request with the payload
    response = requests.post(url, json=payload_data)

    if response.status_code == 200:
        result = response.json()
        predicted_value = result.get("predicted_value")
        logger.info(f"The predicted value is: {predicted_value}")
        return predicted_value
    else:
        logger.error(f"Error: {response.status_code}")
