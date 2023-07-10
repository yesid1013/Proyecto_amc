from flask import Blueprint
from flask_cors import cross_origin
from controllers import UsuarioController

usuario = Blueprint('usuario', __name__)

@cross_origin()
@usuario.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    return UsuarioController.crear_usuario()