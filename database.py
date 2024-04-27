from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Crear la aplicación Flask
app = Flask(__name__)
# Configurar la base de datos SQLite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mascotas.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://huellitas_cig9_user:ItYizwBucx0IGNLG2DVPlRXW2PTQwGPB@dpg-comjq34f7o1s73f5qv3g-a.oregon-postgres.render.com/huellitas_cig9'

#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Clave secreta para las sesiones (cambia esto por tu propia clave)
app.secret_key = 'your_secret_key'

# Inicializar la extensión SQLAlchemy
db = SQLAlchemy(app)
