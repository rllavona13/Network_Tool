from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy import MetaData


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_data():

    mikrotik_list = []
    metadata = MetaData()

    engine = create_engine('mysql://python:yzh8RB0Bcw1VivO3@localhost/test')

    connection = engine.connect()
    sql_data_query = connection.execute('SELECT * FROM devices')

    for row in sql_data_query:

        mikrotik_list.append(row)

        return render_template('show_scan.html', mikrotik_list=row)

    metadata.create_all(engine)


if __name__ == '__main__':

    app.run(port=5000, debug=True)


