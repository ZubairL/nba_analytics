import time

from loguru import logger

from nba.invoke_lgbm_example import invoke_lgbm_example
from nba.main import get_play_by_play_frame
from nba.get_box_scores import get_boxscores
from nba.get_shot_coordinates import get_coordinates
from correlation_and_pca.nba_correlation_checks import correlation_checks
from correlation_and_pca.nba_analysis import conduct_pca_analysis
from machine_learning_models.ols_linear_regression.linear_reg_nba import (
    conduct_ols_linear_regression,
)
from machine_learning_models.random_forest.random_forest_nba import (
    conduct_random_forest,
)


def demo():

    logger.info("Demo initialized.")

    logger.info("Getting Play-By-Play Frame...")

    time.sleep(3)

    demo_play_by_play_frame = get_play_by_play_frame(demo_mode="Yes")

    logger.debug("Demo Play-by-Play Frame:")

    time.sleep(3)

    logger.debug(demo_play_by_play_frame)

    time.sleep(2)

    logger.info("Getting boxscore data...")

    demo_box_score_frame = get_boxscores(demo_mode="Yes")

    logger.debug("Demo Box Score Frame:")

    time.sleep(1)

    logger.debug(demo_box_score_frame)

    logger.info("Getting coordinates...")

    time.sleep(2)

    demo_coords_frame = get_coordinates(demo_mode="Yes")

    logger.debug("Demo Coordinates Frame:")

    time.sleep(2)

    logger.debug(demo_coords_frame)

    logger.info("Conducting correlation analysis...")

    time.sleep(2)

    correlation_checks(demo_mode="Yes")

    time.sleep(3)

    logger.info("Conducting PCA analyis...")

    conduct_pca_analysis()

    time.sleep(3)

    logger.info("Conducting OLS Linear Regression analysis....")

    conduct_ols_linear_regression(demo_mode="Yes")

    time.sleep(3)

    logger.info("Conducting random forest analysis...")

    time.sleep(3)

    conduct_random_forest(demo_mode="Yes")

    time.sleep(3)

    logger.info(
        "Demo invoking LightGBM cloud function to get predicted season wins..."
    )

    invoke_lgbm_example()

    time.sleep(4)

    logger.warning("You will not be able to run the visualization app locally")
    logger.warning("unless you authenticate into our GCP and access BigQuery.")
    logger.info(
        "Please visit this URL to access the visualization app instead:"
    )

    logger.info("https://team-23-mj-6242.uw.r.appspot.com/")


if __name__ == "__main__":
    demo()
