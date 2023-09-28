from flask import Blueprint,jsonify
from flask_cors import cross_origin
from controllers import UsuarioController
from flask_jwt_extended import jwt_required, get_jwt_identity,verify_jwt_in_request,get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError,InvalidHeaderError,JWTDecodeError


usuario = Blueprint('usuario', __name__,url_prefix='/api/v1')

@cross_origin()
@usuario.route('/usuarios', methods=['POST'])
def crear_usuario():
    return UsuarioController.crear_usuario()

@cross_origin()
@usuario.route('/usuarios')
@jwt_required()
def listar_usuarios():
    try:
        verify_jwt_in_request()
        return UsuarioController.listar_usuarios()
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})

@cross_origin()
@usuario.route('/usuario/<id_usuario>')
@jwt_required()
def buscar_usuario(id_usuario):
    return UsuarioController.buscar_usuario(id_usuario)