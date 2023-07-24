from utils.db import db
from models import Servicio

class Tipo_servicio (db.Model):
    __tablename__ = 'tipo_servicio'
    id_tipo_servicio = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(45))

    servicio = db.relationship('Servicio', back_populates='tipo_servicio', cascade="all, delete-orphan")

    def __init__(self,tipo):
        self.tipo = tipo
    
    def getDatos(self):
        return {
            "id_tipo_servicio" : self.id_tipo_servicio,
            "tipo" : self.tipo
        }
