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
@activo.route('/listar_activos_subcliente/<id_subcliente>')
@jwt_required()
def listar_activos_subcliente(id_subcliente):
    return ActivoController.activos_de_subcliente(id_subcliente)