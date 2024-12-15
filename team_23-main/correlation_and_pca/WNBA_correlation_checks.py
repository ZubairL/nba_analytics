import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.feature_selection import mutual_info_classif
from google.cloud import bigquery

client = bigquery.Client()


sql = """
    SELECT *
    FROM `team-23-mj-6242.team_23_dataset.combined_wnba_data`
"""

df = client.query_and_wait(sql).to_dataframe()
print("data imported")


# split independent and response vars
y = df["wins"]
x = df[
    [
        # "AVG_PTS_SCORED",#
        "AVG_ASSISTS",
        "AVG_BLOCKS",
        "AVG_DEF_REBOUNDS",
        "AVG_FIELD_GOAL_PCT",
        "VAR_FIELD_GOAL_PCT",
        # "AVG_FIELD_GOALS_MADE",#
        # "AVG_FIELD_GOALS_ATT",#
        "AVG_FOULS",
        # "AVG_FREE_THROW_PCT",#
        # "AVG_FREE_THROWS_MADE",#
        # "AVG_FREE_THROWS_ATT",#
        # "AVG_OFF_REBOUNDS",
        "AVG_STEALS",
        # "AVG_TEAM_TURNOVERS",#
        "AVG_THREE_PT_FIELD_GOAL_PCT",
        # "AVG_THREE_PT_FIELD_GOALS_MADE",#
        # "AVG_THREE_PT_FIELD_GOALS_ATT",#
        # "AVG_TOT_REBOUNDS",#
        "AVG_TOT_TURNOVERS",
        # "AVG_TURNOVERS",#
        "AVG_PTS_AGAINST",
        "per_pts_off_assists",
        "per_paintshots",
        "per_jumpshots",
        "per_freethrows",
        "per_secondchance",
    ]
]

# adapted from plot_f_test_vs_mi.py from sklearn examples
# mutual information
mi = mutual_info_classif(x, y)
mi /= np.max(mi)
mi_df = pd.DataFrame(mi, columns=["Mutual Info Score"], index=x.columns)

# create MI heatmap
plt.figure(figsize=(15, 8))
sns.heatmap(mi_df, annot=True, cmap="viridis", cbar=False)
plt.title("WNBA Mutual Information")
plt.show()

# correlation matrix
corr_df = x.corr(method="pearson")

# create corr heatmap
plt.figure(figsize=(20, 18))
sns.heatmap(corr_df, annot=True, cmap="coolwarm")
plt.title("WNBA Correlation Matrix Heatmap")
plt.show()

# save to csv
pd.DataFrame(corr_df).to_csv("Corr.csv")
pd.DataFrame(mi_df).to_csv("MutInfo.csv")
