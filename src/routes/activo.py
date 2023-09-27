from flask import Blueprint,jsonify
from flask_cors import cross_origin
from controllers import ActivoController
from flask_jwt_extended import jwt_required,get_jwt_identity,verify_jwt_in_request,get_jwt
from flask_jwt_extended.exceptions import NoAuthorizationError,InvalidHeaderError,JWTDecodeError



activo = Blueprint('activo', __name__,url_prefix='/api/v1')


@cross_origin()
@activo.route('/listar_activos',methods=['GET'])
@jwt_required()
def listar_activos():
    try:
        verify_jwt_in_request()
        id_usuario = get_jwt_identity()
        return ActivoController.listar_activos(id_usuario)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado", "error" : str(ex)})

@cross_origin()
@activo.route("/create_activo", methods = ['POST'])
@jwt_required()
def crear_Activo():
    try:
        verify_jwt_in_request()
        id_usuario = get_jwt_identity()
        return ActivoController.crear_activo(id_usuario)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})


@cross_origin()
@activo.route('/info_activo/<id_activo_hex>')
def info_activo(id_activo_hex):
    return ActivoController.info_activo(id_activo_hex)

@cross_origin()
@activo.route('/activos/<id_subcliente>')
@jwt_required()
def listar_activos_subcliente(id_subcliente):
    return ActivoController.activos_de_subcliente(id_subcliente)

@cross_origin()
@activo.route('/activo/<id_activo>',methods=['PUT'])
@jwt_required()
def editar_activo(id_activo):
    try:
        verify_jwt_in_request()
        return ActivoController.editar_activo(id_activo)
    
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})
    

@cross_origin()
@activo.route('/activo/<id_activo>',methods=['DELETE'])
@jwt_required()
def eliminar_activo(id_activo):
    try:
        verify_jwt_in_request()
        return ActivoController.eliminar_activo(id_activo)
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})

@cross_origin()
@activo.route('/activos_eliminados', methods = ['GET'])
@jwt_required()
def activos_eliminados():
    try:
        verify_jwt_in_request()
        return ActivoController.get_activos_borrados()
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})   

@cross_origin()
@activo.route('/activos/<id_activo>/restaurar',methods=['PUT'])
@jwt_required()
def restaurar_activo(id_activo):
    return ActivoController.restaurar_activo(id_activo)

@cross_origin()
@activo.route('/activos_sin_ficha',methods=['GET'])
@jwt_required()
def activos_sin_ficha_tecnica():
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['perfil'] == 1:
            return ActivoController.activos_sin_ficha_tecnica()
        else :
            return jsonify({"message" : "Acceso denegado" , "status" : 401}) , 401
    
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})

@cross_origin()
@activo.route('/adjuntar_ficha_tecnica/<id_activo>',methods=['PUT'])
@jwt_required()
def adjunar_ficha_tecnica(id_activo):
    try:
        verify_jwt_in_request()
        claims = get_jwt()
        if claims['perfil'] == 1:
            return ActivoController.adjuntar_ficha_tecnica(id_activo)
        else :
            return jsonify({"message" : "Acceso denegado" , "status" : 401}) , 401
    
    except (NoAuthorizationError,JWTDecodeError,InvalidHeaderError,RuntimeError,KeyError) as ex:
        return jsonify({"message" : "Acceso denegado :", "error" : str(ex)})