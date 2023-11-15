from flask import Blueprint,jsonify
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity,verify_jwt_in_request,get_jwt
from controllers import ServicioController
from controllers import UsuarioController
from flask_jwt_extended.exceptions import NoAuthorizationError,InvalidHeaderError,JWTDecodeError


servicio = Blueprint('servicio', __name__,url_prefix='/api/v1')

@cross_origin()
@servicio.route('/servicios/<id_activo>', methods=['POST'])
@jwt_required()
def crear_servicio(id_activo):
    try:
        id_usuario = get_jwt_identity()
        return ServicioController.crear_servicio(id_activo,id_usuario)
    
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})


@cross_origin()
@servicio.route('/servicios')
@jwt_required()
def obtener_servicios():
    try:
        verify_jwt_in_request()
        id_usuario = get_jwt_identity()
        return ServicioController.obtener_servicios_de_usuario(id_usuario)
        
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})


@cross_origin()
@servicio.route('/servicios/<id_activo>')
@jwt_required()
def serivicios_de_un_activo_con_costo(id_activo):
    return ServicioController.serivicios_de_un_activo_con_costo(id_activo)

@cross_origin()
@servicio.route('/servicio/<id_servicio>', methods=['PUT'])
@jwt_required()
def editar_servicio(id_servicio):
    try:
        verify_jwt_in_request()
        return ServicioController.editar_servicio(id_servicio)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})

@cross_origin()
@servicio.route('/servicio/<id_servicio>', methods=['DELETE'])
@jwt_required()
def eliminar_servicio(id_servicio):
    try:
        verify_jwt_in_request()
        return ServicioController.eliminar_servicio(id_servicio)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})

@cross_origin()
@servicio.route('/servicios/<id_servicio>/restaurar', methods=['PUT'])
@jwt_required()
def restaurar_servicio(id_servicio):
    return ServicioController.restaurar_servicio(id_servicio)

@cross_origin()
@servicio.route('/servicios_subcliente/<id_subcliente>')
def servicios_de_un_subcliente(id_subcliente):
    return ServicioController.servicios_de_un_subcliente(id_subcliente)

@cross_origin()
@servicio.route('/servicios_sin_informe')
@jwt_required()
def servicios_sin_informe():
    try:
        verify_jwt_in_request()
        id_usuario = get_jwt_identity()
        return ServicioController.servicios_sin_informe(id_usuario)
        
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})

@cross_origin()
@servicio.route('/informe_servicio/<id_servicio>',methods=['POST'])
@jwt_required()
def adjuntar_informe(id_servicio):
    try:
        verify_jwt_in_request()
        return ServicioController.adjuntar_informe_servicio(id_servicio)
        
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})