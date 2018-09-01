from flask import Flask, render_template, request
import mysql.connector
import sys
import json

app = Flask(__name__)
