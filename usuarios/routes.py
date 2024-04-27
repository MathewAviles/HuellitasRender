from flask import Blueprint, render_template

usuarios_bp = Blueprint('usuarios', __name__, template_folder='templates')

@usuarios_bp.route('/usuarios')
def usuarios_index():
    return render_template('indexu.html')

@usuarios_bp.route('/registrousuario')
def usuarios_register():
    return render_template('register.html')

# Agrega más rutas de usuarios según tus necesidades
