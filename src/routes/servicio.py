from flask import Blueprint
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import ServicioController

servicio = Blueprint('servicio', __name__,url_prefix='/api/v1')

@cross_origin()
@servicio.route('/servicios/<id_activo>', methods=['POST'])
@jwt_required()
def crear_servicio(id_activo):
    id_usuario = get_jwt_identity()
    return ServicioController.crear_servicio(id_activo,id_usuario)

@cross_origin()
@servicio.route('/servicios')
@jwt_required()
def obtener_servicios():
    return ServicioController.obtener_servicios()


@cross_origin()
@servicio.route('/servicios/<id_activo>')
@jwt_required()
def listar_servicios(id_activo):
    return ServicioController.serivicios_de_un_activo(id_activo)

@cross_origin()
@servicio.route('/servicios/<id_servicio>', methods=['PUT'])
@jwt_required()
def editar_servicio(id_servicio):
    return ServicioController.editar_servicio(id_servicio)

@cross_origin()
@servicio.route('/servicios/<id_servicio>', methods=['DELETE'])
@jwt_required()
def eliminar_servicio(id_servicio):
    return ServicioController.eliminar_servicio(id_servicio)

@cross_origin()
@servicio.route('/servicios/<id_servicio>/restaurar', methods=['PUT'])
@jwt_required()
def restaurar_servicio(id_servicio):
    return ServicioController.restaurar_servicio(id_servicio)