from werkzeug.security import check_password_hash
from flask_login import UserMixin

class User(UserMixin):
    # Constructor de la clase User
    def __init__(self, id, email, password, fullname=""):
        self.id = id  # Almacena el ID único del usuario proporcionado al crear una instancia de la clase User
        self.email = email  # Igual
        self.password = password  # Igual
        self.fullname = fullname  # Igual

    # Método de clase para verificar la contraseña
    @classmethod
    def check_password(cls, hashed_password, password):
        # Utiliza la función check_password_hash de Werkzeug para verificar si la contraseña coincide con el hash
        return check_password_hash(hashed_password, password)

