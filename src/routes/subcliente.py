from flask import Blueprint
from flask_cors import cross_origin
from controllers import SubclienteController

subcliente = Blueprint('subcliente', __name__)

@cross_origin()
@subcliente.route('/crear_subcliente', methods=['POST'])
def crear_subcliente():
    return SubclienteController.crear_subcliente()

@cross_origin()
@subcliente.route('/listar_subclientes')
def listar_subclientes():
    return SubclienteController.listar_subclientes()