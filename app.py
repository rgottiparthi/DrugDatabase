from flask import Flask, render_template, request
from socket import *
import sqlite3 as sql

def flaskUpdate():
   s= socket(AF_INET, SOCK_STREAM)

app = Flask(__name__)

@app.route('/')
def index():
   return render_template('home.html')

@app.route('/createProfile')
def createProfile():
   return render_template('createProfile.html')

@app.route('/editProfile')
def editProfile():
   return render_template('editProfile.html')

@app.route('/viewProfile')
def viewProfile():
   conn = sql.connect('drugData.db')
   cur = conn.cursor()
   cur.execute('''SELECT COUNT(UserID) FROM User''')
   numUser = cur.fetchone()[0]
   cur.execute('''SELECT UserID, Age, Sex FROM User''')
   users = cur.fetchall()
   return render_template('viewProfile.html', numUser = numUser, users = users)


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
            cur.execute("INSERT INTO User (UserID, Age, Sex) VALUES (?,?,?)",(username, age, sex) )
            con.commit()
      except:
         con.rollback()
      
      finally:
         return render_template("home.html")
         con.close()

@app.route('/drug-result', methods=['POST', 'GET'])
def drugResult():
    if request.method == 'POST':
        drugName = request.form['Drug Name']

        # connect to the database and acquire a "cursor"
        with sql.connect("drugData.db") as con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Drugs WHERE D_Name = ?", (drugName,))
            result = cur.fetchone()

            if result:
                # unpack the result tuple into individual variables
                drugName, basicDescription, toxicity, indications = result

                # fill in the values in the HTML table
                return render_template("drugResults.html",
                                       drugName=drugName,
                                       basicDescription=basicDescription,
                                       toxicity=toxicity,
                                       indications=indications)
            else:
                return "No results found for this drug name."

if __name__ == '__main__':
   app.run(debug = True)