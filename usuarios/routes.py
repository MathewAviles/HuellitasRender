from flask import render_template, redirect, request, url_for
from database import app, db
from usuarios.models import Usuario

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/usuarios')
def usuarios_index():
    return render_template('usuarios/indexu.html')

@app.route('/crear_usuario', methods=['GET', 'POST'])
def crear_usuario():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        email = request.form['email']
        password = request.form['password']

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(nombre=nombre, email=email)
        nuevo_usuario.set_password(password)
        db.session.add(nuevo_usuario)
        db.session.commit()

        # Redireccionar a alguna página de éxito o a la página de inicio
        return redirect(url_for('home'))
    
    # Si el método es GET, mostrar el formulario de creación de usuarios
    return render_template('usuarios/crear_usuario.html')