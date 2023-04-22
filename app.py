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

@app.route('/submit-profile',methods = ['POST', 'GET'])
def submit_profile():
   if request.method == 'POST':
      try:
         username = request.form['username']
         age = int(request.form['age'])
         sex = request.form['sex']

         # connect to the database and aquire a "cursor"
         with sql.connect("drugData.db") as con:
            cur = con.cursor()
            # insert the form values in the database
            cur.execute("INSERT INTO User (Username, Age, Sex) VALUES (?,?,?)",(username, age, sex) )
            con.commit()
      except:
         con.rollback()
      
      finally:
         return render_template("home.html")
         con.close()




if __name__ == '__main__':
   app.run(debug = True)