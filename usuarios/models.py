from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash
from app import db

class Usuario(db.Model):
    __tablename__ = 'usuarios'

    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)

    # Relación de uno a muchos con la tabla Mascota
    mascotas = relationship('Mascota', backref='usuario', lazy=True)
    def set_password(self, password):
        self.password = generate_password_hash(password)


