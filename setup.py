import sqlite3

conn = sqlite3.connect('drugData.db')
cur = conn.cursor()

# drugs table
cur.execute('''CREATE TABLE Drugs
               (D_Name TEXT PRIMARY KEY,
                Basic_Description TEXT,
                Toxicity TEXT,
                Indications TEXT,
                Food_Interactions TEXT)''')

# products table
cur.execute('''CREATE TABLE Products
               (P_Name TEXT PRIMARY KEY,
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

#conn.execute('''CREATE TABLE Indications
#               (I_Name TEXT,
#                Severity TEXT,
#                Description TEXT
#                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

#conn.execute('''CREATE TABLE Treats
#               (D_Name TEXT,
#                I_Name TEXT,
#                PRIMARY KEY(D_Name_1, D_Name_2),
#                FOREIGN KEY (D_Name_1)
#                    ON DELETE CASCADE ON UPDATE NO ACTION,
#                FOREIGN KEY (I_Name_2)
#                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

cur.execute('''CREATE TABLE User
               (Username TEXT PRIMARY KEY,
                Age INT,
                Sex TEXT)''')

cur.execute('''CREATE TABLE Interacts
               (D_Name_1 TEXT,
                D_Name_2 TEXT,
                I_Description TEXT,
                PRIMARY KEY(D_Name_1, D_Name_2),
                FOREIGN KEY (D_Name_1) REFERENCES Drugs(D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (D_Name_2) REFERENCES Drugs(D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

cur.execute('''CREATE TABLE Takes
               (UserID TEXT PRIMARY KEY,
                D_Name TEXT,
                FOREIGN KEY (D_Name) REFERENCES Drugs(D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

#conn.execute('''CREATE TABLE Has
#               (UserID TEXT,
#                I_Name TEXT,
#                FOREIGN KEY (UserID)
#                    ON DELETE CASCADE ON UPDATE NO ACTION,
#                FOREIGN KEY (I_Name)
#                    ON DELETE CASCADE ON UPDATE NO ACTION)''')


import xml.etree.ElementTree as et

# Parsing the XML file
tree = et.parse('full_database.xml')
root = tree.getroot()

# drugs data
for drug in root:
    name = drug.find("{http://www.drugbank.ca}name").text
    desc = drug.find("{http://www.drugbank.ca}description").text
    toxicity = drug.find("{http://www.drugbank.ca}toxicity").text
    # ADD INDICATIONS
    cur.execute('''INSERT INTO Drugs (D_Name, Basic_Description, Toxicity) 
                    VALUES (?, ?)''', (name, desc, toxicity))
conn.commit()
 

# products data
n = 0
for drug in root:
    if n < 10:
        name = drug.find("{http://www.drugbank.ca}name").text
        products = drug.find("{http://www.drugbank.ca}products")
        for product in products:
            p_name = product.find("{http://www.drugbank.ca}name").text
            p_labeller = product.find("{http://www.drugbank.ca}labeller").text
            p_marketing_start = product.find("{http://www.drugbank.ca}started-marketing-on").text
            p_marketing_end = product.find("{http://www.drugbank.ca}ended-marketing-on").text
            p_dosage = product.find("{http://www.drugbank.ca}dosage-form").text
            p_strength = product.find("{http://www.drugbank.ca}strength").text
            p_route = product.find("{http://www.drugbank.ca}route").text
            p_generic = product.find("{http://www.drugbank.ca}generic").text
            p_otc = product.find("{http://www.drugbank.ca}over-the-counter").text

            cur.execute('''INSERT INTO Products (P_Name, Form, Strength, Route, Manufacturer, 
                            Marketing_start, Marketing_end, Generic, OTC, D_NAME) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                            (p_name, p_dosage, p_strength, p_route, p_labeller, p_marketing_start, p_marketing_end,
                            p_generic, p_otc, name))
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