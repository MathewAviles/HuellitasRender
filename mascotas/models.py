from app import db,app
from sqlalchemy import ForeignKey

class Mascota(db.Model):
     __tablename__ = 'mascotas'

     id = db.Column(db.Integer, primary_key=True)
     nombre = db.Column(db.String(100), nullable=False)
     tipo = db.Column(db.String(50), nullable=False)

     # Clave foránea que apunta al id del usuario
     usuario_id = db.Column(db.Integer, ForeignKey('usuarios.id'), nullable=False)

