# Predictive Factors of Team Success in the WNBA: A Comparative Analysis with the NBA                                       !


## INTERACTIVE WEBSITE AND VISUALIZATION

https://team-23-mj-6242.uw.r.appspot.com/

## DEMO VIDEO

https://www.youtube.com/watch?v=Z5mvUHS3puI

## Description

The Team 22 Project aims to compare predictors of team success between the NBA and WNBA via visualizations and machine learning models.
Key components are:
- Get Data
  - R and Python code to get data from the Wehoop and NBA APIs, respectively.
  - Related Files: CODE/WNBA, CODE/nba
- Data Warehouse / Data Pipeline
  - The data warehouse / data pipeline in BigQuery, built via dbt and SQL to transform the data from the APIs into finalized tables.
  - Related Files: CODE/team_23_data_warehouse 
- Correlation / Mutual Info and PCA
  - Python code to conduct correlation and mutual info checks, and principal component analysis on the finalized datasets.
  - Related Files: CODE/correlation_and_pca
- Implement LightGBM, OLS Linear Regression, and Random Forest Regressor
  - Machine learning models built in Python to predict number of season wins based on the finalized datasets.
  - Related Files: CODE/machine_learning_models
- Visualization App
  - A Dash app built with Python which contains the visualizations and interacts with BigQuery and the LightGBM Cloud Function.
  - Please go to the link below to access the app:
    - https://team-23-mj-6242.uw.r.appspot.com/
  - Related Files: CODE/visualization_app
- The Demo
  - Python file run_demo.py is our code demo, intended for the graders. It can be run with:
    - python run_demo.py

## Installation

pip install -r requirements.txt

You will need to install graphviz if you want to create the LightGBM charts, with:

conda install python-graphviz

## Execution

The file "run_demo.py" was created as a demonstration of how the data was collected and the analyses performed.

Please run the following to execute the demo:

python run_demo.py

## How the Project works

The project has many different applications and scripts that work independently. 

For example:
- The visualization Dash app was deployed on GCP App Engine, and interacts with BigQuery and the LightGBM cloud function. 
- The Pythons scripts can generally be run via python __.py, or via functions framework (LightGBM).
- The data warehouse was built using dbt. If you cd into the data warehouse and then run 'dbt run', the tables will build.
- Various WNBA APIs were accessed via R.

To run the lightgbm model, you will need to first run in terminal:

functions-framework --target train_lgbm --source machine_learning_models/light_gradient_boosting_machine/main.py

This will spin up the functions framework server.

Then, make a POST request to it with the payload (BigQuery table name, ind/dependent variable names, what-if dict.) like this:

{
  "bigquery_table_name": "team-23-mj-6242.team_23_dataset.combined_nba_data",
  "dependent_var": "season_wins",
  "independent_vars": ["AVG_ASSISTS", "AVG_DEF_REBOUNDS", "AVG_FIELD_GOAL_PCT", 
"AVG_FOULS", "AVG_TOT_TURNOVERS", "per_jumpshots", "per_pts_off_assists", "per_secondchance"],
  "what_if_dict": {"AVG_ASSISTS":10, "AVG_DEF_REBOUNDS":10, "AVG_FIELD_GOAL_PCT":10, 
"AVG_FOULS":10, "AVG_TOT_TURNOVERS":10, "per_jumpshots":10, "per_pts_off_assists":10, "per_secondchance":10}
}

You can make a POST request via Insomnia / Postman, etc.

## Clone the Project

Using terminal/command prompt:
- Set working directory to where you want the Python project saved
- Run the following in terminal / command prompt:
  - git clone https://github.com/team-23-mj/team_23
- Project should be cloned successfully.

## Important
Activate conda environment for project upon initialization:

conda activate team_23

## Linting Requirements
Python and SQL linting have been enforced in the repository (via GitHub Actions).
When you commit and push, and/or open a PR, GitHub Actions will invoke the linters.
If the workflow fails after a commit or PR, take a look at the Actions tab of the repo.
Click on the workflow run and you'll be able to see why it failed in the "Lint with black and sqlfluff" section.

Lint Python files with black:

black folder1/folder2/file.py --line-length 79

https://github.com/psf/black

Lint SQL files with sqlfluff:

sqlfluff lint team_23_data_warehouse/models/. --dialect bigquery

Fix the SQL files with sqlfluff:

sqlfluff fix team_23_data_warehouse/models/. --dialect bigquery

https://sqlfluff.com/

## Code References

Example Python code for LightGBM model (Microsoft LightGBM official repo): 
https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/simple_example.py

Example Python code for visualizations for LightGBM model (Microsoft LightGBM official repo):
https://github.com/microsoft/LightGBM/blob/master/examples/python-guide/plot_example.py

Example to get play-by-play data from the NBA API: 
https://github.com/swar/nba_api/blob/master/docs/examples/PlayByPlay.ipynb

Example to get play-by-play data from the WNBA API: 
https://wehoop.sportsdataverse.org/articles/getting-started-wehoop.html#quick-start
