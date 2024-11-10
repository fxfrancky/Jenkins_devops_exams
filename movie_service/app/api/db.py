import os
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
from databases import Database

POSTGRES_USER : str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB : str = os.getenv("POSTGRES_DB")
POSTGRES_HOST = "moviedb-service"
PORT = 5432

DATABASE_URI = "postgresql+psycopg2://{db_username}:{db_password}@{db_host}:{db_port}/{db_name}".format(
        db_username=POSTGRES_USER, 
        db_password=POSTGRES_PASSWORD,
        db_host=POSTGRES_HOST,
        db_port=PORT,
        db_name=POSTGRES_DB
    ) 
engine = create_engine(DATABASE_URI)
metadata = MetaData()

movies = Table(
    'movies',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('plot', String(250)),
    Column('genres', ARRAY(String)),
    Column('casts_id', ARRAY(Integer))
)

database = Database(DATABASE_URI)