from flask import jsonify, request
from models.Usuario import *
import uuid
import binascii
from werkzeug.security import generate_password_hash
import bleach
def crear_usuario():
    try:
        id_usuario = uuid.uuid4().bytes #Generar una nueva UUID y convertirla a formato binario
        correo = bleach.clean(request.json["correo"],tags=bleach.sanitizer.ALLOWED_TAGS)
        contrasena = bleach.clean(request.json["contrasena"],tags=bleach.sanitizer.ALLOWED_TAGS)
        nombre = bleach.clean(request.json["nombre"],tags=bleach.sanitizer.ALLOWED_TAGS)
        direccion = bleach.clean(request.json["direccion"],tags=bleach.sanitizer.ALLOWED_TAGS)
        telefono = bleach.clean(request.json["telefono"],tags=bleach.sanitizer.ALLOWED_TAGS)
        
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

def listar_usuarios(id_usuario):
    try:
        lista = []
        id_usuario_bytes = binascii.unhexlify(id_usuario)
        users = db.session.query(Usuario).filter(Usuario.id_usuario != id_usuario_bytes)
        for user in users:
            id_hex = binascii.hexlify(user.id_usuario).decode() #Convierto el id binario que me da la base de datos a hexadecimal
            datos = {"id_usuario" : id_hex, "nombre" : user.nombre, "correo" : user.correo, "direccion" : user.direccion, "telefono" : user.telefono, "perfil" : user.perfil}
            lista.append(datos)
            
        return jsonify(lista)
    
    except Exception as e:
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})

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

def obtener_perfil_de_usuario(id_usuario):
    try:
        id_usuario_bytes = binascii.unhexlify(id_usuario)

        usuario = db.session.query(Usuario.perfil).filter_by(id_usuario = id_usuario_bytes).first()
        if usuario:
            print(usuario.perfil)
            return usuario.perfil
        else :
            return jsonify({"message" : "Usuario no encontrado"}) , 404
    
    except Exception as e: 
        print (str(e))
        return jsonify({"message" : "Ha ocurrido un error inesperado :", "error" : str(e)})
        
    


        


