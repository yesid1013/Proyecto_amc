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
        return PermisosController.permisos_recibidos(id_usuario)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})

@cross_origin()
@permiso.route('/permiso_usuario/<id_activo>', methods=['GET'])
@jwt_required()
def buscar_permiso_por_activo_y_usuario(id_activo):
    try:
        verify_jwt_in_request()
        id_usuario = get_jwt_identity()
        return PermisosController.buscar_permiso_por_activo_y_usuario(id_usuario,id_activo)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})

@cross_origin()
@permiso.route('/permiso/<id_permiso>', methods=['GET'])
@jwt_required()
def obtener_un_permiso(id_permiso):
    try:
        verify_jwt_in_request()
        return PermisosController.obtener_un_permiso(id_permiso)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})

@cross_origin()
@permiso.route('/permisos/<id_activo>', methods=['GET'])
@jwt_required()
def buscar_permisos_de_activo(id_activo):
    try:
        verify_jwt_in_request()
        return PermisosController.buscar_permisos_de_activo(id_activo)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})

@cross_origin()
@permiso.route('/permisos_creados', methods=['GET'])
@jwt_required()
def permisos_crados():
    try:
        verify_jwt_in_request()
        id_usuario = get_jwt_identity()
        return PermisosController.permisos_creados(id_usuario)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})

@cross_origin()
@permiso.route('/permiso/<id_permiso>', methods=['PUT'])
@jwt_required()
def editar_permiso(id_permiso):
    try:
        verify_jwt_in_request()
        return PermisosController.editar_permiso(id_permiso)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})
    
@cross_origin()
@permiso.route('/permiso/<id_permiso>', methods=['DELETE'])
@jwt_required()
def eliminar_permiso(id_permiso):
    try:
        verify_jwt_in_request()
        return PermisosController.eliminar_permiso(id_permiso)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})
