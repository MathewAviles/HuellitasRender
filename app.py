from database import app, db
from mascotas.routes import *
from usuarios.routes import *


# Crear las tablas en la base de datos
with app.app_context():
    db.create_all()



# Ejecutar la aplicación
if __name__ == "__main__":
    app.run(debug=True)
