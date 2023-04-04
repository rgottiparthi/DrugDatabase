import sqlite3

conn = sqlite3.connect('drugData.db')


conn.execute('''CREATE TABLE Drugs
               (D_Name TEXT PRIMARY KEY,
                Basic_Description TEXT,
                Adverse_Effect_Description TEXT)''') # adverse effects description is not in the file

conn.execute('''CREATE TABLE Products
               (P_Name TEXT PRIMARY KEY,
                Cost REAL,
                Form TEXT,
                Manufacturer TEXT,
                D_NAME TEXT NOT NULL,
                FOREIGN KEY (D_Name) REFERENCES Drugs (D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

conn.execute('''CREATE TABLE Indications
               (I_Name TEXT,
                Severity TEXT,
                Description TEXT
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')

conn.execute('''CREATE TABLE Treats
               (D_Name TEXT,
                I_Name TEXT,
                PRIMARY KEY(D_Name_1, D_Name_2),
                FOREIGN KEY (D_Name_1)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (I_Name_2)
                    ON DELETE CASCADE ON UPDATE NO ACTION''')

conn.execute('''CREATE TABLE User
               (UserID TEXT,
                Age INT,
                Sex TEXT
                Pregnancy TEXT)''')

conn.execute('''CREATE TABLE Interacts
               (D_Name_1 TEXT,
                D_Name_2 TEXT,
                PRIMARY KEY(D_Name_1, D_Name_2)
                FOREIGN KEY (D_Name_1) REFERENCES Drugs(D_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (D_Name_2) REFERENCES Drugs(D_Name))
                    ON DELETE CASCADE ON UPDATE NO ACTION''')

conn.execute('''CREATE TABLE Takes
               (UserID TEXT 
                Age INT,
                Sex TEXT,
                Pregnancy TEXT)''')

conn.execute('''CREATE TABLE Has
               (UserID TEXT,
                I_Name TEXT,
                FOREIGN KEY (UserID)
                    ON DELETE CASCADE ON UPDATE NO ACTION,
                FOREIGN KEY (I_Name)
                    ON DELETE CASCADE ON UPDATE NO ACTION)''')


import xml.etree.ElementTree as et

# Parsing the XML file
tree = et.parse('full_database.xml')
root = tree.getroot()

# drugs data
for drug in root:
    name = drug.find("{http://www.drugbank.ca}name").text
    desc = drug.find("{http://www.drugbank.ca}description").text
    cur.execute("INSERT INTO Drugs (D_Name, Basic_Description) VALUES (?, ?)", (name, desc))
conn.commit()


# products data
for drug in root:
    products = drug.find("{http://www.drugbank.ca}products")
    for product in products:
        product_name = product.find("{http://www.drugbank.ca}name").text
        product_labeller = product.find("{http://www.drugbank.ca}labeller").text
        # not finished

# indications data
for drug in root:
    indication = drug.find("{http://www.drugbank.ca}indication").text
    cur.execute