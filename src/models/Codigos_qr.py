from utils.db import db
from models import Activo

class Codigos_qr (db.Model):
    __tablename__ = 'codigos_qr'
    id_qr = db.Column(db.Integer, primary_key=True, nullable=False)
    url_destino = db.Column(db.String(255),nullable=False)
    google_drive_id = db.Column(db.String(255),nullable=False)

    activo = db.relationship('Activo',uselist=False,
    back_populates="codigos_qr",cascade="all, delete-orphan",single_parent=True)


    def __init__ (self,url_destino,google_drive_id):
        self.url_destino = url_destino
        self.google_drive_id = google_drive_id
    
    def getDatos(self):
        return {
            "id_qr" : self.id_qr,
            "url_destino" : self.url_destino,
            "google_drive_id" : self.google_drive_id
        }