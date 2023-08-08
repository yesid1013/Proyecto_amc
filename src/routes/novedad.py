from flask import Blueprint
from flask_cors import cross_origin
from controllers import NovedadController
from flask_jwt_extended import jwt_required

novedad = Blueprint('novedad', __name__)

@cross_origin()
@novedad.route('/novedad/<id_activo>', methods=['POST'])
@jwt_required()
def crear_novedad(id_activo):
    return NovedadController.crear_novedad(id_activo)

@cross_origin()
@novedad.route('/novedad/<id_activo>')
@jwt_required()
def listar_novedad(id_activo):
    return NovedadController.listar_novedades_de_un_activo(id_activo)

@cross_origin()
@novedad.route('/novedad/<id_novedad>', methods=['PUT'])
@jwt_required()
def editar_novedad(id_novedad):
    return NovedadController.editar_novedad(id_novedad)

@cross_origin()
@novedad.route('/novedad/<id_novedad>', methods=['DELETE'])
@jwt_required()
def eliminar_novedad(id_novedad):
    return NovedadController.eliminar_novedad(id_novedad)

@cross_origin()
@novedad.route('/novedad/<id_novedad>/restaurar', methods=['PUT'])
@jwt_required()
def restaurar_novedad(id_novedad):
    return NovedadController.restaurar_novedad(id_novedad)