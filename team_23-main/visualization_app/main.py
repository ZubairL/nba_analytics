import dash
import pandas as pd
import dash_bootstrap_components as dbc
import requests
import plotly.graph_objects as go
import plotly.express as px

from dash import html, dcc
from dash.dependencies import Input, Output, State, ALL
from loguru import logger
from google.cloud import bigquery
from typing import Tuple

from layout import create_layout

client = bigquery.Client()

TABLE_NAME = "`team-23-mj-6242.team_23_dataset.combined_nba_coordinates`"

rename_cols_dict = {
    "GAME_COUNT": "COUNT_GAMES_PLAYED",
    "AVG_FIELD_GOALS_MADE": "AVG_FIELD_GOALS_MADE",
    "AVG_FIELD_GOALS_ATT": "AVG_FIELD_GOALS_ATTEMPTED",
    "AVG_FIELD_GOAL_PCT": "AVG_FIELD_GOAL_PERCENT",
    "VAR_FIELD_GOAL_PCT": "VARIANCE_FIELD_GOAL_PERCENT",
    "AVG_THREE_PT_FIELD_GOALS_MADE": "AVG_THREE_POINT_FIELD_GOALS_MADE",
    "AVG_THREE_PT_FIELD_GOALS_ATT": "AVG_THREE_POINT_FIELD_GOALS_ATTEMPTED",
    "AVG_THREE_PT_FIELD_GOAL_PCT": "AVG_THREE_POINT_FIELD_GOAL_PERCENT",
    "AVG_FREE_THROWS_MADE": "AVG_FREE_THROWS_MADE",
    "AVG_FREE_THROWS_ATT": "AVG_FREE_THROWS_ATTEMPTED",
    "AVG_FREE_THROW_PCT": "AVG_FREE_THROW_PERCENT",
    "AVG_OFF_REBOUNDS": "AVG_COUNT_OFFENSIVE_REBOUNDS",
    "AVG_DEF_REBOUNDS": "AVG_COUNT_DEFENSIVE_REBOUNDS",
    "AVG_TOT_REBOUNDS": "AVG_COUNT_REBOUNDS",
    "AVG_ASSISTS": "AVG_COUNT_ASSISTS",
    "AVG_STEALS": "AVG_COUNT_STEALS",
    "AVG_BLOCKS": "AVG_COUNT_BLOCKS",
    "AVG_TOT_TURNOVERS": "AVG_COUNT_TURNOVERS",
    "AVG_FOULS": "AVG_COUNT_FOULS",
    "AVG_PTS_SCORED": "AVG_POINTS_SCORED",
    "AVG_PLUS_MINUS_POINTS": "AVG_PLUS_MINUS_POINTS",
    "AVG_PTS_AGAINST": "AVG_POINTS_AGAINST",
    "per_pts_off_assists": "PERCENT_POINTS_OFF_ASSISTS_MADE",
    "per_paintshots": "PERCENT_PAINTSHOTS_MADE",
    "per_jumpshots": "PERCENT_JUMPSHOTS_MADE",
    "per_freethrows": "PERCENT_FREETHROWS_MADE",
    "per_secondchance": "PERCENT_SECOND_CHANCE_OPPORTUNITIES_MADE",
}

undo_rename_cols_dict = {
    "COUNT_GAMES_PLAYED": "GAME_COUNT",
    "AVG_FIELD_GOALS_MADE": "AVG_FIELD_GOALS_MADE",
    "AVG_FIELD_GOALS_ATTEMPTED": "AVG_FIELD_GOALS_ATT",
    "AVG_FIELD_GOAL_PERCENT": "AVG_FIELD_GOAL_PCT",
    "VARIANCE_FIELD_GOAL_PERCENT": "VAR_FIELD_GOAL_PCT",
    "AVG_THREE_POINT_FIELD_GOALS_MADE": "AVG_THREE_PT_FIELD_GOALS_MADE",
    "AVG_THREE_POINT_FIELD_GOALS_ATTEMPTED": "AVG_THREE_PT_FIELD_GOALS_ATT",
    "AVG_THREE_POINT_FIELD_GOAL_PERCENT": "AVG_THREE_PT_FIELD_GOAL_PCT",
    "AVG_FREE_THROWS_MADE": "AVG_FREE_THROWS_MADE",
    "AVG_FREE_THROWS_ATTEMPTED": "AVG_FREE_THROWS_ATT",
    "AVG_FREE_THROW_PERCENT": "AVG_FREE_THROW_PCT",
    "AVG_COUNT_OFFENSIVE_REBOUNDS": "AVG_OFF_REBOUNDS",
    "AVG_COUNT_DEFENSIVE_REBOUNDS": "AVG_DEF_REBOUNDS",
    "AVG_COUNT_REBOUNDS": "AVG_TOT_REBOUNDS",
    "AVG_COUNT_ASSISTS": "AVG_ASSISTS",
    "AVG_COUNT_STEALS": "AVG_STEALS",
    "AVG_COUNT_BLOCKS": "AVG_BLOCKS",
    "AVG_COUNT_TURNOVERS": "AVG_TOT_TURNOVERS",
    "AVG_COUNT_FOULS": "AVG_FOULS",
    "AVG_POINTS_SCORED": "AVG_PTS_SCORED",
    "AVG_PLUS_MINUS_POINTS": "AVG_PLUS_MINUS_POINTS",
    "AVG_POINTS_AGAINST": "AVG_PTS_AGAINST",
    "PERCENT_POINTS_OFF_ASSISTS_MADE": "per_pts_off_assists",
    "PERCENT_PAINTSHOTS_MADE": "per_paintshots",
    "PERCENT_JUMPSHOTS_MADE": "per_jumpshots",
    "PERCENT_FREETHROWS_MADE": "per_freethrows",
    "PERCENT_SECOND_CHANCE_OPPORTUNITIES_MADE": "per_secondchance",
}


def retrieve_bigquery_variable_names_and_players():

    # Fetch NBA independent variables
    get_column_names_nba_query = """
        SELECT column_name
        FROM `team-23-mj-6242.team_23_dataset.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = 'combined_nba_data';
    """
    get_column_names_nba_query_job = client.query(get_column_names_nba_query)
    nba_independent_variables = get_column_names_nba_query_job.to_dataframe()
    nba_independent_variables = list(nba_independent_variables["column_name"])
    exclude_columns = [
        "SEASON_YEAR",
        "TEAM_ID",
        "TEAM_NAME",
        "TEAM_ABBREV",
        "season_wins",
        "season_winner",
    ]
    nba_independent_variables = [
        col for col in nba_independent_variables if col not in exclude_columns
    ]

    nba_independent_variables = [
        rename_cols_dict.get(item, item) for item in nba_independent_variables
    ]

    # Fetch WNBA independent variables
    get_column_names_wnba_query = """
        SELECT column_name
        FROM `team-23-mj-6242.team_23_dataset.INFORMATION_SCHEMA.COLUMNS`
        WHERE table_name = 'combined_wnba_data';
    """
    get_column_names_wnba_query_job = client.query(get_column_names_wnba_query)
    wnba_independent_variables = get_column_names_wnba_query_job.to_dataframe()
    wnba_independent_variables = list(
        wnba_independent_variables["column_name"]
    )
    wnba_exclude_columns = [
        "TEAM_LOC",
        "SEASON",
        "TEAM_ID",
        "TEAM_NAME",
        "TEAM_MASCOT",
        "TEAM_ABBREV",
        "wins",
    ]
    wnba_independent_variables = [
        col
        for col in wnba_independent_variables
        if col not in wnba_exclude_columns
    ]

    wnba_independent_variables = [
        rename_cols_dict.get(item, item) for item in wnba_independent_variables
    ]

    # Fetch distinct player-year combinations for the initial dropdown
    get_player_year_query = f"""
    SELECT DISTINCT PLAYER_NAME, SEASON_YEAR
    FROM {TABLE_NAME}
    ORDER BY PLAYER_NAME, SEASON_YEAR
    """
    player_year_df = client.query(get_player_year_query).to_dataframe()
    # Create 'PLAYER_YEAR' column for display
    player_year_df["PLAYER_YEAR"] = (
        player_year_df["PLAYER_NAME"]
        + " - "
        + player_year_df["SEASON_YEAR"].astype(str)
    )

    return (
        player_year_df,
        nba_independent_variables,
        wnba_independent_variables,
    )


def combine_wnba_nba_tables_and_metrics() -> Tuple[pd.DataFrame, pd.DataFrame]:
    client = bigquery.Client()

    get_combined_nba_data_query = """
        SELECT 
            *
        FROM 
            `team-23-mj-6242.team_23_dataset.combined_nba_data`
    """

    get_combined_nba_data_query_job = client.query(get_combined_nba_data_query)

    combined_nba_data_frame = get_combined_nba_data_query_job.to_dataframe()

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

    metrics = list(df.columns)
    columns_to_exclude = [
        "SEASON_YEAR",
        "TEAM_LOC",
        "TEAM_LOC" "SEASON_YEAR",
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
    # Scale to range [0.1, 1]
    df[metrics] = df[metrics] * 0.9 + 0.1

    return df, metrics


def draw_nba_court(fig=None):
    if fig is None:
        fig = go.Figure()

    court_shapes = []

    court_shapes.append(
        dict(
            type="rect",
            x0=-250,
            y0=-52,
            x1=250,
            y1=418,
            line=dict(color="black", width=2),
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="circle",
            x0=-7.5,
            y0=0 - 7.5,
            x1=7.5,
            y1=0 + 7.5,
            line=dict(color="black", width=2),
            fillcolor="white",
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="line",
            x0=-30,
            y0=-7.5,
            x1=30,
            y1=-7.5,
            line=dict(color="black", width=2),
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="rect",
            x0=-80,
            y0=-52,
            x1=80,
            y1=138,
            line=dict(color="black", width=2),
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="path",
            path="M -60 138 A 60 60 0 0 1 60 138",
            line=dict(color="black", width=2),
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="path",
            path="M -60 138 A 60 60 0 0 0 60 138",
            line=dict(color="black", width=2, dash="dash"),
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="path",
            path="M -40 0 A 40 40 0 0 1 40 0",
            line=dict(color="black", width=2),
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="path",
            path="M -220 92.5 A 237.5 237.5 0 0 1 220 92.5",
            line=dict(color="black", width=2),
            layer="below",
        )
    )

    court_shapes.append(
        dict(
            type="line",
            x0=-220,
            y0=-52,
            x1=-220,
            y1=92.5,
            line=dict(color="black", width=2),
            layer="below",
        )
    )
    court_shapes.append(
        dict(
            type="line",
            x0=220,
            y0=-52,
            x1=220,
            y1=92.5,
            line=dict(color="black", width=2),
            layer="below",
        )
    )

    fig.update_layout(shapes=court_shapes)

    fig.update_layout(
        xaxis=dict(
            range=[-250, 250],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            fixedrange=True,
        ),
        yaxis=dict(
            range=[-52, 418],
            showgrid=False,
            zeroline=False,
            showticklabels=False,
            scaleanchor="x",
            scaleratio=1,
            fixedrange=True,
        ),
        height=500,
        width=470,
        plot_bgcolor="white",
        margin=dict(l=0, r=0, t=0, b=0),
    )

    return fig


df, metrics = combine_wnba_nba_tables_and_metrics()
player_year_df, nba_independent_variables, wnba_independent_variables = (
    retrieve_bigquery_variable_names_and_players()
)

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app_layout = create_layout(df, player_year_df)

app.layout = app_layout


# Callback to update independent variables based on selected league
@app.callback(
    Output("independent-vars-dropdown", "options"),
    Input("league-dropdown", "value"),
)
def update_independent_vars_options(league):
    if league == "NBA":
        options = [
            {"label": var, "value": var} for var in nba_independent_variables
        ]
    elif league == "WNBA":
        options = [
            {"label": var, "value": var} for var in wnba_independent_variables
        ]
    else:
        options = []
    return options


@app.callback(
    Output("independent-vars-inputs", "children"),
    Input("independent-vars-dropdown", "value"),
)
def update_independent_vars_inputs(selected_vars):
    inputs = []
    if selected_vars:
        for var in selected_vars:
            if "per_" in var or "_PCT" in var or "PERCENT" in var:
                # Limit inputs to 0 to 1 for these
                inputs.append(
                    html.Div(
                        [
                            html.Label(var),
                            dcc.Input(
                                id={
                                    "type": "independent-var-input",
                                    "index": var,
                                },
                                type="number",
                                min=0,
                                max=1,
                                step=0.01,
                                value=0,
                            ),
                        ],
                        style={"padding": "10px"},
                    )
                )
            else:
                inputs.append(
                    html.Div(
                        [
                            html.Label(var),
                            dcc.Input(
                                id={
                                    "type": "independent-var-input",
                                    "index": var,
                                },
                                type="number",
                                value=0,
                            ),
                        ],
                        style={"padding": "10px"},
                    )
                )
    return inputs


# Update LightGBM predictions and the graph
@app.callback(
    [
        Output("predicted-value", "children"),
        Output("prediction-history", "data"),
        Output("prediction-graph", "figure"),
    ],
    Input("submit-button", "n_clicks"),
    State("league-dropdown", "value"),
    State("independent-vars-dropdown", "value"),
    State({"type": "independent-var-input", "index": ALL}, "value"),
    State({"type": "independent-var-input", "index": ALL}, "id"),
    State("prediction-history", "data"),
)
def update_prediction(
    n_clicks, league, selected_vars, values, ids, history_data
):
    if n_clicks == 0:
        return (
            "Please select values and click Submit.",
            history_data,
            {"data": [], "layout": {"title": "No predictions yet."}},
        )

    if league == "NBA":
        bigquery_table_name = "combined_nba_data"
        dependent_var = "season_wins"
    elif league == "WNBA":
        bigquery_table_name = "combined_wnba_data"
        dependent_var = "wins"
    else:
        bigquery_table_name = ""
        dependent_var = ""

    var_values = {id["index"]: value for id, value in zip(ids, values)}

    selected_vars = [
        undo_rename_cols_dict.get(item, item) for item in selected_vars
    ]

    logger.debug(selected_vars)

    payload_data = {
        "bigquery_table_name": f"team-23-mj-6242.team_23_dataset.{bigquery_table_name}",
        "dependent_var": dependent_var,
        "independent_vars": selected_vars,
        "what_if_dict": var_values,
    }

    # Cloud Function URL
    url = "https://us-west1-team-23-mj-6242.cloudfunctions.net/train_lgbm"

    # Send POST request with payload
    try:
        response = requests.post(url, json=payload_data)
        response.raise_for_status()
        result = response.json()
        predicted_value = result.get("predicted_value")
        predicted_value = int(predicted_value)
        logger.info(f"The predicted value is: {predicted_value}")

        history_data["attempts"].append(n_clicks)
        history_data["predictions"].append(predicted_value)
        history_data["leagues"].append(league)

        figure = {
            "data": [],
            "layout": {
                "title": "Predicted Season Wins Over Attempts",
                "xaxis": {"title": "Attempt Number"},
                "yaxis": {"title": "Predicted Season Wins"},
            },
        }

        leagues = set(history_data["leagues"])
        colors = {"NBA": "blue", "WNBA": "red"}

        for lg in leagues:
            lg_attempts = [
                attempt
                for attempt, league in zip(
                    history_data["attempts"], history_data["leagues"]
                )
                if league == lg
            ]
            lg_predictions = [
                prediction
                for prediction, league in zip(
                    history_data["predictions"], history_data["leagues"]
                )
                if league == lg
            ]
            figure["data"].append(
                {
                    "x": lg_attempts,
                    "y": lg_predictions,
                    "type": "scatter",
                    "mode": "lines+markers",
                    "name": lg,
                    "marker": {"color": colors.get(lg, "black")},
                }
            )

        return (f"{predicted_value}", history_data, figure)
    except requests.exceptions.HTTPError as http_err:
        logger.error(f"HTTP error occurred: {http_err}")
        return (
            f"HTTP error occurred: {http_err}",
            history_data,
            dash.no_update,
        )
    except Exception as err:
        logger.error(f"Other error occurred: {err}")
        return (f"An error occurred: {err}", history_data, dash.no_update)


# Callback to update radar chart based on selected teams
@app.callback(
    Output("radar-chart", "figure"), [Input("team-selector", "value")]
)
def update_radar_chart(selected_teams):
    fig = go.Figure()

    # no need to exclude metrics anymore since the desired variables are selected below
    # excluded_metrics = [
    #     "AVG_TEAM_TURNOVERS",  # avg_tot_turnovers already exists
    #     "AVG_TURNOVERS",  # avg_tot_turnovers already exists
    #     "season_wins",  # not useful
    #     "wins",  # not useful
    #     "GAME_COUNT",  # not useful
    #     "VAR_FIELD_GOAL_PCT",  # not useful
    #     "AVG_TOT_REBOUNDS",  # since def and off rebounds are already there
    #     "AVG_PTS_AGAINST",  # not useful
    #     "AVG_PTS_SCORED",  # too direct
    #     "AVG_FREE_THROW_PCT",  # just to cut down more variables
    #     "AVG_FIELD_GOALS_ATT",  # just to cut down more variables
    #     "AVG_FIELD_GOALS_MADE",  # just to cut down more variables
    #     "AVG_THREE_PT_FIELD_GOALS_ATT",  # just to cut down more variables
    #     "AVG_FREE_THROWS_ATT",  # just to cut down more variables
    #     "AVG_STEALS",
    # ]

    # order the desired variables
    filtered_metrics = [
        "AVG_COUNT_ASSISTS",
        "PERCENT_POINTS_OFF_ASSISTS_MADE",
        "PERCENT_PAINTSHOTS_MADE",
        "PERCENT_JUMPSHOTS_MADE",
        "PERCENT_FREETHROWS_MADE",
        "PERCENT_SECOND_CHANCE_OPPORTUNITIES_MADE",
        "AVG_FIELD_GOAL_PERCENT",
        "AVG_THREE_POINT_FIELD_GOAL_PERCENT",
        "AVG_THREE_POINT_FIELD_GOALS_MADE",
        "AVG_FREE_THROW_PERCENT",
        "AVG_FREE_THROWS_MADE",
        "AVG_COUNT_OFFENSIVE_REBOUNDS",
        "AVG_COUNT_DEFENSIVE_REBOUNDS",
        "AVG_COUNT_BLOCKS",
        "AVG_COUNT_TURNOVERS",
        "AVG_COUNT_FOULS",
    ]

    filtered_metrics = [
        rename_cols_dict.get(item, item) for item in filtered_metrics
    ]

    for team_season in selected_teams:
        # update parsing to new format
        league_team, season = team_season.rsplit(" (", 1)
        league, team = league_team.split(" - ", 1)
        season = season.rstrip(")")

        # Filter the DataFrame for the selected team and season
        team_data = df[
            (df["TEAM_NAME"] == team)
            & (df["SEASON_YEAR"] == season)
            & (df["league"] == league)
        ]

        if not team_data.empty:
            team_data = team_data.rename(columns=rename_cols_dict)
            league_data = df[df["league"] == league]
            league_data = league_data.rename(columns=rename_cols_dict)

            # normalizing wnba data within wnba data and nba data within nba data
            normalized_data = (
                team_data[filtered_metrics]
                - league_data[filtered_metrics].min()
            ) / (
                league_data[filtered_metrics].max()
                - league_data[filtered_metrics].min()
            )
            normalized_data = normalized_data * 0.9 + 0.1  # Scale to [0.1, 1]

            r = normalized_data[filtered_metrics].iloc[0].values
            theta = filtered_metrics

            fig.add_trace(
                go.Scatterpolar(
                    r=r,
                    theta=theta,
                    fill="toself",
                    name=f"{league} - {team} ({season})",
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
        title="Team Comparison Radar Chart",
    )

    return fig


# # Combined callback to update team and date dropdowns based on selected player-year and team
# @app.callback(
#     [
#         Output("team-dropdown", "options"),
#         Output("team-dropdown", "value"),
#         Output("date-dropdown", "options"),
#         Output("date-dropdown", "value"),
#     ],
#     [
#         Input("player-year-dropdown", "value"),
#         Input("team-dropdown", "value"),
#     ],
# )
# def update_team_and_date_dropdowns(selected_player_year, selected_team):
#     if selected_player_year:
#         player_name, season_year = selected_player_year.split(" - ")
#         get_teams_query = f"""
#         SELECT DISTINCT team_playing_against
#         FROM {TABLE_NAME}
#         WHERE PLAYER_NAME = @player_name AND SEASON_YEAR = @season_year
#         ORDER BY team_playing_against
#         """
#         job_config_teams = bigquery.QueryJobConfig(
#             query_parameters=[
#                 bigquery.ScalarQueryParameter(
#                     "player_name", "STRING", player_name
#                 ),
#                 bigquery.ScalarQueryParameter(
#                     "season_year", "INT64", int(season_year)
#                 ),
#             ]
#         )
#         teams_df = client.query(
#             get_teams_query, job_config=job_config_teams
#         ).to_dataframe()
#         team_options = [
#             {"label": team, "value": team}
#             for team in teams_df["team_playing_against"].unique()
#         ]
#
#         if selected_team:
#             get_dates_query = f"""
#             SELECT DISTINCT GAME_DATE
#             FROM {TABLE_NAME}
#             WHERE PLAYER_NAME = @player_name AND SEASON_YEAR = @season_year
#               AND team_playing_against = @team_playing_against
#             ORDER BY GAME_DATE
#             """
#             job_config_dates = bigquery.QueryJobConfig(
#                 query_parameters=[
#                     bigquery.ScalarQueryParameter(
#                         "player_name", "STRING", player_name
#                     ),
#                     bigquery.ScalarQueryParameter(
#                         "season_year", "INT64", int(season_year)
#                     ),
#                     bigquery.ScalarQueryParameter(
#                         "team_playing_against", "STRING", selected_team
#                     ),
#                 ]
#             )
#             dates_df = client.query(
#                 get_dates_query, job_config=job_config_dates
#             ).to_dataframe()
#             dates_df["GAME_DATE_STR"] = pd.to_datetime(
#                 dates_df["GAME_DATE"].astype(str), format="%Y%m%d"
#             ).dt.strftime("%Y-%m-%d")
#             date_options = [
#                 {"label": date_str, "value": date_str}
#                 for date_str in dates_df["GAME_DATE_STR"].unique()
#             ]
#             return (
#                 team_options,
#                 selected_team,
#                 date_options,
#                 None,
#             )
#         else:
#             return (
#                 team_options,
#                 None,
#                 [],
#                 None,
#             )
#     else:
#         return (
#             [],
#             None,
#             [],
#             None,
#         )


# # Update shot chart based on all the filters
# @app.callback(
#     Output("shot-chart", "figure"),
#     [
#         Input("player-year-dropdown", "value"),
#         Input("team-dropdown", "value"),
#         Input("date-dropdown", "value"),
#     ],
# )
# def update_figure(selected_player_year, selected_team, selected_date):
#     if selected_player_year and selected_team and selected_date:
#         player_name, season_year = selected_player_year.split(" - ")
#         game_date_int = int(pd.to_datetime(selected_date).strftime("%Y%m%d"))
#         get_shot_data_query = f"""
#         SELECT *
#         FROM {TABLE_NAME}
#         WHERE PLAYER_NAME = @player_name AND SEASON_YEAR = @season_year
#           AND team_playing_against = @team_playing_against AND GAME_DATE = @game_date
#         """
#         job_config = bigquery.QueryJobConfig(
#             query_parameters=[
#                 bigquery.ScalarQueryParameter(
#                     "player_name", "STRING", player_name
#                 ),
#                 bigquery.ScalarQueryParameter(
#                     "season_year", "INT64", int(season_year)
#                 ),
#                 bigquery.ScalarQueryParameter(
#                     "team_playing_against", "STRING", selected_team
#                 ),
#                 bigquery.ScalarQueryParameter(
#                     "game_date", "INT64", game_date_int
#                 ),
#             ]
#         )
#         shot_data_df = client.query(
#             get_shot_data_query, job_config=job_config
#         ).to_dataframe()
#
#         if shot_data_df.empty:
#             fig = go.Figure()
#             fig.update_layout(
#                 title="No data available for the selected filters.",
#                 xaxis_title="LOC_X (Court Width)",
#                 yaxis_title="LOC_Y (Court Length)",
#             )
#             return fig
#
#         shot_data_df["SHOT_RESULT"] = shot_data_df["SHOT_MADE_FLAG"].map(
#             {0: "Missed", 1: "Made"}
#         )
#
#         fig = draw_nba_court()
#
#         fig.add_trace(
#             go.Scatter(
#                 x=shot_data_df["LOC_X"],
#                 y=shot_data_df["LOC_Y"],
#                 mode="markers",
#                 marker=dict(
#                     size=7,
#                     color=shot_data_df["SHOT_RESULT"].map(
#                         {"Made": "green", "Missed": "red"}
#                     ),
#                     symbol=shot_data_df["SHOT_RESULT"].map(
#                         {"Made": "circle", "Missed": "x"}
#                     ),
#                     line=dict(width=1, color="black"),
#                 ),
#                 hoverinfo="text",
#                 text=(
#                     "Shot Type: "
#                     + shot_data_df["SHOT_TYPE"]
#                     + "<br>Shot Distance: "
#                     + shot_data_df["SHOT_DISTANCE"].astype(str)
#                     + " ft"
#                     + "<br>Result: "
#                     + shot_data_df["SHOT_RESULT"]
#                 ),
#                 name="Shots",
#             )
#         )
#
#         fig.update_xaxes(
#             range=[-250, 250],
#             showgrid=False,
#             zeroline=False,
#             showticklabels=False,
#             fixedrange=True,
#         )
#         fig.update_yaxes(
#             range=[-52, 418],
#             showgrid=False,
#             zeroline=False,
#             showticklabels=False,
#             scaleanchor="x",
#             scaleratio=1,
#             fixedrange=True,
#         )
#
#         fig.update_layout(
#             title_text=f"{player_name} vs {selected_team}",
#             margin=dict(l=0, r=0, t=50, b=0),
#             showlegend=False,
#             plot_bgcolor="white",
#         )
#
#         return fig
#     else:
#         fig = go.Figure()
#         fig.update_layout(
#             title="Please select all filters to view the shot chart.",
#             xaxis_title="LOC_X (Court Width)",
#             yaxis_title="LOC_Y (Court Length)",
#         )
#         return fig


# Callback to populate dropdown options from NBA data
@app.callback(
    Output("stacked-bar-chart-nba", "figure"),
    Output("season-dropdown-nba", "options"),
    Input("season-dropdown-nba", "value"),
)
def update_nba_graph(selected_season):
    # Query for available seasons
    seasons_query = """
    SELECT DISTINCT season_year
    FROM `team-23-mj-6242.team_23_dataset.new_nba_stack`
    ORDER BY season_year DESC
    """

    seasons_df = client.query(seasons_query).to_dataframe()
    season_options = [
        {"label": str(year), "value": year}
        for year in seasons_df["season_year"]
    ]

    if selected_season is None:
        return (
            {},
            season_options,
        )  # No chart displayed if no season is selected

    # Query for the selected season's data
    play_data_query = f"""
    SELECT
        *
    FROM 
        `team-23-mj-6242.team_23_dataset.new_nba_stack`
    WHERE 
        season_year = {int(selected_season)}
    """

    # play_data_query = f"""
    # SELECT team_name, season_year, paintshot_count, jumpshot_count,
    #        secondchancepaintshot_count, freethrow_count
    # FROM `team-23-mj-6242.team_23_dataset.new_nba_stack`
    # WHERE season_year = {int(selected_season)}
    # """

    play_data = client.query(play_data_query).to_dataframe()

    play_data = play_data.query("team_rank <= 5")

    play_data = play_data.pivot(
        index=["score_team", "season_year"],
        columns="play_category",
        values="count_observations",
    )

    play_data = play_data.reset_index().rename(
        columns={
            "PAINTSHOT": "paintshot_count",
            "JUMPSHOT": "jumpshot_count",
            "SECONDCHANCE": "secondchancepaintshot_count",
            "FREETHROW": "freethrow_count",
            "score_team": "team_name",
        }
    )

    # Calculate the total count for each team to normalize to percentages
    play_data["total_count"] = (
        play_data["paintshot_count"]
        + play_data["jumpshot_count"]
        + play_data["secondchancepaintshot_count"]
        + play_data["freethrow_count"]
    )

    # Reshape the data into long format for the stacked bar chart
    play_data_long = play_data.melt(
        id_vars=["team_name", "season_year", "total_count"],
        value_vars=[
            "paintshot_count",
            "jumpshot_count",
            "secondchancepaintshot_count",
            "freethrow_count",
        ],
        var_name="play_type",
        value_name="count",
    )

    # Calculate percentage for each play type
    play_data_long["percentage"] = (
        play_data_long["count"] / play_data_long["total_count"] * 100
    )

    # Create the stacked bar chart with percentages
    fig = px.bar(
        play_data_long,
        x="team_name",
        y="count",
        color="play_type",
        title=f"Successful Play Type Shot Distribution by Top 5 Teams in {selected_season} Regular Season",
        labels={"team_name": "Team Name", "percentage": "Percentage (%)"},
        height=600,
        text="percentage",
    )

    # Format the percentages to display with one decimal place
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")

    fig.update_layout(
        yaxis_title="Shot Counts", xaxis_title="Team Name", barmode="stack"
    )

    return fig, season_options


################################################


#######################################################################################################
@app.callback(
    Output("stacked-bar-chart-wnba", "figure"),
    Output("season-dropdown-wnba", "options"),
    Input("season-dropdown-wnba", "value"),
)
def update_wnba_graph(selected_season):
    # Query for available seasons
    seasons_query = """
    SELECT DISTINCT season
    FROM `team-23-mj-6242.team_23_dataset.new_wnba_stack`
    ORDER BY season DESC
    """

    seasons_df = client.query(seasons_query).to_dataframe()
    season_options = [
        {"label": str(year), "value": year} for year in seasons_df["season"]
    ]

    if selected_season is None:
        return (
            {},  # Empty figure if no season is selected
            season_options,
        )
    # Query for the selected season's data
    play_data_query = f"""
    SELECT team_name, season, paintshot_count, jumpshot_count, 
           secondchancepaintshot_count, freethrow_count
    FROM `team-23-mj-6242.team_23_dataset.new_wnba_stack`
    WHERE season = {int(selected_season)}
    """

    play_data = client.query(play_data_query).to_dataframe()

    # Calculate the total count for each team to normalize to percentages
    play_data["total_count"] = (
        play_data["paintshot_count"]
        + play_data["jumpshot_count"]
        + play_data["secondchancepaintshot_count"]
        + play_data["freethrow_count"]
    )

    # Reshape the data into long format for the stacked bar chart
    play_data_long = play_data.melt(
        id_vars=["team_name", "season", "total_count"],
        value_vars=[
            "paintshot_count",
            "jumpshot_count",
            "secondchancepaintshot_count",
            "freethrow_count",
        ],
        var_name="play_type",
        value_name="count",
    )

    # Calculate percentage for each play type
    play_data_long["percentage"] = (
        play_data_long["count"] / play_data_long["total_count"] * 100
    )

    # Create the stacked bar chart with percentages
    fig = px.bar(
        play_data_long,
        x="team_name",
        y="count",
        color="play_type",
        title=f"Successful Play Type Shot Distribution by Top 5 Teams in {selected_season} Regular Season",
        labels={"team_name": "Team Name", "percentage": "Percentage (%)"},
        height=600,
        text="percentage",
    )

    # Format the percentages to display with one decimal place
    fig.update_traces(texttemplate="%{text:.1f}%", textposition="inside")

    fig.update_layout(
        yaxis_title="Shot Counts", xaxis_title="Team Name", barmode="stack"
    )

    return fig, season_options


# Callback to open/close dictionary popup
@app.callback(
    Output("popup-modal", "is_open"),
    [Input("open-popup", "n_clicks"), Input("close-popup", "n_clicks")],
    [State("popup-modal", "is_open")],
)
def toggle_modal(open_clicks, close_clicks, is_open):
    if open_clicks or close_clicks:
        return not is_open
    return is_open


# Uncomment this if you're running it locally
# Comment it out again if you're committing
# if __name__ == "__main__":
#
#     app.run_server(debug=True, port=8051)
