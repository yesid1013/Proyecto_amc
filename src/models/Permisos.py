from utils.db import db
from models import Activo

class Permisos(db.Model):
    __tablename__ = 'permisos'
    id_permiso = db.Column(db.BINARY(16), primary_key=True)
    id_usuario = db.Column(db.BINARY(16), db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_activo = db.Column(db.BINARY(16), db.ForeignKey('activo.id_activo'), nullable=False)
    ver_informacion_basica = db.Column(db.SmallInteger,default = 0)
    ver_historial_servicios = db.Column(db.SmallInteger,default = 0)
    ver_novedades = db.Column(db.SmallInteger,default = 0)
    registrar_servicio = db.Column(db.SmallInteger,default = 0)
    registrar_novedad = db.Column(db.SmallInteger,default = 0)

    activo = db.relationship('Activo', back_populates="permisos", uselist=False, single_parent=True)
    usuario = db.relationship('Usuario', back_populates="permisos", uselist=False, single_parent=True)
