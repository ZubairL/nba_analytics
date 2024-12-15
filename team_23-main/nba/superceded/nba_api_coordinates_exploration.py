import pandas

from nba_api.stats.endpoints import shotchartdetail
from google.cloud import bigquery
from loguru import logger

response = shotchartdetail.ShotChartDetail(
    team_id="1610612737",
    player_id="1628416",
    game_id_nullable="0021800007",
    context_measure_simple="FGA",  # <-- Default is 'PTS' and will only return made shots, but we want all shot attempts
)

shot_df = response.get_data_frames()[0]


leauge_df = response.get_data_frames()[1]
