from flask import jsonify, request
from models.Activo import *
import uuid
import binascii

def crear_activo(id_usuario):
    try:
        id_activo = uuid.uuid4().bytes
        id_primario = request.json["id_primario"]
        id_secundario = request.json["id_secundario"]
        id_usuario = id_usuario
        id_qr = request.json["id_qr"]
        ubicacion = request.json["ubicacion"]
        tipo_de_equipo = request.json["tipo_de_equipo"]
        fabricante = request.json["fabricante"]
        modelo = request.json["modelo"]
        num_serie = request.json["num_serie"]
        datos_relevantes = request.json["datos_relevantes"]
        imagen_equipo = request.json["imagen_equipo"]
        id_subcliente = request.json["id_subcliente"]
        ficha_tecnica = request.json["ficha_tecnica"]

        if id_secundario == "":
            id_secundario = None
        
        if modelo == "":
            modelo = None
        
        if num_serie == "":
            num_serie = None
        
        if datos_relevantes == "":
            datos_relevantes = None
        
        if imagen_equipo == "":
            imagen_equipo == None
        
        if ficha_tecnica == "":
            ficha_tecnica == None

        id_usuario_bytes = binascii.unhexlify(id_usuario) #El id_usuario de hexadecimal a binario
        id_subcliente_bytes = binascii.unhexlify(id_subcliente) #El id_subcliente de hexadecimal a binario

        new_activo = Activo(id_activo,id_qr,id_primario,id_secundario,id_usuario_bytes,ubicacion,tipo_de_equipo,fabricante,modelo,num_serie,datos_relevantes,imagen_equipo,id_subcliente_bytes,ficha_tecnica)
        db.session.add(new_activo)
        db.session.commit()
        return jsonify({"message": "Activo creado correctamente", "status" : 200})

    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    

def listar_activos():
    try:
        activos = db.session.query(Activo).all()
        if not activos:
            return jsonify({"message" : "No se encontraron activos" , "status" : 404}) , 404
        else:
            toactivos = [activo.getDatos() for activo in activos]
            return jsonify(toactivos)

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def activos_de_subcliente(id_subcliente): # Listar los activos de un subcliente
    try:
        lista = []
        id_subcliente_bytes = binascii.unhexlify(id_subcliente) #el id hexadecimal que se pasa por la url lo convierto a binario

        activos = db.session.query(Activo.id_activo,Activo.id_primario,Activo.id_secundario,Activo.tipo_de_equipo,Activo.fabricante, Activo.modelo, Activo.num_serie, Activo.ubicacion, Activo.imagen_equipo).filter_by(id_subcliente=id_subcliente_bytes, estado = 1).all()
        

        if not activos:
            return jsonify({"message" : "No se encontraron activos" , "status" : 404}) , 404
        else:
            for activo in activos:
                datos = {"id_primario" : activo.id_primario, "id_secundario" : activo.id_secundario, "tipo_de_equipo": activo.tipo_de_equipo,"fabricante" : activo.fabricante, "modelo" : activo.modelo, "num_serie" : activo.num_serie, "ubicacion" : activo.ubicacion, "imagen" : activo.imagen_equipo}
                lista.append(datos)

            return jsonify(lista)
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def editar_activo(id_activo):
    try:
        id_activo_bytes = binascii.unhexlify(id_activo)
        activo = Activo.query.get(id_activo_bytes)

        if not activo:
            return jsonify({"message" : "Activo no encontrado", "status" : 404}) , 404
        
        else:
            activo.id_primario = request.json["id_primario"]
            activo.id_secundario = request.json["id_secundario"]
            activo.ubicacion = request.json["ubicacion"]
            activo.tipo_de_equipo = request.json["tipo_de_equipo"]
            activo.fabricante = request.json["fabricante"]
            activo.modelo = request.json["modelo"]
            activo.num_serie = request.json["num_serie"]
            activo.datos_relevantes = request.json["datos_relevantes"]
            #Pendiente de poder actualizar imagen y ficha tecnica

            db.session.commit()
            return jsonify({"message" : "Activo actualizado exitosamente", "status" : 200}) , 200
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    


def eliminar_activo(id_activo):
    try:
        id_activo_bytes = binascii.unhexlify(id_activo)
        activo = Activo.query.get(id_activo_bytes)

        if not activo:
            return jsonify({"message" : "Activo no encontrado", "status" : 404}) , 404

        else:
            activo.estado = 0
            db.session.commit()
            return jsonify({"message" : "Activo eliminado", "status" : 200})
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
    
def restaurar_activo(id_activo):
    try:
        id_activo_bytes = binascii.unhexlify(id_activo)
        activo = Activo.query.get(id_activo_bytes)

        if not activo:
            return jsonify({"message" : "Activo no encontrado", "status" : 404}) , 404
        
        else:
            activo.estado = 1
            db.session.commit()
            return jsonify({"message" : "Activo restaurado", "status" : 200})
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
