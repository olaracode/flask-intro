"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
# El bloque de importaciones
import os
from flask import Flask, request, jsonify, url_for
from flask_migrate import Migrate
from flask_swagger import swagger
from flask_cors import CORS
from utils import APIException, generate_sitemap
from admin import setup_admin

# Importacion de modelos 
from models import db, User

# Se inicializa la aplicacion de Flask
app = Flask(__name__)

# Que los slashes no son estrictos
# .../user/login/ -> tracking slash
app.url_map.strict_slashes = False # Sea falso. Lo de arriba no aplica

## Configura la base de datos
db_url = os.getenv("DATABASE_URL")

if db_url is not None:
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://")
# Si no hay base de datos local, se usa una temporal
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:////tmp/test.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Las migraciones
MIGRATE = Migrate(app, db)
db.init_app(app) # Se activa la BBDD
CORS(app) # CORS -> Estandar de comunicacion web.
# Cross-Origin Resource Sharing

# El panel de administracion
setup_admin(app)


# Empieza Nuestra API
# Handle/serialize errors like a JSON object
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code

@app.route('/')
def sitemap():
    return generate_sitemap(app)

# AQUI ESCRIBES TU CODIGO
# ENDPOINTS
# @app.route('/endpoint', methods=['POST' | 'GET' | 'PATCH' - 'PUT' | 'DELETE'])
# def funcion_a_ejecutar():
# ...
# ...
# return { "results": personajes[] }
# Decorador

# Endpoint GET users


# Endpoint GET /info
@app.route("/info", methods=['GET'])
def get_info():

    informacion_cohorte = {
        "Academia": "4geeks",
        "Pensum": "Fullstack Developer(JS|Python)",
        "Cohorte": 44
    }
    if informacion_cohorte["Academia"] == "4geeks":
        print("hola")

    return jsonify(informacion_cohorte), 200

# Depende de si la informacion es FIJA? O es dinamica?
students = [
    {
        "name": "Jose Carlos",
        "id": 1
    },
    {
        "name": "Manuel",
        "id": 2

    },
    {
        "name": "Juan",
        "id": 3
    },
    {
        "name": "Luis",
        "id": 4
    }
]

@app.route("/students", methods=['GET'])
def get_students():
    students_info = {
        "total": len(students),
        "data": students
    }
    return jsonify(students_info), 200

# Endpoint que me traiga 1 usuario y que lo busque por id
@app.route("/student/<int:id>", methods=['GET'])
def get_student_by_id(id):
    for student in students:
        if student.get("id") == id:
            return jsonify(student), 200 # Esta linea termina la funcion

    # Quiere decir que no encontro al usuario
    return jsonify({"error": "student not found"}), 404

# Metodo GET | POST | PUT | DELETE
@app.route("/student", methods=['POST', 'PUT'])
def create_or_update_student():
    # VALIDO SI ES POST
    if request.method == "POST":
        # Recibimos el body de tipo JSON en nuestro endpoint
        data = request.get_json()
        print("Nuevo estudiante",data)

        # Extraigo de data la variable del nombre
        new_student_name = data.get("name", None) # -> accediendo al valor nombre
        if new_student_name is None:
            return jsonify({"error": "Todos los campos son requeridos"}), 400
        
        print(new_student_name)
        return jsonify({"Probando": "El metodo post"})
    elif request.method == "PUT":
        return jsonify({"probando": "el metodo PUT"})

users = [
    {"name": "John", "age": 30, "email": "john@example.com", "id": 3},
    {"name": "Jane", "age": 25, "email": "jane@example.com", "id": 150},
    {"name": "Bob", "age": 40, "email": "bob@example.com", "id": 10}
]

# Busquemos la lista de usuario
# busquemos un usuario basado en su id
# Creemos un nuevo usuario
# Metodo get de lista
# metodo get de uno solo(RUTA DINAMICA)
# un post con un body

@app.route("/users", methods=["GET"])
def get_users():
    return jsonify(users), 200

@app.route("/user/<int:id>", methods=["GET"])
def get_user_by_id(id):
    for user in users:
        if user.get("id") == id:
            return jsonify(user), 200 # es un return condicional
    
    # Tienen que tener un RETURN el caso por defecto
    return jsonify({"error": "user not found"}), 404

@app.route("/user", methods=["POST"])
def create_user():
    new_user = request.get_json() # la informacion del body json
    # name | age | email
    name = new_user.get("name", None)
    age = new_user.get("age", None)
    email = new_user.get("email", None)

    if name is None or age is None or email is None:
        return jsonify({"error": "All fields required"}), 400
    
    for user in users:
        if user.get("email") == email:
            return jsonify({"error": "Correo ya registrado a un usuario"}), 400

    return jsonify({"user": {"name": name, "age": age, "email": email}}), 201

# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=False)
