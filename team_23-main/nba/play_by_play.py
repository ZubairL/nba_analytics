import pandas

from nba_api.stats.static import teams
from loguru import logger
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonType
from nba_api.stats.endpoints import playbyplay
from nba_api.stats.endpoints import boxscoretraditionalv2


def get_game_id_history(
    team_abbreviation,
    season=Season.default,
    season_type=SeasonType.regular,
) -> pandas.DataFrame:
    nba_teams = teams.get_teams()

    # Select the dictionary for the Pacers, which contains their team ID
    team_object = [
        team for team in nba_teams if team["abbreviation"] == team_abbreviation
    ][0]
    team_id = team_object["id"]
    logger.debug(f"Team ID: {team_id}")

    gamefinder = leaguegamefinder.LeagueGameFinder(
        team_id_nullable=team_id,
        season_nullable=season,
        season_type_nullable=season_type,
    )

    games_dict = gamefinder.get_normalized_dict()
    games = games_dict["LeagueGameFinderResults"]

    games_id_history = []

    for game in games:
        game_date = game["GAME_DATE"]
        game_id = game["GAME_ID"]
        games_id_history.append({"game_date": game_date, "game_id": game_id})

    games_id_frame = pandas.DataFrame(games_id_history)

    games_id_frame = games_id_frame.sort_values(
        by="game_date", ascending=False
    )

    return games_id_frame


# Earliest game would be game_index == -1 (iloc[-1]), latest is 0 (iloc[0]).
def get_play_by_play(games_id_frame, game_index=0) -> pandas.DataFrame:
    game_date = games_id_frame["game_date"].iloc[game_index]

    logger.debug(game_date)

    game_id = games_id_frame.loc[
        games_id_frame["game_date"] == game_date, "game_id"
    ]

    play_by_play_frame = playbyplay.PlayByPlay(game_id).get_data_frames()[0]

    boxscore = boxscoretraditionalv2.BoxScoreTraditionalV2(game_id=game_id)

    team_stats_df = boxscore.get_data_frames()[1]
    visitor_team = team_stats_df.iloc[0]["TEAM_NAME"]
    home_team = team_stats_df.iloc[1]["TEAM_NAME"]

    play_by_play_frame["game_date"] = game_date
    play_by_play_frame["visitor_team"] = visitor_team
    play_by_play_frame["home_team"] = home_team

    logger.debug(play_by_play_frame)

    return play_by_play_frame


if __name__ == "__main__":
    current_game_ids_frame = get_game_id_history("GSW")
    current_play_by_play_frame = get_play_by_play(current_game_ids_frame)
