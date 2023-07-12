from flask import Blueprint
from flask_cors import cross_origin
from controllers import SubclienteController

subcliente = Blueprint('subcliente', __name__)

@cross_origin()
@subcliente.route('/crear_subcliente', methods=['POST'])
def login_normal():
    return SubclienteController.crear_subcliente()