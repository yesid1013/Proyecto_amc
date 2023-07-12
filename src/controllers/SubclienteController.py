from flask import jsonify, request
from models.Subcliente import *
import uuid
import binascii

def crear_subcliente():
    try:
        id_subcliente = uuid.uuid4().bytes
        nombre = request.json["subcliente"]
        contacto = request.json["contacto"]
        direccion = request.json["direccion"]

        new_subcliente = Subcliente(id_subcliente,nombre,contacto,direccion)
        db.session.add(new_subcliente)
        db.session.commit()

        return jsonify({"message": "Usuario creado correctamente", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})