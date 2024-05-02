import mysql.connector
from werkzeug.security import check_password_hash
from itsdangerous import URLSafeTimedSerializer 
from datetime import datetime, timedelta
from flask_login import UserMixin
from config import Config

class User(UserMixin):
    # Constructor de la clase User
    def __init__(self, id, email, password, fullname=""):
        self.id = id  # Almacena el ID único del usuario proporcionado al crear una instancia de la clase User
        self.email = email  # Igual
        self.password = password  # Igual
        self.fullname = fullname  # Igual
        
    def get_token(self):
        serial = URLSafeTimedSerializer(Config.SECRET_KEY)
        expires_at = datetime.now() + timedelta(minutes=10)  # 10 minutos de expiración del token
        token = serial.dumps({'user_id': self.id, 'expires_at': expires_at.isoformat()})
        return token

    @staticmethod
    def verify_token(token):
        serial = URLSafeTimedSerializer(Config.SECRET_KEY)
        try:    
            data = serial.loads(token)
            if datetime.fromisoformat(data['expires_at']) < datetime.now():
                # El token ha expirado
                return None
            return data['user_id']
        except:
            return None
            
    # Método de clase para verificar la contraseña
    @classmethod
    def check_password(cls, hashed_password, password):
        # Utiliza la función check_password_hash de Werkzeug para verificar si la contraseña coincide con el hash
        return check_password_hash(hashed_password, password)

# Función para buscar un usuario por su ID
def buscar_usuario_por_id(user_id):
    try:
        connection = mysql.connector.connect(host='localhost',
                                             database='db_proyecto',
                                             user='root',
                                             password='')
        if connection.is_connected():
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user WHERE id = %s", (user_id,))
            user = cursor.fetchone()
            if user:
                return User(user['id'], user['email'], user['password'], user['fullname'])
            else:
                return None
    except mysql.connector.Error as error:
        print("Error al conectar a la base de datos:", error)
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()
