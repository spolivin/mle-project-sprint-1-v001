import os
import yaml

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine


def create_connection():
    """Connects to PostreSQL database."""

    # Loading envirornmental variables
    load_dotenv()

    # Retrieving the values of env-variables
    host = os.environ.get("DB_DESTINATION_HOST")
    port = os.environ.get("DB_DESTINATION_PORT")
    db = os.environ.get("DB_DESTINATION_NAME")
    username = os.environ.get("DB_DESTINATION_USER")
    password = os.environ.get("DB_DESTINATION_PASSWORD")

    # Establishing a connection
    db_conn = create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{db}",
        connect_args={"sslmode": "require"},
    )

    return db_conn


def get_data():
    """Saves the cleaned data from the DB in the local dir."""

    # Reading parameters
    with open("params.yaml", "r") as fd:
        params = yaml.safe_load(fd)

    # Pulling the data from DB
    db_conn = create_connection()
    data = pd.read_sql(
        "SELECT * FROM flats_clean", db_conn, index_col=params["index_col"]
    )
    data.drop(params["cols_to_drop"], axis=1, inplace=True)
    db_conn.dispose()

    # Locally saving the data
    os.makedirs("data", exist_ok=True)
    data.to_csv("data/initial_data_flats.csv", index=None)


if __name__ == "__main__":
    get_data()
