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