import sqlite3

conn = sqlite3.connect('drugData.db')


conn.execute('''CREATE TABLE Drugs
               (D_Name TEXT PRIMARY KEY,
                Basic_Description TEXT,
                Adverse_Effect_Description TEXT)''')

conn.execute('''CREATE TABLE Products
               (P_Name TEXT PRIMARY KEY,
                Cost REAL,
                Form TEXT,
                Manufacturer TEXT,
                D_NAME TEXT NOT NULL
                FOREIGN KEY (D_Name) REFERENCES Drugs (D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

conn.execute('''CREATE TABLE Indications
               (I_Name TEXT PRIMARY KEY,
                Severity TEXT,
                Description TEXT)''')

conn.execute('''CREATE TABLE User
               (UserID TEXT PRIMARY KEY,
                Age INTEGER,
                Sex TEXT
                Pregnancy TEXT)''')