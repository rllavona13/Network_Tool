from sqlalchemy import create_engine
from sqlalchemy import MetaData
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def sql_query():

    engine = create_engine('mysql://python:yzh8RB0Bcw1VivO3@localhost/test')

    with engine.connect() as connection:

        sql_data_query = connection.execute('SELECT * FROM devices')

        for row in sql_data_query:

            data = row[1] + row[2]

            return render_template('test.html', data=data)


if __name__ == '__main__':

    app.run(debug=True)
