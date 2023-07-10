from utils.db import db

class Tipo_servicio (db.Model):
    __tablename__ = 'tipo_servicio'
    id_tipo_servicio = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(45))

    servicio = db.relationship('Servicio', backref='tipo_servicio', lazy=True)

    def __init__(self,tipo):
        self.tipo = tipo
    
    def getDatos(self):
        return {
            "id_tipo_servicio" : self.id_tipo_servicio,
            "tipo" : self.tipo
        }
