import pymysql
from app.config.config import DB_HOST, DB_PORT, DB_PASSWORD, DB_NAME, DB_USER
from werkzeug.security import generate_password_hash

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

# Consulta de creación de tablas

create_admin_table = """
    CREATE TABLE IF NOT EXISTS admin (
        id INT AUTO_INCREMENT PRIMARY KEY,
        role INT DEFAULT '0',
        user VARCHAR(255) NOT NULL,
        email VARCHAR(255),
        password VARCHAR(255) NOT NULL
    );
"""

create_teacher_table = """
    CREATE TABLE IF NOT EXISTS teacher (
        id INT PRIMARY KEY AUTO_INCREMENT,
        role INT DEFAULT '1',
        username VARCHAR(255),
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        age INT,
        dni VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        paswordTeacher VARCHAR(255)
    );
"""

create_stundent_table = """
    CREATE TABLE IF NOT EXISTS student (
        id INT PRIMARY KEY AUTO_INCREMENT,
        role INT DEFAULT '2',
        username VARCHAR(255),
        firstname VARCHAR(255),
        lastname VARCHAR(255),
        age INT,
        dni VARCHAR(255),
        email VARCHAR(255),
        password VARCHAR(255),
        teacher_id INT,
        FOREIGN KEY (teacher_id) REFERENCES teacher(id)
    );
"""

create_candidate_table = '''
    CREATE TABLE IF NOT EXISTS candidate (
        id INT AUTO_INCREMENT PRIMARY KEY,
        role INT DEFAULT '3',
        username TEXT,
        firstname TEXT,
        lastname TEXT,
        age INTEGER,
        dni TEXT,
        email TEXT,
        password TEXT,
        teacher_id INT,
        FOREIGN KEY (teacher_id) REFERENCES teacher(id)
    );
'''

create_subjects_table = """
    CREATE TABLE IF NOT EXISTS subjects (
        id INT PRIMARY KEY AUTO_INCREMENT,
        math TEXT,
        geography TEXT,
        language TEXT,
        english TEXT,
        teacher_id INT,
        student_id INT,
        FOREIGN KEY (teacher_id) REFERENCES teacher(id),
        FOREIGN KEY (student_id) REFERENCES student(id)
    );
"""
create_commissions_table = """
    CREATE TABLE IF NOT EXISTS commissions(
        id INT PRIMARY KEY AUTO_INCREMENT,
        name VARCHAR(255),
        teacher_id INT,
        student_id INT,
        FOREIGN KEY (teacher_id) REFERENCES teacher(id),
        FOREIGN KEY (student_id) REFERENCES student(id)
    );
"""

def crear_administrador(connection):
    query_check_admin_table = "SHOW TABLES LIKE 'admin'"
    query_count_admins = "SELECT COUNT(*) FROM admin"
    query_insert_admin = "INSERT INTO admin (user, password, email) VALUES (%s, %s, %s)"
    
    table_exists = execute_query(connection, query_check_admin_table)
    
    if not table_exists:
        print("Tabla 'admin' no encontrada. Creando la tabla...")
        print(create_admin_table) 
        execute_query(connection, create_admin_table)
        print("Tabla 'admin' creada.")
    
    count = execute_query(connection, query_count_admins)[0][0]
    
    if count == 0:
        username = 'admin'
        password_hash = generate_password_hash('admin')
        email = 'admin@admin.com'
        values = (username, password_hash, email)
        execute_query(connection, query_insert_admin, values)
        print("Administrador creado.")
    else:
        print("Ya existe un administrador en la base de datos.")


def create_tables():
    connection = connect()

    if connection:
        execute_query(connection, create_admin_table)
        execute_query(connection, create_teacher_table)
        execute_query(connection, create_candidate_table)
        execute_query(connection, create_stundent_table)
        execute_query(connection, create_subjects_table)
        execute_query(connection, create_commissions_table)
        crear_administrador(connection)
        
    disconnect(connection)

create_tables()