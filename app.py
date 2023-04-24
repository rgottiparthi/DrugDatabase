from flask import Flask, render_template, request
from socket import *
import sqlite3 as sql
import plotly.graph_objs as go
import plotly.offline as pyo
import networkx as nx

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
   
   cur.execute('''
      SELECT u.UserID, u.Age, u.Sex, t.D_Name, h.I_Name 
      FROM User u
      LEFT JOIN Takes t ON u.UserID = t.UserID
      LEFT JOIN Has h ON u.UserID = h.UserID
   ''')
   
   users = cur.fetchall()
   numUser = len(users)
   
   return render_template('viewProfiles.html', numUser=numUser, users=users)


@app.route('/search')
def search():
   return render_template('search.html')

@app.route('/interactionsGraph')
def inputGraph():
   return render_template('interactionsGraph.html')

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
         new_drug = request.form.get('drug name')
         if new_drug:
            cur.execute("SELECT D_Name FROM Drugs WHERE D_Name = ?", (new_drug,) )
            d_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Takes (UserID, D_Name) VALUES (?,?)", (username, d_id,) )

         new_indication = request.form.get('indication name')
         if new_indication:
            cur.execute("SELECT I_Name FROM Indications WHERE I_Name = ?", (new_indication,) )
            i_id = cur.fetchone()[0]
            cur.execute("INSERT INTO Has (UserID, I_Name) VALUES (?,?)", (username, i_id,) )

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

@app.route('/product-result', methods=['POST', 'GET'])
def product():
    if request.method == 'POST':
      productName = request.form['Product Name']
         # connect to the database and acquire a "cursor"
      with sql.connect("drugData.db") as con:
            cur = con.cursor()
            cur.execute('''SELECT Products.*, Drugs.Basic_Description, Drugs.Toxicity, Drugs.Indications
                           FROM Products
                           JOIN Drugs ON Products.D_Name = Drugs.D_Name
                           WHERE Products.P_Name = ?;''', (productName,))
            result = cur.fetchall()

            if result:
                  # fill in the values in the HTML table
                  attributes = ["Product Name", "Form", "Strength", "Route", "Manufacturer", "Marketing Start",
                              "Marketing End", "Generic", "OTC"]
                  product_data = result[0]
                  return render_template("productResults.html", attributes=attributes, product_data=product_data)
            else:
                  return "No results found for this product name."

@app.route('/delete-profile', methods=['POST', 'GET'])
def deleteProfile():
   if request.method == 'POST':
        username = request.form['username']

        # connect to the database and acquire a "cursor"
        with sql.connect("drugData.db") as con:
            cur = con.cursor()
            cur.execute('''DELETE FROM User WHERE UserID = ?;''', (username,))
            return render_template("home.html")

@app.route('/graph', methods=['POST', 'GET'])
def graph():
   if request.method == 'POST':
      drugs = []
      for i in range(10):
         drug_name = request.form.get(f"Drug {i+1} Name")
         if drug_name:
               drugs.append(drug_name)
         else:
            drugs.append(None)
      
      # Connect to the SQLite database
      conn = sql.connect('drugData.db')

      # Execute SQL query to retrieve drug interaction data
      cur = conn.cursor()
      #cur.execute('SELECT D_Name_1, D_Name_2, I_Description FROM Interacts WHERE D_Name_1 = ? LIMIT 10', ("Ibuprofen",))
      cur.execute('''SELECT D_Name_1, D_Name_2, I_Description
                     FROM Interacts
                     WHERE (D_Name_1 IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                     AND D_Name_2 IN (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                     AND D_Name_1 < D_Name_2)''', (drugs[0], drugs[1], drugs[2], drugs[3], drugs[4], drugs[5], drugs[6], drugs[7], drugs[8], drugs[9], drugs[0], drugs[1], drugs[2], drugs[3], drugs[4], drugs[5], drugs[6], drugs[7], drugs[8], drugs[9]))


      # Fetch the results and create a list of edges
      interactions = cur.fetchall()

      numInteractions = 0
      # Create the graph
      G = nx.Graph()
      for interaction in interactions:
         numInteractions += 1
         D_Name_1, D_Name_2, description = interaction
         G.add_edge(D_Name_1, D_Name_2, description=description)

      # Close the database connection
      conn.close()

      # Define node positions for the graph layout
      pos = nx.spring_layout(G)

      # Create a list of edge trace objects with descriptions
      edge_trace = []
      for edge in G.edges():
         x0, y0 = pos[edge[0]]
         x1, y1 = pos[edge[1]]
         trace = go.Scatter(x=[x0, x1, None], y=[y0, y1, None],
                           mode='lines',
                           line=dict(width=10),
                           hoverinfo='text', # set hoverinfo to "text"
                           hovertext=G[edge[0]][edge[1]]['description']) # set hovertext to description
         edge_trace.append(trace)

      # Create a list of node trace objects
      node_trace = go.Scatter(x=[], y=[], text=[], mode='markers', hoverinfo='text',
                              marker=dict(color='black', size=20, line=dict(width=2)))

      # Add node positions and labels to the node trace
      for node in G.nodes():
         x, y = pos[node]
         node_trace['x'] += tuple([x])
         node_trace['y'] += tuple([y])
         node_trace['text'] += tuple([node])

      # Create the figure object
      fig = go.Figure(data=edge_trace + [node_trace],
                     layout=go.Layout(
                        title='<br>Drug Interaction Graph',
                        titlefont_size=16,
                        showlegend=True,
                        hovermode='closest',
                        margin=dict(b=20, l=5, r=5, t=40),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False)))

      # Display the figure
      pyo.plot(fig, filename='templates/drug_interaction_graph.html')

      return render_template("interactionsGraphResults.html", interactions=interactions, numInteractions=numInteractions )

if __name__ == '__main__':
   app.run(debug = True)