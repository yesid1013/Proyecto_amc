from flask import jsonify, request
from models.Permisos import *
from models.Activo import Activo
from models.Usuario import Usuario
from utils.validation import validation_permiso
import uuid
import binascii
import bleach


def registrar_permiso():
    try:

        validation = validation_permiso(request.json)
        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400

        id_permiso = uuid.uuid4().bytes
        id_usuario = bleach.clean(request.json['id_usuario'],tags=bleach.sanitizer.ALLOWED_TAGS)
        id_activo = bleach.clean(request.json['id_activo'],tags=bleach.sanitizer.ALLOWED_TAGS)
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
    
def permisos_otorgados(id_usuario): #muestra los activos a los que otros usuarios han otorgado permisos
    try: #El id_usuario que recibo en la función es el usuario que ingreso a la plataforma

        id_usuario_bytes = binascii.unhexlify(id_usuario)
        permisos = Permisos.query.filter_by(id_usuario = id_usuario_bytes).all() #Busco si el usuario que ingreso le han otorgado permisos

        if not permisos:
            return jsonify({"message": "No tienes permisos otorgados", "status" : 404})
        else:
            lista = [permiso.getDatos() for permiso in permisos]
            return jsonify(lista)
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)})

def permisos_creados(id_usuario): #Ver los permisos que un usuario ha creado
    try:
        id_usuario_bytes = binascii.unhexlify(id_usuario)

        permisos = db.session.query(Permisos.id_permiso,Activo.tipo_de_equipo,Usuario.nombre,Permisos.ver_informacion_basica,Permisos.ver_historial_servicios,Permisos.ver_novedades,Permisos.registrar_servicio,Permisos.registrar_novedad).join(Activo, Activo.id_activo == Permisos.id_activo).join(Usuario, Usuario.id_usuario == Permisos.id_usuario).filter(Activo.id_usuario == id_usuario_bytes).all()

        if not permisos:
            return jsonify({"message": "No haz creados permisos", "status" : 404})
        else:
            lista = [{"id_permiso" :  binascii.hexlify(permiso.id_permiso).decode(),"activo" : permiso.tipo_de_equipo,"usuario" : permiso.nombre,"ver_informacion_basica" : permiso.ver_informacion_basica, "ver_historial_servicios" : permiso.ver_historial_servicios, "ver_novedades" : permiso.ver_novedades, "registrar_servicio" : permiso.registrar_servicio, "registrar_novedad" : permiso.registrar_novedad} for permiso in permisos]
            return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)})
    
def editar_permiso(id_permiso):
    try: 
        id_permiso_bytes = binascii.unhexlify(id_permiso)
        permiso = Permisos.query.get(id_permiso_bytes)

        if not permiso:
            return jsonify({"message" : "Permiso no encontrado", "status" : 404}) , 404
        else:
            id_usuario = bleach.clean(request.json['id_usuario'],tags=bleach.sanitizer.ALLOWED_TAGS)
            id_activo = bleach.clean(request.json['id_activo'],tags=bleach.sanitizer.ALLOWED_TAGS)
            ver_informacion_basica = request.json['ver_informacion_basica']
            ver_historial_servicios = request.json['ver_historial_servicios']
            ver_novedades = request.json['ver_novedades']
            registrar_servicio = request.json['registrar_servicio']
            registrar_novedad = request.json['registrar_novedad']

            id_usuario_bytes = binascii.unhexlify(id_usuario)
            id_activo_bytes = binascii.unhexlify(id_activo)
            
            permiso.id_usuario = id_usuario_bytes
            permiso.id_activo = id_activo_bytes
            permiso.ver_informacion_basica = ver_informacion_basica
            permiso.ver_historial_servicios = ver_historial_servicios
            permiso.ver_novedades = ver_novedades
            permiso.registrar_servicio = registrar_servicio
            permiso.registrar_novedad = registrar_novedad

            db.session.commit()

            return jsonify({"message": "Permiso editado correctamente", "status" : 200}), 200

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)})
