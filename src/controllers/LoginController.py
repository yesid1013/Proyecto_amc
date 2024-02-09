from flask import jsonify, request
from models.Usuario import *
from flask_jwt_extended import create_access_token
import binascii
from werkzeug.security import check_password_hash
from utils.validation import validation_login
import bleach
from google.oauth2 import id_token
from google.auth.transport import requests
from decouple import config
import uuid


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
                id_hex = binascii.hexlify(usuario.id_usuario).decode() #El id del usuario lo convierto a hexadecimal
                access_token = create_access_token(identity=id_hex)                
                return jsonify({"token" : access_token,"nombre" : usuario.nombre})
            else:
                return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 400}) , 400
        else:
            return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 400}) , 400
                                 
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e) })

def login_google():
    try:
        info_usuario = validar_token_acceso_google(request.json["token_google"])

        token = crear_usuario_de_google(info_usuario)

        return token
    
    except ValueError as e:
        return jsonify({"message" : "Token no válido", "error" : str(e) }) , 403
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e) })

def validar_token_acceso_google(token_google):
    try:
        # Verificar el token de acceso con las claves públicas de Google
        info_usuario = id_token.verify_oauth2_token(
            token_google,
            requests.Request(),
            audience= config('ID_CLIENT')
        )

        # Si el token es válido, devolver la información del usuario
        return info_usuario
    

    except ValueError as e:
        # El token no es válido
        raise ValueError("Token no válido")

def crear_usuario_de_google(info_usuario):
    try:
        correo = info_usuario["email"]
    
        usuario = Usuario.query.filter_by(correo=correo).first()

        if usuario: #Si existe el usuario le devuelvo un token con sus datos
            id_user_hex = binascii.hexlify(usuario.id_usuario).decode()
            access_token = create_access_token(identity=id_user_hex)                
            return jsonify({"token" : access_token,"nombre" : usuario.nombre}) , 200
        else: #Si no existe el usuario se registra en la bd y se e da el token
            id_usuario = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
            nombre = info_usuario["name"]
            direccion = None
            telefono = None

            new_user = Usuario(id_usuario,correo,None,nombre,direccion,telefono)
            db.session.add(new_user)
            db.session.commit()

            id_user_new_hex = binascii.hexlify(id_usuario).decode()
            access_token = create_access_token(identity=id_user_new_hex)

            return jsonify({"token" : access_token,"nombre" : nombre , "message" : "Usuario creado correctamente"}), 200
        
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado", "error" : str(e) })
