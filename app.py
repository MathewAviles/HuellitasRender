from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

# Función para crear la aplicación Flask
def create_app():
    app = Flask(__name__)
    # Configuración de la base de datos SQLite
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mascotas.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    # Secret key para sesiones (cambiar por tu propia clave)
    app.secret_key = 'your_secret_key'
    return app

# Inicialización de la aplicación Flask
app = create_app()
# Inicialización de la extensión SQLAlchemy
db = SQLAlchemy(app)

# Importar las rutas desde el archivo routes.py
from mascotas.routes import mascotas_bp
from usuarios.routes import usuarios_bp

# Registrar las rutas en la aplicación
app.register_blueprint(mascotas_bp)
app.register_blueprint(usuarios_bp)

# Ruta principal home
@app.route('/')
def home():
    return render_template('home.html')

# Ejecución de la aplicación
if __name__ == "__main__":
    # Ejecutar las operaciones dentro del contexto de la aplicación
    with app.app_context():
        # Crear la base de datos si no existe
        db.create_all()
    app.run(debug=True)
