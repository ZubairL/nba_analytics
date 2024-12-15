{{ config(materialized='table') }}

WITH pbp_regseas AS (
    SELECT
        a.season_winner,
        a.event_id,
        a.sequence_number,--No NA values
        a.play_id, --No NA values
        a.play_type,
        a.play_description,
        a.away_score,
        a.home_score, --No NA
        a.period_number, --No NA
        a.time_left_in_period,
        a.scoring_play_bool, --No NA
        a.score_value, --No NA
        a.team_id,
        a.athlete_id_1,
        a.athlete_id_2,
        a.athlete_id_3,
        a.shooting_play_bool,
        a.season,
        a.away_team_id,
        a.away_team_name,
        a.away_team_mascot,
        a.home_team_id,
        a.home_team_name,
        a.home_team_mascot,
        a.game_id, --No NA
        a.clock_minutes,--No NA
        a.clock_seconds, --No NA
        a.half, --No NA
        a.start_quarter_seconds_remaining, --No NA
        a.start_half_seconds_remaining, --No NA
        a.start_game_seconds_remaining, --No NA
        a.game_play_number, --No NA
        a.game_date,
        a.coordinate_x,
        a.coordinate_y,
        a.shot_type_grp,
        b.type_abbreviation,
        LAG(a.start_game_seconds_remaining)
            OVER (PARTITION BY a.season, a.game_id ORDER BY a.game_play_number)
            AS previous_score,
        LAG(a.start_game_seconds_remaining)
            OVER (PARTITION BY a.season, a.game_id ORDER BY a.game_play_number)
        - a.start_game_seconds_remaining
            AS timediff_from_prev_score
    FROM
        {{ ref('wnba_pbp_sorted') }} AS a
    INNER JOIN
        {{ source('team_23_project', 'wnba-schedule-2019-2024-v2') }} AS b
        ON
            a.game_id = CAST(b.id AS string)
            AND a.season = b.season
    WHERE
        b.type_abbreviation = 'STD' AND a.scoring_play_bool = True
        AND a.play_type NOT LIKE 'No Shot%'
    ORDER BY a.season ASC, a.game_id ASC, a.game_play_number ASC
)

SELECT
    pbp_regseas.*,
    COALESCE(play_description LIKE '%assist%', False) AS pts_off_assist_bool,
    IF(
        ABS(coordinate_y) <= 8,
        IF(
            ABS(coordinate_x) BETWEEN 28 AND 47,
            IF(shot_type_grp <> 'Free throw', True, False),
            False
        ), False
    ) AS pts_in_paint_bool,
    COALESCE(shot_type_grp = 'Jump shot', False) AS jumpshot_bool,
    COALESCE(shot_type_grp = 'Free throw', False) AS freethrow_bool,
    COALESCE(shot_type_grp = 'Paint shot', False) AS paintshot_bool,
    COALESCE(shot_type_grp = 'Second chance paint shot', False)
        AS secondchance_bool
FROM pbp_regseas
