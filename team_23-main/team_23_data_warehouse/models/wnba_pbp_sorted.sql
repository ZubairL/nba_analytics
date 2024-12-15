{{ config(materialized='table') }}

WITH wnba_pbp_sorted AS (
    SELECT
        type_text AS play_type,
        `TEXT` AS play_description, --NO NA VALUES
        period_display_value AS period_type, --NO NA VALUES
        clock_display_value AS time_left_in_period,
        athlete_id_1, --NO NA
        athlete_id_2, --NO NA
        athlete_id_3, --NO NA
        wallclock AS wall_clock_time,
        away_team_id,
        away_team_name, --NO NA
        away_team_mascot, --NO NA
        away_team_abbrev,
        away_team_name_alt,
        home_team_id,
        home_team_name,
        home_team_mascot,
        home_team_abbrev, --NO NA
        home_team_name_alt, --NO NA
        game_id, --NO NA
        `TIME` AS time_left_in_period_alt, --NO NA
        lead_game_half, --NO NA
        type_abbreviation,
        home_timeout_called,
        away_timeout_called,
        lead_half,
        lag_half,
        CAST(ROUND(CAST(
            IF(team_id = 'NA' OR team_id = 'nan', '999', team_id)
            AS FLOAT64
        )) AS INT64) AS team_id,
        CAST(id AS INT64) AS event_id,
        CAST(sequence_number AS INT64) AS sequence_number,
        CAST(type_id AS INT64) AS play_id,
        CAST(away_score AS INT64) AS away_score,
        CAST(home_score AS INT64) AS home_score,
        CAST(period_number AS INT64) AS period_number, --NO NA
        CAST(scoring_play AS BOOLEAN) AS scoring_play_bool, --NO NA
        CAST(score_value AS INT64) AS score_value, --NO NA
        --NO NA
        CAST(shooting_play AS BOOLEAN) AS shooting_play_bool,
        CAST(coordinate_x_raw AS FLOAT64) AS raw_coordinate_x, --NO NA
        CAST(coordinate_y_raw AS FLOAT64) AS raw_coordinate_y, --NO NA
        CAST(season AS INT64) AS season, --NO NA
        CAST(season_type AS INT64) AS season_type, --NO NA
        CAST(home_team_spread AS FLOAT64) AS home_team_spread, --NO NA
        CAST(game_spread AS FLOAT64) AS game_spread, --NO NA
        CAST(home_favorite AS BOOLEAN) AS home_favorite_bool, --NO NA
        -- CAST(LEAD_QTR AS INT64) AS LEAD_QUARTER, --FLAG NA ISSUES
        CAST(game_spread_available AS BOOLEAN) AS game_spread_available_bool,
        CAST(qtr AS INT64) AS game_quarter,
        --NO NA
        CAST(clock_minutes AS FLOAT64) AS clock_minutes,
        --NO NA
        CAST(clock_seconds AS FLOAT64) AS clock_seconds,
        --NO NA
        CAST(half AS INT64) AS half,
        CAST(game_half AS INT64) AS game_half, --NO NA
        -- CAST(END_QUARTER_SECONDS_REMAINING AS INT64)
        --AS END_QUARTER_SECONDS_REMAINING, --FLAG NA ISSUES
        -- CAST(END_HALF_SECONDS_REMAINING AS INT64)
        --AS END_HALF_SECONDS_REMAINING, --FLAG NA ISSUES
        -- CAST(END_GAME_SECONDS_REMAINING AS INT64)
        --AS END_GAME_SECONDS_REMAINING, --FLAG NA ISSUES
        CAST(
            ROUND(CAST(IF(lead_qtr = 'nan', '999', lead_qtr) AS FLOAT64))
            AS INT64
        ) AS lead_quarter,
        CAST(start_quarter_seconds_remaining AS FLOAT64)
            AS start_quarter_seconds_remaining,
        CAST(start_half_seconds_remaining AS FLOAT64)
            AS start_half_seconds_remaining,
        --NO NA
        CAST(start_game_seconds_remaining AS FLOAT64)
            AS start_game_seconds_remaining,
        -- CAST(LAG_QTR AS INT64) AS LAG_QUARTER, --FLAG NA ISSUES
        -- CAST(LAG_GAME_HALF AS INT64) AS LAG_GAME_HALF, --FLAG NA ISSUES
        CAST(game_play_number AS INT64) AS game_play_number,
        CAST(NULLIF(end_quarter_seconds_remaining, 'NA') AS FLOAT64)
            AS end_quarter_seconds_remaining,
        CAST(NULLIF(end_half_seconds_remaining, 'NA') AS FLOAT64)
            AS end_half_seconds_remaining, --NO NA
        CAST(NULLIF(end_game_seconds_remaining, 'NA') AS FLOAT64)
            AS end_game_seconds_remaining, --NO NA
        CAST(`PERIOD` AS INT64) AS period_number_alt, --NO NA
        CAST(
            ROUND(CAST(IF(lag_qtr = 'nan', '999', lag_qtr) AS FLOAT64))
            AS INT64
        ) AS lag_qtr,
        CAST(
            ROUND(
                CAST(IF(lag_game_half = 'nan', '999', lag_game_half) AS FLOAT64)
            )
            AS INT64
        ) AS lag_game_half,
        CAST(coordinate_x AS FLOAT64) AS coordinate_x,
        CAST(coordinate_y AS FLOAT64) AS coordinate_y,
        CAST(game_date AS DATE) AS game_date,
        CAST(game_date_time AS DATETIME) AS game_date_time,
        CASE
            WHEN game_date BETWEEN '2013-05-01' AND '2013-10-31' THEN 2013
            WHEN game_date BETWEEN '2014-05-01' AND '2014-10-31' THEN 2014
            WHEN game_date BETWEEN '2015-05-01' AND '2015-10-31' THEN 2015
            WHEN game_date BETWEEN '2016-05-01' AND '2016-10-31' THEN 2016
            WHEN game_date BETWEEN '2017-05-01' AND '2017-10-31' THEN 2017
            WHEN game_date BETWEEN '2018-05-01' AND '2018-10-31' THEN 2018
            WHEN game_date BETWEEN '2019-05-01' AND '2019-10-31' THEN 2019
            WHEN game_date BETWEEN '2020-05-01' AND '2020-10-31' THEN 2020
            WHEN game_date BETWEEN '2021-05-01' AND '2021-10-31' THEN 2021
            WHEN game_date BETWEEN '2022-05-01' AND '2022-10-31' THEN 2022
            WHEN game_date BETWEEN '2023-05-01' AND '2023-10-31' THEN 2023
            WHEN game_date BETWEEN '2024-05-01' AND '2024-10-31' THEN 2024
        END AS season_year
    FROM
        {{ source('team_23_project', 'wnba-pbp-2019-2024') }}
    WHERE
        sequence_number NOT LIKE '%sequence_number%'
),

wnba_pbp_winner AS (

    SELECT
        wnba_pbp_sorted.play_type,
        wnba_pbp_sorted.play_description,
        wnba_pbp_sorted.period_type,
        wnba_pbp_sorted.time_left_in_period,
        wnba_pbp_sorted.team_id,
        wnba_pbp_sorted.athlete_id_1,
        wnba_pbp_sorted.athlete_id_2,
        wnba_pbp_sorted.athlete_id_3,
        wnba_pbp_sorted.wall_clock_time,
        wnba_pbp_sorted.away_team_id,
        wnba_pbp_sorted.away_team_name,
        wnba_pbp_sorted.away_team_mascot,
        wnba_pbp_sorted.away_team_abbrev,
        wnba_pbp_sorted.away_team_name_alt,
        wnba_pbp_sorted.home_team_id,
        wnba_pbp_sorted.home_team_name,
        wnba_pbp_sorted.home_team_mascot,
        wnba_pbp_sorted.home_team_abbrev,
        wnba_pbp_sorted.home_team_name_alt,
        wnba_pbp_sorted.game_id,
        wnba_pbp_sorted.time_left_in_period_alt,
        wnba_pbp_sorted.lead_game_half,
        wnba_pbp_sorted.type_abbreviation,
        wnba_pbp_sorted.home_timeout_called,
        wnba_pbp_sorted.away_timeout_called,
        wnba_pbp_sorted.lead_half,
        wnba_pbp_sorted.lag_half,
        wnba_pbp_sorted.event_id,
        wnba_pbp_sorted.sequence_number,
        wnba_pbp_sorted.play_id,
        wnba_pbp_sorted.away_score,
        wnba_pbp_sorted.home_score,
        wnba_pbp_sorted.period_number,
        wnba_pbp_sorted.scoring_play_bool,
        wnba_pbp_sorted.score_value,
        wnba_pbp_sorted.shooting_play_bool,
        wnba_pbp_sorted.raw_coordinate_x,
        wnba_pbp_sorted.raw_coordinate_y,
        wnba_pbp_sorted.season,
        wnba_pbp_sorted.season_type,
        wnba_pbp_sorted.home_team_spread,
        wnba_pbp_sorted.game_spread,
        wnba_pbp_sorted.home_favorite_bool,
        wnba_pbp_sorted.game_spread_available_bool,
        wnba_pbp_sorted.game_quarter,
        wnba_pbp_sorted.clock_minutes,
        wnba_pbp_sorted.clock_seconds,
        wnba_pbp_sorted.half,
        wnba_pbp_sorted.game_half,
        wnba_pbp_sorted.lead_quarter,
        wnba_pbp_sorted.start_quarter_seconds_remaining,
        wnba_pbp_sorted.start_half_seconds_remaining,
        wnba_pbp_sorted.start_game_seconds_remaining,
        wnba_pbp_sorted.game_play_number,
        wnba_pbp_sorted.end_quarter_seconds_remaining,
        wnba_pbp_sorted.end_half_seconds_remaining,
        wnba_pbp_sorted.end_game_seconds_remaining,
        wnba_pbp_sorted.period_number_alt,
        wnba_pbp_sorted.lag_qtr,
        wnba_pbp_sorted.lag_game_half,
        wnba_pbp_sorted.coordinate_x,
        wnba_pbp_sorted.coordinate_y,
        wnba_pbp_sorted.game_date,
        wnba_pbp_sorted.game_date_time,
        wnba_pbp_sorted.season_year,
        wnba_nba_winners_by_year.season_winner
    FROM
        wnba_pbp_sorted
    LEFT JOIN
        {{ ref('wnba_nba_winners_by_year') }} AS wnba_nba_winners_by_year
        ON
            wnba_pbp_sorted.season_year = wnba_nba_winners_by_year.year
            AND
            wnba_nba_winners_by_year.league LIKE 'WNBA'
    ORDER BY
        wnba_pbp_sorted.game_date, wnba_pbp_sorted.game_id,
        wnba_pbp_sorted.event_id
)

SELECT
    a.*,
    b.`Shot_Type_Group_WNBA` AS shot_type_grp
FROM
    wnba_pbp_winner AS a
LEFT JOIN
    {{ source('team_23_project', 'shot_type_grouping') }} AS b
    ON
        a.play_type = b.`Play_Type_WNBA`
