from utils.db import db

class Costo_servicio(db.Model):
    __tablename__ = 'costo_servicio'
    id_costo_servicio = db.Column(db.BINARY(16), primary_key=True)
    id_servicio = db.Column(db.BINARY(16), db.ForeignKey('servicio.id_servicio'), nullable=False)
    costo = db.Column(db.Integer, nullable=False)
    documento_cotizacion = db.Column(db.String(255))

    def __init__(self,id_costo_servicio,id_servicio,costo,documento_cotizacion):
        self.id_costo_servicio = id_costo_servicio
        self.id_servicio = id_servicio
        self.costo = costo
        self.documento_cotizacion = documento_cotizacion
    
    def getDatos(self):
        return {
            "id_costo_servicio" : self.id_costo_servicio,
            "id_servicio" : self.id_servicio,
            "costo" : self.costo,
            "documento_cotizacion" : self.documento_cotizacion
        }