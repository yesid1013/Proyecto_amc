from flask import Blueprint
from flask_cors import cross_origin
from controllers import NovedadController
from flask_jwt_extended import jwt_required

novedad = Blueprint('novedad', __name__)

@cross_origin()
@jwt_required()
@novedad.route('/crear_novedad/<id_activo>', methods=['POST'])
def crear_novedad(id_activo):
    return NovedadController.crear_novedad(id_activo)