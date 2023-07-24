from utils.db import db
from models.Costo_servicio import Costo_servicio
from models import Activo
from models import Usuario
from models import Tipo_servicio

class Servicio(db.Model):
    __tablename__ = 'servicio'
    id_servicio = db.Column(db.BINARY(16), primary_key=True)
    id_activo = db.Column(db.BINARY(16), db.ForeignKey('activo.id_activo'), nullable=False)
    fecha_ejecucion = db.Column(db.DateTime,nullable = False)
    id_usuario = db.Column(db.BINARY(16), db.ForeignKey('usuario.id_usuario'), nullable=False)
    id_tipo_servicio = db.Column(db.Integer, db.ForeignKey('tipo_servicio.id_tipo_servicio'), nullable=False)
    descripcion = db.Column(db.String(60), nullable = False)
    observaciones = db.Column(db.String(60))
    imagenes = db.Column(db.String(255))
    informe = db.Column(db.String(255))
    estado = db.Column(db.SmallInteger,nullable = False, default = 1)

    activo = db.relationship('Activo', back_populates="servicio", uselist=False, single_parent=True)
    usuario = db.relationship('Usuario', back_populates="servicio", uselist=False, single_parent=True)
    tipo_servicio = db.relationship('Tipo_servicio', back_populates="servicio", uselist=False, single_parent=True)

    costo_servicio = db.relationship('Costo_servicio', back_populates='servicio',cascade="all,delete-orphan")

    def __init__ (self,id_servicio,id_activo,fecha_ejecucion,id_usuario,id_tipo_servicio,descripcion,observaciones,imagenes,informe):
        self.id_servicio = id_servicio
        self.id_activo = id_activo
        self.fecha_ejecucion = fecha_ejecucion
        self.id_usuario = id_usuario
        self.id_tipo_servicio = id_tipo_servicio
        self.descripcion = descripcion
        self.observaciones = observaciones
        self.imagenes = imagenes
        self.informe = informe
        self.estado = 1

    def getDatos(self):
        return {
            "id_servicio" : self.id_servicio,
            "id_activo" : self.id_activo,
            "fecha_ejecucion" : self.fecha_ejecucion,
            "id_usuario" : self.id_usuario,
            "id_tipo_servicio" : self.id_tipo_servicio,
            "descripcion" : self.descripcion,
            "observaciones" : self.observaciones,
            "imagenes" : self.imagenes,
            "informe" : self.informe
        }
 