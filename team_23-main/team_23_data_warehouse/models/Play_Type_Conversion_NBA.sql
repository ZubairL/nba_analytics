{{ config(materialized='table') }}

-- FINALIZED_MATCHED_PLAY_TYPE IS THE LAST COLUMN IN THE DATASET -- 

WITH combined_desc AS (
    SELECT
        *,
        COALESCE(home_description, neutral_description, visitor_description)
            AS combined
    FROM
        {{ ref('nba_pbp_sorted') }}
),

finalized AS (
    SELECT
        combined_desc.nba_game_id,
        combined_desc.event_number,
        combined_desc.event_type,
        combined_desc.event_action_type,
        combined_desc.period,
        combined_desc.wall_clock_time,
        combined_desc.pctimestring,
        combined_desc.home_description,
        combined_desc.neutral_description,
        combined_desc.visitor_description,
        combined_desc.score,
        combined_desc.score_margin,
        combined_desc.game_date,
        combined_desc.visitor_team,
        combined_desc.home_team,
        combined_desc.combined,
        combined_desc.difference_time_left_in_period,
        combined_desc.season_year,
        combined_desc.season_winner,
        -- Using CASE with LIKE to find the play type in the description
        CASE
            WHEN
                combined LIKE '%Turnaround Fade Away Jump Shot%'
                THEN 'Fade Away Jump Shot'
            WHEN
                combined LIKE '%Driving Floating Bank Jump Shot%'
                THEN 'Driving Floating Bank Jump Shot'
            WHEN
                combined LIKE '%Fade Away Bank Jump Shot%'
                THEN 'Fade Away Bank Jump Shot'
            WHEN
                combined LIKE '%Turnaround Bank Jump Shot%'
                THEN 'Turnaround Bank Jump Shot'
            WHEN
                combined LIKE '%Driving Floating Jump Shot%'
                THEN 'Driving Floating Jump Shot'
            WHEN
                combined LIKE '%Turnaround Jump Shot%'
                THEN 'Turnaround Jump Shot'
            WHEN
                combined LIKE '%Step Back Jump Shot%'
                THEN 'Step Back Jump Shot'
            WHEN
                combined LIKE '%Driving Jump Shot Bank%'
                THEN 'Driving Jump Shot Bank'
            WHEN
                combined LIKE '%Running Pullup Jump Shot%'
                THEN 'Running Pullup Jump Shot'
            WHEN
                combined LIKE '%Fade Away Jump Shot%'
                THEN 'Fade Away Jump Shot'
            WHEN combined LIKE '%Jump Shot Bank%' THEN 'Jump Shot Bank'
            WHEN combined LIKE '%Driving Jump Shot%' THEN 'Driving Jump Shot'
            WHEN
                combined LIKE '%Pullup Bank Jump Shot%'
                THEN 'Pullup Bank Jump Shot'
            WHEN combined LIKE '%Driving Layup Shot%' THEN 'Driving Layup Shot'
            WHEN combined LIKE '%Running Jump Shot%' THEN 'Running Jump Shot'
            WHEN combined LIKE '%Floating Jump Shot%' THEN 'Floating Jump Shot'
            WHEN combined LIKE '%Pullup Jump Shot%' THEN 'Pullup Jump Shot'
            WHEN combined LIKE '%Jump Shot%' THEN 'Jump Shot'
            WHEN combined LIKE '%Driving Layup%' THEN 'Driving Layup Shot'
            WHEN combined LIKE '%Cutting Layup Shot%' THEN 'Cutting Layup Shot'
            WHEN combined LIKE '%Running Layup%' THEN 'Running Layup Shot'
            WHEN combined LIKE '%Putback Layup%' THEN 'Layup Shot Putback'
            WHEN
                combined LIKE '%Driving Finger Roll Layup%'
                THEN 'Driving Finger Roll Layup'
            WHEN combined LIKE '%Reverse Layup Shot%' THEN 'Reverse Layup Shot'
            WHEN combined LIKE '%Layup Shot%' THEN 'Layup Shot'
            WHEN
                combined LIKE '%Turnaround Bank Hook Shot%'
                THEN 'Turnaround Bank Hook Shot'
            WHEN
                combined LIKE '%Turnaround Hook Shot%'
                THEN 'Turnaround Hook Shot'
            WHEN combined LIKE '%Driving Hook Shot%' THEN 'Driving Hook Shot'
            WHEN combined LIKE '%Hook Shot Bank%' THEN 'Hook Shot Bank'
            WHEN combined LIKE '%Hook Driving Bank%' THEN 'Hook Driving Bank'
            WHEN combined LIKE '%Hook Shot%' THEN 'Hook Shot'
            --WHEN combined LIKE '%REBOUND%' THEN 'Rebound'--
            WHEN combined LIKE '%Tip%' THEN 'Tip Shot'
            --WHEN combined LIKE '%S.FOUL%' THEN 'Shooting Foul'
            --WHEN combined LIKE '%P.FOUL%' THEN 'Personal Foul'
            --WHEN combined LIKE '%Bad Pass%' THEN 'Bad Pass'
            --WHEN combined LIKE '%Timeout%' THEN 'Timeout'
            --WHEN combined LIKE 'SUB: % FOR %' THEN 'Substitution'
            WHEN combined LIKE '%Free Throw 1 of 2%' THEN 'Free Throw - 1 of 2'
            WHEN combined LIKE '%Free Throw 2 of 2%' THEN 'Free Throw - 2 of 2'
            WHEN combined LIKE '%Free Throw 1 of 3%' THEN 'Free Throw - 1 of 3'
            WHEN combined LIKE '%Free Throw 2 of 3%' THEN 'Free Throw - 2 of 3'
            WHEN combined LIKE '%Free Throw 3 of 3%' THEN 'Free Throw - 3 of 3'
            WHEN combined LIKE '%Free Throw 1 of 1%' THEN 'Free Throw - 1 of 1'
            ELSE 'Other' -- If no play type is found, mark it as 'Other'
        END AS matched_play_type
    FROM
        combined_desc
),

finalizedcte AS (
    SELECT
        finalized.nba_game_id,
        finalized.event_number,
        finalized.event_type,
        finalized.event_action_type,
        finalized.period,
        finalized.wall_clock_time,
        finalized.pctimestring,
        finalized.home_description,
        finalized.neutral_description,
        finalized.visitor_description,
        finalized.score,
        finalized.score_margin,
        finalized.game_date,
        finalized.visitor_team,
        finalized.home_team,
        finalized.combined,
        finalized.difference_time_left_in_period,
        finalized.season_year,
        finalized.season_winner,

        -- Case statement to map play types to shot type groups
        CASE
            WHEN
                finalized.matched_play_type LIKE '%Driving Layup Shot%'
                THEN 'Paint shot'
            WHEN finalized.matched_play_type LIKE '%Jump Shot%' THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Pullup Jump Shot%'
                THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Layup Shot%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Cutting Layup Shot%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type
                LIKE '%Driving Floating Bank Jump Shot%'
                THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Floating Jump Shot%'
                THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Driving Floating Jump Shot%'
                THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Driving Finger Roll Layup%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Running Layup Shot%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Layup Shot Putback%'
                THEN 'Second chance paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Turnaround Jump Shot%'
                THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Step Back Jump Shot%'
                THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Hook Shot%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Driving Hook Shot%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Turnaround Hook Shot%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Running Jump Shot%'
                THEN 'Jump shot'
            WHEN
                finalized.matched_play_type LIKE '%Tip Shot%'
                THEN 'Second chance paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Turnaround Bank Hook Shot%'
                THEN 'Paint shot'
            WHEN
                finalized.matched_play_type LIKE '%Free Throw - 1 of 2%'
                THEN 'Free throw'
            WHEN
                finalized.matched_play_type LIKE '%Free Throw - 2 of 2%'
                THEN 'Free throw'
            WHEN
                finalized.matched_play_type LIKE '%Free Throw - 1 of 1%'
                THEN 'Free throw'
            WHEN
                finalized.matched_play_type LIKE '%Free Throw - 2 of 3%'
                THEN 'Free throw'
            WHEN
                finalized.matched_play_type LIKE '%Free Throw - 1 of 3%'
                THEN 'Free throw'
            WHEN
                finalized.matched_play_type LIKE '%Free Throw - 3 of 3%'
                THEN 'Free throw'
            ELSE 'Other'
        END AS finalized_matched_type

    FROM finalized
    WHERE
        matched_play_type != 'Other'
        AND score IS NOT NULL
        AND score != ''
),

score_calc AS (
    SELECT
        *,
        CAST(SPLIT(score, ' - ')[OFFSET(0)] AS INT64) AS visitor_score,
        CAST(SPLIT(score, ' - ')[OFFSET(1)] AS INT64) AS home_score
    FROM finalizedcte
),

score_calc2 AS (
    SELECT
        *,
        visitor_score - LAG(visitor_score)
            OVER (PARTITION BY season_year, nba_game_id ORDER BY event_number)
            AS prev_visitor_score,
        home_score - LAG(home_score)
            OVER (PARTITION BY season_year, nba_game_id ORDER BY event_number)
            AS prev_home_score
    FROM score_calc
)

SELECT
    *,
    (visitor_score + home_score)
    - COALESCE(prev_visitor_score + prev_home_score, 0) AS score_value,
    COALESCE(combined LIKE '%AST%', FALSE) AS pts_off_assist_bool,
    COALESCE(finalized_matched_type = 'Jump shot', FALSE) AS jumpshot_bool,
    COALESCE(finalized_matched_type = 'Free throw', FALSE) AS freethrow_bool,
    COALESCE(finalized_matched_type = 'Paint shot', FALSE) AS paintshot_bool,
    COALESCE(finalized_matched_type = 'Second chance paint shot', FALSE)
        AS secondchance_bool,
    CASE
        WHEN home_description IS NOT NULL THEN home_team
        WHEN visitor_description IS NOT NULL THEN visitor_team
    END AS score_team
FROM score_calc2
