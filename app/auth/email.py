from app.db.db_init import connect, disconnect
import pymysql


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