from flask import Flask,render_template,request,redirect,url_for,session, flash

# Función para crear la aplicación Flask
def create_app():
    app = Flask(__name__)
    return app

# Inicialización de la aplicación
app = create_app()

# Ruta principal home
@app.route('/')
def home():
    return render_template('home.html')

# Ejecución de la aplicación
if __name__ == "__main__":
    app.run(debug=True)