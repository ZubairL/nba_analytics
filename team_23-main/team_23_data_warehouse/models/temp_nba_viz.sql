{{ config(materialized='table') }}

SELECT
    season_winner,
    finalized_matched_type,
    CAST(season_year AS STRING) AS season_year,
    COUNT(*) AS count
FROM {{ ref('Play_Type_Conversion_NBA') }}
WHERE season_winner IS NOT null
GROUP BY season_year, season_winner, finalized_matched_type
