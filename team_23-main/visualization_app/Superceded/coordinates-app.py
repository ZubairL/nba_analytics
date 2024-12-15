import dash
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

from google.cloud import bigquery
from dash import dcc, html
from dash.dependencies import Input, Output

# Initialize BigQuery client
client = bigquery.Client()

# Update the table name as requested
TABLE_NAME = "`team-23-mj-6242.team_23_dataset.combined_nba_coordinates`"

# Fetch distinct player-year combinations for the initial dropdown
get_player_year_query = f"""
SELECT DISTINCT PLAYER_NAME, SEASON_YEAR
FROM {TABLE_NAME}
ORDER BY PLAYER_NAME, SEASON_YEAR
"""
player_year_df = client.query(get_player_year_query).to_dataframe()
# Create a 'PLAYER_YEAR' column for display
player_year_df["PLAYER_YEAR"] = (
    player_year_df["PLAYER_NAME"]
    + " - "
    + player_year_df["SEASON_YEAR"].astype(str)
)


def draw_court(fig):
    # Define the court shapes
    court_shapes = [
        # Main court boundary (rotated)
        dict(
            type="rect",
            x0=0,
            y0=-250,
            x1=470,
            y1=250,
            line=dict(color="black", width=2),
            layer="below",
        ),
        # Backboard (rotated)
        dict(
            type="line",
            x0=0,
            y0=-30,
            x1=0,
            y1=30,
            line=dict(color="black", width=2),
        ),
        # Hoop (rotated)
        dict(
            type="circle",
            x0=7.5,
            y0=-7.5,
            x1=-7.5,
            y1=7.5,
            line=dict(color="orange", width=2),
            fillcolor="orange",
        ),
        # Restricted area (rotated)
        dict(
            type="circle",
            x0=0,
            y0=-40,
            x1=80,
            y1=40,
            line=dict(color="black", width=2),
        ),
        # Paint area (key rectangle, rotated)
        dict(
            type="rect",
            x0=0,
            y0=-80,
            x1=190,
            y1=80,
            line=dict(color="black", width=2),
            layer="below",
            fillcolor="rgba(0,0,0,0)",
        ),
        # Free throw line top arc (rotated)
        dict(
            type="circle",
            x0=190 - 60,
            y0=-60,
            x1=190 + 60,
            y1=60,
            line=dict(color="black", width=2),
        ),
        # Three-point line (arc, rotated)
        dict(
            type="path",
            path="M 0 -220 A 237.5 237.5 0 0 1 0 220",
            line=dict(color="black", width=2),
        ),
        # Half-court line (rotated)
        dict(
            type="line",
            x0=470,
            y0=-250,
            x1=470,
            y1=250,
            line=dict(color="black", width=2),
        ),
        # Center circle at half-court (rotated)
        dict(
            type="circle",
            x0=470 - 60,
            y0=-60,
            x1=470 + 60,
            y1=60,
            line=dict(color="black", width=2),
        ),
    ]

    # Add shapes to the figure
    fig.update_layout(shapes=court_shapes)

    # Hide axis lines and ticks for a cleaner look
    fig.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
    fig.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

    return fig


# Initialize the app
app = dash.Dash(__name__)

# Create the app layout
app.layout = html.Div(
    [
        html.H1("Basketball Shot Chart (Horizontal Court)"),
        # Dropdown to select player-year
        dcc.Dropdown(
            id="player-year-dropdown",
            options=[
                {"label": player_year, "value": player_year}
                for player_year in player_year_df["PLAYER_YEAR"].unique()
            ],
            value=None,
            placeholder="Select a player and season year",
        ),
        # Dropdown to select playing against team
        dcc.Dropdown(
            id="team-dropdown",
            options=[],
            value=None,
            placeholder="Select a team",
        ),
        # Dropdown to select game date
        dcc.Dropdown(
            id="date-dropdown",
            options=[],
            value=None,
            placeholder="Select a game date",
        ),
        # Graph to display the scatter plot
        dcc.Graph(id="shot-chart"),
    ]
)


# Combined callback to update team and date dropdowns based on selected player-year and team
@app.callback(
    [
        Output("team-dropdown", "options"),
        Output("team-dropdown", "value"),
        Output("date-dropdown", "options"),
        Output("date-dropdown", "value"),
    ],
    [
        Input("player-year-dropdown", "value"),
        Input("team-dropdown", "value"),
    ],
)
def update_team_and_date_dropdowns(selected_player_year, selected_team):
    if selected_player_year:
        # Parse player name and season year
        player_name, season_year = selected_player_year.split(" - ")
        # Use parameterized query to prevent SQL injection
        get_teams_query = f"""
        SELECT DISTINCT team_playing_against
        FROM {TABLE_NAME}
        WHERE PLAYER_NAME = @player_name AND SEASON_YEAR = @season_year
        ORDER BY team_playing_against
        """
        job_config_teams = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "player_name", "STRING", player_name
                ),
                bigquery.ScalarQueryParameter(
                    "season_year", "INT64", int(season_year)
                ),
            ]
        )
        teams_df = client.query(
            get_teams_query, job_config=job_config_teams
        ).to_dataframe()
        team_options = [
            {"label": team, "value": team}
            for team in teams_df["team_playing_against"].unique()
        ]

        if selected_team:
            # Get dates for the selected team
            get_dates_query = f"""
            SELECT DISTINCT GAME_DATE
            FROM {TABLE_NAME}
            WHERE PLAYER_NAME = @player_name AND SEASON_YEAR = @season_year
              AND team_playing_against = @team_playing_against
            ORDER BY GAME_DATE
            """
            job_config_dates = bigquery.QueryJobConfig(
                query_parameters=[
                    bigquery.ScalarQueryParameter(
                        "player_name", "STRING", player_name
                    ),
                    bigquery.ScalarQueryParameter(
                        "season_year", "INT64", int(season_year)
                    ),
                    bigquery.ScalarQueryParameter(
                        "team_playing_against", "STRING", selected_team
                    ),
                ]
            )
            dates_df = client.query(
                get_dates_query, job_config=job_config_dates
            ).to_dataframe()
            # Convert GAME_DATE from integer to string format YYYY-MM-DD
            dates_df["GAME_DATE_STR"] = pd.to_datetime(
                dates_df["GAME_DATE"].astype(str), format="%Y%m%d"
            ).dt.strftime("%Y-%m-%d")
            date_options = [
                {"label": date_str, "value": date_str}
                for date_str in dates_df["GAME_DATE_STR"].unique()
            ]
            return (
                team_options,
                selected_team,
                date_options,
                None,
            )  # Keep selected team, reset date
        else:
            return (
                team_options,
                None,
                [],
                None,
            )  # Reset team and date selections
    else:
        return (
            [],
            None,
            [],
            None,
        )  # Reset all selections if player-year is not selected


# Define the callback to update the graph based on the selected filters
@app.callback(
    Output("shot-chart", "figure"),
    [
        Input("player-year-dropdown", "value"),
        Input("team-dropdown", "value"),
        Input("date-dropdown", "value"),
    ],
)
def update_figure(selected_player_year, selected_team, selected_date):
    if selected_player_year and selected_team and selected_date:
        player_name, season_year = selected_player_year.split(" - ")
        # Convert selected_date back to GAME_DATE format (YYYYMMDD)
        game_date_int = int(pd.to_datetime(selected_date).strftime("%Y%m%d"))
        # Query BigQuery for the shot data
        get_shot_data_query = f"""
        SELECT *
        FROM {TABLE_NAME}
        WHERE PLAYER_NAME = @player_name AND SEASON_YEAR = @season_year
          AND team_playing_against = @team_playing_against AND GAME_DATE = @game_date
        """
        job_config = bigquery.QueryJobConfig(
            query_parameters=[
                bigquery.ScalarQueryParameter(
                    "player_name", "STRING", player_name
                ),
                bigquery.ScalarQueryParameter(
                    "season_year", "INT64", int(season_year)
                ),
                bigquery.ScalarQueryParameter(
                    "team_playing_against", "STRING", selected_team
                ),
                bigquery.ScalarQueryParameter(
                    "game_date", "INT64", game_date_int
                ),
            ]
        )
        shot_data_df = client.query(
            get_shot_data_query, job_config=job_config
        ).to_dataframe()

        if shot_data_df.empty:
            # Return an empty figure with a message
            fig = go.Figure()
            fig.update_layout(
                title="No data available for the selected filters.",
                xaxis_title="Location Y (Court Length)",
                yaxis_title="Location X (Court Width)",
            )
            return fig

        # Create 'SHOT_RESULT' column
        shot_data_df["SHOT_RESULT"] = shot_data_df["SHOT_MADE_FLAG"].map(
            {0: "Missed", 1: "Made"}
        )
        # Create the scatter plot
        fig = px.scatter(
            shot_data_df,
            x="LOC_Y",
            y="LOC_X",
            color="SHOT_RESULT",
            color_discrete_map={"Missed": "red", "Made": "green"},
            labels={"SHOT_RESULT": "Shot Result"},
            hover_data=["SHOT_TYPE", "SHOT_DISTANCE"],
            title=f"Shot Chart for {player_name} on {selected_date} vs {selected_team}",
        )

        # Set axes ranges and update layout
        fig.update_xaxes(range=[-50, 420], fixedrange=True)
        fig.update_yaxes(range=[-250, 250], fixedrange=True)
        fig.update_layout(
            xaxis_title="Location Y (Court Length)",
            yaxis_title="Location X (Court Width)",
            yaxis=dict(scaleanchor="x", scaleratio=1),
            transition_duration=500,
            plot_bgcolor="lightgray",
        )

        fig = draw_court(fig)

        return fig
    else:
        # Return an empty figure prompting user to make selections
        fig = go.Figure()
        fig.update_layout(
            title="Please select all filters to view the shot chart.",
            xaxis_title="Location Y (Court Length)",
            yaxis_title="Location X (Court Width)",
        )
        return fig


# Run the app
if __name__ == "__main__":
    app.run_server(debug=True)
