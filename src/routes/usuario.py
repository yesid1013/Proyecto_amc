from flask import Blueprint
from flask_cors import cross_origin
from controllers import UsuarioController

usuario = Blueprint('usuario', __name__)

@cross_origin()
@usuario.route('/crear_usuario', methods=['POST'])
def crear_usuario():
    return UsuarioController.crear_usuario()

@cross_origin()
@usuario.route('/listar_usuarios')
def listar_usuarios():
    return UsuarioController.listar_usuarios()

@cross_origin()
@usuario.route('/buscar_usuario/<id_usuario>')
def buscar_usuario(id_usuario):
    return UsuarioController.buscar_usuario(id_usuario)