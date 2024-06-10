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
    postgres_hook = PostgresHook('destination_db')

    # Retrieving the connection object
    db_conn = postgres_hook.get_sqlalchemy_engine()
    
    # Instantiating metadata object
    metadata = MetaData()

    # Creating the table
    flats_table = Table(
        'flats_init',
        metadata,
        Column('id', BigInteger, primary_key=True, autoincrement=True),
        Column('flat_id', BigInteger),
        Column('build_year', BigInteger),
        Column('building_type_int', BigInteger),
        Column('latitude', Float),
        Column('longitude', Float),
        Column('ceiling_height', Float),
        Column('flats_count', BigInteger),
        Column('floors_total', BigInteger),
        Column('has_elevator', Boolean),
        Column('floor', BigInteger),
        Column('kitchen_area', Float),
        Column('living_area', Float),
        Column('rooms', BigInteger),
        Column('is_apartment', Boolean),
        Column('studio', Boolean),
        Column('total_area', Float),
        Column('price', BigInteger),
        UniqueConstraint('flat_id', name='unique_flat_id_constraint'),
    ) 

    # Checking the existence of table in DB and adding a new table (if needed)
    if not inspect(db_conn).has_table(flats_table.name):
        metadata.create_all(db_conn)


def extract(**kwargs):
    """Extracts the information from the database."""

    postgres_hook = PostgresHook('destination_db')

    db_conn = postgres_hook.get_conn()

    # Defining a SQL-query for extracting data from DB
    sql = f"""
    SELECT
        f.id flat_id, b.build_year, b.building_type_int, b.latitude, b.longitude,
        b.ceiling_height, b.flats_count, b.floors_total, b.has_elevator, f.floor,
        f.kitchen_area, f.living_area, f.rooms, f.is_apartment, f.studio, f.total_area,
        f.price
    FROM flats f
    LEFT JOIN buildings b ON b.id = f.building_id
    """

    # Extracting data
    data = pd.read_sql(sql, db_conn)
    db_conn.close()
    
    # Pushing the extracted data to the next task
    ti = kwargs['ti']
    ti.xcom_push('extracted_data', data)


def load(**kwargs):
    """Loads the extracted data to the database."""

    postgres_hook = PostgresHook('destination_db')

    # Pulling the data from the previous task
    ti = kwargs['ti']
    data = ti.xcom_pull(task_ids='extract', key='extracted_data')
    
    # Inserting data into a new table
    postgres_hook.insert_rows(
            table="flats_init",
            replace=True,
            target_fields=data.columns.tolist(),
            replace_index=['flat_id'],
            rows=data.values.tolist()
    )
