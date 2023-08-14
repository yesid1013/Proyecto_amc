from flask import jsonify, request
from models.Servicio import *
import binascii
import uuid
from datetime import datetime
from models.Tipo_servicio import Tipo_servicio
from models.Usuario import Usuario
from controllers import GoogleDriveController
from utils.validation import validation_servicio
import bleach

def crear_servicio(id_activo,id_usuario):
    try:
        validation = validation_servicio(request.json)
        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400

        id_servicio = uuid.uuid4().bytes
        fecha_ejecucion = request.json["fecha_ejecucion"]
        id_tipo_servicio = request.json["id_tipo_servicio"]
        descripcion = bleach.clean(request.json["descripcion"],tags=bleach.sanitizer.ALLOWED_TAGS)
        observaciones = bleach.clean(request.json["observaciones"],tags=bleach.sanitizer.ALLOWED_TAGS)
        informe = request.json["informe"]
        
        if informe:
            id_folder = "1L5aLI-JdlZ3dDJ2LxnWSbxBn70yt0nPA"
            response = GoogleDriveController.uploadFile(informe,id_folder)
            informe = response["webViewLink"]

        id_usuario_bytes = binascii.unhexlify(id_usuario)
        id_activo_bytes = binascii.unhexlify(id_activo)
        fecha_datetime = datetime.strptime(fecha_ejecucion, '%d-%m-%Y %H:%M:%S')

        new_servicio = Servicio(id_servicio,id_activo_bytes,fecha_datetime,id_usuario_bytes,id_tipo_servicio,descripcion,observaciones,informe)

        db.session.add(new_servicio)
        db.session.commit()

        return jsonify({"message": "Servicio creado correctamente", "status" : 201}) , 201
    
    except ValueError as e:
        return jsonify ({"message" : "Fecha inválida, por favor ingresa una fecha y hora válida."}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def serivicios_de_un_activo(id_activo):
    try:
        lista = []
        id_activo_bytes = binascii.unhexlify(id_activo)

        servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio, Servicio.id_activo, Servicio.fecha_ejecucion,Tipo_servicio.tipo,Usuario.nombre,Servicio.descripcion,Servicio.observaciones,Servicio.imagenes,Servicio.informe).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).join(Usuario,Servicio.id_usuario == Usuario.id_usuario).filter(Servicio.id_activo == id_activo_bytes, Servicio.estado == 1).all()

        for servicio in servicios:
            datos = {"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(),"numero_servicio" : servicio.numero_servicio ,"fecha_ejecucion" : servicio.fecha_ejecucion, "tipo" : servicio.tipo, "descripcion" : servicio.descripcion, "observaciones" : servicio.observaciones, "imagenes" : servicio.imagenes, "informe" : servicio.informe,"nombre_usuario" : servicio.nombre}
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
            servicio.descripcion = bleach.clean(request.json["decripcion"],tags=bleach.sanitizer.ALLOWED_TAGS)
            servicio.observaciones = bleach.clean(request.json["observaciones"],tags=bleach.sanitizer.ALLOWED_TAGS)
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


def restaurar_servicio(id_servicio):
    try:
        id_servicio_bytes = binascii.unhexlify(id_servicio)
        servicio = Servicio.query.get(id_servicio_bytes)

        if not servicio:
            return jsonify({"message" : "Servicio no encontrado", "status" : 404}) , 404
        
        else:
            servicio.estado = 1
            db.session.commit()
            return jsonify({"message" : "Servicio restaurado exitosamente", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
