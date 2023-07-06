from utils.db import db
from sqlalchemy.sql import func

class Usuario(db.Model):
    __tablename__ = 'usuarios'
    id_usuario = db.Column(db.String(36), primary_key=True)
    correo = db.Column(db.String(50), unique= True, nullable = False)
    contrasena = db.Column(db.String(50), nullable = True)
    nombre = db.Column(db.String(100), nullable = False)
    direccion = db.Column(db.String(100), nullable = True)
    telefono = db.Column(db.String(10), nullable = True)
    perfil = db.Column(db.Integer,nullable = False, default = 1)

    def __init__(self,id_usuario,correo,contrasena,nombre,direccion,telefono):
        self.id_usuario = id_usuario
        self.correo = correo
        self.contrasena = contrasena
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.perfil = 1
    
    def getDatos (self):
        return {
            "id_usuario" : self.id_usuario,
            "correo" : self.correo,
            "contrasena" : self.contrasena,
            "nombre" : self.nombre,
            "direccion" : self.direccion,
            "telefono" : self.telefono,
            "perfil" : self.perfil
        }
