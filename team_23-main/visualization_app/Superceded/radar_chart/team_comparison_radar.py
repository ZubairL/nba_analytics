import plotly.graph_objects as go
import pandas as pd

from dash import Dash, dcc, html, Input, Output
from google.cloud import bigquery
from typing import Tuple


def combine_wnba_nba_tables_and_metrics() -> Tuple[pd.DataFrame, pd.DataFrame]:

    client = bigquery.Client()

    # Define BigQuery query
    get_combined_nba_data_query = """
        SELECT 
            *
        FROM 
            `team-23-mj-6242.team_23_dataset.combined_nba_data`
    """

    get_combined_nba_data_query_job = client.query(get_combined_nba_data_query)

    combined_nba_data_frame = get_combined_nba_data_query_job.to_dataframe()

    # Define BigQuery query
    get_combined_wnba_data_query = """
        SELECT 
            *
        FROM 
            `team-23-mj-6242.team_23_dataset.combined_wnba_data`
    """

    get_combined_wnba_data_query_job = client.query(
        get_combined_wnba_data_query
    )

    combined_wnba_data_frame = get_combined_wnba_data_query_job.to_dataframe()

    combined_wnba_data_frame = combined_wnba_data_frame.rename(
        columns={"wins": "season_wins", "SEASON": "SEASON_YEAR"}
    ).assign(league="WNBA")

    combined_nba_data_frame["league"] = "NBA"

    combined_wnba_nba_frame = pd.concat(
        [combined_wnba_data_frame, combined_nba_data_frame]
    )

    df = combined_wnba_nba_frame.copy()

    df["SEASON_YEAR"] = df["SEASON_YEAR"].astype(str)

    # Normalize metrics to range [0.1, 1] to avoid the dead center
    metrics = list(df.columns)
    columns_to_exclude = [
        "SEASON_YEAR",
        "TEAM_ID",
        "TEAM_NAME",
        "TEAM_MASCOT",
        "TEAM_ABBREV",
        "league",
        "season_winner",
        "AVG_PLUS_MINUS_POINTS",
    ]

    metrics = [col for col in metrics if col not in columns_to_exclude]

    df[metrics] = (df[metrics] - df[metrics].min()) / (
        df[metrics].max() - df[metrics].min()
    )
    df[metrics] = df[metrics] * 0.9 + 0.1  # Scale to range [0.1, 1]

    return df, metrics


df, metrics = combine_wnba_nba_tables_and_metrics()

# Initialize Dash App
app = Dash(__name__)

# Layout with dropdowns for team and season selection
app.layout = html.Div(
    [
        html.H1("NBA/WNBA Team Comparison Radar Chart"),
        html.Div(
            [
                html.Label("Select Teams:"),
                dcc.Dropdown(
                    id="team-selector",
                    options=[
                        {
                            "label": f"{team} ({season})",
                            "value": f"{team}-{season}",
                        }
                        for team, season in zip(
                            df["TEAM_NAME"], df["SEASON_YEAR"]
                        )
                    ],
                    multi=True,
                    value=[
                        "Dallas-2022",
                        "Indiana-2023",
                    ],  # Default selected teams
                ),
            ],
            style={
                "width": "45%",
                "display": "inline-block",
                "padding": "10px",
            },
        ),
        dcc.Graph(id="radar-chart"),
    ]
)


# Callback to update radar chart based on selected teams
@app.callback(
    Output("radar-chart", "figure"), [Input("team-selector", "value")]
)
def update_radar_chart(selected_teams):
    fig = go.Figure()

    for team_season in selected_teams:
        team, season = team_season.split("-")
        team_data = df[
            (df["TEAM_NAME"] == team) & (df["SEASON_YEAR"] == season)
        ]
        if not team_data.empty:
            r = team_data[metrics].iloc[0].values
            theta = metrics

            fig.add_trace(
                go.Scatterpolar(
                    r=r,
                    theta=theta,
                    fill="toself",
                    name=f"{team} ({season})",
                    mode="lines",
                    line=dict(width=0),
                )
            )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                showticklabels=False,
                range=[0, 1],
            )
        ),
        showlegend=True,
        title="Interactive Team Comparison Radar Chart",
    )

    return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
