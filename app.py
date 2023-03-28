from flask import Flask, render_template, request
from socket import *
import sqlite3 as sql

def flaskUpdate():
   s= socket(AF_INET, SOCK_STREAM)

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('home.html')

if __name__ == '__main__':
   app.run(debug = True)