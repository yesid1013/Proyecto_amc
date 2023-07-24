from flask import Blueprint
from flask_cors import cross_origin
from controllers import EmpresaController
from flask_jwt_extended import jwt_required

empresa = Blueprint("empresa", __name__)

@cross_origin()
@empresa.route('/crear_empresa',methods=['POST'])
@jwt_required()
def crear_empresa():
    return EmpresaController.crear_empresa()

@cross_origin()
@empresa.route('/listar_empresas')
@jwt_required()
def listar_empresas():
    return EmpresaController.listar_empresas()