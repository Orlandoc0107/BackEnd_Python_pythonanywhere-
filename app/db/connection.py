from app.db.db_init import connect, disconnect
import pymysql
from app.auth.jwt import generate_token
from werkzeug.security import check_password_hash, generate_password_hash


#
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
        

######

def editadmin(id, user, emai, password):
    password = generate_password_hash(password)
    connection = connect()
    query = f"UPDATE admin SET user = '{user}', email = '{emai}', password = '{password}' WHERE id = %s"
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query, (id,))
                connection.commit()
                print("Datos Actualizados")
        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {str(e)}")
        finally:
            cursor.close()
            disconnect(connection)
            
    else:
        return {'messager':'Ocurrio un Error'}
######

def listcandidate():
    connection = connect()
    resultados_dict = []

    if connection:
        try:
            with connection.cursor() as cursor:
                consulta = f"SELECT * FROM candidate"
                cursor.execute(consulta)
                resultados = cursor.fetchall()

                for resultado in resultados:
                    candidato = {
                        'id': resultado[0],
                        'role': resultado[1],
                        'username': resultado[2],
                        'firstname': resultado[3],
                        'lastname': resultado[4],
                        'age': resultado[5],
                        'dni': resultado[6],
                        'email': resultado[7],
                    }
                    resultados_dict.append(candidato)

        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {str(e)}")
        finally:
            connection.close()

    return resultados_dict
#####
def liststudent():
    connection = connect()
    resultados_dict = []

    if connection:
        try:
            with connection.cursor() as cursor:
                consulta = f"SELECT * FROM student"
                cursor.execute(consulta)
                resultados = cursor.fetchall()

                for resultado in resultados:
                    student = {
                        'id': resultado[0],
                        'role': resultado[1],
                        'username': resultado[2],
                        'firstname': resultado[3],
                        'lastname': resultado[4],
                        'age': resultado[5],
                        'dni': resultado[6],
                        'email': resultado[7],
                    }
                    resultados_dict.append(student)

        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {str(e)}")
        finally:
            connection.close()

    return resultados_dict
#####
def listteacher():
    connection = connect()
    resultados_dict = []

    if connection:
        try:
            with connection.cursor() as cursor:
                consulta = f"SELECT * FROM teacher"
                cursor.execute(consulta)
                resultados = cursor.fetchall()

                for resultado in resultados:
                    teacher = {
                        'id': resultado[0],
                        'role': resultado[1],
                        'username': resultado[2],
                        'firstname': resultado[3],
                        'lastname': resultado[4],
                        'age': resultado[5],
                        'dni': resultado[6],
                        'email': resultado[7],
                    }
                    resultados_dict.append(teacher)

        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {str(e)}")
        finally:
            connection.close()

    return resultados_dict
#####
def listcommissions():
    connection = connect()
    resultados_dict = []

    if connection:
        try:
            with connection.cursor() as cursor:
                consulta = f"SELECT * FROM commissions"
                cursor.execute(consulta)
                resultados = cursor.fetchall()

                for resultado in resultados:
                    commissions = {
                        'id': resultado[0],
                        'role': resultado[1],
                        'username': resultado[2],
                        'firstname': resultado[3],
                        'lastname': resultado[4],
                        'age': resultado[5],
                        'dni': resultado[6],
                        'email': resultado[7],
                    }
                    resultados_dict.append(commissions)

        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {str(e)}")
        finally:
            connection.close()

    return resultados_dict
#####
def email_exists(email):
    connection = connect()
    query = f"SELECT email FROM teacher WHERE email = '{email}'"
    query = f"SELECT email FROM stundent WHERE email = '{email}'"
    query = f"SELECT email FROM candidate WHERE email = '{email}'"
    
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    return True
        except pymysql.Error as e:
            print(f"Error al verificar el correo electrónico: {str(e)}")

    disconnect(connection)
    return False

###

def id_exists(email):
    connection = connect()
    query = f"SELECT id FROM candidate WHERE email = '{email}'"
    
    if connection:
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                result = cursor.fetchone()
                if result:
                    return result
        except pymysql.Error as e:
            print(f"Error : {str(e)}")

    disconnect(connection)
    return False