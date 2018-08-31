from sqlalchemy import create_engine
from sqlalchemy import MetaData


metadata = MetaData()

engine = create_engine('mysql://python:yzh8RB0Bcw1VivO3@localhost/test')

with engine.connect() as connection:

    sql_data_query = connection.execute('SELECT * FROM devices')

    for row in sql_data_query:
        print(row)

metadata.create_all(engine)
