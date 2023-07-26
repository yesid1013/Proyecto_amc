from flask import jsonify, request
from models.Servicio import *
import binascii
import uuid
from datetime import datetime

def crear_servicio(id_activo,id_usuario):
    try:
        id_servicio = uuid.uuid4().bytes
        fecha_ejecucion = request.json["fecha_ejecucion"]
        id_tipo_servicio = request.json["id_tipo_servicio"]
        descripcion = request.json["descripcion"]
        observaciones = request.json["observaciones"]
        imagenes = None
        informe = None

        id_usuario_bytes = binascii.unhexlify(id_usuario)
        id_activo_bytes = binascii.unhexlify(id_activo)
        fecha_datetime = datetime.strptime(fecha_ejecucion, '%d-%m-%Y %H:%M:%S')

        new_servicio = Servicio(id_servicio,id_activo_bytes,fecha_datetime,id_usuario_bytes,id_tipo_servicio,descripcion,observaciones,imagenes,informe)

        db.session.add(new_servicio)
        db.session.commit()

        return jsonify({"message": "Servicio creado correctamente", "status" : 200}) , 200
    
    except ValueError as e:
        return jsonify ({"message" : "Fecha inválida, por favor ingresa una fecha y hora válida."}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})