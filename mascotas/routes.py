from flask import render_template, redirect, request, url_for, session, flash, make_response
from database import app,db
from mascotas.models import Mascota,Sexo,ImagenMascota
from usuarios.models import Usuario
from zipfile import ZipFile
import base64
import os 


@app.route('/', methods=['GET'])
def home():
    # Obtener todas las mascotas de la base de datos
    mascotas = Mascota.query.all()

    # Convertir las imágenes a cadenas codificadas en base64
    for mascota in mascotas:
        mascota.imagen1 = base64.b64encode(mascota.imagen1).decode('utf-8')

    # Renderizar la plantilla HTML con las mascotas
    return render_template('home.html', mascotas=mascotas)


@app.route('/mascotas', methods=['GET'])
def mostrar_mascotas():
    # Obtener el usuario actual (esto dependerá de cómo manejes la autenticación)
    usuario_actual = Usuario.query.get(session['user_id'])

    # Obtener todas las mascotas del usuario actual de la base de datos
    mascotas = Mascota.query.filter_by(usuario_id=usuario_actual.id).all()

    # Renderizar la plantilla HTML con las mascotas
    return render_template('mascotas/mascotas.html', mascotas=mascotas)



@app.route('/reconocimiento_mascotas')
def reconocimiento_mascotas():
    return render_template('mascotas/reconocimientomascotas.html')


@app.route('/crear_mascota', methods=['GET', 'POST'])
def crear_mascota():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form['nombre']
            edad = request.form['edad']
            raza = request.form['raza']
            sexo_id = request.form['sexo_id']
            descripcion = request.form['descripcion']
            fecha_desaparicion = request.form['fecha_desaparicion']
            lugar_desaparicion = request.form['lugar_desaparicion']
            contacto = request.form['contacto']

            # Obtener las imágenes del formulario
            imagen1 = request.files['imagen1'].read() if 'imagen1' in request.files else None
            imagen2 = request.files['imagen2'].read() if 'imagen2' in request.files else None
            imagen3 = request.files['imagen3'].read() if 'imagen3' in request.files else None

            # Verificar que se haya ingresado al menos la primera imagen
            if imagen1 is None:
                flash('¡Debes ingresar al menos una imagen!', 'error')
                return redirect(url_for('crear_mascota'))

            # Crear una nueva mascota
            nueva_mascota = Mascota(nombre=nombre, edad=edad, raza=raza, sexo_id=sexo_id, 
                                    descripcion=descripcion, fecha_desaparicion=fecha_desaparicion, 
                                    lugar_desaparicion=lugar_desaparicion, contacto=contacto, 
                                    usuario_id=session['user_id'], imagen1=imagen1, imagen2=imagen2, imagen3=imagen3)
            db.session.add(nueva_mascota)
            db.session.commit()

            # Redireccionar a alguna página de éxito o a la página de inicio
            flash('¡Registro exitoso!', 'success')
            return redirect(url_for('home'))
        except Exception as e:
            # Si ocurre un error, mostrar un mensaje de error y redireccionar al formulario de creación de mascotas
            flash(f'¡Ocurrió un error al crear la mascota! {str(e)}', 'error')
            return redirect(url_for('crear_mascota'))
    
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



@app.route('/editar_mascota/<int:id>', methods=['GET', 'POST'])
def editar_mascota(id):
    # Buscar la mascota en la base de datos
    mascota = Mascota.query.get(id)

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

        # Actualizar los datos de la mascota
        mascota.nombre = nombre
        mascota.edad = edad
        mascota.raza = raza
        mascota.sexo_id = sexo_id
        mascota.descripcion = descripcion
        mascota.fecha_desaparicion = fecha_desaparicion
        mascota.lugar_desaparicion = lugar_desaparicion
        mascota.contacto = contacto

        db.session.commit()

        # Redireccionar a alguna página de éxito o a la página de inicio
        flash('¡Mascota actualizada con éxito!', 'success')
        return redirect(url_for('home'))

    # Si el método es GET, mostrar el formulario de edición de mascotas
    sexos = Sexo.query.all()
    return render_template('mascotas/editar_mascota.html', mascota=mascota, sexos=sexos)


@app.route('/eliminar_mascota/<int:id>', methods=['POST'])
def eliminar_mascota(id):
    # Buscar la mascota en la base de datos
    mascota = Mascota.query.get(id)

    if mascota:
        # Verificar si el usuario actual es el propietario de la mascota o es un administrador
        usuario_actual = Usuario.query.get(session['user_id'])
        if usuario_actual.id == mascota.usuario_id or usuario_actual.rol == 'admin':
            # Eliminar la mascota de la base de datos
            db.session.delete(mascota)
            db.session.commit()
            flash('¡Mascota eliminada con éxito!', 'success')
        else:
            flash('¡No tienes permisos para eliminar esta mascota!', 'error')
    else:
        flash('¡La mascota no fue encontrada!', 'error')

    # Redireccionar a alguna página de éxito o a la página de inicio
    return redirect(url_for('home'))
