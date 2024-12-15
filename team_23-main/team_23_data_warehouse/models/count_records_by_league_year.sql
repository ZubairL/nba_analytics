{{ config(materialized='table') }}

WITH COUNT_RECORDS_WNBA AS (
    SELECT
        "wnba" AS LEAGUE,
        EXTRACT(YEAR FROM GAME_DATE) AS GAME_YEAR,
        COUNT(EVENT_ID) AS COUNT_RECORDS
    FROM
        {{ ref('wnba_pbp_sorted') }}
    GROUP BY
        EXTRACT(YEAR FROM GAME_DATE)
),

COUNT_RECORDS_NBA AS (
    SELECT
        "nba" AS LEAGUE,
        EXTRACT(YEAR FROM GAME_DATE) AS GAME_YEAR,
        COUNT(NBA_GAME_ID) AS COUNT_RECORDS
    FROM
        {{ ref('nba_pbp_sorted') }}
    GROUP BY
        EXTRACT(YEAR FROM GAME_DATE)
)

SELECT *
FROM
    COUNT_RECORDS_WNBA
UNION ALL
SELECT *
FROM
    COUNT_RECORDS_NBA
ORDER BY
    LEAGUE ASC, GAME_YEAR ASC