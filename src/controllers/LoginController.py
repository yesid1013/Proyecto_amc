from flask import jsonify, request
from models.Usuario import *
from flask_jwt_extended import create_access_token
import binascii
from werkzeug.security import check_password_hash
from utils.validation import validation_login
import bleach

def login():
    try:
        validation = validation_login(request.json) #Validacion de datos

        if validation is not True:
            return jsonify({"message": "Datos invalidos", "errors": validation, "status": 400}), 400
        
        correo = bleach.clean(request.json["correo"],tags=bleach.sanitizer.ALLOWED_TAGS) #Saneamiento de datos
        contrasena = bleach.clean(request.json["contrasena"],tags=bleach.sanitizer.ALLOWED_TAGS)  

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
        return jsonify({"message" : "Ha ocurrido un error inesperadoooo :", "error" : str(e) })
