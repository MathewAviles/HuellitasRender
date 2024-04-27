from app import db,app
from sqlalchemy import ForeignKey

class Mascota(db.Model):
     __tablename__ = 'mascotas'

     id = db.Column(db.Integer, primary_key=True)
     nombre = db.Column(db.String(100), nullable=False)
     edad = db.Column(db.Integer, nullable=False)
     raza = db.Column(db.String(100), nullable=False)
     sexo_id = db.Column(db.Integer, db.ForeignKey('sexos.id'), nullable=False)
     descripcion = db.Column(db.String(500), nullable=False)
     fecha_desaparicion = db.Column(db.Date, nullable=False)
     lugar_desaparicion = db.Column(db.String(200), nullable=False)
     contacto = db.Column(db.String(20), nullable=False)

     # Clave foránea que apunta al id del usuario
     usuario_id = db.Column(db.Integer, ForeignKey('usuarios.id'), nullable=False)
     sexo = db.relationship('Sexo', backref=db.backref('mascotas', lazy=True))


class Sexo(db.Model):
    __tablename__ = 'sexos'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)

