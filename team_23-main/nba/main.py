import time
import pandas

from itertools import product
from loguru import logger
from nba_api.stats.library.parameters import SeasonType

from nba.play_by_play import get_game_id_history, get_play_by_play


def get_play_by_play_frame(demo_mode="No") -> pandas.DataFrame:

    if demo_mode == "Yes":
        game_seasons = ["2023-24"]
        nba_teams = ["BOS"]

    else:
        game_seasons = [
            "2018-19",
            "2019-20",
            "2020-21",
            "2021-22",
            "2022-23",
            "2023-24",
        ]

        nba_teams = [
            "ATL",
            "BOS",
            "BKN",
            "CHA",
            "CHI",
            "CLE",
            "DAL",
            "DEN",
            "DET",
            "GSW",
            "HOU",
            "IND",
            "LAC",
            "LAL",
            "MEM",
            "MIA",
            "MIL",
            "MIN",
            "NOP",
            "NYK",
            "OKC",
            "ORL",
            "PHI",
            "PHX",
            "POR",
            "SAC",
            "SAS",
            "TOR",
            "UTA",
            "WAS",
        ]

    nba_teams_play_by_play = []

    for season, team in product(game_seasons, nba_teams):
        game_id_frame = get_game_id_history(
            team, season=season, season_type=SeasonType.regular
        )
        count_games = len(game_id_frame)
        logger.debug(f"Count games is {count_games}.")

        if demo_mode == "Yes":
            count_games = 3

        for i in range(count_games):
            try:
                logger.debug(f"Team {team} - Game {i} of {count_games}.")
                time.sleep(2)
                play_by_play_frame = get_play_by_play(game_id_frame, i)
                nba_teams_play_by_play.append(play_by_play_frame)
            except Exception:
                pass

    all_nba_teams_play_by_play_frame = pandas.concat(nba_teams_play_by_play)

    all_nba_teams_play_by_play_frame = (
        all_nba_teams_play_by_play_frame.drop_duplicates(
            subset=["GAME_ID", "EVENTNUM"]
        )
    )

    # Save to CSV
    # all_nba_teams_play_by_play_frame.to_csv(
    #     "nba/source_files/all_nba_teams_play_by_play_frame_all_years.csv"
    # )

    return all_nba_teams_play_by_play_frame
