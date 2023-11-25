from flask import Blueprint, url_for, redirect, request
from app.db.db_init import connect, disconnect, execute_query
from flask_restx import Api, Resource
from app.auth.jwt_utils import generate_token
from app.auth.email import email_exists
from app.auth.id import id_exists
from app.auth.login import login_admin
from werkzeug.security import generate_password_hash

auth_routes = Blueprint('auth_routes', __name__)

api = Api(auth_routes, version='1.0', title='EducAdmin', description='EducAdmin API REST')

# register candidate
namespace1 = api.namespace('admin', description='End Point Admin')
@namespace1.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        
        user = data.get('user')
        password = data.get('password')
        
        token = login_admin(user, password)
        print ('el token llega a la ruta')
        print (token)
        
        if token is not None:
            return token
        else:
            return {'message': 'Error de inicio de sesión'}

namespace2 = api.namespace('candidate', description='End Point Candidates')

@namespace2.route('/register')
class Register(Resource):
    def post(self):
        data = request.get_json()
        
        email = data.get('email')
        password = data.get('password')
        
        hashed_password  = generate_password_hash(password)
        exists = email_exists(email)

        if exists:
            
            return {'message': 'El correo electrónico ya está registrado'}, 400  
        else:
            role = 3
            
            query = f"INSERT INTO candidate (role, email, password) VALUES ('{role}', '{email}', '{hashed_password}')"
            connection = connect()  
            
            if connection:
                try:
                    execute_query(connection, query)
                    id = id_exists(email)
                    token = generate_token({'id': id, 'email': email, 'role': role})
                    disconnect(connection)
                    return {'message': 'Usuario registrado exitosamente', 'token': token }
                except Exception as e:
                    print(f"Error al registrarse: {e}")
                    disconnect(connection)
                    return {'message': 'Error'}, 500  
            else:
                return {'message': 'No hay conexión a la base de datos'}, 500 

##
@auth_routes.route('/')
def index():
    return redirect(url_for('api_doc'))


##
def init_app(app):
    app.register_blueprint(auth_routes, url_prefix='/')
    return api
