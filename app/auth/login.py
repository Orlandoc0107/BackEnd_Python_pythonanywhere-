from app.db.db_init import connect, disconnect
import pymysql
from app.auth.jwt_utils import generate_token
from werkzeug.security import check_password_hash, generate_password_hash


def login_admin(user, password):
    connection = connect()

    if not connection:
        print("No hay conexión a la base de datos MySQL.")
        return

    try:
        cursor = connection.cursor()
        query = "SELECT * FROM admin WHERE user = %s"
        values = (user,)
        cursor.execute(query, values)
        result = cursor.fetchone()

        if not result:
            print("No se encontró un usuario con ese nombre.")
            return

        id, role, email = result[:3]
        hashed_password = generate_password_hash(password)

        if check_password_hash(result[4], password):
            token = generate_token({'id': id, 'email': email, 'role': role})
            print("Inicio de sesión exitoso.")
            return {'token': token}
        else:
            print("Credenciales incorrectas. Verifica tu usuario y contraseña.")
    except pymysql.Error as e:
        print(f"Error al ejecutar la consulta: {str(e)}")
    finally:
        cursor.close()
        disconnect(connection)