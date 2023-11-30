from flask import Flask, render_template, request, g

import sqlite3

app = Flask(__name__)

# Función para obtener la conexión a la base de datos
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect('base_de_datos.db')
        g.db.row_factory = sqlite3.Row
    return g.db

# Función para cerrar la conexión a la base de datos
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Crear una tabla si no existe
with app.app_context():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY,
            nombre TEXT,
            edad INTEGER
        )
    ''')
    db.commit()

# Ruta para manejar la página de registro e inicio de sesión
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Procesar los datos del formulario y almacenarlos en la base de datos
        # (Aquí debes agregar la lógica para manejar los datos del formulario)
        pass

    # Consultar datos
    db = get_db()
    cursor = db.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()

    # Renderizar la plantilla HTML con los datos de la base de datos
    return render_template('index.html', usuarios=usuarios)

# Cerrar la conexión después de cada solicitud
@app.teardown_appcontext
def teardown_db(e=None):
    close_db()

if __name__ == '__main__':
    app.run(debug=True)
