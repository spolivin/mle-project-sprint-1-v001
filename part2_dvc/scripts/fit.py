import joblib
import os
import yaml

import pandas as pd
from catboost import CatBoostRegressor
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler


def fit_model():
    """Trains and saves the model in the local dir."""
	
    # Reading the parameters
    with open('params.yaml', 'r') as fd:
        params = yaml.safe_load(fd)
	
    # Loading the data to DataFrame
    data = pd.read_csv('data/initial_data_flats.csv')

    # Selecting features to be scaled
    cat_features = data.select_dtypes('int64').drop('price', axis=1)
    cat_features_uniq_counts = cat_features.nunique()
    cat_features_to_scale = cat_features_uniq_counts[cat_features_uniq_counts > 10].index.tolist()
    num_features = data.select_dtypes('float64').columns.tolist()
    features_to_scale = num_features + cat_features_to_scale

    # Instantiating a columns preprocessor
    preprocessor = make_column_transformer(
        (StandardScaler(), features_to_scale),
        remainder='passthrough',
        verbose_feature_names_out=False,
    )

    # Building a pipeline
    model = CatBoostRegressor(verbose=False)
    pipe = make_pipeline(preprocessor, model)
    
    # Separating features from target
    target = data[params['target_col']]
    features = data.drop(params['target_col'], axis=1)

    # Training the model
    pipe.fit(features, target)
    
	# Locally saving the trained model
    os.makedirs('models', exist_ok=True)
    with open('models/fitted_model_flats.pkl', 'wb') as fd:
        joblib.dump(pipe, fd)


if __name__ == '__main__':
	fit_model()
