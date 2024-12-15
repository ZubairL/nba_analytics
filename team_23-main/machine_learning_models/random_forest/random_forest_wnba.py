import pandas
import numpy as np
from sklearn.ensemble import RandomForestRegressor
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
)
from loguru import logger

from sklearn.tree import export_graphviz

# from IPython.display import Image
import graphviz

""" REFERENCES """

# https://www.datacamp.com/tutorial/random-forests-classifier-python


client = bigquery.Client(project="team-23-mj-6242")

table_id = "team-23-mj-6242.team_23_dataset.combined_wnba_data"

query = f"""
    SELECT *
    FROM `{table_id}`
    
"""

df = client.query(query).to_dataframe()


# Variable selection based on Carsten's PCA
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
y = df["wins"]


# train/test data
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# fitting model
rf = RandomForestRegressor(n_estimators=1000, max_depth=15, random_state=42)
rf.fit(X_train, y_train)

# finding predictions
y_pred = rf.predict(X_test)

# metric calculations
print("Mean Squared Error (MSE):", metrics.mean_squared_error(y_test, y_pred))
print(
    "Mean Absolute Error (MAE):", metrics.mean_absolute_error(y_test, y_pred)
)
r2 = r2_score(y_test, y_pred)
print("R² Score:", r2)
