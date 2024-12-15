{{ config(materialized='table') }}

WITH nba_pbp_unique_games AS (
    SELECT DISTINCT
        nba_game_id,
        visitor_team,
        home_team,
        season_year
    FROM
        {{ ref('nba_pbp_sorted') }}
)

SELECT
    nba_all_coords.*,
    nba_pbp_unique_games.visitor_team,
    nba_pbp_unique_games.home_team,
    nba_pbp_unique_games.season_year,
    nba_abbrev_1.franchise AS home_franchise,
    nba_abbrev_2.franchise AS away_franchise,
    CASE
        WHEN
            nba_all_coords.team_name = nba_abbrev_1.franchise
            THEN nba_abbrev_2.franchise
        ELSE nba_abbrev_1.franchise
    END AS team_playing_against
FROM
    {{ source('team_23_project', 'nba-all-coordinates') }} AS nba_all_coords
LEFT JOIN
    nba_pbp_unique_games
    ON
        nba_all_coords.game_id = nba_pbp_unique_games.nba_game_id
LEFT JOIN
    {{ source('team_23_project', 'nba-team-abbreviations') }} AS nba_abbrev_1
    ON
        nba_all_coords.htm = nba_abbrev_1.abbrev
LEFT JOIN
    {{ source('team_23_project', 'nba-team-abbreviations') }} AS nba_abbrev_2
    ON
        nba_all_coords.vtm = nba_abbrev_2.abbrev
