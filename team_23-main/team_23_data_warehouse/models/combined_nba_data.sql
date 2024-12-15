{{ config(materialized='table') }}

SELECT
    a.*,
    b.per_pts_off_assists,
    b.per_paintshots,
    b.per_jumpshots,
    b.per_freethrows,
    b.per_secondchance
FROM {{ ref('nba_teambox_season_avgs') }} AS a
INNER JOIN {{ ref('nba_pbp_scoring_avg') }} AS b
    ON a.team_name = b.score_team AND a.season_year = b.season_year
