import pandas
import lightgbm as lgb
import matplotlib.pyplot as plt
import math

from flask import jsonify
from sklearn.model_selection import train_test_split
from google.cloud import bigquery
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from loguru import logger

# conda install python-graphviz

""" REFERENCES """
# The following code was partially sourced from Microsoft's official LightGBM repository:

# https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/simple_example.py

# https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/plot_example.py


def train_lgbm(request):

    request_json = request.get_json()

    table_name = request_json["bigquery_table_name"]  # BigQuery table name
    dependent_var = request_json["dependent_var"]  # dependent_var
    independent_vars = request_json[
        "independent_vars"
    ]  # List of independent vars
    what_if_dict = request_json["what_if_dict"]

    logger.debug(table_name)

    if "wnba" in table_name:
        relative_path_save_images = "machine_learning_models/light_gradient_boosting_machine/Metrics/wnba/"
        league = "WNBA"
    else:
        relative_path_save_images = "machine_learning_models/light_gradient_boosting_machine/Metrics/nba/"
        league = "NBA"

    # Initialize BigQuery client
    client = bigquery.Client()

    # Query the BigQuery table
    query = f"SELECT * FROM `{table_name}`"
    dataframe = client.query(query).to_dataframe()

    x = dataframe[independent_vars]

    y = dataframe[f"{dependent_var}"]

    X_train, X_test, y_train, y_test = train_test_split(
        x, y, test_size=0.2, random_state=47
    )

    lgb_train = lgb.Dataset(X_train, y_train)
    lgb_eval = lgb.Dataset(X_test, y_test, reference=lgb_train)

    evals_result = {}  # to record eval results for plotting

    # Specify model configuration
    params = {
        "boosting_type": "gbdt",
        "objective": "regression",
        "metric": {"l2", "l1"},
        "num_leaves": 20,  # Finalized
        "learning_rate": 0.1,  # Finalized
        "feature_fraction": 0.9,
        "bagging_fraction": 0.8,
        "bagging_freq": 1,
        "verbose": -1,  # Remove most logging functionality
        "max_depth": 3,  # Finalized
    }

    logger.info("Starting training...")
    # train
    gbm = lgb.train(
        params,
        lgb_train,
        num_boost_round=1000,
        valid_sets=lgb_eval,
        callbacks=[
            lgb.early_stopping(stopping_rounds=10),
            lgb.record_evaluation(evals_result),
            lgb.log_evaluation(10),
        ],
    )

    logger.info("Starting predicting...")

    y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)

    logger.info("Conducting model evaluation...")

    mse_test = mean_squared_error(y_test, y_pred)
    logger.info(f"The MSE of prediction is: {mse_test}.")

    mae_test = mean_absolute_error(y_test, y_pred)
    logger.info(f"The MAE of prediction is: {mae_test}.")

    r2 = round(r2_score(y_test, y_pred), 2)
    logger.info(
        f"The R² (coefficient of determination) of prediction is: {r2}."
    )

    what_if_frame = pandas.DataFrame(what_if_dict, index=[0])

    prediction_object = gbm.predict(
        what_if_frame, num_iteration=gbm.best_iteration
    )

    logger.info("Providing Prediction for What-If Dict:")
    logger.debug(what_if_dict)
    prediction = prediction_object[0]

    logger.info(f"Prediction: {prediction}.")

    """ IF YOU WOULD LIKE TO CREATE THE CHARTS, PLEASE UNCOMMENT THE BELOW """
    """ AND RUN IN TERMINAL: conda install python-graphviz """
    """ BEFORE RUNNING LOCALLY """

    # logger.info("Plotting metrics recorded during training...")
    # ax = lgb.plot_metric(evals_result, metric="l1")
    # ax.set_title(f"Metric l1 (MAE) During Training - {league}")
    # plt.savefig(relative_path_save_images + "training_l1_metric.png")
    #
    # ax = lgb.plot_metric(evals_result, metric="l2")
    # ax.set_title(f"Metric l2 (MSE) During Training - {league}")
    # plt.savefig(relative_path_save_images + "training_l2_metric.png")
    #
    # logger.info("Plotting feature importances...")
    # ax = lgb.plot_importance(gbm, max_num_features=25)
    # ax.set_title(f"Feature Importances - {league}")
    # plt.tight_layout()
    # plt.savefig(relative_path_save_images + "feature_importances.png")
    #
    # # Get feature importances
    # feature_importances = gbm.feature_importance(importance_type='split')
    # feature_importance_dict = dict(zip(gbm.feature_name(), feature_importances))
    #
    # num_features = len(independent_vars)
    #
    # num_cols = math.ceil(math.sqrt(num_features))
    # num_rows = math.ceil(num_features / num_cols)
    #
    # fig, axes = plt.subplots(num_rows, num_cols, figsize=(num_cols * 4, num_rows * 3))
    #
    # axes = axes.flatten()
    #
    # for idx, (feature_name, ax) in enumerate(zip(independent_vars, axes)):
    #     importance = feature_importance_dict.get(feature_name, 0)
    #     # Feature used in splitting
    #     if importance > 0:
    #         lgb.plot_split_value_histogram(
    #             gbm, feature=feature_name, bins="auto", ax=ax
    #         )
    #         ax.set_title(feature_name, fontsize=10)
    #         ax.set_xlabel("Split Value", fontsize=8)
    #         ax.set_ylabel("Frequency", fontsize=8)
    #         ax.tick_params(axis='both', which='major', labelsize=6)
    #     else:
    #         # Feature not used in splitting
    #         ax.text(0.5, 0.5, 'Not used in splitting', horizontalalignment='center',
    #                 verticalalignment='center', fontsize=10)
    #         ax.set_title(feature_name + ' (Unused)', fontsize=10)
    #         ax.set_xticks([])
    #         ax.set_yticks([])
    #
    # for idx in range(num_features, num_rows * num_cols):
    #     fig.delaxes(axes[idx])
    #
    # plt.tight_layout()
    #
    # plt.savefig(relative_path_save_images + "split_value_histogram.png")
    #
    # last_tree_index = gbm.num_trees() - 1
    #
    # logger.info("Plotting 1st tree with graphviz...")
    # first_tree_graph = lgb.create_tree_digraph(gbm, tree_index=0, name="Tree1")
    # first_tree_graph.render(
    #     filename=relative_path_save_images + "first_tree",
    #     format="png",
    #     view=False,
    # )
    #
    # logger.info("Plotting last tree with graphviz...")
    # last_tree_graph = lgb.create_tree_digraph(
    #     gbm, tree_index=last_tree_index, name="LastTree"
    # )
    # last_tree_graph.render(
    #     filename=relative_path_save_images + "last_tree",
    #     format="png",
    #     view=False,
    # )

    return jsonify({"predicted_value": prediction}), 200


# functions-framework --target train_lgbm --source machine_learning_models/light_gradient_boosting_machine/main.py
