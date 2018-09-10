from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy import MetaData
import MySQLdb


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def get_data():

    db = MySQLdb.connect("localhost", "python", "yzh8RB0Bcw1VivO3", "test")
    cursor = db.cursor()
    sql_query = 'SELECT * FROM devices'

    try:
        cursor.execute(sql_query)
        results = cursor.fetchall()
        return render_template('show_scan.html', mikrotik_list=results)

    except:
        return render_template('show_scan.html', mikrotik_list="Error: Cannot fetch data from Database")


if __name__ == '__main__':

    app.run(port=5000, debug=True)

