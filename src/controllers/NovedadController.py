from flask import jsonify,request
from models.Novedad import *
import binascii
import uuid

def crear_novedad(id_activo):
    try:
        id_novedad = uuid.uuid4().bytes
        id_activo_bytes = binascii.unhexlify(id_activo)
        nombre_reporta = request.json["nombre_reporta"]
        nombre_empresa = request.json["nombre_empresa"]
        cargo = request.json["cargo"]
        descripcion_reporte = request.json["descripcion_reporte"]
        imagenes = request.json["imagenes"]

        new_novedad = Novedad(id_novedad,id_activo_bytes,nombre_reporta,nombre_empresa,cargo,descripcion_reporte,imagenes)
        db.session.add(new_novedad)
        db.session.commit()

        return jsonify({"message": "Novedad creada correctamente", "status" : 200}) , 200
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
