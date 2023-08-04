from flask import Blueprint
from flask_cors import cross_origin
from controllers import ActivoController
from flask_jwt_extended import jwt_required,get_jwt_identity

activo = Blueprint('activo', __name__)

@cross_origin()
@activo.route('/crear_activo', methods=['POST'])
@jwt_required()
def crear_activo():
    current_user_id = get_jwt_identity()
    return ActivoController.crear_activo(current_user_id)

@cross_origin()
@activo.route('/listar_activos')
@jwt_required()
def listar_activos():
    return ActivoController.listar_activos()

@cross_origin()
@activo.route('/info_activo/<id_activo_hex>')
def info_activo(id_activo_hex):
    return ActivoController.info_activo(id_activo_hex)

@cross_origin()
@activo.route('/listar_activos_subcliente/<id_subcliente>')
@jwt_required()
def listar_activos_subcliente(id_subcliente):
    return ActivoController.activos_de_subcliente(id_subcliente)

@cross_origin()
@activo.route('/editar_activo/<id_activo>',methods=['PUT'])
@jwt_required()
def editar_activo(id_activo):
    return ActivoController.editar_activo(id_activo)

@cross_origin()
@activo.route('/eliminar_activo/<id_activo>',methods=['DELETE'])
@jwt_required()
def eliminar_activo(id_activo):
    return ActivoController.eliminar_activo(id_activo)

@cross_origin()
@activo.route('/restaurar_activo/<id_activo>',methods=['PUT'])
@jwt_required()
def restaurar_activo(id_activo):
    return ActivoController.restaurar_activo(id_activo)