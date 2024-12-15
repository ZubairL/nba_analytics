from google.cloud import bigquery
import pandas as pd
import warnings
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
)
from sklearn.metrics import mean_squared_error, r2_score

warnings.filterwarnings(
    "ignore", message="Pandas requires version '2.8.4' or newer of 'numexpr'"
)
warnings.filterwarnings(
    "ignore",
    message="Pandas requires version '1.3.6' or newer of 'bottleneck'",
)

client = bigquery.Client(project="team-23-mj-6242")

table_id = "team-23-mj-6242.team_23_dataset.nba_teambox_season_avgs"


query = f"""
    SELECT *
    FROM `{table_id}`
    LIMIT 10000
"""

df = client.query(query).to_dataframe()


features = [
    "GAME_COUNT",
    "season_wins",
    "AVG_FIELD_GOALS_MADE",
    "AVG_FIELD_GOALS_ATT",
    "AVG_FIELD_GOAL_PCT",
    "VAR_FIELD_GOAL_PCT",
    "AVG_THREE_PT_FIELD_GOALS_MADE",
    "AVG_THREE_PT_FIELD_GOALS_ATT",
    "AVG_THREE_PT_FIELD_GOAL_PCT",
    "AVG_FREE_THROWS_MADE",
    "AVG_FREE_THROWS_ATT",
    "AVG_FREE_THROW_PCT",
    "AVG_OFF_REBOUNDS",
    "AVG_DEF_REBOUNDS",
    "AVG_TOT_REBOUNDS",
    "AVG_ASSISTS",
    "AVG_STEALS",
    "AVG_BLOCKS",
    "AVG_TOT_TURNOVERS",
    "AVG_FOULS",
    "AVG_PTS_SCORED",
    "AVG_PLUS_MINUS_POINTS",
    "AVG_PTS_AGAINST",
]

X = df[features]
y = df["season_winner"]
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Train a Logistic Regression model (multinomial for multiple classes)
model = LogisticRegression(
    multi_class="multinomial", solver="lbfgs", max_iter=500
)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)

# Evaluation
print("Accuracy:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))
print("\nConfusion Matrix:\n", confusion_matrix(y_test, y_pred))

# Optional: View predictions and actual values
predictions = pd.DataFrame({"Actual": y_test, "Predicted": y_pred})
print(predictions.head())
