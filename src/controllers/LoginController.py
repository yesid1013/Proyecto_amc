from flask import jsonify, request
from models.Usuario import *
from flask_jwt_extended import create_access_token
import binascii

def login():
    try:
        correo = request.json["correo"]
        contrasena = request.json["contrasena"]

        usuario = Usuario.query.filter_by(correo=correo,contrasena=contrasena).first()
        if not usuario:
            return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 404}) , 404
        
        else:
            id_hex = binascii.hexlify(usuario.id_usuario).decode()
            access_token = create_access_token(identity=id_hex)                
            return jsonify({"token" : access_token, "user_id" : id_hex, "nombre" : usuario.nombre})
                                 
                 
                

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e) })
