from flask import jsonify, request
from models.Permisos import *
import uuid
import binascii

def registrar_permiso():
    try:

        id_permiso = uuid.uuid4().bytes
        id_usuario = request.json['id_usuario']
        id_activo = request.json['id_activo']
        ver_informacion_basica = request.json['ver_informacion_basica']
        ver_historial_servicios = request.json['ver_historial_servicios']
        ver_novedades = request.json['ver_novedades']
        registrar_servicio = request.json['registrar_servicio']
        registrar_novedad = request.json['registrar_novedad']

        id_usuario_bytes = binascii.unhexlify(id_usuario)
        id_activo_bytes = binascii.unhexlify(id_activo)

        new_permiso = Permisos(id_permiso,id_usuario_bytes,id_activo_bytes,ver_informacion_basica,ver_historial_servicios,ver_novedades,registrar_servicio,registrar_novedad)

        db.session.add(new_permiso)
        db.session.commit()
        return jsonify({"message": "Permiso creado correctamente", "status" : 201}), 201
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)})