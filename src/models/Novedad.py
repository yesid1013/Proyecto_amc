from utils.db import db
from models import Activo

class Novedad(db.Model):
    __tablename__ = 'novedad'
    id_novedad = db.Column(db.BINARY(16), primary_key=True)
    id_activo = db.Column(db.BINARY(16), db.ForeignKey('activo.id_activo'), nullable=False)
    fecha = db.Column(db.TIMESTAMP)
    nombre_reporta = db.Column(db.String(100),nullable=False)
    nombre_empresa = db.Column(db.String(100),nullable=False)
    cargo = db.Column(db.String(50),nullable=False)
    descripcion_reporte = db.Column(db.String(100),nullable=False)
    imagenes = db.Column(db.String(255))
    estado = db.Column(db.SmallInteger,nullable = False, default = 1)

    activo = db.relationship('Activo', back_populates="novedad", uselist=False, single_parent=True)


    def __init__(self,id_novedad,id_activo,nombre_reporta,nombre_empresa,cargo,descripcion_reporte,imagenes):
        self.id_novedad = id_novedad
        self.id_activo = id_activo
        self.nombre_reporta = nombre_reporta
        self.nombre_empresa = nombre_empresa
        self.cargo = cargo
        self.descripcion_reporte = descripcion_reporte
        self.imagenes = imagenes
        self.estado = 1
    
    def getDatos (self):
        return {
            "id_novedad" : self.id_novedad,
            "id_activo" : self.id_activo,
            "fecha" : self.fecha,
            "nombre_reporta" : self.nombre_reporta,
            "nombre_empresa" : self.nombre_empresa,
            "cargo" : self.cargo,
            "descripcion_reporte" : self.descripcion_reporte,
            "imagenes" : self.imagenes
        }



