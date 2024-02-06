from utils.db import db
from models import Activo

class Codigos_qr (db.Model):
    __tablename__ = 'codigos_qr'
    id_qr = db.Column(db.Integer, primary_key=True, nullable=False)
    ruta_imagen = db.Column(db.String(255),nullable=False)


    activo = db.relationship('Activo',uselist=False,
    back_populates="codigos_qr",cascade="all, delete-orphan",single_parent=True)


    def __init__ (self,ruta_imagen):
        self.ruta_imagen = ruta_imagen
    
    def getDatos(self):
        return {
            "id_qr" : self.id_qr,
            "google_drive_id" : self.google_drive_id
        }