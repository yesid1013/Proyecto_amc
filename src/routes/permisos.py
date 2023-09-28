from flask import Blueprint,jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity,verify_jwt_in_request,get_jwt
from controllers import PermisosController
from flask_jwt_extended.exceptions import NoAuthorizationError,InvalidHeaderError,JWTDecodeError


permiso = Blueprint('permiso', __name__,url_prefix='/api/v1')

@cross_origin()
@permiso.route('/permisos', methods=['POST'])
@jwt_required()
def crear_permiso():
    try:
        return PermisosController.registrar_permiso()
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})

@cross_origin()
@permiso.route('/permisos', methods=['GET'])
@jwt_required()
def permisos_otorgados():
    try:
        verify_jwt_in_request()
        id_usuario = get_jwt_identity()
        return PermisosController.permisos_otorgados(id_usuario)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})
