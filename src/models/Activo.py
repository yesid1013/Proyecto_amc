from utils.db import db

class Activo(db.Model):
    __tablename__ = 'activo'
    id_activo = db.Column(db.Binary(16), primary_key=True)
    id_qr = db.Column(db.Integer, db.ForeignKey('codigos_qr.id_qr'), nullable=True)
    id_primario = db.Column(db.String(6),nullable = True)
    id_secundario = db.Column(db.String(7),nullable = True)
    id_usuario = db.Column(db.Binary(16), db.ForeignKey('usuario.id_usuario'), nullable=False)
    fecha_registro = db.Column(db.TIMESTAMP)
    ubicacion = db.Column(db.String(45),nullable = False)
    tipo_de_equipo = db.Column(db.String(55),nullable = False)
    fabricante = db.Column(db.String(45),nullable = False)
    modelo = db.Column(db.String(45))
    num_serie = db.Column(db.String(45))
    datos_relevantes = db.Column(db.String(45))
    imagen_equipo = db.Column(db.String(255),nullable = True)
    id_subcliente = db.Column(db.Binary(16), db.ForeignKey('subcliente.id_subcliente'), nullable=False)
    ficha_tecnica = db.Column(db.String(255),nullable = True)

    novedad = db.relationship('Novedad', backref='activo', lazy=True)
    servicio = db.relationship('Servicio', backref='activo', lazy=True)

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
    
    def getDatos(self):
        return {
            "id_activo" : self.id_activo,
            "id_qr" : self.id_qr,
            "id_primario" : self.id_primario,
            "id_secundario" : self.id_secundario,
            "id_usuario" : self.id_usuario,
            "fecha_registro" : self.fecha_registro,
            "ubicacion" : self.ubicacion,
            "tipo_de_equipo" : self.tipo_de_equipo,
            "fabricante" : self.fabricante,
            "modelo" : self.modelo,
            "num_serie" : self.num_serie,
            "datos_relevantes" : self.datos_relevantes,
            "imagen_equipo" : self.imagen_equipo,
            "id_subcliente" : self.id_subcliente,
            "ficha_tecnica" : self.ficha_tecnica

        }

        
        
    

