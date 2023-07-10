from flask import jsonify, request
from models.Usuario import *
import uuid

def crear_usuario():
    try:
        new_uuid = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
        id_usuario = new_uuid.hex()
        correo = request.json["correo"]
        contrasena = request.json["contrasena"]
        nombre = request.json["nombre"]
        direccion = request.json["direccion"]
        telefono = request.json["telefono"]
        
        usuario = Usuario.query.filter_by(correo=correo).first()

        if not usuario:
            new_user = Usuario(id_usuario,correo,contrasena,nombre,direccion,telefono)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Usuario creado correctamente", "status" : 200})
        else:
            return jsonify({"message": "El usuario ya se encuentra registrado", "status" : 400}) , 400
    
    except Exception as e:
        return jsonify({"Ha ocurrido un error" : str(e)})


