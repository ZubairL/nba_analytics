{{ config(materialized='table') }}


WITH starter AS (
    SELECT
        *,
        CASE
            WHEN play_type LIKE '%Driving Layup Shot%' THEN 'Paint shot'
            WHEN play_type LIKE '%Jump Shot%' THEN 'Jump shot'
            WHEN play_type LIKE '%Pullup Jump Shot%' THEN 'Jump shot'
            WHEN play_type LIKE '%Layup Shot%' THEN 'Paint shot'
            WHEN play_type LIKE '%Cutting Layup Shot%' THEN 'Paint shot'
            WHEN
                play_type LIKE '%Driving Floating Bank Jump Shot%'
                THEN 'Jump shot'
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
        END AS grouped_play_type
    FROM {{ ref('wnba_pbp_scoring') }}

),

filtering_other AS (
    SELECT *
    FROM starter
    WHERE grouped_play_type <> 'Other'
),



top_teams AS (
    SELECT
        team_name,
        wins,
        season,
        ROW_NUMBER() OVER (PARTITION BY season ORDER BY wins DESC) AS rank

    FROM {{ ref('combined_wnba_data') }}
)

SELECT
    ft.season,
    ft.team_name,
    -- Count each type of shot
    COUNT(CASE WHEN pt.grouped_play_type = 'Paint shot' THEN 1 END)
        AS paintshot_count,
    COUNT(CASE WHEN pt.grouped_play_type = 'Jump shot' THEN 1 END)
        AS jumpshot_count,
    COUNT(
        CASE WHEN pt.grouped_play_type = 'Second chance paint shot' THEN 1 END
    ) AS secondchancepaintshot_count,
    COUNT(CASE WHEN pt.grouped_play_type = 'Free throw' THEN 1 END)
        AS freethrow_count
FROM
    filtering_other AS pt
INNER JOIN
    top_teams AS ft
    ON
        pt.home_team_mascot = ft.team_name
        AND pt.season = ft.season
WHERE
    ft.rank <= 5
GROUP BY
    ft.season, ft.team_name
ORDER BY
    ft.season, ft.team_name
