from flask import Blueprint
from flask_cors import cross_origin
from controllers import Costo_servicioController
from flask_jwt_extended import jwt_required,get_jwt_identity

costo_servicio = Blueprint('costo_servicio', __name__)

@cross_origin()
@costo_servicio.route("/crear_costo_servicio/<id_servicio>",methods=['POST'])
@jwt_required()
def crear_costo_servicio(id_servicio):
    return Costo_servicioController.crear_costo_servicio(id_servicio)

@cross_origin()
@costo_servicio.route("/cotizacion_de_un_servicio/<id_servicio>")
@jwt_required()
def cotizacion_de_un_servicio(id_servicio):
    return Costo_servicioController.cotizacion_de_un_servicio(id_servicio)

@cross_origin()
@costo_servicio.route("/editar_cotizacion/<id_costo_servicio>",methods=['PUT'])
@jwt_required()
def editar_cotizacion(id_costo_servicio):
    return Costo_servicioController.editar_cotizacion(id_costo_servicio)