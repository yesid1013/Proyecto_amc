from flask import jsonify, request
from models.Usuario import *
import uuid
import binascii
from werkzeug.security import generate_password_hash
def crear_usuario():
    try:
        id_usuario = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
        correo = request.json["correo"]
        contrasena = request.json["contrasena"]
        nombre = request.json["nombre"]
        direccion = request.json["direccion"]
        telefono = request.json["telefono"]
        
        usuario = Usuario.query.filter_by(correo=correo).first()

        if not usuario:
            contrasena_encriptada = generate_password_hash(contrasena,'pbkdf2:sha256',16)

            new_user = Usuario(id_usuario,correo,contrasena_encriptada,nombre,direccion,telefono)
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "Usuario creado correctamente", "status" : 200})
        else:
            return jsonify({"message": "El usuario ya se encuentra registrado", "status" : 400}) , 400
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

def listar_usuarios():
    try:
        lista = []
        users = db.session.query(Usuario).all()
        for user in users:
            id_hex = binascii.hexlify(user.id_usuario).decode() #Convierto el id binario que me da la base de datos a hexadecimal
            datos = {"id" : id_hex, "nombre" : user.nombre, "correo" : user.correo, "contraseña" : user.contrasena, "direccion" : user.direccion, "telefono" : user.telefono, "perfil" : user.perfil}
            lista.append(datos)
            
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"Ha ocurrido un error" : str(e)})

def buscar_usuario(id_usuario):
    try:
        id_bytes = binascii.unhexlify(id_usuario) # el id hexadecimal que se pasa por la url lo convierto a binario
        
        usuario = Usuario.query.get(id_bytes)
        if not usuario:
            return jsonify({"message" : "Usuario no encontrado"}) , 404
        else:
            return jsonify ({"correo" : usuario.correo, "nombre" : usuario.nombre, "direccion" : usuario.direccion, "telefono" : usuario.telefono})
    
    except Exception as e: 
        print (str(e))
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
        
    


        


