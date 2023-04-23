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

@app.route('/viewProfiles')
def viewProfiles():
   conn = sql.connect('drugData.db')
   cur = conn.cursor()
   cur.execute('''SELECT COUNT(UserID) FROM User''')

   numUser = cur.fetchone()[0]
   numDrugs = list
   numIndications = list

   cur.execute('''SELECT UserID FROM User''')
   UserIDs = cur.fetchall()

   for UserIDs in users:
      cur.execute('''SELECT COUNT(D_Name) FROM Takes WHERE UserID = ?''', (UserIDs,))
      userTakes = cur.fetchall()
      numDrugs.insert(userTakes)

   for UserIDs in users:
      cur.execute('''SELECT COUNT(I_Name) FROM Takes WHERE UserID = ?''', (UserIDs,))
      userHas = cur.fetchall()
      numIndications.insert(userHas)

   cur.execute('''SELECT UserID, Age, Sex FROM User''')
   users = cur.fetchall()

   cur.execute('''SELECT D_Name FROM Takes''', ())
   drugs = cur.fetchall()

   cur.execute('''SELECT I_Name FROM Has''', ())
   indications = cur.fetchall()

   return render_template('viewProfiles.html', numUser = numUser, users = users, drugs = drugs, numDrugs = numDrugs, indications=indications, numIndications=numIndications)


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
         return render_template("viewProfiles.html")
         con.close()

@app.route('/update-profile',methods = ['POST', 'GET'])
def update_profile():
   if request.method == 'POST':
      try:
         # connect to the database and acquire a "cursor"
         with sql.connect("drugData.db") as con:
            cur = con.cursor()

         username = request.form['username']
         print(username)
         new_username = request.form.get('new username')
         print(new_username)
         if new_username:
            cur.execute("UPDATE User SET UserID = ? WHERE UserID = ?", (new_username, username,))
            cur.execute("SELECT UserID FROM User")
         new_age = request.form.get('age')
         if new_age:
            new_age = int(new_age)
            cur.execute("UPDATE User SET Age = ? WHERE UserID = ?", (new_age, new_username,))
         
         new_sex = request.form.get('sex')
         if new_sex:
            cur.execute("UPDATE User SET Sex = ? WHERE UserID = ?", (new_sex, new_username,))


         new_drug = request.form.get('drug name')
         new_indication = request.form.get('indication name')

         # insert the form values in the database
         if new_drug:
            cur.execute("SELECT * FROM Drugs WHERE D_Name = ?", (new_drug,) )
            result = cur.fetchone()
            if result:
               cur.execute("INSERT OR IGNORE INTO Takes (UserID, D_Name) VALUES (?,?)", (new_username, new_drug,) )
         
         if new_indication:
            cur.execute("SELECT * FROM Indications WHERE I_Name = ?", (new_indication,) )
            result = cur.fetchone()
            if result:
               cur.execute("INSERT OR IGNORE INTO Has (User_ID, I_Name) VALUES (?,?)", (new_username, new_indication,) )

         con.commit()
      except:
         con.rollback()
      
      finally:
         con.close()
         return render_template("home.html")
         
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