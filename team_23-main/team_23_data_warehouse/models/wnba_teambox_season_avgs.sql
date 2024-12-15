{{ config(materialized='table') }}

SELECT
    SEASON,
    TEAM_ID,
    TEAM_LOC,
    TEAM_NAME,
    TEAM_ABBREV,
    COUNT(DISTINCT GAME_ID) AS GAME_COUNT,
    --AVG(FAST_BREAK_PTS) AS AVG_FAST_BREAK_PTS,
    --AVG(PTS_IN_PAINT) AS AVG_PTS_IN_PAINT,
    --AVG(TURNOVER_PTS) AS AVG_TURNOVER_PTS,
    --AVG(LARGEST_LEAD) AS AVG_LARGEST_LEAD,
    AVG(TEAM_SCORE) AS AVG_PTS_SCORED,
    AVG(ASSISTS) AS AVG_ASSISTS,
    AVG(BLOCKS) AS AVG_BLOCKS,
    AVG(DEF_REBOUNDS) AS AVG_DEF_REBOUNDS,
    AVG(FIELD_GOAL_PCT) / 100 AS AVG_FIELD_GOAL_PCT,
    VARIANCE(FIELD_GOAL_PCT / 100) AS VAR_FIELD_GOAL_PCT,
    AVG(FIELD_GOALS_MADE) AS AVG_FIELD_GOALS_MADE,
    AVG(FIELD_GOALS_ATT) AS AVG_FIELD_GOALS_ATT,
    AVG(FOULS) AS AVG_FOULS,
    AVG(FREE_THROW_PCT) AS AVG_FREE_THROW_PCT,
    AVG(FREE_THROWS_MADE) AS AVG_FREE_THROWS_MADE,
    AVG(FREE_THROWS_ATT) AS AVG_FREE_THROWS_ATT,
    AVG(OFF_REBOUNDS) AS AVG_OFF_REBOUNDS,
    AVG(STEALS) AS AVG_STEALS,
    AVG(TEAM_TURNOVERS) AS AVG_TEAM_TURNOVERS,
    AVG(THREE_PT_FIELD_GOAL_PCT) / 100 AS AVG_THREE_PT_FIELD_GOAL_PCT,
    AVG(THREE_PT_FIELD_GOALS_MADE) AS AVG_THREE_PT_FIELD_GOALS_MADE,
    AVG(THREE_PT_FIELD_GOALS_ATT) AS AVG_THREE_PT_FIELD_GOALS_ATT,
    AVG(TOT_REBOUNDS) AS AVG_TOT_REBOUNDS,
    AVG(TOT_TURNOVERS) AS AVG_TOT_TURNOVERS,
    AVG(TURNOVERS) AS AVG_TURNOVERS,
    AVG(OPP_TEAM_SCORE) AS AVG_PTS_AGAINST
FROM
    {{ ref('wnba_teambox') }}
GROUP BY
    SEASON,
    TEAM_ID,
    TEAM_LOC,
    TEAM_NAME,
    TEAM_ABBREV
ORDER BY
    SEASON ASC,
    TEAM_ID ASC