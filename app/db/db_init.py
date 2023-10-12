import pymysql
from app.config.config import DB_HOST, DB_PORT, DB_PASSWORD, DB_NAME, DB_USER


def connect():
    try:
        connection = pymysql.connect(
            host= DB_HOST,
            port=DB_PORT,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME
        )
        print("Conexión a la base de datos MySQL establecida correctamente.")
        return connection
    except pymysql.Error as e:
        print(f"Error al conectar a MySQL: {str(e)}")
        return None

def disconnect(connection):
    if connection:
        connection.close()
        print("Conexión a la base de datos MySQL cerrada.")

def execute_query(connection, query, values=None):
    if connection:
        try:
            with connection.cursor() as cursor:
                if values:
                    cursor.execute(query, values)
                else:
                    cursor.execute(query)
                connection.commit()
                print("Consulta ejecutada con éxito.")
                if cursor.rowcount > 0:
                    return cursor.fetchall()
        except pymysql.Error as e:
            print(f"Error al ejecutar la consulta: {str(e)}")
    else:
        print("No hay conexión a la base de datos MySQL.")
    return None

create_user_table = """
CREATE TABLE IF NOT EXISTS user (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NULL,
    first_name VARCHAR(255) NULL,
    last_name VARCHAR(255) NULL,
    age INT NULL,
    email VARCHAR(255) UNIQUE, 
    google_auth_id VARCHAR(255) UNIQUE, 
    password VARCHAR(255) NULL,
    profile_photo VARCHAR(255) NULL,
    rol VARCHAR(255) NOT NULL -- Puede ser 'admin', 'teacher', 'student', 'candidate'
);
"""

create_course_table = """
CREATE TABLE IF NOT EXISTS course (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    creation DATE,
    administrador_id INT NULL,
    teacher_id INT NULL,
    student_id INT NULL
);
"""

create_subject_table = """
CREATE TABLE IF NOT EXISTS subject (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    total_notes INT NULL,
    teacher_id INT NULL
);
"""

create_note_table = """
CREATE TABLE IF NOT EXISTS note (
    id INT AUTO_INCREMENT PRIMARY KEY,
    subject_id INT NULL, -- Clave foránea a subjects (id)
    student_id INT NULL, -- Clave foránea a users (id)
    note INT -- Nota individual
);
"""

def create_tables():
    connection = connect()

    if connection:
        execute_query(connection, create_user_table)
        execute_query(connection, create_course_table)
        execute_query(connection, create_subject_table)
        execute_query(connection, create_note_table)

    disconnect(connection)

create_tables()
