from flask import Flask, render_template, redirect, url_for, request, flash
from config import config
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from models.ModelUser import ModelUser
from models.entities.User import User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(db, id)

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User(None, email, password)  # Creamos el objeto User con email y password
        logged_user = ModelUser.login(db, user)  # Pasamos el objeto User a la función login
        if logged_user:
            login_user(logged_user)
            return redirect(url_for('inicio'))
        else:
            flash("Usuario no encontrado o contraseña incorrecta.", 'warning')
    return render_template('auth/login.html')


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/inicio')
def inicio():
    return render_template('inicio.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        fullname = request.form['name'] + ' ' + request.form['lastName']

        if not email or not password or not fullname:
            flash('Por favor, completa todos los campos del formulario.', 'danger')
            return redirect(url_for('register_form'))

        user = User(None, email, password, fullname)

        try:
            if ModelUser.register(db, user):
                flash('Registro exitoso!', 'success')
                return redirect(url_for('login'))
            else:
                flash('Error en el registro. Intente de nuevo.', 'danger')
        except Exception as ex:
            flash('Error en el registro. Intente de nuevo.', 'danger')
            print(ex)
            db.connection.rollback()

    return redirect(url_for('register_form'))

@app.route('/register', methods=['GET'])
def register_form():
    return render_template('auth/register.html')

@app.route('/reset_password')
def reset_request():
   
    return render_template('auth/reset-password.html', Title='Reset Request')

if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=config['development'].PORT)
