import os

from sqlalchemy import (Column, Integer, MetaData, String, Table,
                        create_engine, ARRAY)

from databases import Database

POSTGRES_USER : str = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DB : str = os.getenv("POSTGRES_DB")
DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@cast-service:5432/{POSTGRES_DB}"

engine = create_engine(DATABASE_URI)
metadata = MetaData()

casts = Table(
    'casts',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String(50)),
    Column('nationality', String(20)),
)

database = Database(DATABASE_URI)