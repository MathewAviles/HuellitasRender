from flask import render_template, redirect, request, url_for
from database import app, db
from mascotas.models import Mascota


@app.route('/mascotas')
def mascotas_index():
    return render_template('mascotas/indexm.html')