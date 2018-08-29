import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy import inspect

metadata = MetaData()

engine = create_engine('mysql://python:yzh8RB0Bcw1VivO3@localhost/test')

with engine.connect() as connection:

    sql_data = connection.execute('SELECT * FROM devices')

    for row in sql_data:
        print(row)

metadata.create_all(engine)
