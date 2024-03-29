from utils.db import db
from models import Activo
from models import Empresa

class Subcliente(db.Model):
    __tablename__ = 'subcliente'
    id_subcliente = db.Column(db.BINARY(16), primary_key=True)
    id_empresa = db.Column(db.Integer, db.ForeignKey('empresa.id_empresa'),nullable=False)
    nombre = db.Column(db.String(100),nullable=False)
    contacto = db.Column(db.String(50))
    direccion = db.Column(db.String(100),nullable=False)
    
    activo = db.relationship("Activo", back_populates="subcliente",cascade="all, delete-orphan")
    empresa = db.relationship('Empresa', back_populates="subcliente", uselist=False, single_parent=True)


    def __init__ (self,id_subcliente,id_empresa,nombre,contacto,direccion):
        self.id_subcliente = id_subcliente
        self.id_empresa = id_empresa
        self.nombre = nombre
        self.contacto = contacto
        self.direccion = direccion
    
    def getDatos(self):
        return {
            "id_subcliente" : self.id_subcliente,
            "nombre" : self.nombre,
            "contacto" : self.contacto,
            "direccion" : self.direccion
        }
