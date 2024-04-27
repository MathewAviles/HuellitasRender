from flask import render_template, redirect, request, url_for, session,flash
from database import app, db
from werkzeug.security import check_password_hash
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
        flash('¡Registro exitoso! Por favor inicia sesión.', 'success')
        return redirect(url_for('home'))
    
    # Si el método es GET, mostrar el formulario de creación de usuarios
    return render_template('usuarios/crear_usuario.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Obtener datos del formulario
        email = request.form['email']
        password = request.form['password']

        # Buscar al usuario en la base de datos
        usuario = Usuario.query.filter_by(email=email).first()

        # Verificar la contraseña
        if usuario and check_password_hash(usuario.password, password):
            # Iniciar sesión
            session['user_id'] = usuario.id
            flash('¡Gracias por iniciar sesión.', 'success')
            return redirect(url_for('home'))

        # Si la verificación falla, mostrar un mensaje de error
        flash('Credenciales incorrectas. Por favor, inténtalo de nuevo.', 'error')
        

    # Si el método es GET, mostrar el formulario de inicio de sesión
    return render_template('usuarios/login.html')


@app.route('/logout')
def logout():
    # Eliminar user_id de la sesión
    session.pop('user_id', None)

    # Redirigir al usuario a la página de inicio
    flash('Cierre de sesion exitoso!', 'success')
    return redirect(url_for('home'))
    