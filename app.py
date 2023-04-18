from flask import Flask, render_template, request
from socket import *
import sqlite3 as sql

def flaskUpdate():
   s= socket(AF_INET, SOCK_STREAM)

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('home.html')

@app.route('/profile')
def profile():
   return render_template('profile.html')

@app.route('/aggregate')
def aggregate():
   return render_template('aggregate.html')

@app.route('/insert')
def insert():
   return render_template('insert.html')

@app.route('/search')
def search():
   return render_template('search.html')


if __name__ == '__main__':
   app.run(debug = True)