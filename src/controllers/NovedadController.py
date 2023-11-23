from flask import jsonify,request
from models.Novedad import *
import binascii
import uuid
from io import BytesIO
from controllers import GoogleDriveController
from utils.validation import validation_novedad
import bleach

def crear_novedad(id_activo):
    try:
        validation = validation_novedad(request.json)
        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400

        id_novedad = uuid.uuid4().bytes
        id_activo_bytes = binascii.unhexlify(id_activo) # Convierto el id hexadecimal a binario
        nombre_reporta = bleach.clean(request.json["nombre_reporta"],tags=bleach.sanitizer.ALLOWED_TAGS)
        nombre_empresa = bleach.clean(request.json["nombre_empresa"],tags=bleach.sanitizer.ALLOWED_TAGS)
        cargo = bleach.clean(request.json["cargo"],tags=bleach.sanitizer.ALLOWED_TAGS)
        descripcion_reporte = bleach.clean(request.json["descripcion_reporte"],tags=bleach.sanitizer.ALLOWED_TAGS)
        imagenes = request.json["imagenes"]

        if imagenes["name"] != None and imagenes["content"] != None and imagenes["mimeType"] != None: 
            id_folder = "1m6h1aZAqPh-vgtMw0sQtEM3RIlEoAFdC"
            upload_response = GoogleDriveController.uploadFile(imagenes,id_folder)
            imagen_link = upload_response["webViewLink"]
        else:
            imagen_link = None

        new_novedad = Novedad(id_novedad,id_activo_bytes,nombre_reporta,nombre_empresa,cargo,descripcion_reporte,imagen_link)
        db.session.add(new_novedad)
        db.session.commit()

        return jsonify({"message": "Novedad creada correctamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def listar_novedades_de_un_activo(id_activo):
    try:
        id_activo_bytes = binascii.unhexlify(id_activo) # Convierto el id hexadecimal a binario
        novedades = db.session.query(Novedad).filter_by(id_activo = id_activo_bytes, estado = 1).all()
        toNovedades = [novedad.getDatos() for novedad in novedades]
        return jsonify(toNovedades)


    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def editar_novedad(id_novedad):
    try:
        id_novedad_bytes = binascii.unhexlify(id_novedad) # Convierto el id hexadecimal a binario
        novedad = Novedad.query.get(id_novedad_bytes)

        if not novedad:
            return jsonify({"message" : "Novedad no encontrada", "status" : 404}), 404
        else:
            novedad.nombre_reporta = bleach.clean(request.json["nombre_reporta"],tags=bleach.sanitizer.ALLOWED_TAGS)
            novedad.nombre_empresa = bleach.clean(request.json["nombre_empresa"],tags=bleach.sanitizer.ALLOWED_TAGS)
            novedad.cargo = bleach.clean(request.json["cargo"],tags=bleach.sanitizer.ALLOWED_TAGS)
            novedad.descripcion_reporte = bleach.clean(request.json["descripcion_reporte"],tags=bleach.sanitizer.ALLOWED_TAGS)
            novedad.imagenes = request.json["imagenes"]

            db.session.commit()

            return jsonify({"message" : "Novedad actualizada exitosamente", "status" : 200})
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def eliminar_novedad(id_novedad):
    try:
        id_novedad_bytes = binascii.unhexlify(id_novedad)
        novedad = Novedad.query.get(id_novedad_bytes)

        if not novedad:
            return jsonify({"message" : "Novedad no encontrada", "status" : 404}), 404
        else:
            novedad.estado = 0
            db.session.commit()
            return jsonify({"message" : "Novedad eliminada", "status" : 200})
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def restaurar_novedad(id_novedad):
    try:
        id_novedad_bytes = binascii.unhexlify(id_novedad)
        novedad = Novedad.query.get(id_novedad_bytes)

        if not novedad:
            return jsonify({"message" : "Novedad no encontrada", "status" : 404}), 404
        else:
            novedad.estado = 1
            db.session.commit()
            return jsonify({"message" : "Novedad restaurada exitosamente", "status" : 200})
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})


