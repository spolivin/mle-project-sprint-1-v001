import joblib
import json
import os
import yaml

import pandas as pd
from sklearn.model_selection import cross_validate


def evaluate_model():
    # Reading the parameters
    with open("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)

    # Loading the trained model
    with open("models/fitted_model_flats.pkl", "rb") as fd:
        pipeline = joblib.load(fd)

    # Reading the data
    data = pd.read_csv("data/initial_data_flats.csv")

    # Separating features from target
    target = data[params["target_col"]]
    features = data.drop(params["target_col"], axis=1)

    # Launching cross-validation
    cv_res = cross_validate(
        pipeline,
        features,
        target,
        cv=params["n_splits"],
        n_jobs=params["n_jobs"],
        scoring=params["metrics"],
    )
    for key, value in cv_res.items():
        cv_res[key] = round(value.mean(), 3)

    # Locally saving cross-validation results
    os.makedirs("cv_results", exist_ok=True)
    with open("cv_results/cv_res_flats.json", "w") as fd:
        json.dump(cv_res, fd)


if __name__ == "__main__":
    evaluate_model()
