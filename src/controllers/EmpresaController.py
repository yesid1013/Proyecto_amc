from flask import jsonify, request
from models.Empresa import *
from utils.validation import validation_empresa
import uuid
import binascii
import bleach

def crear_empresa():
    try:
        validation = validation_empresa(request.json)

        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400

        id_empresa = uuid.uuid4().bytes
        nombre = bleach.clean(request.json["nombre"],tags=bleach.sanitizer.ALLOWED_TAGS)
        telefono = bleach.clean(request.json["telefono"],tags=bleach.sanitizer.ALLOWED_TAGS)
        direccion = bleach.clean(request.json["direccion"],tags=bleach.sanitizer.ALLOWED_TAGS)

        new_empresa = Empresa(id_empresa,nombre,telefono,direccion)
        db.session.add(new_empresa)
        db.session.commit()
        return jsonify({"message": "Empresa creada correctamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    

def listar_empresas():
    try:
        empresas = db.session.query(Empresa).all()

        if not empresas:
            return jsonify({"message" : "No se encontraron empresas" , "status" : 404}) , 404
        
        else:
            to_empresas= [empresa.getDatos() for empresa in empresas]
            return jsonify(to_empresas)
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})