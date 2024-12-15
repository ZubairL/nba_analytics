import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import math

from flask import jsonify
from sklearn.model_selection import train_test_split
from google.cloud import bigquery
from sklearn import metrics
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    precision_score,
    recall_score,
    ConfusionMatrixDisplay,
    r2_score,
    mean_squared_error,
)
from loguru import logger


def conduct_ols_linear_regression(demo_mode="No"):

    if demo_mode == "Yes":
        df = pd.read_csv("nba/demo_resources/combined_nba_data.csv")

    else:

        client = bigquery.Client(project="team-23-mj-6242")
        logger.info("BigQuery Client initialized.")

        table_id = "team-23-mj-6242.team_23_dataset.combined_nba_data"

        query = f"""
            SELECT *
            FROM `{table_id}`
            
        """

        df = client.query(query).to_dataframe()

    X = df[
        [
            "AVG_ASSISTS",
            "AVG_DEF_REBOUNDS",
            "AVG_FIELD_GOAL_PCT",
            "AVG_FOULS",
            "AVG_TOT_TURNOVERS",
            "per_jumpshots",
            "per_pts_off_assists",
            "per_secondchance",
        ]
    ]
    y = df["season_wins"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    mse = mean_squared_error(y_test, y_pred)  # Mean Squared Error
    r2 = r2_score(y_test, y_pred)  # R-squared score

    print(f"Mean Squared Error: {mse}")
    print(
        "Mean Absolute Error (MAE):",
        metrics.mean_absolute_error(y_test, y_pred),
    )
    print(f"R-squared: {r2}")
