from flask import jsonify, request
from models.Empresa import *
import uuid
import binascii

def crear_empresa():
    try:
        id_empresa = uuid.uuid4().bytes
        nombre = request.json['nombre']
        telefono = request.json['telefono']
        direccion = request.json['direccion']

        new_empresa = Empresa(id_empresa,nombre,telefono,direccion)
        db.session.add(new_empresa)
        db.session.commit()
        return jsonify({"message": "Empresa creada correctamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})