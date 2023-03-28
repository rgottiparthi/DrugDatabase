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

conn.execute('''CREATE TABLE Treats
               (D_Name TEXT,
                I_Name TEXT,
                PRIMARY KEY(D_Name_1, D_Name_2)
                FOREIGN KEY (D_Name_1) 
                FOREIGN KEY (I_Name_2)''')

conn.execute('''CREATE TABLE User
               (UserID TEXT,
                Age INT,
                Sex TEXT
                Pregnancy TEXT)''')

conn.execute('''CREATE TABLE Interacts
               (D_Name_1 TEXT,
                D_Name_2 TEXT,
                PRIMARY KEY(D_Name_1, D_Name_2)
                FOREIGN KEY (D_Name_1) REFERENCES Drugs(D_Name),
                FOREIGN KEY (D_Name_2) REFERENCES Drugs(D_Name))''')

conn.execute('''CREATE TABLE Takes
               (UserID TEXT 
                Age INTEGER,
                Sex TEXT
                Pregnancy TEXT)''')

