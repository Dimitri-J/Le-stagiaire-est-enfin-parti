from app.db import get_db_config, db_connect
import mysql.connector
from app import app
import json


# Afficher les valeurs utilisateurs dans le tableau puis db
# Mettre le cemin absolu de votre config.json
path = "./config.json"
config = get_db_config(path)

#connect to database
myDB = db_connect(config)
cursor = myDB.cursor()
dbOK = myDB.is_connected()


if __name__ == "__main__":
    pass

# Load the JSON data
with open('data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)




# Insert the data into the table
for item in data['materiel']:
    for key, value in item.items():
        try:
            query = (f'''INSERT INTO materiel (type, taille, etat) VALUES ("{value[0]}", "{value[1]}", "{value[2]}")''')
            print(query)
            cursor.execute(query)
            myDB.commit()
        except mysql.connector.Error as e:
            print(e)

for item in data['employé.e informatique']:
    for key, value in item.items():
        try:
            query = (f'''INSERT INTO employe (nom, prenom, age, poste) VALUES ("{value[0]}", "{value[1]}", "{value[2]}", "{value[3]}")''')
            print(query)
            cursor.execute(query)
            myDB.commit()
        except mysql.connector.Error as e:
            print (e)

