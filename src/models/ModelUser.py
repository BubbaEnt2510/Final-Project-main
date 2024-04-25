from models.entities.User import User
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

class ModelUser():
    
    @classmethod
    def login(cls, db, email, password):
        try:
            cursor = db.connection.cursor()
            sql = "SELECT id, email, password, fullname FROM user WHERE email = %s"
            cursor.execute(sql, (email,))
            row = cursor.fetchone()
            if row:
                user = User(row[0], row[1], row[2], row[3])
                if check_password_hash(user.password, password):
                    return user
            return None
        except Exception as ex:
            raise Exception(ex)
        


    @classmethod
    def register(cls, db, user):
        try:
            # Generar hash de la contraseña
            hashed_password = generate_password_hash(user.password)
            # Establecer conexión a la base de datos
            cursor = db.connection.cursor()
            # Construir la consulta SQL para insertar un nuevo usuario
            sql = "INSERT INTO user (email, password, fullname) VALUES ('{}', '{}', '{}')".format(user.email, hashed_password, user.fullname)
            # Ejecutar la consulta SQL
            cursor.execute(sql)
            # Confirmar la transacción
            db.connection.commit()
            # Retornar True si el registro es exitoso
            return True
        except Exception as ex:
            # Si algo sale mal, hacer rollback de la transacción
            db.connection.rollback()
            raise Exception(ex)



    @classmethod
    def get_by_id(self, db, id):
        try:
            # Establece una conexión a la base de datos
            cursor = db.connection.cursor()
            # Construye la consulta SQL
            sql = "SELECT id, email, fullname FROM user WHERE id = {}".format(id)
            # Ejecuta la consulta SQL
            cursor.execute(sql)
            # Obtiene la primera fila del resultado
            row = cursor.fetchone()
            # Verifica si se encontró un usuario con el correo electrónico proporcionado
            if row != None:
                # Si se encuentra un usuario, crea una instancia de User con los datos obtenidos de la base de datos
                return User(row[0], row[1], None, row[2])
                
            else:
                # Si no se encuentra ningún usuario, retorna None
                return None
        except Exception as ex:
    # Si algo sale mal durante el intento de ejecución, lo capturamos aquí para entender qué sucedió.
    # Después, levantamos la misma excepción para detener la ejecución del programa y mostrar el error.
    # Queremos tener claridad sobre qué pasó y dónde ocurrió el problema exactamente.
            raise Exception(ex)