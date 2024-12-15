{{ config(materialized='table') }}

WITH nba_team_stats_by_game_id AS (
    SELECT
        *,
        points - plusminuspoints AS opp_team_score
    FROM
        {{ source('team_23_project', 'nba_team_stats_by_game_id') }}
),

nba_teambox_season_avgs AS (
    SELECT
        nba_pbp_sorted.season_year,
        nba_team_stats_by_game_id.teamid AS team_id,
        nba_team_stats_by_game_id.teamname AS team_name,
        nba_team_stats_by_game_id.teamtricode AS team_abbrev,
        COUNT(DISTINCT nba_pbp_sorted.nba_game_id) AS game_count,
        AVG(nba_team_stats_by_game_id.fieldgoalsmade) AS avg_field_goals_made,
        AVG(nba_team_stats_by_game_id.fieldgoalsattempted)
            AS avg_field_goals_att,
        AVG(nba_team_stats_by_game_id.fieldgoalspercentage)
            AS avg_field_goal_pct,
        VARIANCE(nba_team_stats_by_game_id.fieldgoalspercentage)
            AS var_field_goal_pct,
        AVG(nba_team_stats_by_game_id.threepointersmade)
            AS avg_three_pt_field_goals_made,
        AVG(nba_team_stats_by_game_id.threepointersattempted)
            AS avg_three_pt_field_goals_att,
        AVG(nba_team_stats_by_game_id.threepointerspercentage)
            AS avg_three_pt_field_goal_pct,
        AVG(nba_team_stats_by_game_id.freethrowsmade) AS avg_free_throws_made,
        AVG(nba_team_stats_by_game_id.freethrowsattempted)
            AS avg_free_throws_att,
        AVG(nba_team_stats_by_game_id.freethrowspercentage)
            AS avg_free_throw_pct,
        AVG(nba_team_stats_by_game_id.reboundsoffensive) AS avg_off_rebounds,
        AVG(nba_team_stats_by_game_id.reboundsdefensive) AS avg_def_rebounds,
        AVG(nba_team_stats_by_game_id.reboundstotal) AS avg_tot_rebounds,
        AVG(nba_team_stats_by_game_id.assists) AS avg_assists,
        AVG(nba_team_stats_by_game_id.steals) AS avg_steals,
        AVG(nba_team_stats_by_game_id.blocks) AS avg_blocks,
        AVG(nba_team_stats_by_game_id.turnovers) AS avg_tot_turnovers,
        AVG(nba_team_stats_by_game_id.foulspersonal) AS avg_fouls,
        AVG(nba_team_stats_by_game_id.points) AS avg_pts_scored,
        AVG(nba_team_stats_by_game_id.plusminuspoints) AS avg_plus_minus_points,
        AVG(nba_team_stats_by_game_id.opp_team_score) AS avg_pts_against
    FROM
        nba_team_stats_by_game_id
    LEFT JOIN
        {{ ref('nba_pbp_sorted') }} AS nba_pbp_sorted
        ON
            nba_team_stats_by_game_id.gameid = nba_pbp_sorted.nba_game_id
    GROUP BY
        nba_pbp_sorted.season_year,
        nba_team_stats_by_game_id.teamid,
        nba_team_stats_by_game_id.teamname,
        nba_team_stats_by_game_id.teamtricode
)

SELECT
    nba_teambox_season_avgs.season_year,
    nba_teambox_season_avgs.team_id,
    nba_teambox_season_avgs.team_name,
    nba_teambox_season_avgs.team_abbrev,
    nba_teambox_season_avgs.game_count,
    count_season_wins_nba.wins AS season_wins,
    wnba_nba_winners_by_year.season_winner,
    nba_teambox_season_avgs.avg_field_goals_made,
    nba_teambox_season_avgs.avg_field_goals_att,
    nba_teambox_season_avgs.avg_field_goal_pct,
    nba_teambox_season_avgs.var_field_goal_pct,
    nba_teambox_season_avgs.avg_three_pt_field_goals_made,
    nba_teambox_season_avgs.avg_three_pt_field_goals_att,
    nba_teambox_season_avgs.avg_three_pt_field_goal_pct,
    nba_teambox_season_avgs.avg_free_throws_made,
    nba_teambox_season_avgs.avg_free_throws_att,
    nba_teambox_season_avgs.avg_free_throw_pct,
    nba_teambox_season_avgs.avg_off_rebounds,
    nba_teambox_season_avgs.avg_def_rebounds,
    nba_teambox_season_avgs.avg_tot_rebounds,
    nba_teambox_season_avgs.avg_assists,
    nba_teambox_season_avgs.avg_steals,
    nba_teambox_season_avgs.avg_blocks,
    nba_teambox_season_avgs.avg_tot_turnovers,
    nba_teambox_season_avgs.avg_fouls,
    nba_teambox_season_avgs.avg_pts_scored,
    nba_teambox_season_avgs.avg_plus_minus_points,
    nba_teambox_season_avgs.avg_pts_against
FROM
    nba_teambox_season_avgs
LEFT JOIN
    {{ ref('count_season_wins_nba') }} AS count_season_wins_nba
    ON
        nba_teambox_season_avgs.team_id = count_season_wins_nba.team_id
        AND
        CAST(count_season_wins_nba.season AS INT64)
        = nba_teambox_season_avgs.season_year
LEFT JOIN
    {{ ref('wnba_nba_winners_by_year') }} AS wnba_nba_winners_by_year
    ON
        nba_teambox_season_avgs.season_year = wnba_nba_winners_by_year.year
        AND
        wnba_nba_winners_by_year.league = 'NBA'
WHERE
    nba_teambox_season_avgs.season_year IS NOT NULL
ORDER BY
    nba_teambox_season_avgs.season_year ASC,
    nba_teambox_season_avgs.team_id ASC
