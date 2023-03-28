import sqlite3

conn = sqlite3.connect('drugData.db')


conn.execute('''CREATE TABLE Drugs
               (D_Name TEXT,
                Basic_Description TEXT,
                Adverse_Effect_Description TEXT)''')

conn.execute('''CREATE TABLE Indications
               (I_Name TEXT,
                Severity TEXT,
                Description TEXT)''')

conn.execute('''CREATE TABLE User
               (UserID TEXT,
                Age INT,
                Sex TEXT
                Pregnancy TEXT)''')