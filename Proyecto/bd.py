import sqlite3

# Conectar a la base de datos (o crearla si no existe)
conn = sqlite3.connect('base_de_datos.db')

# Crear un cursor para ejecutar consultas SQL
cursor = conn.cursor()

# Crear una tabla si no existe
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY,
        nombre TEXT,
        edad INTEGER
    )
''')

# Agregar datos a la tabla
cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", ('Juan', 25))
cursor.execute("INSERT INTO usuarios (nombre, edad) VALUES (?, ?)", ('María', 30))

# Guardar los cambios
conn.commit()

# Consultar datos
cursor.execute("SELECT * FROM usuarios")
usuarios = cursor.fetchall()
print("Usuarios:")
for usuario in usuarios:
    print(usuario)

# Cerrar la conexión
conn.close()
