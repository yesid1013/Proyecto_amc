from utils.db import db

class Codigos_qr(db.Model):
    __tablename__ = 'codigo'
    id_qr = db.Column(db.Integer, primary_key=True)
    url_destino = db.Column(db.String(255),nullable=False)
    google_drive_id = db.Column(db.String(255),nullable=False)

    activo = db.relationship('Activo', backref='codigos_qr', lazy=True)

    def __init__(self,url_destino,google_drive_id):
        self.url_destino = url_destino
        self.google_drive_id = google_drive_id
    
    def getDatos(self):
        return {
            "id_qr" : self.id_qr,
            "url_destino" : self.url_destino,
            "google_drive_id" : self.google_drive_id
        }