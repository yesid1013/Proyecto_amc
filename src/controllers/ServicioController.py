from flask import jsonify, request
from models.Servicio import *
import binascii
import uuid
from datetime import datetime
import pytz
from models.Tipo_servicio import Tipo_servicio
from models.Usuario import Usuario
from models.Activo import Activo
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
        id_tipo_servicio = int(request.json["id_tipo_servicio"])
        descripcion = bleach.clean(request.json["descripcion"],tags=bleach.sanitizer.ALLOWED_TAGS)
        observaciones = request.json["observaciones"]
        observaciones_usuario = request.json["observaciones_usuario"]
        #informe = request.json["informe"]
        orden_de_servicio = request.json["orden_de_servicio"]

        if observaciones is not None:
            observaciones = bleach.clean(observaciones, tags=bleach.sanitizer.ALLOWED_TAGS)
        else:
            observaciones = None
        
        if observaciones_usuario is not None:
            observaciones_usuario = bleach.clean(observaciones_usuario, tags=bleach.sanitizer.ALLOWED_TAGS)
        else:
            observaciones_usuario = None
        
        # if informe["name"] != None and informe["content"] != None and informe["mimeType"] != None: 
        #     id_folder = "1L5aLI-JdlZ3dDJ2LxnWSbxBn70yt0nPA"
        #     response = GoogleDriveController.uploadFile(informe,id_folder)
        #     informe = response["webViewLink"]
        # else:
        informe = None
        
        if orden_de_servicio["name"] != None and orden_de_servicio["content"] != None and orden_de_servicio["mimeType"] != None: 
            id_folder = "1vVTG_28NG5VL4gSLRSRJtqzzyptl0Ax-"
            response = GoogleDriveController.uploadFile(orden_de_servicio,id_folder)
            orden_de_servicio = response["webViewLink"]
        else:
            orden_de_servicio = None

        id_usuario_bytes = binascii.unhexlify(id_usuario)
        id_activo_bytes = binascii.unhexlify(id_activo)

        #Formateo de fecha
        fecha_utc = datetime.fromisoformat(fecha_ejecucion)
        zona_horaria_colombia = pytz.timezone('America/Bogota')
        fecha_colombia = fecha_utc.astimezone(zona_horaria_colombia)
        fecha = fecha_colombia.strftime('%Y-%m-%d %H:%M:%S')

        new_servicio = Servicio(id_servicio,id_activo_bytes,fecha,id_usuario_bytes,id_tipo_servicio,descripcion,observaciones,observaciones_usuario,informe,orden_de_servicio)

        db.session.add(new_servicio)
        db.session.commit()

        return jsonify({"message": "Servicio creado correctamente", "status" : 201}) , 201
    
    except ValueError as e:
        return jsonify ({"message" : "Fecha inválida, por favor ingresa una fecha y hora válida."}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)}), 500
    
def serivicios_de_un_activo(id_activo):
    try:
        lista = []
        id_activo_bytes = binascii.unhexlify(id_activo)

        servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio, Servicio.id_activo, Servicio.fecha_ejecucion,Tipo_servicio.tipo,Usuario.nombre,Servicio.descripcion,Servicio.observaciones,Servicio.informe).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).join(Usuario,Servicio.id_usuario == Usuario.id_usuario).filter(Servicio.id_activo == id_activo_bytes, Servicio.estado == 1).all()

        for servicio in servicios:
            datos = {"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(),"numero_servicio" : servicio.numero_servicio ,"fecha_ejecucion" : servicio.fecha_ejecucion, "tipo" : servicio.tipo, "descripcion" : servicio.descripcion, "observaciones" : servicio.observaciones, "imagenes" : servicio.imagenes, "informe" : servicio.informe,"nombre_usuario" : servicio.nombre}
            lista.append(datos)
            
        return jsonify(lista)

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def obtener_todos_los_servicios():
    try:
        servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio,Activo.tipo_de_equipo,Activo.id_primario,Servicio.fecha_ejecucion,Usuario.nombre,Tipo_servicio.tipo,Servicio.id_tipo_servicio,Servicio.descripcion,Servicio.observaciones,Servicio.observaciones_usuario,Servicio.informe, Servicio.orden_de_servicio).join(Activo,Servicio.id_activo == Activo.id_activo).join(Usuario, Servicio.id_usuario == Usuario.id_usuario).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).filter(Servicio.estado == 1).all()

        if not servicios:
            return jsonify({"message" : "Servivicos no encontrados", "status" : 404}) , 404
        else:
            lista = [{"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(), "numero_servicio" : servicio.numero_servicio, "activo" : servicio.tipo_de_equipo,"activo_id_primario" : servicio.id_primario,"fecha_ejecucion" : servicio.fecha_ejecucion.strftime('%Y-%m-%d %H:%M:%S'), "nombre_usuario" : servicio.nombre, "tipo_servicio" : servicio.tipo,"id_tipo_servicio" : servicio.id_tipo_servicio ,"descripcion" : servicio.descripcion, "observaciones" : servicio.observaciones,"observaciones_usuario" : servicio.observaciones_usuario ,"informe" : servicio.informe,"orden_de_servicio" : servicio.orden_de_servicio} for servicio in servicios]
            return jsonify(lista)

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})


def obtener_servicios_de_usuario(id_usuario):
    try:
        id_usuario_bytes = binascii.unhexlify(id_usuario)
        servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio,Activo.tipo_de_equipo,Activo.id_primario,Servicio.fecha_ejecucion,Usuario.nombre,Tipo_servicio.tipo,Servicio.id_tipo_servicio,Servicio.descripcion,Servicio.observaciones,Servicio.observaciones_usuario,Servicio.informe,Servicio.orden_de_servicio).join(Activo,Servicio.id_activo == Activo.id_activo).join(Usuario, Servicio.id_usuario == Usuario.id_usuario).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).filter(Servicio.id_usuario == id_usuario_bytes, Servicio.estado == 1).all()

        if not servicios:
            return jsonify({"message" : "Servivicos no encontrados", "status" : 404}) , 404
        else:
            lista = [{"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(), "numero_servicio" : servicio.numero_servicio, "activo" : servicio.tipo_de_equipo,"activo_id_primario" : servicio.id_primario ,"fecha_ejecucion" : servicio.fecha_ejecucion.strftime('%Y-%m-%d %H:%M:%S'), "nombre_usuario" : servicio.nombre, "tipo_servicio" : servicio.tipo,"id_tipo_servicio" : servicio.id_tipo_servicio ,"descripcion" : servicio.descripcion, "observaciones" : servicio.observaciones,"observaciones_usuario" : servicio.observaciones_usuario, "informe" : servicio.informe, "orden_de_servicio" : servicio.orden_de_servicio} for servicio in servicios]
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
            fecha_ejecucion = request.json["fecha_ejecucion"]
            fecha_utc = datetime.fromisoformat(fecha_ejecucion)
            zona_horaria_colombia = pytz.timezone('America/Bogota')
            fecha_colombia = fecha_utc.astimezone(zona_horaria_colombia)
            fecha = fecha_colombia.strftime('%Y-%m-%d %H:%M:%S')

            if request.json["observaciones"] is not None:
                observaciones = bleach.clean(request.json["observaciones"], tags=bleach.sanitizer.ALLOWED_TAGS)
            else:
                observaciones = None
        
            if request.json["observaciones_usuario"] is not None:
                observaciones_usuario = bleach.clean(request.json["observaciones_usuario"], tags=bleach.sanitizer.ALLOWED_TAGS)
            else:
                observaciones_usuario = None

            servicio.fecha_ejecucion = fecha 
            servicio.id_tipo_servicio = request.json["id_tipo_servicio"]
            servicio.descripcion = bleach.clean(request.json["descripcion"],tags=bleach.sanitizer.ALLOWED_TAGS)
            servicio.observaciones = observaciones
            servicio.observaciones_usuario = observaciones_usuario

            id_activo = bleach.clean(request.json["id_activo"],tags=bleach.sanitizer.ALLOWED_TAGS)
            id_activo_bytes = binascii.unhexlify(id_activo)
            servicio.id_activo = id_activo_bytes

            orden_de_servicio = request.json["orden_de_servicio"]
            if orden_de_servicio["name"] != None and orden_de_servicio["content"] != None and orden_de_servicio["mimeType"] != None: 
                id_folder = "1vVTG_28NG5VL4gSLRSRJtqzzyptl0Ax-"
                response = GoogleDriveController.uploadFile(orden_de_servicio,id_folder)
                servicio.orden_de_servicio = response["webViewLink"]
            else:
                orden_de_servicio = None

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
