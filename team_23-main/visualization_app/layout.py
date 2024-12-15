import dash_bootstrap_components as dbc

from dash import html, dcc


nba_wnba_stats_dict = {
    "COUNT_GAMES_PLAYED": "The total number of games played in the regular season.",
    "AVG_FIELD_GOALS_MADE": "The average number of field goals made per game.",
    "AVG_FIELD_GOALS_ATTEMPTED": "The average number of field goal attempts per game.",
    "AVG_FIELD_GOAL_PERCENT": "The average field goal shooting percentage per game.",
    "VARIANCE_FIELD_GOAL_PERCENT": "The variance in field goal shooting percentage across games.",
    "AVG_THREE_POINT_FIELD_GOALS_MADE": "The average number of three-point field goals made per game.",
    "AVG_THREE_POINT_FIELD_GOALS_ATTEMPTED": "The average number of three-point field goals attempted per game.",
    "AVG_THREE_POINT_FIELD_GOAL_PERCENT": "The average shooting percentage for three-point field goals per game.",
    "AVG_FREE_THROWS_MADE": "The average number of free throws made per game.",
    "AVG_FREE_THROWS_ATTEMPTED": "The average number of free throws attempted per game.",
    "AVG_FREE_THROW_PERCENT": "The average free throw shooting percentage per game.",
    "AVG_COUNT_OFFENSIVE_REBOUNDS": "The average number of offensive rebounds per game.",
    "AVG_COUNT_DEFENSIVE_REBOUNDS": "The average number of defensive rebounds per game.",
    "AVG_COUNT_REBOUNDS": "The average total rebounds (offensive and defensive) per game.",
    "AVG_COUNT_ASSISTS": "The average number of assists per game.",
    "AVG_COUNT_STEALS": "The average number of steals per game.",
    "AVG_COUNT_BLOCKS": "The average number of blocks per game.",
    "AVG_COUNT_TURNOVERS": "The average number of turnovers per game.",
    "AVG_COUNT_FOULS": "The average number of personal fouls committed per game.",
    "AVG_POINTS_SCORED": "The average number of points scored per game.",
    "AVG_PLUS_MINUS_POINTS": "The average plus-minus score per game.",
    "AVG_POINTS_AGAINST": "The average number of points scored by the opposing team per game.",
    "PERCENT_POINTS_OFF_ASSISTS_MADE": "The percentage of total points scored that were assisted.",
    "PERCENT_PAINTSHOTS_MADE": "The percentage of total shots made that were from the paint.",
    "PERCENT_JUMPSHOTS_MADE": "The percentage of total shots made that were jump shots.",
    "PERCENT_FREETHROWS_MADE": "The percentage of total points that came from free throws.",
    "PERCENT_SECOND_CHANCE_OPPORTUNITIES_MADE": "The percentage of total shots made that "
    "were second-chance opportunities (Miss and try scoring again)",
}


variable_list = html.Ul(
    [html.Li(f"{key}: {value}") for key, value in nba_wnba_stats_dict.items()]
)


def create_layout(df, player_year_df):
    # Tableau URL
    url = (
        "https://public.tableau.com/views/ShotChartDashboard/ShotChartComparison?"
        ":language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"
    )

    guiding_texts = {
        "Introduction": "Welcome to the WNBA/NBA Success Visualization App! This tool lets you explore team dynamics, compare playstyles, and predict outcomes across the WNBA and NBA. To get started, check out the definitions of key basketball terms by clicking the button below.",
        "Radar Chart": "First, let's start with the radar chart. This chart allows you to compare teams' overall performance across multiple metrics. For example, see how the 2023 WNBA champs, the Aces, excel in 3-point shooting, while the NBA champs, the Nuggets, shine in team assists and points off of assists. Select your favorite teams and discover their strengths!",
        "Shot Type Distribution": "Next, now that you have an idea of how teams compare, let's dive deeper into their offensive strategies. The shot type chart highlights the composition of shot types made by each team. Are they more reliant on paint shots, jump shots, or free throws? Use the dropdown to explore how the top five best teams in each league build their offense.",
        "Shot Chart": "Breaking shot types down further, the shot chart provides a detailed view of where teams score on the court. Visualize shot locations to see if teams favor mid-range shots, the paint, or beyond the arc.",
        "What-If Tool": "Putting it all together, the Wins Predictor Tool lets you simulate team performance by adjusting key metrics like field goal percentage, turnovers, and defensive rebounds to predict season wins. For reference, the 2023 NBA champion Denver Nuggets recorded a 50% field goal percentage, 14 turnovers per game, and 33 defensive rebounds per game. Similarly, the 2023 WNBA champion Las Vegas Aces averaged 21 assists per game, 16 fouls per game, and 29 defensive rebounds per game. Try starting with these values, then see how slight changes in these metrics could affect their win totals or explore how other teams might emulate their success! Note: The NBA regular season consists of 82 games, while the WNBA regular season consists of 40 games.",
    }

    alert_style = {
        "margin": "10px",
        "font-family": "'Arial', sans-serif",
        "font-size": "18px",
        "padding": "20px",
        "border-radius": "10px",
        "background-color": "#f8f9fa",
        "color": "#495057",
        "box-shadow": "0px 4px 8px rgba(0, 0, 0, 0.1)",
    }

    app_layout = (
        html.Div(
            [
                html.H1(
                    "WNBA/NBA Success Visualization App",
                    style={"textAlign": "center"},
                ),
                dbc.Alert(
                    guiding_texts["Introduction"],
                    color="light",
                    style=alert_style,
                ),
                # Data Dictionary button below
                dbc.Row(
                    dbc.Col(
                        dbc.Button(
                            "Click to Show Data Dictionary",
                            id="open-popup",
                            n_clicks=0,
                            color="primary",
                            size="lg",
                            className="mt-3 mb-3",
                            style={
                                "font-weight": "bold",
                                "border-radius": "8px",
                            },
                        ),
                        width="auto",
                    ),
                    justify="center",
                ),
                dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("Data Dictionary")),
                        dbc.ModalBody(variable_list),
                        dbc.ModalFooter(
                            dbc.Button(
                                "Close", id="close-popup", className="ml-auto"
                            )
                        ),
                    ],
                    id="popup-modal",
                    is_open=False,
                    size="lg",
                ),
                # Radar Chart Section
                html.H2(
                    "🎯NBA/WNBA Team Comparison Radar Chart",
                    style={"textAlign": "center"},
                ),
                dbc.Alert(
                    guiding_texts["Radar Chart"],
                    color="light",
                    style=alert_style,
                ),
                html.Div(
                    [
                        html.Label("Select Teams:"),
                        dcc.Dropdown(
                            id="team-selector",
                            options=[
                                {
                                    # updated labels to show NBA/WNBA
                                    "label": f"{row['league']} - {row['TEAM_NAME']} ({row['SEASON_YEAR']})",
                                    "value": f"{row['league']} - {row['TEAM_NAME']} ({row['SEASON_YEAR']})",
                                }
                                for _, row in df.iterrows()
                            ],
                            multi=True,
                            value=[
                                "NBA - Nuggets (2023)",
                                "WNBA - Aces (2023)",
                            ],
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
        ),
        html.H2(
            "📊Shot Type Count by Team and Season",
            style={"textAlign": "center"},
        ),
        dbc.Alert(
            guiding_texts["Shot Type Distribution"],
            color="light",
            style=alert_style,
        ),
        html.H3(
            "NBA Shot Type Count by Team and Season",
            style={"textAlign": "center"},
        ),
        # Dropdown for Season Year
        dcc.Dropdown(
            id="season-dropdown-nba",
            options=[],
            placeholder="Select a season",
        ),
        dcc.Graph(id="stacked-bar-chart-nba"),
        html.H3(
            "WNBA Shot Type Count by Team and Season",
            style={"textAlign": "center"},
        ),
        # Dropdown for Season Year
        dcc.Dropdown(
            id="season-dropdown-wnba",
            options=[],
            placeholder="Select a season",
        ),
        dcc.Graph(id="stacked-bar-chart-wnba"),
        # # Coordinate Shot Chart Section
        # html.Div(
        #     [
        #         html.H1(
        #             "Coordinate Shot Chart", style={"textAlign": "center"}
        #         ),
        #         # Dropdowns for player-year, team, and date
        #         dcc.Dropdown(
        #             id="player-year-dropdown",
        #             options=[
        #                 {"label": player_year, "value": player_year}
        #                 for player_year in player_year_df[
        #                     "PLAYER_YEAR"
        #                 ].unique()
        #             ],
        #             value="Zion Williamson - 2024",
        #             placeholder="Select Player - Year",
        #         ),
        #         dcc.Dropdown(
        #             id="team-dropdown",
        #             options=[],
        #             value="Atlanta Hawks",
        #             placeholder="Select Opposing Team",
        #         ),
        #         dcc.Dropdown(
        #             id="date-dropdown",
        #             options=[],
        #             value="2023-11-04",
        #             placeholder="Select Game Date",
        #         ),
        #         html.Div(
        #             dcc.Graph(
        #                 id="shot-chart",
        #                 style={"width": "80%", "height": "auto"},
        #             ),
        #             style={
        #                 "display": "flex",
        #                 "justifyContent": "center",
        #                 "alignItems": "center",
        #             },
        #         ),
        #     ]
        # ),
        html.H2("🏀Shot Chart", style={"textAlign": "center"}),
        dbc.Alert(
            guiding_texts["Shot Chart"], color="light", style=alert_style
        ),
        html.Div(
            [
                dbc.Button(
                    " Click for League Shot Chart Comparison",
                    color="primary",
                    size="lg",
                    href=url,
                )
            ],
            id="shot-chart-button",
            className="d-grid gap-2 col-6 mx-auto",
            style={"padding": "60px"},
        ),
        html.H1(
            "🔮NBA/WNBA Regular Season Wins Predictor",
            style={"textAlign": "center"},
        ),
        dbc.Alert(
            guiding_texts["What-If Tool"], color="light", style=alert_style
        ),
        dbc.Container(
            [
                # League Selection
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Select League"),
                                dcc.Dropdown(
                                    id="league-dropdown",
                                    options=[
                                        {"label": "NBA", "value": "NBA"},
                                        {"label": "WNBA", "value": "WNBA"},
                                    ],
                                    value="NBA",
                                ),
                            ],
                            width=12,
                        ),
                    ],
                    style={"padding": "10px"},
                ),
                # Independent Variable Selection
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Select Independent Variables"),
                                dcc.Dropdown(
                                    id="independent-vars-dropdown",
                                    options=[],
                                    multi=True,
                                ),
                            ],
                            width=12,
                        ),
                    ],
                    style={"padding": "10px"},
                ),
                # Dynamic Input Fields for Variables
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(id="independent-vars-inputs"),
                            width=12,
                        ),
                    ],
                    style={"padding": "10px"},
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Button(
                                    "Submit",
                                    id="submit-button",
                                    n_clicks=0,
                                    className="btn btn-primary",
                                    style={"marginTop": "20px"},
                                )
                            ],
                            width=12,
                            style={"textAlign": "center"},
                        ),
                    ]
                ),
                # Prediction Output
                html.H2("Predicted Season Wins:", style={"marginTop": "30px"}),
                dcc.Loading(
                    id="loading",
                    type="default",
                    children=html.Div(
                        id="predicted-value",
                        style={
                            "fontSize": 24,
                            "fontWeight": "bold",
                            "textAlign": "center",
                        },
                    ),
                ),
                # Prediction History Graph
                html.H2("Prediction History:", style={"marginTop": "40px"}),
                dcc.Graph(id="prediction-graph"),
                dcc.Store(
                    id="prediction-history",
                    data={
                        "attempts": [],
                        "predictions": [],
                        "leagues": [],
                    },
                ),
            ]
        ),
    )

    return app_layout
