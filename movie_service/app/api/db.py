import os
from sqlalchemy import (Column, DateTime, Integer, MetaData, String, Table,
                        create_engine, ARRAY)
from databases import Database


POSTGRES_USER : str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB : str = os.getenv("POSTGRES_DB")
POSTGRES_HOST = "moviedb-service"
POSTGRES_PORT = '5432'
DATABASE_URI = "postgresql://movie_db_username:movie_db_password@moviedb-service:5432/movie_db_dev"

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