{{ config(materialized='table') }}

SELECT
    season_winner,
    CAST(season AS STRING) AS season_year,
    CASE
        WHEN play_type LIKE '%Driving Layup Shot%' THEN 'Paint shot'
        WHEN play_type LIKE '%Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Pullup Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Layup Shot%' THEN 'Paint shot'
        WHEN play_type LIKE '%Cutting Layup Shot%' THEN 'Paint shot'
        WHEN play_type LIKE '%Driving Floating Bank Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Floating Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Driving Floating Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Driving Finger Roll Layup%' THEN 'Paint shot'
        WHEN play_type LIKE '%Running Layup Shot%' THEN 'Paint shot'
        WHEN
            play_type LIKE '%Layup Shot Putback%'
            THEN 'Second chance paint shot'
        WHEN play_type LIKE '%Turnaround Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Step Back Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Hook Shot%' THEN 'Paint shot'
        WHEN play_type LIKE '%Driving Hook Shot%' THEN 'Paint shot'
        WHEN play_type LIKE '%Turnaround Hook Shot%' THEN 'Paint shot'
        WHEN play_type LIKE '%Running Jump Shot%' THEN 'Jump shot'
        WHEN play_type LIKE '%Tip Shot%' THEN 'Second chance paint shot'
        WHEN play_type LIKE '%Turnaround Bank Hook Shot%' THEN 'Paint shot'

        -- Free Throws
        WHEN play_type LIKE 'Free Throw - 1 of 2' THEN 'Free throw'
        WHEN play_type LIKE 'Free Throw - 2 of 2' THEN 'Free throw'
        WHEN play_type LIKE 'Free Throw - 1 of 1' THEN 'Free throw'
        WHEN play_type LIKE 'Free Throw - 2 of 3' THEN 'Free throw'
        WHEN play_type LIKE 'Free Throw - 1 of 3' THEN 'Free throw'
        WHEN play_type LIKE 'Free Throw - 3 of 3' THEN 'Free throw'

        ELSE 'Other'
    END AS grouped_play_type,
    COUNT(*) AS count
FROM {{ ref('wnba_pbp_scoring') }}

WHERE
    play_type NOT IN ('N/A', 'Other')
GROUP BY
    season, season_winner, grouped_play_type
