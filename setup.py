import sqlite3

conn = sqlite3.connect('drugData.db')
cur = conn.cursor()

# drugs table
cur.execute("DROP TABLE IF EXISTS Drugs")
cur.execute('''CREATE TABLE Drugs
               (D_Name TEXT PRIMARY KEY,
                Basic_Description TEXT,
                Toxicity TEXT,
                Indications TEXT)''')

# products table
cur.execute("DROP TABLE IF EXISTS Products")
cur.execute('''CREATE TABLE Products
               (P_ID INTEGER PRIMARY KEY,
                P_Name TEXT,
                Form TEXT,
                Strength TEXT,
                Route TEXT,
                Manufacturer TEXT,
                Marketing_start DATE,
                Marketing_end DATE,
                Generic TEXT,
                OTC TEXT,
                D_NAME TEXT NOT NULL,
                FOREIGN KEY (D_Name) REFERENCES Drugs (D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

cur.execute("DROP TABLE IF EXISTS Indications")
cur.execute('''CREATE TABLE Indications
               (I_Name TEXT PRIMARY KEY,
                Description TEXT)''')

cur.execute("DROP TABLE IF EXISTS Treats")
cur.execute('''CREATE TABLE Treats
               (D_Name TEXT,
                I_Name TEXT,
                PRIMARY KEY(D_Name, I_Name),
                FOREIGN KEY (D_Name) REFERENCES Drugs (D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (I_Name) REFERENCES Indications (I_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

cur.execute("DROP TABLE IF EXISTS User")
cur.execute('''CREATE TABLE User
               (UserID TEXT PRIMARY KEY,
                Age INT,
                Sex TEXT,
                Pregnancy TEXT,
                Indication1 TEXT,
                Indication2 TEXT,
                Indication3 TEXT)''')

cur.execute("DROP TABLE IF EXISTS Interacts")
cur.execute('''CREATE TABLE Interacts
               (D_Name_1 TEXT,
                D_Name_2 TEXT,
                I_Description TEXT,
                PRIMARY KEY(D_Name_1, D_Name_2),
                FOREIGN KEY (D_Name_1) REFERENCES Drugs(D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (D_Name_2) REFERENCES Drugs(D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

cur.execute("DROP TABLE IF EXISTS Takes")
cur.execute('''CREATE TABLE Takes
               (UserID TEXT PRIMARY KEY,
                D_Name TEXT,
                FOREIGN KEY (D_Name) REFERENCES Drugs(D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

cur.execute("DROP TABLE IF EXISTS Has")
cur.execute('''CREATE TABLE Has
               (UserID TEXT,
                I_Name TEXT,
                PRIMARY KEY(UserID, I_Name),
                FOREIGN KEY (UserID) REFERENCES User (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (I_Name) REFERENCES Indications (I_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')


import xml.etree.ElementTree as et
import csv

# Parsing the XML file
tree = et.parse("drugData.xml")
root = tree.getroot()

# importing indications.csv file
indications_file = open("indications.csv")
contents = csv.reader(indications_file)
cur.executemany("INSERT INTO Indications (I_Name, Description) VALUES (?, ?)", contents)
conn.commit()

# drugs data
n = 0
for drug in root:
    if n < 10:
        name = drug.find("{http://www.drugbank.ca}name").text
        desc = drug.find("{http://www.drugbank.ca}description").text
        toxicity = drug.find("{http://www.drugbank.ca}toxicity").text
        indication = drug.find("{http://www.drugbank.ca}indication").text
        cur.execute('''INSERT INTO Drugs (D_Name, Basic_Description, Toxicity, Indications) 
                        VALUES (?, ?, ?, ?)''', (name, desc, toxicity, indication))
    n += 1
conn.commit()
 

# products data
n = 0
productID = 0
for drug in root:
    if n < 10:
        name = drug.find("{http://www.drugbank.ca}name").text
        products = drug.find("{http://www.drugbank.ca}products")
        for product in products:
            country = product.find("{http://www.drugbank.ca}country").text
            if(country == 'US'):
                p_name = product.find("{http://www.drugbank.ca}name").text
                p_labeller = product.find("{http://www.drugbank.ca}labeller").text
                p_marketing_start = product.find("{http://www.drugbank.ca}started-marketing-on").text
                p_marketing_end = product.find("{http://www.drugbank.ca}ended-marketing-on").text
                p_dosage = product.find("{http://www.drugbank.ca}dosage-form").text
                p_strength = product.find("{http://www.drugbank.ca}strength").text
                p_route = product.find("{http://www.drugbank.ca}route").text
                p_generic = product.find("{http://www.drugbank.ca}generic").text
                p_otc = product.find("{http://www.drugbank.ca}over-the-counter").text
                cur.execute('''INSERT INTO Products (P_ID, P_Name, Form, Strength, Route, Manufacturer, 
                                Marketing_start, Marketing_end, Generic, OTC, D_NAME) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                                (productID, p_name, p_dosage, p_strength, p_route, p_labeller, p_marketing_start, p_marketing_end,
                                p_generic, p_otc, name))
                productID += 1
    n += 1
conn.commit()


# drug interactions data
n = 0
for drug in root:
    if n < 10:
        d1 = drug.find("{http://www.drugbank.ca}name").text
        interactions = drug.find("{http://www.drugbank.ca}drug-interactions")
        for i in interactions:
            d2 = i.find("{http://www.drugbank.ca}name").text
            i_desc = i.find("{http://www.drugbank.ca}description").text
            cur.execute("INSERT INTO Interacts (D_Name_1, D_Name_2, I_Description) VALUES (?, ?, ?)",
                        (d1, d2, i_desc))
    n += 1
conn.commit()



res = cur.execute("SELECT * FROM Drugs")
rec = res.fetchall()
for x in range(3):
    print(rec[x], "\n")

res2 = cur.execute("SELECT * FROM Indications")
rec2 = res.fetchall()
for x in range(3):
    print(rec2[x], "\n")


n = 0
for drug in root:
    if n < 10:
        name = drug.find("{http://www.drugbank.ca}name").text
        indication_desc = drug.find("{http://www.drugbank.ca}indication").text
        for row in content:
            if row[0] in indication_desc:
                cur.execute("INSERT INTO Treats (D_Name, I_Name) VALUES (?, ?)", (name, row[0]))
    n += 1
conn.commit()