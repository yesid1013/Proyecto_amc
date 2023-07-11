from flask import jsonify, request
from models.Usuario import *
from flask_jwt_extended import create_access_token
import binascii
from werkzeug.security import check_password_hash

def login():
    try:
        correo = request.json["correo"]
        contrasena = request.json["contrasena"]

        usuario = Usuario.query.filter_by(correo=correo).first()
        if usuario:
            if usuario.verif_contrasena(contrasena):
                id_hex = binascii.hexlify(usuario.id_usuario).decode()
                access_token = create_access_token(identity=id_hex)                
                return jsonify({"token" : access_token, "user_id" : id_hex, "nombre" : usuario.nombre})
            else:
                return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 401}) , 401
        else:
            return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 401}) , 401
                                 
                 
                

    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e) })
