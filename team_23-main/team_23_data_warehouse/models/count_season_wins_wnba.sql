{{ config(materialized='table') }}

SELECT
    team_id,
    team_name,
    season,
    COUNT(*) AS wins
FROM
    {{ ref('wnba_teambox') }}
WHERE
    team_winner = true
    AND LOWER(team_name) NOT LIKE 'team wnba%'
GROUP BY
    team_id, team_name, season
ORDER BY
    season ASC, team_name ASC
