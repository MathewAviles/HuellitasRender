from flask import render_template, redirect, request, url_for, session, flash
from database import app,db
from mascotas.models import Mascota,Sexo,ImagenMascota
from usuarios.models import Usuario
from zipfile import ZipFile
import os 


@app.route('/mascotas')
def mascotas_index():
    return render_template('mascotas/indexm.html')


@app.route('/reconocimiento_mascotas')
def reconocimiento_mascotas():
    return render_template('mascotas/reconocimientomascotas.html')


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


@app.route('/reconocimiento', methods=['GET', 'POST'])
def reconocimiento():
    if request.method == 'POST':
        # Obtener datos del formulario
        nombre_mascota = request.form['nombre_mascota']
        imagenes = request.files.getlist('imagen')

        for imagen in imagenes:
            # Leer la imagen en formato binario
            imagen_binaria = imagen.read()

            # Crear una nueva imagen de mascota
            nueva_imagen = ImagenMascota(nombre_mascota=nombre_mascota, imagen=imagen_binaria)
            db.session.add(nueva_imagen)

        db.session.commit()

        # Redireccionar a alguna página de éxito o a la página de inicio
        flash('¡Imágenes subidas con éxito!', 'success')
        return redirect(url_for('home'))
    
    # Si el método es GET, mostrar el formulario de subida de imágenes
    mascotas = Mascota.query.filter_by(usuario_id=session['user_id']).all()
    return render_template('mascotas/reconocimiento.html', mascotas=mascotas)


@app.route('/admin_mascotas')
def admin_mascotas():
    # Verificar si el usuario es un administrador
    usuario_actual = Usuario.query.get(session['user_id'])
    if usuario_actual.rol != 'admin':
        flash('¡Acceso denegado!', 'error')
        return redirect(url_for('home'))

    # Si el usuario es un administrador, mostrar todas las mascotas
    mascotas = Mascota.query.all()
    return render_template('mascotas/admin_mascotas.html', mascotas=mascotas)


@app.route('/descargar_imagenes/<string:nombre_mascota>')
def descargar_imagenes(nombre_mascota):
    # Buscar las imágenes de la mascota en la base de datos
    imagenes = ImagenMascota.query.filter_by(nombre_mascota=nombre_mascota).all()
    if not imagenes:
        flash('¡No se encontraron imágenes para esta mascota!', 'error')
        return redirect(url_for('home'))

    # Crear un archivo zip para las imágenes
    nombre_zip = f'{nombre_mascota}.zip'
    ruta_zip = os.path.join(os.getcwd(), nombre_zip)  # Ruta completa al archivo zip
    with ZipFile(ruta_zip, 'w') as zipf:
        for i, imagen in enumerate(imagenes):
            # Guardar cada imagen en el archivo zip con un nombre único
            nombre_imagen = f'{nombre_mascota}_{i}.jpg'
            with open(nombre_imagen, 'wb') as imgf:
                imgf.write(imagen.imagen)
            zipf.write(nombre_imagen)
            os.remove(nombre_imagen)  # Eliminar el archivo de imagen después de agregarlo al zip

    # Mostrar un mensaje flash y redireccionar a la página de inicio
    flash('¡Las imágenes se han descargado correctamente!', 'success')
    return redirect(url_for('home'))