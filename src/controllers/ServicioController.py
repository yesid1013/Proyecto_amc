from flask import jsonify, request
from models.Servicio import *
import binascii
import uuid
from datetime import datetime
import pytz
from models.Tipo_servicio import Tipo_servicio
from models.Costo_servicio import Costo_servicio
from models.Usuario import Usuario
from models.Activo import Activo
from models.Subcliente import Subcliente
from controllers import GoogleDriveController
from utils.validation import validation_servicio
import bleach
from sqlalchemy.orm import aliased



def crear_servicio(id_activo,id_usuario):
    try:
        validation = validation_servicio(request.json)
        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400

        id_servicio = uuid.uuid4().bytes
        fecha_ejecucion = request.json["fecha_ejecucion"]
        id_tipo_servicio = int(request.json["id_tipo_servicio"])
        descripcion = bleach.clean(request.json["descripcion"],tags=bleach.sanitizer.ALLOWED_TAGS)
        orden_de_servicio = request.json["orden_de_servicio"]

        observaciones = saneamiento_de_datos(request.json["observaciones"])
        observaciones_usuario = saneamiento_de_datos(request.json["observaciones_usuario"])

        #Convertir id a binario
        id_usuario_bytes = binascii.unhexlify(id_usuario)
        id_activo_bytes = binascii.unhexlify(id_activo)

        #Formateo de fecha
        fecha = formatear_fecha(fecha_ejecucion)

        informe = None
        
        new_servicio = Servicio(id_servicio,id_activo_bytes,fecha,id_usuario_bytes,id_tipo_servicio,descripcion,observaciones,observaciones_usuario,informe,orden_de_servicio)

        db.session.add(new_servicio)
        db.session.commit()

        return jsonify({"message": "Servicio creado correctamente", "status" : 201}) , 201
    
    except ValueError as e:
        return jsonify ({"message" : "Fecha inválida, por favor ingresa una fecha y hora válida."}), 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)}), 500
    
def serivicios_de_un_activo_con_costo(id_activo):
    try:
        lista = []
        id_activo_bytes = binascii.unhexlify(id_activo)

        # servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio, Servicio.id_activo, Servicio.fecha_ejecucion,Tipo_servicio.tipo,Usuario.nombre,Servicio.descripcion,Servicio.observaciones,Servicio.informe, Costo_servicio.documento_cotizacion).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).join(Costo_servicio, Servicio.id_servicio == Costo_servicio.id_servicio).join(Usuario,Servicio.id_usuario == Usuario.id_usuario).filter(Servicio.id_activo == id_activo_bytes, Servicio.estado == 1).all()

        costo_servicio_alias = aliased(Costo_servicio)

        servicios = db.session.query(
        Servicio.id_servicio,
        Servicio.numero_servicio,
        Servicio.id_activo,
        Servicio.fecha_ejecucion,
        Tipo_servicio.tipo,
        Usuario.nombre,
        Servicio.descripcion,
        Servicio.observaciones,
        Servicio.informe,
        costo_servicio_alias.documento_cotizacion
        ).join(
            Tipo_servicio,
            Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio
        ).join(
            Usuario,
            Servicio.id_usuario == Usuario.id_usuario
        ).outerjoin(
            costo_servicio_alias,
            Servicio.id_servicio == costo_servicio_alias.id_servicio
        ).filter(
            Servicio.id_activo == id_activo_bytes,
            Servicio.estado == 1
        ).all()

        for servicio in servicios:
            datos = {"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(),"numero_servicio" : servicio.numero_servicio ,"fecha_ejecucion" : servicio.fecha_ejecucion.strftime('%Y-%m-%d %H:%M:%S'), "tipo" : servicio.tipo, "descripcion" : servicio.descripcion, "observaciones" : servicio.observaciones, "informe" : servicio.informe,"nombre_usuario" : servicio.nombre, "costo" : servicio.documento_cotizacion }
            lista.append(datos)
            
        return jsonify(lista)

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def serivicios_de_un_activo_sin_costo(id_activo):
    try:
        id_activo_bytes = binascii.unhexlify(id_activo)

        servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio, Servicio.id_activo, Servicio.fecha_ejecucion,Tipo_servicio.tipo,Usuario.nombre,Servicio.descripcion,Servicio.observaciones,Servicio.informe).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).join(Usuario,Servicio.id_usuario == Usuario.id_usuario).filter(Servicio.id_activo == id_activo_bytes, Servicio.estado == 1).all()

        if not servicios:
            return jsonify({"message" : "Servivicos no encontrados", "status" : 404}) , 404


        lista = [{"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(),"numero_servicio" : servicio.numero_servicio ,"fecha_ejecucion" : servicio.fecha_ejecucion.strftime('%Y-%m-%d %H:%M:%S'), "tipo" : servicio.tipo, "descripcion" : servicio.descripcion, "observaciones" : servicio.observaciones, "informe" : servicio.informe,"nombre_usuario" : servicio.nombre} for servicio in servicios]
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


def obtener_servicios_de_usuario(id_usuario): #Obtener los servicio de los activos del usuario
    try:
        id_usuario_bytes = binascii.unhexlify(id_usuario)
        servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio,Activo.tipo_de_equipo,Activo.id_primario,Servicio.fecha_ejecucion,Usuario.nombre,Tipo_servicio.tipo,Servicio.id_tipo_servicio,Servicio.descripcion,Servicio.observaciones,Servicio.observaciones_usuario,Servicio.informe,Servicio.orden_de_servicio).join(Activo,Servicio.id_activo == Activo.id_activo).join(Usuario, Servicio.id_usuario == Usuario.id_usuario).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).filter(Activo.id_usuario == id_usuario_bytes, Servicio.estado == 1).all()

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
            fecha = formatear_fecha(fecha_ejecucion)

            observaciones = saneamiento_de_datos(request.json["observaciones"])
            observaciones_usuario = saneamiento_de_datos(request.json["observaciones_usuario"])

            id_activo = bleach.clean(request.json["id_activo"],tags=bleach.sanitizer.ALLOWED_TAGS)
            id_activo_bytes = binascii.unhexlify(id_activo)
            
            orden_de_servicio = request.json["orden_de_servicio"]
            if orden_de_servicio["name"] != None and orden_de_servicio["content"] != None and orden_de_servicio["mimeType"] != None: 
                id_folder = "1vVTG_28NG5VL4gSLRSRJtqzzyptl0Ax-"
                response = GoogleDriveController.uploadFile(orden_de_servicio,id_folder)
                servicio.orden_de_servicio = response["webViewLink"]
            
            servicio.fecha_ejecucion = fecha 
            servicio.id_tipo_servicio = request.json["id_tipo_servicio"]
            servicio.descripcion = bleach.clean(request.json["descripcion"],tags=bleach.sanitizer.ALLOWED_TAGS)
            servicio.observaciones = observaciones
            servicio.observaciones_usuario = observaciones_usuario
            servicio.id_activo = id_activo_bytes

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

def servicios_de_un_subcliente(id_subcliente):
    try:
        id_subcliente_bytes = binascii.unhexlify(id_subcliente)
        servicios = db.session.query(Servicio.descripcion, Subcliente.nombre, Activo.tipo_de_equipo).join(Activo,Servicio.id_activo == Activo.id_activo).join(Subcliente, Activo.id_subcliente == Subcliente.id_subcliente).filter(Subcliente.id_subcliente == id_subcliente_bytes).all()

        lista = [{"descripcion" : servicio.descripcion, "nombre_subcliente" : servicio.nombre, "activo" : servicio.tipo_de_equipo} for servicio in servicios]

        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def servicios_sin_informe(id_usuario):
    try:
        id_usuario_bytes = binascii.unhexlify(id_usuario)

        servicios = db.session.query(Servicio.id_servicio,Servicio.numero_servicio,Activo.tipo_de_equipo,Servicio.fecha_ejecucion,Tipo_servicio.tipo,Servicio.descripcion).join(Activo,Servicio.id_activo == Activo.id_activo).join(Tipo_servicio, Servicio.id_tipo_servicio == Tipo_servicio.id_tipo_servicio).filter(Servicio.informe == None, Servicio.id_usuario == id_usuario_bytes, Activo.id_usuario == id_usuario_bytes).all()

        if not servicios:
            return jsonify({"message" : "No hay servicios", "status" : 404}) , 404

        lista = [{"id_servicio" : binascii.hexlify(servicio.id_servicio).decode(), "numero_servicio" : servicio.numero_servicio, "activo" : servicio.tipo_de_equipo, "fecha_ejecucion" : servicio.fecha_ejecucion.strftime('%Y-%m-%d %H:%M:%S'), "tipo_servicio" : servicio.tipo, "descripcion" : servicio.descripcion} for servicio in servicios]

        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def adjuntar_informe_servicio(id_servicio):
    try:
        id_servicio_bytes = binascii.unhexlify(id_servicio)
        servicio = Servicio.query.get(id_servicio_bytes)

        if servicio.informe == None:
            informe_servicio = request.json["informe_servicio"]
            servicio.informe = informe_servicio
            db.session.commit()
            return jsonify({"message" : "Informe adjuntado correctamente", "url_archivo" : informe_servicio ,"status" : 200})

        else:
            return jsonify({"message" : "El servicio ya tiene informe"}) , 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e)})
    
def formatear_fecha(fecha_ejecucion):
    fecha_utc = datetime.fromisoformat(fecha_ejecucion)
    zona_horaria_colombia = pytz.timezone('America/Bogota')
    fecha_colombia = fecha_utc.astimezone(zona_horaria_colombia)
    fecha = fecha_colombia.strftime('%Y-%m-%d %H:%M:%S')
    return fecha

def saneamiento_de_datos(request):
    return bleach.clean(request, tags=bleach.sanitizer.ALLOWED_TAGS) if request is not None else None


