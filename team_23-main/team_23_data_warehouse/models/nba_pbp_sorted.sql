{{ config(materialized='table') }}

WITH nba_pbp_sorted AS (
    SELECT
        game_id AS nba_game_id,
        eventnum AS event_number,
        eventmsgtype AS event_type,
        eventmsgactiontype AS event_action_type,
        period,
        wctimestring AS wall_clock_time,
        pctimestring,
        --    PCTIMESTRING AS TIME_LEFT_IN_PERIOD,
        homedescription AS home_description,
        neutraldescription AS neutral_description,
        visitordescription AS visitor_description,
        score,
        scoremargin AS score_margin,
        game_date,
        visitor_team,
        home_team,
        PARSE_TIME('%M:%S', pctimestring) AS time_left_in_period,
        PARSE_TIME(
            '%M:%S',
            LAG(pctimestring)
                OVER (PARTITION BY game_id, period ORDER BY eventnum)
        ) AS lag_time_left_in_period,
        TIME_DIFF(
            PARSE_TIME(
                '%M:%S',
                LAG(pctimestring)
                    OVER (PARTITION BY game_id, period ORDER BY eventnum)
            ),
            PARSE_TIME('%M:%S', pctimestring),
            SECOND
        ) AS difference_time_left_in_period,
        CASE
            WHEN game_date BETWEEN '2017-10-01' AND '2018-06-30' THEN 2018
            WHEN game_date BETWEEN '2018-10-01' AND '2019-06-30' THEN 2019
            WHEN game_date BETWEEN '2019-10-01' AND '2020-06-30' THEN 2020
            WHEN game_date BETWEEN '2020-10-01' AND '2021-06-30' THEN 2021
            WHEN game_date BETWEEN '2021-10-01' AND '2022-06-30' THEN 2022
            WHEN game_date BETWEEN '2022-10-01' AND '2023-06-30' THEN 2023
            WHEN game_date BETWEEN '2023-10-01' AND '2024-06-30' THEN 2024
        END
            AS
            season_year
    FROM
        {{ source('team_23_project', 'nba-pbp-2018-2024') }}
)

SELECT
    nba_pbp_sorted.nba_game_id,
    nba_pbp_sorted.event_number,
    nba_pbp_sorted.event_type,
    nba_pbp_sorted.event_action_type,
    nba_pbp_sorted.period,
    nba_pbp_sorted.wall_clock_time,
    nba_pbp_sorted.pctimestring,
    nba_pbp_sorted.home_description,
    nba_pbp_sorted.neutral_description,
    nba_pbp_sorted.visitor_description,
    nba_pbp_sorted.score,
    nba_pbp_sorted.score_margin,
    nba_pbp_sorted.game_date,
    nba_pbp_sorted.visitor_team,
    nba_pbp_sorted.home_team,
    nba_pbp_sorted.time_left_in_period,
    nba_pbp_sorted.lag_time_left_in_period,
    nba_pbp_sorted.difference_time_left_in_period,
    nba_pbp_sorted.season_year,
    wnba_nba_winners_by_year.season_winner
FROM
    nba_pbp_sorted
LEFT JOIN
    {{ ref('wnba_nba_winners_by_year') }} AS wnba_nba_winners_by_year
    ON
        nba_pbp_sorted.season_year = wnba_nba_winners_by_year.year
        AND
        wnba_nba_winners_by_year.league LIKE 'NBA'
ORDER BY
    nba_pbp_sorted.game_date,
    nba_pbp_sorted.nba_game_id,
    nba_pbp_sorted.period,
    nba_pbp_sorted.event_number
