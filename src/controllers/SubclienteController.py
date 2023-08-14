from flask import jsonify, request
from models.Subcliente import *
import uuid
import binascii
from models.Empresa import Empresa
from utils.validation import validation_subcliente

def crear_subcliente():
    try:
        validation = validation_subcliente(request.json)
        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400
        
        id_subcliente = uuid.uuid4().bytes
        id_empresa = request.json["id_empresa"]
        nombre = request.json["nombre"]
        contacto = request.json["contacto"]
        direccion = request.json["direccion"]

        id_empresa_bytes = binascii.unhexlify(id_empresa) #El id_empresa de hexadecimal a binario

        new_subcliente = Subcliente(id_subcliente,id_empresa_bytes,nombre,contacto,direccion)
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
            id_hex = binascii.hexlify(subcliente.id_subcliente).decode() #Convierto el id binario que me da la base de datos a hexadecimal
            datos = {"id_subcliente" : id_hex, "nombre" : subcliente.nombre, "contacto" : subcliente.contacto, "direccion" : subcliente.direccion}
            lista.append(datos)
            
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    

def subclientes_de_empresa(id_empresa): #Listar los subclientes de una empresa
    try:
        lista = []
        id_empresa_bytes = binascii.unhexlify(id_empresa)

        subclientes = db.session.query(Subcliente.id_subcliente,Subcliente.nombre).filter_by(id_empresa=id_empresa_bytes).all()

        for subcliente in subclientes:
            id_subcliente_hex = binascii.hexlify(subcliente.id_subcliente).decode()
            datos = {"id_subcliente" : id_subcliente_hex, "nombre" : subcliente.nombre}
            lista.append(datos)
        

        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})