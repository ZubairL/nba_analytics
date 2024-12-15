{{ config(materialized='table') }}

WITH wnba_winners AS (
    SELECT
        2024 AS year,
        'To Be Decided' AS season_winner,
        'WNBA' AS league
    UNION ALL
    SELECT
        2023 AS year,
        'Las Vegas Aces' AS season_winner,
        'WNBA' AS league
    UNION ALL
    SELECT
        2022 AS year,
        'Las Vegas Aces' AS season_winner,
        'WNBA' AS league
    UNION ALL
    SELECT
        2021 AS year,
        'Chicago Sky' AS season_winner,
        'WNBA' AS league
    UNION ALL
    SELECT
        2020 AS year,
        'Seattle Storm' AS season_winner,
        'WNBA' AS league
    UNION ALL
    SELECT
        2019 AS year,
        'Washington Mystics' AS season_winner,
        'WNBA' AS league
    UNION ALL
    SELECT
        2018 AS year,
        'Seattle Storm' AS season_winner,
        'WNBA' AS league
),

nba_winners AS (
    SELECT
        2024 AS year,
        'Boston Celtics' AS season_winner,
        'NBA' AS league
    UNION ALL
    SELECT
        2023 AS year,
        'Denver Nuggets' AS season_winner,
        'NBA' AS league
    UNION ALL
    SELECT
        2022 AS year,
        'Golden State Warriors' AS season_winner,
        'NBA' AS league
    UNION ALL
    SELECT
        2021 AS year,
        'Milwaukee Bucks' AS season_winner,
        'NBA' AS league
    UNION ALL
    SELECT
        2020 AS year,
        'Los Angeles Lakers' AS season_winner,
        'NBA' AS league
    UNION ALL
    SELECT
        2019 AS year,
        'Toronto Raptors' AS season_winner,
        'NBA' AS league
    UNION ALL
    SELECT
        2018 AS year,
        'Golden State Warriors' AS season_winner,
        'NBA' AS league
)

SELECT
    year,
    season_winner,
    league
FROM
    wnba_winners
UNION ALL
SELECT
    year,
    season_winner,
    league
FROM
    nba_winners
ORDER BY
    league, year
