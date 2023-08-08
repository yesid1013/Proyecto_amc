from utils.db import db
from models import Activo

class Codigos_qr (db.Model):
    __tablename__ = 'codigos_qr'
    id_qr = db.Column(db.Integer, primary_key=True, nullable=False)
    google_drive_id = db.Column(db.String(33),nullable=False)
    web_view_link = db.Column(db.String(83),nullable=False)

    activo = db.relationship('Activo',uselist=False,
    back_populates="codigos_qr",cascade="all, delete-orphan",single_parent=True)


    def __init__ (self,google_drive_id,web_view_link):
        self.google_drive_id = google_drive_id
        self.web_view_link = web_view_link
    
    def getDatos(self):
        return {
            "id_qr" : self.id_qr,
            "google_drive_id" : self.google_drive_id
        }