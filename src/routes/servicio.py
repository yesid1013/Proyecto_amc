from flask import Blueprint
from flask_cors import cross_origin
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers import ServicioController

servicio = Blueprint('servicio', __name__)

@cross_origin()
@servicio.route('/crear_servicio/<id_activo>', methods=['POST'])
@jwt_required()
def crear_novedad(id_activo):
    id_usuario = get_jwt_identity()
    return ServicioController.crear_servicio(id_activo,id_usuario)


@cross_origin()
@servicio.route('/listar_servicios/<id_activo>')
@jwt_required()
def listar_servicios(id_activo):
    return ServicioController.serivicios_de_un_activo(id_activo)