# app.py

from flask import Flask, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import send_from_directory

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///registros1.db'
db = SQLAlchemy(app)

class Registro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

@app.route('/')
def index():
    registros = Registro.query.all()
    return render_template('index.html', registros=registros)

@app.route('/registro', methods=['POST'])
def registro():
    nombre = request.form.get('nombre')
    email = request.form.get('email')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm_password')  # Add this line

    # Validate password confirmation
    if password != confirm_password:
        return jsonify({'error': 'Passwords do not match. Please enter matching passwords.'})

    nuevo_registro = Registro(nombre=nombre, email=email, password=password)
    db.session.add(nuevo_registro)
    db.session.commit()

    return jsonify({'message': f'Registration successful for {nombre} with email {email}!'})

from flask import jsonify

@app.route('/iniciar', methods=['POST'])
def iniciar():
    email = request.form.get('login_email')
    password = request.form.get('login_password')

    # Debugging line
    print(f'Email: {email}, Password: {password}')

    usuario = Registro.query.filter_by(email=email, password=password).first()

    # Debugging line
    print(f'User: {usuario}')

    if usuario:
        return jsonify({'message': f'Welcome, {usuario.nombre}! Login successful.'})
    else:
        return jsonify({'error': 'Incorrect email or password. Please try again.'})

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
