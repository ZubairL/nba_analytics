{{ config(materialized='table') }}

WITH ranked_teams AS (
    SELECT
        team_name,
        season_wins,
        season_year,
        ROW_NUMBER()
            OVER (PARTITION BY season_year ORDER BY season_wins DESC)
            AS rank
    FROM
        {{ ref('combined_nba_data') }}
),

scoring_events AS (
    SELECT
        nba_game_id,
        event_number,
        event_type,
        event_action_type,
        period,
        wall_clock_time,
        pctimestring,
        home_description,
        neutral_description,
        visitor_description,
        score,
        score_margin,
        game_date,
        visitor_team,
        home_team,
        combined,
        difference_time_left_in_period,
        season_year,
        season_winner,
        finalized_matched_type,
        visitor_score,
        home_score,
        score_value,
        pts_off_assist_bool,
        jumpshot_bool,
        freethrow_bool,
        paintshot_bool,
        secondchance_bool,
        score_team,
        -- Use LAG to get previous scores for comparison
        LAG(visitor_score)
            OVER (PARTITION BY nba_game_id ORDER BY event_number)
            AS prev_visitor_score_lag,
        LAG(home_score)
            OVER (PARTITION BY nba_game_id ORDER BY event_number)
            AS prev_home_score_lag
    FROM
        {{ ref('Play_Type_Conversion_NBA') }}
),

scoring_classification AS (
    SELECT
        *,
        CASE
            WHEN
                visitor_score != prev_visitor_score_lag
                OR home_score != prev_home_score_lag
                THEN 'Scoring Event'
            ELSE 'Non-scoring Event'
        END AS event_type_1
    FROM
        scoring_events
),

finalized_nba_play_types AS (

    SELECT
        *,
        CASE
            WHEN jumpshot_bool = true THEN 'JUMPSHOT'
            WHEN freethrow_bool = true THEN 'FREETHROW'
            WHEN paintshot_bool = true THEN 'PAINTSHOT'
            WHEN secondchance_bool = true THEN 'SECONDCHANCE'
        END AS category
    FROM
        scoring_classification
    WHERE
        event_type_1 = 'Scoring Event'
    ORDER BY
        nba_game_id, event_number
)

SELECT
    finalized_nba_play_types.score_team,
    finalized_nba_play_types.season_year,
    finalized_nba_play_types.category AS play_category,
    ranked_teams.rank AS team_rank,
    COUNT(*) AS count_observations
FROM
    finalized_nba_play_types
LEFT JOIN
    ranked_teams
    ON
        finalized_nba_play_types.score_team = ranked_teams.team_name
        AND
        finalized_nba_play_types.season_year = ranked_teams.season_year
WHERE
    finalized_nba_play_types.season_year IS NOT null
GROUP BY
    ranked_teams.rank,
    finalized_nba_play_types.score_team,
    finalized_nba_play_types.season_year,
    finalized_nba_play_types.category
ORDER BY
    finalized_nba_play_types.score_team,
    finalized_nba_play_types.season_year
