from flask import jsonify, request
from models.Usuario import *
from flask_jwt_extended import create_access_token

def login():
    try:
        correo = request.json["correo"]
        contrasena = request.json["contrasena"]

        usuario = Usuario.query.filter_by(correo=correo,contrasena=contrasena).first()
        if not usuario:
            return jsonify({"message" : "Correo o contraseña incorrecta" , "status" : 404}) , 404
        
        else:
            access_token = create_access_token(identity=usuario.id_usuario)                
            return jsonify({"token" : access_token, "user_id" : usuario.id_usuario, "nombre" : usuario.nombre})
                                 
                
                

    except Exception as e:
        return jsonify({"Ha ocurrido un error " : str(e) })
