import pandas as pd
from airflow.providers.postgres.hooks.postgres import PostgresHook
from sqlalchemy import (
    Boolean,
    Column,
    Float,
    BigInteger,
    MetaData,
    Table,
    UniqueConstraint,
    inspect,
)


def create_table():
    """Initializes the table in the database."""

    # Instantiating a PostgreSQL hook
    postgres_hook = PostgresHook("destination_db")

    # Retrieving the connection object
    db_conn = postgres_hook.get_sqlalchemy_engine()

    # Instantiating metadata object
    metadata = MetaData()

    # Creating the table
    flats_table = Table(
        "flats_clean",
        metadata,
        Column("id", BigInteger, primary_key=True, autoincrement=True),
        Column("flat_id", BigInteger),
        Column("build_year", BigInteger),
        Column("building_type_int", BigInteger),
        Column("latitude", Float),
        Column("longitude", Float),
        Column("ceiling_height", Float),
        Column("flats_count", BigInteger),
        Column("floors_total", BigInteger),
        Column("has_elevator", Boolean),
        Column("floor", BigInteger),
        Column("kitchen_area", Float),
        Column("living_area", Float),
        Column("rooms", BigInteger),
        Column("is_apartment", Boolean),
        Column("studio", Boolean),
        Column("total_area", Float),
        Column("price", BigInteger),
        UniqueConstraint("flat_id", name="unique_flat_id_constraint_clean"),
    )

    # Checking the existence of table in DB and adding a new table (if needed)
    if not inspect(db_conn).has_table(flats_table.name):
        metadata.create_all(db_conn)


def extract(**kwargs):
    """Extracts the information from the prepared DB."""

    postgres_hook = PostgresHook("destination_db")

    db_conn = postgres_hook.get_conn()

    # SQL-query
    sql = f"""
    SELECT *
    FROM flats_init
    """

    # Extracting data from DB
    data = pd.read_sql(sql, db_conn)
    db_conn.close()

    # Pushing extracted data to the next task
    ti = kwargs["ti"]
    ti.xcom_push("extracted_data", data)


def transform(**kwargs):
    """Cleans the data from duplicates and outliers."""

    # Pulling data from the previous task
    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="extract", key="extracted_data")

    # Removing duplicates
    feature_cols = data.columns.drop(["id", "flat_id"]).tolist()
    is_duplicated_features = data.duplicated(subset=feature_cols, keep=False)
    data = data[~is_duplicated_features].reset_index(drop=True)

    # Removing outliers
    num_cols = data[feature_cols].select_dtypes(["float", "int"]).columns
    threshold = 1.5
    potential_outliers = pd.DataFrame()

    for col in num_cols:
        quartile_1 = data[col].quantile(0.25)
        quartile_3 = data[col].quantile(0.75)
        iq_range = quartile_3 - quartile_1
        margin = threshold * iq_range
        lower = quartile_1 - margin
        upper = quartile_3 + margin
        potential_outliers[col] = ~data[col].between(lower, upper)

    outliers = potential_outliers.any(axis=1)
    data = data[~outliers]

    # Pushing the transformed data to the next task
    ti.xcom_push("transformed_data", data)


def load(**kwargs):
    """Loads the extracted data to the DB."""

    postgres_hook = PostgresHook("destination_db")

    ti = kwargs["ti"]
    data = ti.xcom_pull(task_ids="transform", key="transformed_data")

    postgres_hook.insert_rows(
        table="flats_clean",
        replace=True,
        target_fields=data.columns.tolist(),
        replace_index=["flat_id"],
        rows=data.values.tolist(),
    )
