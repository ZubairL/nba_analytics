{{ config(materialized='table') }}

WITH game_results AS (
    SELECT
        gameid AS game_id,
        teamid AS team_id,
        teamname AS team_name,
        plusminuspoints AS plus_minus_points,

        -- Extract season from the game_id prefix with
        -- a fallback for unexpected cases
        CASE
            WHEN LEFT(CAST(gameid AS STRING), 3) = '218' THEN '2019'
            WHEN LEFT(CAST(gameid AS STRING), 3) = '219' THEN '2020'
            WHEN LEFT(CAST(gameid AS STRING), 3) = '220' THEN '2021'
            WHEN LEFT(CAST(gameid AS STRING), 3) = '221' THEN '2022'
            WHEN LEFT(CAST(gameid AS STRING), 3) = '222' THEN '2023'
            ELSE 'unknown season'
        END AS inferred_season,

        -- Rank teams by their plus_minus_points for each game
        ROW_NUMBER()
            OVER (PARTITION BY gameid ORDER BY plusminuspoints DESC)
            AS rank
    FROM
        {{ source('team_23_project', 'nba_team_stats_by_game_id') }}
)

SELECT
    game_results.team_id,
    game_results.team_name,
    nba_pbp_sorted.season_year AS season,
    --    game_results.inferred_season,
    COUNT(DISTINCT game_results.game_id) AS wins
FROM
    game_results
LEFT JOIN
    {{ ref('nba_pbp_sorted') }} AS nba_pbp_sorted
    ON
        game_results.game_id = nba_pbp_sorted.nba_game_id
WHERE
    game_results.rank = 1
    AND
    nba_pbp_sorted.season_year IS NOT NULL
GROUP BY
    game_results.team_id, game_results.team_name, nba_pbp_sorted.season_year
ORDER BY
    nba_pbp_sorted.season_year ASC, wins DESC
