from flask import jsonify,request
from models.Novedad import *
import binascii
import uuid
from io import BytesIO
from controllers import GoogleDriveController
from utils.validation import validation_novedad

def crear_novedad(id_activo):
    try:
        validation = validation_novedad(request.json)
        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400

        id_novedad = uuid.uuid4().bytes
        id_activo_bytes = binascii.unhexlify(id_activo) # Convierto el id hexadecimal a binario
        nombre_reporta = request.json["nombre_reporta"]
        nombre_empresa = request.json["nombre_empresa"]
        cargo = request.json["cargo"]
        descripcion_reporte = request.json["descripcion_reporte"]
        imagenes = request.json["imagenes"]

        if imagenes:
            id_folder = "1m6h1aZAqPh-vgtMw0sQtEM3RIlEoAFdC"
            upload_response = GoogleDriveController.uploadFile(imagenes,id_folder)
            id_imagen = upload_response["id"]

        new_novedad = Novedad(id_novedad,id_activo_bytes,nombre_reporta,nombre_empresa,cargo,descripcion_reporte,id_imagen)
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
            novedad.nombre_reporta = request.json["nombre_reporta"]
            novedad.nombre_empresa = request.json["nombre_empresa"]
            novedad.cargo = request.json["cargo"]
            novedad.descripcion_reporte = request.json["descripcion_reporte"]
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


