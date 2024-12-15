# Import packages
from dash import Dash, html
import dash_bootstrap_components as dbc

# Tableau URL
url = "https://public.tableau.com/views/ShotChartDashboard/ShotChartComparison?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link"

# Initialize app
# app = Dash()
app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

# App layout
# fmt: off
app.layout = html.Div(
    [
        dbc.Button(" Click for League Shot Chart Comparison", color = "primary", size = "lg",
        href= url)
    ],
    className="d-grid gap-2 col-6 mx-auto",
)

app.run(debug=True)
# fmt: on
