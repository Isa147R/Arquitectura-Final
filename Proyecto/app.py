from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Configuración de la base de datos
DATABASE = 'database.db'

def create_table():
    conn = sqlite3.connect(DATABASE, detect_types=sqlite3.PARSE_DECLTYPES|sqlite3.PARSE_COLNAMES)
    print("Database connection successful")
    conn.execute('PRAGMA encoding = "UTF-8"')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()



create_table()

def insert_user(username, email, password):
    hashed_password = generate_password_hash(password, method='sha256')
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)', (username, email, hashed_password))
    print("User inserted successfully")
    conn.commit()
    conn.close()

def user_exists(username, email):
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE username = ? OR email = ?', (username, email))
    count = cursor.fetchone()[0]
    conn.close()
    return count > 0


def get_all_users():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email FROM users')
    users = cursor.fetchall()
    print(f"Users: {users}") 
    conn.close()
    return users

@app.route('/')
def index():
    users = get_all_users()
    return render_template('index.html', users=users)

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        try:
            username = request.form['username']
            email = request.form['email']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password == confirm_password:
                insert_user(username, email, password)
            else:
                print("Error: Las contraseñas no coinciden.")
        except Exception as e:
            print(f"Error during registration: {e}")

    return redirect(url_for('index'))

@app.route('/view_users')
def view_users():
    users = get_all_users()
    return render_template('view_users.html', users=users)

if __name__ == '__main__':
    app.run(debug=True)
