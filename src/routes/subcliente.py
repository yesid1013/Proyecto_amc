from flask import Blueprint
from flask_cors import cross_origin
from controllers import SubclienteController
from flask_jwt_extended import jwt_required

subcliente = Blueprint('subcliente', __name__,url_prefix='/api/v1')

@cross_origin()
@subcliente.route('/subclientes', methods=['POST'])
@jwt_required()
def crear_subcliente():
    return SubclienteController.crear_subcliente()

@cross_origin()
@subcliente.route('/subclientes')
def listar_subclientes():
    return SubclienteController.listar_subclientes()

@cross_origin()
@subcliente.route('/subclientes/<id_empresa>')
@jwt_required()
def subclientes_de_empresa(id_empresa):
    return SubclienteController.subclientes_de_empresa(id_empresa)