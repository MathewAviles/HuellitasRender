from flask import render_template, redirect, request, url_for, session, flash
from database import app,db
from mascotas.models import Mascota,Sexo


@app.route('/mascotas')
def mascotas_index():
    return render_template('mascotas/indexm.html')


@app.route('/crear_mascota', methods=['GET', 'POST'])
def crear_mascota():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']
        raza = request.form['raza']
        sexo_id = request.form['sexo_id']
        descripcion = request.form['descripcion']
        fecha_desaparicion = request.form['fecha_desaparicion']
        lugar_desaparicion = request.form['lugar_desaparicion']
        contacto = request.form['contacto']


        # Crear una nueva mascota
        nueva_mascota = Mascota(nombre=nombre, edad=edad, raza=raza, sexo_id=sexo_id, 
                                descripcion=descripcion, fecha_desaparicion=fecha_desaparicion, 
                                lugar_desaparicion=lugar_desaparicion, contacto=contacto, usuario_id=session['user_id'])
        db.session.add(nueva_mascota)
        db.session.commit()

        # Redireccionar a alguna página de éxito o a la página de inicio
        flash('¡Registro exitoso!', 'success')
        return redirect(url_for('home'))
    
    # Si el método es GET, mostrar el formulario de creación de mascotas
    sexos = Sexo.query.all()
    return render_template('mascotas/crear_mascota.html', sexos=sexos)
