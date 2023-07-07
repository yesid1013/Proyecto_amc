from utils.db import db

class Subcliente(db.Model):
    __tablename__ = 'subcliente'
    id_subcliente = db.Column(db.Binary(16), primary_key=True)
    nombre = db.Column(db.String(100),nullable=False)
    contacto = db.Column(db.String(50))
    direccion = db.Column(db.String(100),nullable=False)

    activo = db.relationship('Activo', backref='subcliente', lazy=True)

    def __init__ (self,id_subcliente,nombre,contacto,direccion):
        self.id_subcliente = id_subcliente
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
