from utils.db import db
import binascii
from models import Subcliente

class Empresa (db.Model):
    __tablename__ = 'empresa'
    id_empresa = db.Column(db.BINARY(16), primary_key=True)
    nombre = db.Column(db.String(50),nullable=False)
    telefono = db.Column(db.String(10),nullable=False)
    direccion = db.Column(db.String(50),nullable=False)

    subcliente = db.relationship("Subcliente", back_populates="empresa",cascade="all,delete-orphan")

    def __init__(self,id_empresa,nombre,telefono,direccion):
        self.id_empresa = id_empresa
        self.nombre = nombre
        self.telefono = telefono
        self.direccion = direccion
    

    def getDatos (self) :
        return {
            "id_empresa" : binascii.hexlify(self.id_empresa).decode(), 
            "nombre" : self.nombre, 
            "telefono" : self.telefono, 
            "direccion" : self.direccion}