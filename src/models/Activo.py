from utils.db import db
from models import Novedad
from models import Servicio
from models import Subcliente
from models import Codigos_qr
from models import Usuario
from models import Permisos
from sqlalchemy.sql import func
import binascii

class Activo(db.Model):
    __tablename__ = 'activo'
    id_activo = db.Column(db.BINARY(16), primary_key=True)
    id_qr = db.Column(db.Integer, db.ForeignKey('codigos_qr.id_qr'), nullable=False,unique= True)
    id_primario = db.Column(db.String(6),nullable = False,unique= True)
    id_secundario = db.Column(db.String(7),nullable = True,unique= True)
    id_usuario = db.Column(db.BINARY(16), db.ForeignKey('usuario.id_usuario'), nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP(timezone=True),nullable=False,server_default=func.now())
    ubicacion = db.Column(db.String(45),nullable = False)
    tipo_de_equipo = db.Column(db.String(55),nullable = False)
    fabricante = db.Column(db.String(45),nullable = False)
    modelo = db.Column(db.String(45))
    num_serie = db.Column(db.String(45))
    datos_relevantes = db.Column(db.String(45))
    imagen_equipo = db.Column(db.String(255),nullable = True)
    id_subcliente = db.Column(db.BINARY(16), db.ForeignKey('subcliente.id_subcliente'), nullable=False)
    ficha_tecnica = db.Column(db.String(255),nullable = True)
    estado = db.Column(db.SmallInteger,nullable = False, default = 1)

    subcliente = db.relationship('Subcliente', back_populates="activo", uselist=False, single_parent=True)
    codigos_qr = db.relationship('Codigos_qr', back_populates="activo", single_parent=True, cascade="all,delete-orphan")
    usuario = db.relationship('Usuario', back_populates="activo", uselist=False, single_parent=True)


    novedad = db.relationship('Novedad', back_populates='activo', cascade="all,delete-orphan")
    servicio = db.relationship('Servicio', back_populates='activo', cascade="all,delete-orphan")
    permisos = db.relationship('Permisos', back_populates='activo',cascade="all,delete-orphan")

    def __init__(self,id_activo,id_qr,id_primario,id_secundario,id_usuario,ubicacion,tipo_de_equipo,fabricante,modelo,num_serie,datos_relevantes,imagen_equipo,id_subcliente,ficha_tecnica):
        self.id_activo = id_activo
        self.id_qr = id_qr
        self.id_primario = id_primario
        self.id_secundario = id_secundario
        self.id_usuario = id_usuario
        self.ubicacion = ubicacion
        self.tipo_de_equipo = tipo_de_equipo
        self.fabricante = fabricante
        self.modelo = modelo
        self.num_serie = num_serie
        self.datos_relevantes = datos_relevantes
        self.imagen_equipo = imagen_equipo
        self.id_subcliente = id_subcliente
        self.ficha_tecnica = ficha_tecnica
        self.estado = 1
    
    def getDatos(self):
        return {
            "id_activo" : binascii.hexlify(self.id_activo).decode() ,
            "id_qr" : self.id_qr,
            "id_primario" : self.id_primario,
            "id_secundario" : self.id_secundario,
            "id_usuario" : binascii.hexlify(self.id_usuario).decode() ,
            "fecha_registro" : self.fecha_registro,
            "ubicacion" : self.ubicacion,
            "tipo_de_equipo" : self.tipo_de_equipo,
            "fabricante" : self.fabricante,
            "modelo" : self.modelo,
            "num_serie" : self.num_serie,
            "datos_relevantes" : self.datos_relevantes,
            "imagen_equipo" : self.imagen_equipo,
            "id_subcliente" : binascii.hexlify(self.id_subcliente).decode() ,
            "ficha_tecnica" : self.ficha_tecnica

        }

        
        
    

