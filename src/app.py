from flask import Flask, render_template, redirect, url_for, request, flash
from config import config
from flask_mysqldb import MySQL
from flask_login import LoginManager, login_user, logout_user
from models.ModelUser import ModelUser
from models.entities.User import User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash
from flask_mail import Mail, Message

app = Flask(__name__)
db = MySQL(app)
login_manager_app = LoginManager(app)
app.config.from_object(config['development'])  
mail = Mail(app)  



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
        logged_user = ModelUser.login(db,email,password) 
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

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if request.method == 'POST':
        email = request.form['email']
        cursor = db.connection.cursor()
        cursor.execute("SELECT * FROM user WHERE email = %s", (email,))
        user_tuple = cursor.fetchone()
        cursor.close()

        if user_tuple:
            user = User(*user_tuple)  # Crear un objeto User a partir de la tupla
            # Si se encuentra el usuario, enviar el correo electrónico para restablecer la contraseña
            send_reset_email(user)
            flash('Se ha enviado un correo electrónico para restablecer la contraseña. Por favor, revisa tu bandeja de entrada.', 'success')
            return redirect(url_for('login'))
        else:
             # Si no se encuentra el usuario, mostrar un mensaje de error
            flash('No se encontró ningún usuario con ese correo electrónico. Por favor, verifica la dirección de correo electrónico.', 'danger')
    return render_template('auth/reset-password.html', Title='Reset Request')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    user_id = User.verify_token(token)
    if user_id is None:
        flash('El token es inválido o ha expirado. Por favor, inténtalo de nuevo.', 'warning')
        return redirect(url_for('reset_request'))

    if request.method == 'POST':
        new_password = request.form['new-password']
        confirm_password = request.form['confirm-password']

        if new_password != confirm_password:
            flash('Las contraseñas no coinciden. Por favor, inténtalo de nuevo.', 'danger')
            return redirect(url_for('reset_token', token=token))

        hashed_password = generate_password_hash(new_password,
                                                 method=config['development'].HASH_METHOD,
                                                 salt_length=config['development'].HASH_SALT_LENGTH)
        # Aquí actualizamos la contraseña del usuario en la base de datos
        cursor = db.connection.cursor()
        try:
            cursor.execute("UPDATE user SET password = %s WHERE id = %s", (hashed_password, user_id))
            db.connection.commit()
            flash('¡Contraseña cambiada exitosamente! Por favor, inicie sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as ex:
            flash('Error al actualizar la contraseña. Por favor, inténtalo de nuevo.', 'danger')
            print(ex)
            db.connection.rollback()
        finally:
            cursor.close()

    return render_template('auth/change-password.html', title='Cambiar Contraseña')

def send_reset_email(user):
    user_instance = User(user.id, user.email, user.password, user.fullname)
    token = user_instance.get_token()
    msg = Message('Solicitud de cambio de contraseña', recipients = [user.email], sender = 'noreplytimereminder@gmail.com')
    msg.body = f''' Para cambiar su contraseña. Por favor haga click en link de abajo.
    
    {url_for('reset_token', token=token, _external=True)}
    
    Si usted no envió una peticion para reestablecer su contraseña. Por favor ignore este mensaje.
    
    '''
    mail.send(msg)
    
if __name__ == '__main__':
    app.config.from_object(config['development'])
    app.run(port=config['development'].PORT)
