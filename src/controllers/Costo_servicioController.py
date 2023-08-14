from flask import request,jsonify
from models.Costo_servicio import *
import uuid
import binascii
import bleach

def crear_costo_servicio(id_servicio):
    try:
        id_costo_servicio = uuid.uuid4().bytes
        id_servicio_bytes = binascii.unhexlify(id_servicio)
        costo = bleach.clean(request.json["costo"],tags=bleach.sanitizer.ALLOWED_TAGS)
        documento_cotizacion = None

        new_costo_servicio = Costo_servicio(id_costo_servicio,id_servicio_bytes,costo,documento_cotizacion)
        db.session.add(new_costo_servicio)
        db.session.commit()

        return jsonify({"message": "Cotizacion creada correctamente", "status" : 200}) , 200
    
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
