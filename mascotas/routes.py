from flask import Blueprint, render_template

mascotas_bp = Blueprint('mascotas', __name__, template_folder='templates', static_folder='static')

@mascotas_bp.route('/mascotas')
def mascotas_index():
    return render_template('indexm.html')

@mascotas_bp.route('/registromascotas')
def mascotas_add():
    return render_template('add.html')

# Agrega más rutas de mascotas según tus necesidades
