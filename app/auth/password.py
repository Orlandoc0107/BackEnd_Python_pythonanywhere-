from werkzeug.security import check_password_hash
from app.db.db_init import connect ,disconnect
from app.auth.jwt import generate_token

def check_password_admin(password, email):
    connection = connect()
    if connection:
        try:
            cursor = connection.cursor()
            query = f"SELECT * FROM admin WHERE email = %s"
            cursor.execute(query, (email,))
            result = cursor.fetchone()
            disconnect()
            print(result[3])
            if result and check_password_hash(result[8], password):
                token = generate_token()
                return {'token': token}
                
        except:
            return {'message' : 'Algunos de los dtos no coninciden'}