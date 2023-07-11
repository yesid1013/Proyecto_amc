from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from utils.db import db
from routes.usuario import usuario
from routes.login import login
app = Flask(__name__)

CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:barranquilla91#$%@localhost/proyecto_amc'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config["JWT_COOKIE_SECURE"] = False
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_SECRET_KEY"] = "9fdb92015ffc4bdabb52c1dc158b12c6"

jwt = JWTManager(app)
db.init_app(app)

app.register_blueprint(usuario)
app.register_blueprint(login)

def pagina_no_encontrada(error):
    return jsonify({"message" : "Pagina no encontrada"})

if __name__=="__main__":
    app.register_error_handler(404 , pagina_no_encontrada)
    app.run(port=5000, debug=True)