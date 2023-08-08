from flask import Blueprint
from flask_cors import cross_origin
from controllers import UsuarioController

usuario = Blueprint('usuario', __name__,url_prefix='/api/v1')

@cross_origin()
@usuario.route('/usuarios', methods=['POST'])
def crear_usuario():
    return UsuarioController.crear_usuario()

@cross_origin()
@usuario.route('/usuarios')
def listar_usuarios():
    return UsuarioController.listar_usuarios()

@cross_origin()
@usuario.route('/usuario/<id_usuario>')
def buscar_usuario(id_usuario):
    return UsuarioController.buscar_usuario(id_usuario)