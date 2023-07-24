from utils.db import db
from models import Servicio
from models import Activo
from werkzeug.security import check_password_hash

class Usuario(db.Model):
    __tablename__ = 'usuario'
    id_usuario = db.Column(db.BINARY(16), primary_key=True)
    correo = db.Column(db.String(50), unique= True, nullable = False)
    contrasena = db.Column(db.String(105), nullable = True)
    nombre = db.Column(db.String(100), nullable = False)
    direccion = db.Column(db.String(100), nullable = True)
    telefono = db.Column(db.String(10), nullable = True)
    perfil = db.Column(db.SmallInteger,nullable = False, default = 1)

    servicio = db.relationship('Servicio', back_populates='usuario',cascade="all, delete-orphan" )
    activo = db.relationship('Activo', back_populates='usuario', cascade="all,delete-orphan")

    def __init__(self,id_usuario,correo,contrasena,nombre,direccion,telefono):
        self.id_usuario = id_usuario
        self.correo = correo
        self.contrasena = contrasena
        self.nombre = nombre
        self.direccion = direccion
        self.telefono = telefono
        self.perfil = 1
    
    def verif_contrasena(self,contrasena):
        return check_password_hash(self.contrasena,contrasena)

    
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
