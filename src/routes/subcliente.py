from flask import Blueprint
from flask_cors import cross_origin
from controllers import SubclienteController

subcliente = Blueprint('subcliente', __name__)

@cross_origin()
@subcliente.route('/subclientes', methods=['POST'])
def crear_subcliente():
    return SubclienteController.crear_subcliente()

@cross_origin()
@subcliente.route('/subclientes')
def listar_subclientes():
    return SubclienteController.listar_subclientes()

@cross_origin()
@subcliente.route('/subclientes/<id_empresa>')
def subclientes_de_empresa(id_empresa):
    return SubclienteController.subclientes_de_empresa(id_empresa)