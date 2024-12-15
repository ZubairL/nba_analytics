from google.cloud import bigquery
from loguru import logger
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

import pandas
import plotly.graph_objects as go


def prepare_bigquery_table():

    client = bigquery.Client()

    # Define BigQuery query
    get_wnba_teambox_season_avgs_query = """
        SELECT 
            *
        FROM 
            `team-23-mj-6242.team_23_dataset.combined_wnba_data`
    """

    get_wnba_teambox_season_avgs_query_job = client.query(
        get_wnba_teambox_season_avgs_query
    )

    wnba_teambox_season_avgs = (
        get_wnba_teambox_season_avgs_query_job.to_dataframe()
    )

    wnba_teambox_season_avgs.columns

    # Drop string columns, correlated features & response vars
    wnba_teambox_season_avgs_numerical = wnba_teambox_season_avgs.drop(
        [
            "SEASON",
            "TEAM_ID",
            "TEAM_NAME",
            "TEAM_ABBREV",
            "TEAM_LOC",
            # "season_winner",
            "wins",
            "AVG_PTS_SCORED",  #
            "AVG_FIELD_GOALS_MADE",  #
            "AVG_FIELD_GOALS_ATT",  #
            "AVG_FREE_THROW_PCT",  #
            "AVG_FREE_THROWS_MADE",  #
            "AVG_FREE_THROWS_ATT",  #
            "AVG_OFF_REBOUNDS",
            "AVG_TEAM_TURNOVERS",  #
            "AVG_THREE_PT_FIELD_GOALS_MADE",  #
            "AVG_THREE_PT_FIELD_GOALS_ATT",  #
            "AVG_TOT_REBOUNDS",  #
            "AVG_TURNOVERS",  #
        ],
        axis=1,
    )

    corr_matrix = wnba_teambox_season_avgs_numerical.corr()

    return wnba_teambox_season_avgs_numerical, corr_matrix


def plot_pca_variance(df):
    # Center and scale data
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)

    # Perform PCA
    pca = PCA()
    pca.fit(df_scaled)

    loadings_frame = pandas.DataFrame(
        pca.components_.T,
        columns=[f"PC{i + 1}" for i in range(len(df.columns))],
        index=df.columns,
    )

    # Create plot
    explained_variance = pca.explained_variance_ratio_
    cumulative_variance = explained_variance.cumsum()

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=[f"PC {i+1}" for i in range(len(explained_variance))],
            y=explained_variance,
            name="Individual Component Variance",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=[f"PC {i+1}" for i in range(len(cumulative_variance))],
            y=cumulative_variance,
            mode="lines+markers",
            name="Cumulative Variance",
        )
    )

    fig.update_layout(
        title="WNBA PCA - Explained Variance by Component",
        xaxis_title="Principal Component",
        yaxis_title="Variance Explained",
        legend=dict(x=0.8, y=1.2),
    )
    fig.show()

    # save to csv
    pandas.DataFrame(loadings_frame).to_csv("wnba_loadings_frame.csv")

    return loadings_frame


# Identify variables in the top 7 PCA components and use an
# arbitrary cutoff max absolute loading value.
def identify_variables_via_pca(loadings_frame):

    top_7_components_frame = loadings_frame[
        ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6", "PC7"]
    ]

    top_7_components_frame = top_7_components_frame.reset_index()

    top_7_components_frame = top_7_components_frame.rename(
        columns={"index": "variable"}
    ).sort_values(
        by=["PC1", "PC2", "PC3", "PC4", "PC5", "PC6", "PC7"], ascending=False
    )

    top_7_components_frame["max_across_components"] = (
        top_7_components_frame[
            ["PC1", "PC2", "PC3", "PC4", "PC5", "PC6", "PC7"]
        ]
        .abs()
        .max(axis=1)
    )

    # Use arbitrary cutoff value (0.4)
    loadings_across_top_7 = top_7_components_frame.sort_values(
        by="max_across_components", ascending=False
    ).query("max_across_components >= 0.35")

    return loadings_across_top_7


if __name__ == "__main__":
    (
        wnba_teambox_season_avgs_numerical,
        wnba_teambox_season_avgs_numerical_corr_matrix,
    ) = prepare_bigquery_table()

    loadings_frame = plot_pca_variance(wnba_teambox_season_avgs_numerical)

    wnba_loadings_across_top_7_components = identify_variables_via_pca(
        loadings_frame
    )
