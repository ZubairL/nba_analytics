{{ config(materialized='table') }}

SELECT
    a.*,
    b.per_pts_off_assists,
    b.per_paintshots,
    b.per_jumpshots,
    b.per_freethrows,
    b.per_secondchance,
    c.wins
FROM {{ ref('wnba_teambox_season_avgs') }} AS a
INNER JOIN {{ ref('wnba_pbp_scoring_avg') }} AS b
    ON a.team_id = b.team_id AND a.season = b.season
INNER JOIN {{ ref('count_season_wins_wnba') }} AS c
    ON a.team_id = c.team_id AND a.season = c.season
