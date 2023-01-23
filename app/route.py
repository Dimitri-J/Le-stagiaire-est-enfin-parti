from flask import render_template, request, redirect, url_for, jsonify
from .db import get_db_config, db_connect
import mysql.connector
from app import app
 



# Mettre le chemin absolu de votre config.json pour connecter la db
path = "./config.json"
config = get_db_config(path)

# Connect to database
myDB = db_connect(config)
cursor = myDB.cursor()
dbOK = myDB.is_connected()


#------------------------------------------------------------------------------#

### Les routes /api/materiel et /api/employe permettent de récupérer tous les 
### matériels et tous les employés respectivement.
### Tandis que les routes /api/materiel/<int:id> et /api/employe/<int:id> 
### permettent de récupérer un matériel ou un employé spécifique en utilisant 
### son identifiant.

### Les routes /api/materiel et /api/employe avec la méthode POST 
### permettent d'ajouter un nouveau matériel ou employé en utilisant les données
### envoyées dans la requête.

### Les routes /api/materiel/<int:id> et /api/employe/<int:id> 
### avec la méthode PUT permettent de mettre à jour un matériel ou employé 
### existant en utilisant les données envoyées dans la requête.

### Les routes /api/materiel/<int:id> et /api/employe/<int:id> 
### avec la méthode DELETE permettent de supprimer un matériel ou employé 
### existant en utilisant son identifiant.

#------------------------------------------------------------------------------#

### Afficher les valeurs utilisateurs dans le tableau puis db

### View data DB ###

@app.route('/', methods=["GET", "POST"])   # == @app.route('/index')
def index():

    if request.method == "GET":

        try:
            query_1="""
                SELECT * FROM `materiel`;
            """
            cursor.execute(query_1)
            result_select_1 = cursor.fetchall()
            
            query_2="""
                SELECT * FROM `employe`;
            """
            cursor.execute(query_2)
            result_select_2 = cursor.fetchall()            

            return render_template('index.html', configHTML=config, dbOK__=dbOK,
                HTML_Result=result_select_1, HTML_Result_2=result_select_2)
        

        except mysql.connector.Error as e:
            return render_template('index.html', configHTML=config, error=e)

#### CRUD Materiels

@app.route('/api/materiel', methods=['GET'])
def get_materiel():
    query = """SELECT * FROM materiel"""
    cursor.execute(query)
    materiels = cursor.fetchall()
    materiels_list = []
    for materiel in materiels:
        materiels_list.append({"id":materiel[0], "type":materiel[1],
            "taille":materiel[2], "etat":materiel[3]})
    return jsonify(materiels_list)

@app.route('/api/materiel/<int:id>', methods=['GET'])
def get_materiel_by_id(id):
    query = """SELECT * FROM materiel WHERE id = {}""".format(id)
    cursor.execute(query)
    materiel = cursor.fetchone()
    return jsonify({"id":materiel[0], "type":materiel[1], "taille":materiel[2],
    "etat":materiel[3]})

@app.route('/api/materiel', methods=['POST'])
def add_materiel():
    data = request.get_json()
    query = f"""INSERT INTO materiel (type,taille,etat) VALUES ("{data["type"]}"
        ,"{data["taille"]}", "{data["etat"]}")"""
    cursor.execute(query)
    myDB.commit()
    return jsonify({'message': 'materiel added successfully'}), 201

@app.route('/api/materiel/<int:id>', methods=['PUT'])
def update_materiel(id):
    data = request.get_json()
    query = f"""UPDATE materiel SET type = '{data["type"]}',
        taille = '{data["taille"]}', etat = '{data["etat"]}' WHERE id = {id}"""
    cursor.execute(query)
    myDB.commit()
    return jsonify({'message': 'materiel updated successfully'})

@app.route('/api/materiel/<int:id>', methods=['DELETE'])
def delete_materiel(id):
    query = """DELETE FROM materiels WHERE id = {}""".format(id)
    cursor.execute(query)
    myDB.commit()
    return jsonify({'message': 'materiel deleted successfully'})

#### CRUD Employes

@app.route('/api/employe', methods=['GET'])
def get_employe():
    query = """SELECT * FROM employe"""
    cursor.execute(query)
    employe = cursor.fetchall()
    employe_list = []
    for materiel in employe:
        employe_list.append({"id":materiel[0], "nom":materiel[1],
            "prenom":materiel[2], "age":materiel[3], "poste":materiel[4]})
    return jsonify(employe_list)

@app.route('/api/employe/<int:id>', methods=['GET'])
def get_employe_by_id(id):
    query = """SELECT * FROM employe WHERE id = {}""".format(id)
    cursor.execute(query)
    materiel = cursor.fetchone()
    return jsonify({"id":materiel[0], "nom":materiel[1], "prenom":materiel[2],
        "age":materiel[3], "poste":materiel[4]})

@app.route('/api/employe', methods=['POST'])
def add_employe():
    data = request.get_json()
    query = """INSERT INTO employe (nom,prenom,age,poste) VALUES ('{}', '{}',
        '{}', '{}')""".format(data["nom"], data["prenom"], data["age"],
        data["poste"])
    cursor.execute(query)
    myDB.commit()
    return jsonify({'message': 'person added successfully'}), 201

@app.route('/api/employe/<int:id>', methods=['PUT'])
def update_employe(id):
    data = request.get_json()
    query = """UPDATE employe SET nom = '{}', prenom = '{}', age = '{}',
        poste = '{}' WHERE id = {}""".format(data["nom"], data["prenom"],
        data["age"], data["poste"], id)
    cursor.execute(query)
    myDB.commit()
    return jsonify({'message': 'person updated successfully'})

@app.route('/api/employe/<int:id>', methods=['DELETE'])
def delete_employe(id):
    query = """DELETE FROM employe WHERE id = {}""".format(id)
    cursor.execute(query)
    myDB.commit()
    return jsonify({'message': 'person deleted successfully'})


