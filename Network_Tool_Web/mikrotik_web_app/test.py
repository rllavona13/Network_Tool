import mysql.connector
from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def get_data():

    cnx = mysql.connector.connect(user='python',
                                  password='yzh8RB0Bcw1VivO3',
                                  host='localhost',
                                  database='test')
    cursor = cnx.cursor()

    query = "SELECT * FROM devices"

    cursor.execute(query)

    for (name, ip, scanned_date) in cursor:

        return render_template("index.html", data=('%s', '%s', '%s') % (name, ip, scanned_date))

    cursor.close()
    cnx.close()


if __name__ == '__main__':

    app.run(port=5000, debug=True)


