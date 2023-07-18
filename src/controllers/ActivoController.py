from flask import jsonify, request
from models.Activo import *
import uuid
import binascii

def crear_activo(id_usuario):
    try:
        id_activo = uuid.uuid4().bytes
        id_primario = request.json["id_primario"]
        id_secundario = request.json["id_secundario"]
        id_usuario = id_usuario
        id_qr = request.json["id_qr"]
        ubicacion = request.json["ubicacion"]
        tipo_de_equipo = request.json["tipo_de_equipo"]
        fabricante = request.json["fabricante"]
        modelo = request.json["modelo"]
        num_serie = request.json["num_serie"]
        datos_relevantes = request.json["datos_relevantes"]
        imagen_equipo = request.json["imagen_equipo"]
        id_subcliente = request.json["id_subcliente"]
        ficha_tecnica = request.json["ficha_tecnica"]

        id_usuario_bytes = binascii.unhexlify(id_usuario) #El id_usuario de hexadecimal a binario
        id_subcliente_bytes = binascii.unhexlify(id_subcliente) #El id_subcliente de hexadecimal a binario

        new_activo = Activo(id_activo,id_qr,id_primario,id_secundario,id_usuario_bytes,ubicacion,tipo_de_equipo,fabricante,modelo,num_serie,datos_relevantes,imagen_equipo,id_subcliente_bytes,ficha_tecnica)
        db.session.add(new_activo)
        db.session.commit()
        return jsonify({"message": "Activo creado correctamente", "status" : 200})

    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
        
    