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

@cross_origin()
@jwt_required()
@novedad.route('/listar_novedad/<id_activo>')
def listar_novedad(id_activo):
    return NovedadController.listar_novedades_de_un_activo(id_activo)

@cross_origin()
@jwt_required()
@novedad.route('/editar_novedad/<id_novedad>', methods=['PUT'])
def editar_novedad(id_novedad):
    return NovedadController.editar_novedad(id_novedad)

@cross_origin()
@jwt_required()
@novedad.route('/eliminar_novedad/<id_novedad>', methods=['DELETE'])
def eliminar_novedad(id_novedad):
    return NovedadController.eliminar_novedad(id_novedad)