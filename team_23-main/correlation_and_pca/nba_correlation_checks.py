import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from sklearn.feature_selection import mutual_info_classif
from google.cloud import bigquery
from loguru import logger


def correlation_checks(demo_mode="No"):

    if demo_mode == "Yes":

        df = pd.read_csv("nba/demo_resources/combined_nba_data.csv")

    else:

        client = bigquery.Client()
        logger.info("BigQuery Client initialized.")

        sql = """
            SELECT *
            FROM `team-23-mj-6242.team_23_dataset.combined_nba_data`
        """

        df = client.query_and_wait(sql).to_dataframe()

    logger.info("Data imported.")

    # split independent and response vars
    y = df["season_wins"]
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
            # "AVG_OFF_REBOUNDS",#
            "AVG_STEALS",
            "AVG_THREE_PT_FIELD_GOAL_PCT",
            # "AVG_THREE_PT_FIELD_GOALS_MADE",#
            # "AVG_THREE_PT_FIELD_GOALS_ATT",#
            # "AVG_TOT_REBOUNDS",#
            "AVG_TOT_TURNOVERS",
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
    plt.title("NBA Mutual Information")
    plt.show()

    # correlation matrix
    corr_df = x.corr(method="pearson")
    corr_max = corr_df.abs().unstack()
    corr_max_sort = corr_max.sort_values(ascending=False)
    corr_max_val = corr_max_sort[(corr_max_sort < 1.0) & (corr_max_sort > 0.6)]
    print(corr_max_val)

    # create corr heatmap
    plt.figure(figsize=(20, 18))
    sns.heatmap(corr_df, annot=True, cmap="coolwarm")
    plt.title("NBA Correlation Matrix Heatmap")
    plt.show()

    # save to csv
    # pd.DataFrame(corr_df).to_csv("nba_corr.csv")
    # pd.DataFrame(mi_df).to_csv("nba_mut_info.csv")
