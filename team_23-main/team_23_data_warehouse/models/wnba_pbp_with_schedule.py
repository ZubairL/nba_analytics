import pandas


def model(dbt, session):

    # Materialize as a table
    dbt.config(
        materialized="table",
    )

    # wnba_pbp_df = dbt.ref("wnba_pbp_sorted").toPandas()

    wnba_sched_df = dbt.source(
        "team_23_project", "wnba-schedule-2019-2024-v2"
    ).toPandas()

    # wnba_sched_df = wnba_sched_df.filter(["type_abbreviation", "season", "id"])
    #
    # wnba_pbp_df_with_schedule = pandas.merge(
    #     left=wnba_pbp_df,
    #     right=wnba_sched_df,
    #     left_on=["season", "game_id"],
    #     right_on=["season", "id"],
    #     suffixes=("_pbp", "_sched"),
    # )

    return wnba_sched_df
