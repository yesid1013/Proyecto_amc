from flask import request,jsonify
from models.Costo_servicio import *
from models.Servicio import Servicio
from models.Activo import Activo
from models.Tipo_servicio import Tipo_servicio
from utils.validation import validation_costo_servicio
from controllers import GoogleDriveController
import uuid
import binascii
import bleach

def crear_costo_servicio(id_servicio):
    try:
        validation = validation_costo_servicio(request.json)
        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400

        id_costo_servicio = uuid.uuid4().bytes
        id_servicio_bytes = binascii.unhexlify(id_servicio)
        costo = request.json["costo"]
        documento_cotizacion = request.json["documento_cotizacion"]

        if documento_cotizacion:
            id_folder = "1A-5He-r8oSQUsHxrKoEvHS1lVedFHe8l"
            response = GoogleDriveController.uploadFile(documento_cotizacion,id_folder)
            url_documento_cotizacion = response["webViewLink"]

        new_costo_servicio = Costo_servicio(id_costo_servicio,id_servicio_bytes,costo,url_documento_cotizacion)
        db.session.add(new_costo_servicio)
        db.session.commit()

        return jsonify({"message": "Cotizacion creada correctamente","url_archivo" : url_documento_cotizacion ,"status" : 201}) , 201
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def cotizacion_de_un_servicio(id_servicio):
    try:
        lista = []
        id_servicio_bytes = binascii.unhexlify(id_servicio)

        cotizaciones = db.session.query(Costo_servicio.id_costo_servicio,Costo_servicio.costo,Costo_servicio.documento_cotizacion).filter_by(id_servicio = id_servicio_bytes, estado = 1 ).all()

        if not cotizaciones:
            return jsonify({"message" : "No se encontraron cotizaciones" , "status" : 404}) , 404
        else:
            for cotizacion in cotizaciones:
                datos = {"id_costo_servicio" : binascii.hexlify(cotizacion.id_costo_servicio).decode(), "costo" : cotizacion.costo, "documento_cotizacion" : cotizacion.documento_cotizacion}
                lista.append(datos)

            return jsonify(datos)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def editar_cotizacion (id_costo_servicio):
    try:
        id_costo_servicio_bytes = binascii.unhexlify(id_costo_servicio)
        costo_servicio = Costo_servicio.query.get(id_costo_servicio_bytes)

        if not costo_servicio:
            return jsonify({"message" : "No se encontraron cotizaciones" , "status" : 404}) , 404
        else:
            costo_servicio.costo = bleach.clean(request.json["fabricante"],tags=bleach.sanitizer.ALLOWED_TAGS)
            #pendiente actualizar documento de cotizacion
            db.session.commit()
            return jsonify({"message" : "Cotizacion actualizada exitosamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def eliminar_cotizacion(id_costo_servicio):
    try:
        id_costo_servicio_bytes = binascii.unhexlify(id_costo_servicio)
        costo_servicio = Costo_servicio.query.get(id_costo_servicio_bytes)

        if not costo_servicio:
            return jsonify({"message" : "No se encontraron cotizaciones" , "status" : 404}) , 404
        else:
            costo_servicio.estado = 0
            db.session.commit()
            return jsonify({"message" : "Cotizacion eliminada exitosamente", "status" : 200}) , 200
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def restaurar_cotizacion(id_costo_servicio):
    try:
        id_costo_servicio_bytes = binascii.unhexlify(id_costo_servicio)
        costo_servicio = Costo_servicio.query.get(id_costo_servicio_bytes)

        if not costo_servicio:
            return jsonify({"message" : "No se encontraron cotizaciones" , "status" : 404}) , 404
        else:
            costo_servicio.estado = 1
            db.session.commit()
            return jsonify ({"message" : "Cotizacion restaurada exitosamente", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def servicios_sin_cotizacion(id_usuario):
    try:
        id_usuario_bytes = binascii.unhexlify(id_usuario)

        servicios_sin_costo  = db.session.query(Servicio.id_servicio, Servicio.numero_servicio,Activo.tipo_de_equipo,Servicio.fecha_ejecucion,Servicio.descripcion,Tipo_servicio.tipo).outerjoin(Costo_servicio).join(Activo, Servicio.id_activo == Activo.id_activo).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).filter(Costo_servicio.id_costo_servicio.is_(None),Servicio.id_usuario == id_usuario_bytes, Activo.id_usuario == id_usuario_bytes).all()

        if not servicios_sin_costo:
            return jsonify({"message" : "No hay cotizaciones pendientes" , "status" : 404})

        lista = [{"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(), "activo" : servicio.tipo_de_equipo, "numero_servicio" : servicio.numero_servicio, "fecha_ejecucion" : servicio.fecha_ejecucion.strftime('%Y-%m-%d %H:%M:%S'), "descripcion" : servicio.descripcion, "tipo_servicio" : servicio.tipo} for servicio in servicios_sin_costo]

        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)})