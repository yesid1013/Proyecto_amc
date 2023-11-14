from utils.db import db
from models import Activo
import binascii


class Permisos(db.Model):
    __tablename__ = 'permisos'
    id_permiso = db.Column(db.BINARY(16), primary_key=True)
    id_usuario = db.Column(db.BINARY(16), db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_activo = db.Column(db.BINARY(16), db.ForeignKey('activo.id_activo'), nullable=False)
    ver_informacion_basica = db.Column(db.SmallInteger,default = 0)
    ver_historial_servicios = db.Column(db.SmallInteger,default = 0)
    ver_novedades = db.Column(db.SmallInteger,default = 0)
    ver_costo_servicio = db.Column(db.SmallInteger,default = 0)
    registrar_servicio = db.Column(db.SmallInteger,default = 0)
    registrar_novedad = db.Column(db.SmallInteger,default = 0)

    activo = db.relationship('Activo', back_populates="permisos", uselist=False, single_parent=True)
    usuario = db.relationship('Usuario', back_populates="permisos", uselist=False, single_parent=True)

    def __init__(self,id_permiso,id_usuario,id_activo,ver_informacion_basica,ver_historial_servicios,ver_novedades,registrar_servicio,registrar_novedad):
        self.id_permiso = id_permiso
        self.id_usuario = id_usuario
        self.id_activo = id_activo
        self.ver_informacion_basica = ver_informacion_basica
        self.ver_historial_servicios = ver_historial_servicios
        self.ver_novedades = ver_novedades
        self.registrar_servicio = registrar_servicio
        self.registrar_novedad = registrar_novedad
    
    def getDatos (self):
        return {
            "id_permiso" : binascii.hexlify(self.id_permiso).decode() ,
            "id_activo" : binascii.hexlify(self.id_activo).decode() ,
            "id_usuario" : binascii.hexlify(self.id_usuario).decode(),
            "ver_informacion_basica" : self.ver_informacion_basica,
            "ver_historial_servicios" : self.ver_historial_servicios,
            "ver_novedades" : self.ver_novedades,
            "registrar_servicio" : self.registrar_servicio,
            "registrar_novedad" : self.registrar_novedad,
        }
