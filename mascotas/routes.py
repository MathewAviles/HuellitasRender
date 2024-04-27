from flask import render_template
from database import app
from mascotas.models import Mascota


@app.route('/mascotas')
def mascotas_index():
    return render_template('mascotas/indexm.html')