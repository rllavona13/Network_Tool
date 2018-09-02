from flask import Flask, render_template, request
import mysql.connector
import sys
import json

app = Flask(__name__)

config_file = open('auth.json')
config = json.load(config_file)
config_file.close()


@app.route('/')
def get_home():
    return render_template('home.html')


def add_task():
    pass


def main_function():
    pass


if __name__ == '__main__':

    app.run(port=5000, debug=True)
