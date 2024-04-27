from app import db,app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Mascota(db.Model):
     __tablename__ = 'mascotas'

     id = db.Column(db.Integer, primary_key=True)
     nombre = db.Column(db.String(100), nullable=False)
     tipo = db.Column(db.String(50), nullable=False)

     # Clave foránea que apunta al id del usuario
     usuario_id = db.Column(db.Integer, ForeignKey('usuarios.id'), nullable=False)

     # Crear las tablas en la base de datos
with app.app_context():
     db.create_all()