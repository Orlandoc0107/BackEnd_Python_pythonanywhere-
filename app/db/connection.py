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

def roles(id_user, role_user):
    try:
        with connect() as connection:
            query = "UPDATE candidate SET role = %s WHERE id = %s"
            print(id_user)
            print(role_user)
            with connection.cursor() as cursor:
                cursor.execute(query, (role_user, id_user))
                connection.commit()
                t_teacher = transferir_teacher()
                t_studente = transferir_student()
                clears = limpiar_candidatos()
                return t_teacher, t_studente , clears
    except pymysql.Error as e:
        print(f"Error al actualizar el rol: {str(e)}")
        return False  


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

##
def transferir_teacher():
    try:
        connection = connect()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM candidate WHERE role = 1")
            profesor_records = cursor.fetchall()

            for profesor in profesor_records:
                id_profesor = profesor['id']
                role_profesor = profesor['role']
                username_profesor = profesor['username']
                firstname_profesor = profesor['firstname']
                lastname_profesor = profesor['lastname']
                age_profesor = profesor['age']
                dni_profesor = profesor['dni']
                email_profesor = profesor['email']
                password_profesor = profesor['password']

                
                cursor.execute("SELECT * FROM teacher WHERE email = %s", (email_profesor,))
                existing_teacher = cursor.fetchone()

                if not existing_teacher:
                    
                    cursor.execute(
                        "INSERT INTO teacher (role, username, firstname, lastname, age, dni, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (role_profesor, username_profesor, firstname_profesor, lastname_profesor, age_profesor, dni_profesor, email_profesor, password_profesor)
                    )
                else:
                    print(f"El profesor con correo electrónico {email_profesor} ya existe en la tabla de profesores.")

            connection.commit()

        print('Profesores transferidos')

    except pymysql.Error as e:
        print(f"Error durante la transferencia de profesores: {str(e)}")

    finally:
        if connection:
            connection.close()
            
def transferir_student():
    try:
        connection = connect()
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            cursor.execute("SELECT * FROM candidate WHERE role = 2")
            student_records = cursor.fetchall()
            print(type(student_records))

            for student in student_records:
                id_student = student['id']
                role_student = student['role']
                username_student = student['username']
                firstname_student = student['firstname']
                lastname_student = student['lastname']
                age_student = student['age']
                dni_student = student['dni']
                email_student = student['email']
                password_student = student['password']

                
                cursor.execute("SELECT * FROM student WHERE email = %s", (email_student,))
                existing_student = cursor.fetchone()

                if not existing_student:
                    
                    
                    cursor.execute(
                        "INSERT INTO student (role, username, firstname, lastname, age, dni, email, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                        (role_student, username_student, firstname_student, lastname_student, age_student, dni_student, email_student, password_student)
                    )
                else:
                    print(f"El student con correo electrónico {email_student} ya existe en la tabla de student.")

            connection.commit()

        print('students transferidos')

    except pymysql.Error as e:
        print(f"Error durante la transferencia de student: {str(e)}")

    finally:
        if connection:
            connection.close()
            
#
def limpiar_candidatos(id):
    try:
        connection = connect()

        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # Eliminar candidato por ID
            cursor.execute("DELETE FROM candidate WHERE id = %s", (id,))
            connection.commit()

        print(f"Candidato con ID {id} eliminado correctamente.")

    except pymysql.Error as e:
        print(f"Error al limpiar el registro del candidato: {str(e)}")

    finally:
        if connection:
            connection.close()