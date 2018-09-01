from flask import Flask, render_template, request
import mysql.connector
import sys
import json

app = Flask(__name__)

config_file = open('auth.json')
config = json.load(config_file)
config_file.close()


def get_home():
    pass


def add_task():
    pass


def main_function():
    pass
