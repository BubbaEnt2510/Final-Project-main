
class Config:
    
    # Clase base de configuración con una clave secreta para la aplicación
    SECRET_KEY = 'A!!_*JCES*NMgh.;:PfG59¿2'
    
    # Configuraciones de hash
    HASH_METHOD = 'pbkdf2:sha256'
    HASH_SALT_LENGTH = 16
    HASH_ITERATIONS = 100000
    
    # Configuración de Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'noreplytimereminder@gmail.com'
    MAIL_PASSWORD = 'cvoi hokr kgzb ojho'
    MAIL_DEFAULT_SENDER = 'noreplytimereminder@gmail.com'


# Definición de la clase de configuración para el entorno de desarrollo
class DevelopmentConfig(Config):
    # Configuraciones específicas para el entorno de desarrollo
    DEBUG = True  # Habilita el modo de depuración
    PORT = 5252  # Puerto en el que se ejecutará la aplicación
    MYSQL_HOST = 'localhost'  # Dirección del servidor de la base de datos MySQL
    MYSQL_USER = 'root'  # Nombre de usuario de la base de datos MySQL
    MYSQL_PASSWORD = ''  # Contraseña de la base de datos MySQL
    MYSQL_DB = 'flask_login'  # Nombre de la base de datos MySQL

# Se crea un Diccionario para que almacene y que mapea nombres de configuraciones a clases de configuración
config = {
    'development': DevelopmentConfig  # Establece relaciones el nombre 'development' a la clase DevelopmentConfig
}
