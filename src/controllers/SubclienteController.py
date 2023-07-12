from flask import jsonify, request
from models.Subcliente import *
import uuid
import binascii

def crear_subcliente():
    try:
        id_subcliente = uuid.uuid4().bytes
        nombre = request.json["nombre"]
        contacto = request.json["contacto"]
        direccion = request.json["direccion"]

        new_subcliente = Subcliente(id_subcliente,nombre,contacto,direccion)
        db.session.add(new_subcliente)
        db.session.commit()

        return jsonify({"message": "Subcliente creado correctamente", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def listar_subclientes():
    try:

        lista = []
        subclientes = db.session.query(Subcliente).all()
        for subcliente in subclientes:
            id_hex = binascii.hexlify(subcliente.id_subcliente).decode()
            datos = {"id_subcliente" : id_hex, "nombre" : subcliente.nombre, "contacto" : subcliente.contacto, "direccion" : subcliente.direccion}
            lista.append(datos)
            
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})