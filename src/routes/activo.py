from flask import Blueprint,jsonify
from flask_cors import cross_origin
from controllers import ActivoController
from flask_jwt_extended import jwt_required,get_jwt_identity,verify_jwt_in_request
from flask_jwt_extended.exceptions import NoAuthorizationError,InvalidHeaderError,JWTDecodeError



activo = Blueprint('activo', __name__,url_prefix='/api/v1')


@cross_origin()
@activo.route('/listar_activos',methods=['GET'])
@jwt_required()
def listar_activos():
    return ActivoController.listar_activos()

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
@activo.route('/activos/<id_activo>',methods=['PUT'])
@jwt_required()
def editar_activo(id_activo):
    return ActivoController.editar_activo(id_activo)

@cross_origin()
@activo.route('/activos/<id_activo>',methods=['DELETE'])
@jwt_required()
def eliminar_activo(id_activo):
    return ActivoController.eliminar_activo(id_activo)

@cross_origin()
@activo.route('/activos/<id_activo>/restaurar',methods=['PUT'])
@jwt_required()
def restaurar_activo(id_activo):
    return ActivoController.restaurar_activo(id_activo)