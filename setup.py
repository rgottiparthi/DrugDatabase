import sqlite3

conn = sqlite3.connect('drugData.db')


conn.execute('''CREATE TABLE Drugs
               (D_Name TEXT,
                Basic_Description TEXT,
                Adverse_Effect_Description TEXT)''')