from flask import jsonify, request
from models.Activo import *
import uuid
import binascii

def crear_activo(id_usuario):
    try:
        id_activo = uuid.uuid4().bytes
        id_qr = ""
        id_primario = request.json["id_primario"]
        id_secundario = request.json["id_secundario"]
        id_usuario = id_usuario
        ubicacion = request.json["ubicacion"]
        tipo_de_equipo = request.json["tipo_de_equipo"]
        fabricante = request.json["fabricante"]
        modelo = request.json["modelo"]
        num_serie = request.json["num_serie"]
        datos_relevantes = request.json["datos_relevantes"]
        imagen_equipo = request.json["imagen_equipo"]
        id_subcliente = request.json["id_subcliente"]
        ficha_tecnica = request.json["ficha_tecnica"]

        id_primario = Activo.query.filter_by(id_primario = id_primario).first() #Buscar si el id_primario ingresado ya se encuetra registrado

        if not id_primario:
            id_secundario = Activo.query.filter_by(id_primario = id_primario).first()
            if not id_secundario:
                new_activo = Activo(id_activo,id_qr,id_primario,id_secundario,id_usuario,ubicacion,tipo_de_equipo,fabricante,modelo,num_serie,datos_relevantes,imagen_equipo,id_subcliente,ficha_tecnica)
                db.session.add(new_activo)
                db.session.commit()
                return jsonify({"message": "Activo creado correctamente", "status" : 200})
            else:
                return jsonify({"message": "El id secundario que ingreso ya a sido utilizado", "status" : 400}),400
        else:
            return jsonify({"message": "El id primario que ingreso ya a sido utilizado", "status" : 400}),400



    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})