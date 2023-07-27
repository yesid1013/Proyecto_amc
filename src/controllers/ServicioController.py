from flask import jsonify, request
from models.Servicio import *
import binascii
import uuid
from datetime import datetime
from models.Tipo_servicio import Tipo_servicio

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
    
def serivicios_de_un_activo(id_activo):
    try:
        lista = []
        id_activo_bytes = binascii.unhexlify(id_activo)

        servicios = db.session.query(Servicio.id_servicio, Servicio.id_activo, Servicio.fecha_ejecucion,Tipo_servicio.tipo,Servicio.descripcion,Servicio.observaciones,Servicio.imagenes,Servicio.informe).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).filter(Servicio.id_activo == id_activo_bytes, Servicio.estado == 1).all()

        for servicio in servicios:
            datos = {"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(), "fecha_ejecucion" : servicio.fecha_ejecucion, "tipo" : servicio.tipo, "descripcion" : servicio.descripcion, "observaciones" : servicio.observaciones, "imagenes" : servicio.imagenes, "informe" : servicio.informe}
            lista.append(datos)
            
        return jsonify(lista)

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
    
def editar_servicio(id_servicio):
    try:
        id_servicio_bytes = binascii.unhexlify(id_servicio)

        servicio = Servicio.query.get(id_servicio_bytes)
        if not servicio:
            return jsonify({"message" : "Servivico no encontrado", "status" : 404}) , 404
        
        else:
            fecha_datetime = datetime.strptime(request.json["fecha_ejecucion"], '%d-%m-%Y %H:%M:%S')
            servicio.fecha_ejecucion = fecha_datetime 
            servicio.id_tipo_servicio = request.json["id_tipo_servicio"]
            servicio.descripcion = request.json["descripcion"]
            servicio.observaciones = request.json["observaciones"]
            imagenes = None
            informe = None

            db.session.commit()
            return jsonify({"message" : "Servicio actualizado exitosamente", "status" : 200}) , 200
    
    except ValueError as e:
        return jsonify ({"message" : "Fecha inválida, por favor ingresa una fecha y hora válida."}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def eliminar_servicio(id_servicio):
    try:
        id_servicio_bytes = binascii.unhexlify(id_servicio)
        servicio = Servicio.query.get(id_servicio_bytes)

        if not servicio:
            return jsonify({"message" : "Servicio no encontrado", "status" : 404}) , 404
        
        else:
            servicio.estado = 0
            db.session.commit()
            return jsonify({"message" : "Servicio eliminado", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})


    


