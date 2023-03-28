import sqlite3

conn = sqlite3.connect('drugData.db')


conn.execute('''CREATE TABLE Reviews
               (Username TEXT,
                MovieID TEXT,
                ReviewTime DATETIME,
                Rating REAL,
                Review TEXT)''')