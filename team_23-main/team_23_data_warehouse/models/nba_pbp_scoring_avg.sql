{{ config(materialized='table') }}

WITH pbp_pts_off_assists AS (
    SELECT
        season_year,
        season_winner,
        score_team,
        SUM(CASE
            WHEN pts_off_assist_bool = True
                THEN score_value
            ELSE 0
        END) AS pts_off_assists,
        SUM(CASE
            WHEN pts_off_assist_bool = True
                THEN score_value
            ELSE 0
        END) / SUM(score_value) AS per_pts_off_assists
    FROM
        {{ ref('Play_Type_Conversion_NBA') }}
    GROUP BY season_year, season_winner, score_team
),

pbp_pts_in_paint AS (
    SELECT
        season_year,
        score_team,
        SUM(CASE
            WHEN paintshot_bool = True
                THEN 1
            ELSE 0
        END) AS paintshots,
        SUM(CASE
            WHEN paintshot_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_number) AS per_paintshots
    FROM
        {{ ref('Play_Type_Conversion_NBA') }}
    GROUP BY season_year, score_team
),

pbp_jumpshots AS (
    SELECT
        season_year,
        score_team,
        SUM(CASE
            WHEN jumpshot_bool = True
                THEN 1
            ELSE 0
        END) AS jumpshots,
        SUM(CASE
            WHEN jumpshot_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_number) AS per_jumpshots
    FROM
        {{ ref('Play_Type_Conversion_NBA') }}
    GROUP BY season_year, score_team
),

pbp_freethrows AS (
    SELECT
        season_year,
        score_team,
        SUM(CASE
            WHEN freethrow_bool = True
                THEN 1
            ELSE 0
        END) AS freethrows,
        SUM(CASE
            WHEN freethrow_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_number) AS per_freethrows
    FROM
        {{ ref('Play_Type_Conversion_NBA') }}
    GROUP BY season_year, score_team
),

pbp_secondchance AS (
    SELECT
        season_year,
        score_team,
        SUM(CASE
            WHEN secondchance_bool = True
                THEN 1
            ELSE 0
        END) AS secondchance_shots,
        SUM(CASE
            WHEN secondchance_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_number) AS per_secondchance
    FROM
        {{ ref('Play_Type_Conversion_NBA') }}
    GROUP BY season_year, score_team
)

SELECT
    pbp_pts_off_assists.season_year,
    pbp_pts_off_assists.season_winner,
    pbp_pts_off_assists.score_team,
    pbp_pts_off_assists.per_pts_off_assists,
    pbp_pts_in_paint.per_paintshots,
    pbp_jumpshots.per_jumpshots,
    pbp_freethrows.per_freethrows,
    pbp_secondchance.per_secondchance
FROM
    pbp_pts_off_assists
INNER JOIN pbp_pts_in_paint
    ON
        pbp_pts_off_assists.season_year = pbp_pts_in_paint.season_year
        AND pbp_pts_off_assists.score_team = pbp_pts_in_paint.score_team
INNER JOIN pbp_jumpshots
    ON
        pbp_pts_off_assists.season_year = pbp_jumpshots.season_year
        AND pbp_pts_off_assists.score_team = pbp_jumpshots.score_team
INNER JOIN pbp_freethrows
    ON
        pbp_pts_off_assists.season_year = pbp_freethrows.season_year
        AND pbp_pts_off_assists.score_team = pbp_freethrows.score_team
INNER JOIN pbp_secondchance
    ON
        pbp_pts_off_assists.season_year = pbp_secondchance.season_year
        AND pbp_pts_off_assists.score_team = pbp_secondchance.score_team
