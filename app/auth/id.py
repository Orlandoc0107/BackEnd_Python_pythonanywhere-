from app.db.db_init import connect, disconnect, execute_query
import pymysql


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


