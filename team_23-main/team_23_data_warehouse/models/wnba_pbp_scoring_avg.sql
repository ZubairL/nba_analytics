{{ config(materialized='table') }}

WITH pbp_pts_off_assists AS (
    SELECT
        season,
        season_winner,
        team_id,
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
        {{ ref('wnba_pbp_scoring') }}
    GROUP BY season, season_winner, team_id
),

pbp_pts_in_paint AS (
    SELECT
        season,
        team_id,
        SUM(CASE
            WHEN paintshot_bool = True
                THEN 1
            ELSE 0
        END) AS paintshots,
        SUM(CASE
            WHEN paintshot_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_id) AS per_paintshots
    FROM
        {{ ref('wnba_pbp_scoring') }}
    GROUP BY season, team_id
),

pbp_jumpshots AS (
    SELECT
        season,
        team_id,
        SUM(CASE
            WHEN jumpshot_bool = True
                THEN 1
            ELSE 0
        END) AS jumpshots,
        SUM(CASE
            WHEN jumpshot_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_id) AS per_jumpshots
    FROM
        {{ ref('wnba_pbp_scoring') }}
    GROUP BY season, team_id
),

pbp_freethrows AS (
    SELECT
        season,
        team_id,
        SUM(CASE
            WHEN freethrow_bool = True
                THEN 1
            ELSE 0
        END) AS freethrows,
        SUM(CASE
            WHEN freethrow_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_id) AS per_freethrows
    FROM
        {{ ref('wnba_pbp_scoring') }}
    GROUP BY season, team_id
),

pbp_secondchance AS (
    SELECT
        season,
        team_id,
        SUM(CASE
            WHEN secondchance_bool = True
                THEN 1
            ELSE 0
        END) AS secondchance_shots,
        SUM(CASE
            WHEN secondchance_bool = True
                THEN 1
            ELSE 0
        END) / COUNT(event_id) AS per_secondchance
    FROM
        {{ ref('wnba_pbp_scoring') }}
    GROUP BY season, team_id
)

SELECT
    pbp_pts_off_assists.season,
    pbp_pts_off_assists.season_winner,
    pbp_pts_off_assists.team_id,
    pbp_pts_off_assists.per_pts_off_assists,
    pbp_pts_in_paint.per_paintshots,
    pbp_jumpshots.per_jumpshots,
    pbp_freethrows.per_freethrows,
    pbp_secondchance.per_secondchance
FROM
    pbp_pts_off_assists
INNER JOIN pbp_pts_in_paint
    ON
        pbp_pts_off_assists.season = pbp_pts_in_paint.season
        AND pbp_pts_off_assists.team_id = pbp_pts_in_paint.team_id
INNER JOIN pbp_jumpshots
    ON
        pbp_pts_off_assists.season = pbp_jumpshots.season
        AND pbp_pts_off_assists.team_id = pbp_jumpshots.team_id
INNER JOIN pbp_freethrows
    ON
        pbp_pts_off_assists.season = pbp_freethrows.season
        AND pbp_pts_off_assists.team_id = pbp_freethrows.team_id
INNER JOIN pbp_secondchance
    ON
        pbp_pts_off_assists.season = pbp_secondchance.season
        AND pbp_pts_off_assists.team_id = pbp_secondchance.team_id
