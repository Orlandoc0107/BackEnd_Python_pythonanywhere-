from flask import Blueprint, url_for, redirect, request, jsonify
from app.db.db_init import connect, disconnect, execute_query
from flask_restx import Api, Resource
from app.auth.jwt import generate_token
from app.db.connection import (editadmin, email_exists, id_exists, listcandidate, liststudent,
    listteacher, login_admin, listcommissions, roles , limpiar_candidatos)
from werkzeug.security import generate_password_hash
from app.config.config import SECRET_KEY
import jwt

auth_routes = Blueprint('auth_routes', __name__)

api = Api(auth_routes, version='1.0', title='EducAdmin', description='EducAdmin API REST')
key = SECRET_KEY

# register candidate
namespace1 = api.namespace('admin', description='End Point Admin')
@namespace1.route('/login')
class Login(Resource):
    def post(self):
        data = request.get_json()
        
        user = data.get('user')
        password = data.get('password')
        
        token = login_admin(user, password)
        print (token)
        
        if token is not None:
            return token
        else:
            return {'message': 'Error de inicio de sesión'}

#Edit
@namespace1.route('/edit')
class Edit(Resource):
    def put(self):
        data = request.headers.get('Authorization')
        token = data.split()[1]
        try:
            payload = jwt.decode(token, key, algorithms='HS256')
            id = payload.get('user_id')
            role = payload.get('role')
            email = payload.get('email')
            
            data = request.get_json()
            user = data.get('user')
            emai = data.get('email')
            password = data.get('password')
            if role == 0:
                edit = editadmin(id, user, emai, password)
                return {'message':'Datos Actualizados'}
            else:
                return {'message':'No tienes los permisos suficientes'}
            
        except jwt.ExpiredSignatureError:
            return {'payload': None, 'error': 'Token Expirado'}
        except jwt.InvalidTokenError:
            return {'payload': None, 'error': 'Token Invalido'}

#List candidate
@namespace1.route('/users')
class List(Resource):
    def get(self):
        data = request.headers.get('Authorization')
        token = data.split()[1]
        try:
            payload = jwt.decode(token, key, algorithms='HS256')
            role = payload.get('role')

            if role == 0:
                resultados = listcandidate()
                resultados_json = jsonify(resultados)

                return resultados_json
            else:
                return {'message': 'No tienes los permisos suficientes'}
            
        except jwt.ExpiredSignatureError:
            return {'payload': None, 'error': 'Token Expirado'}
        except jwt.InvalidTokenError:
            return {'payload': None, 'error': 'Token Invalido'}
#
#List student
@namespace1.route('/student')
class List(Resource):
    def get(self):
        data = request.headers.get('Authorization')
        token = data.split()[1]
        try:
            payload = jwt.decode(token, key, algorithms='HS256')
            role = payload.get('role')

            if role == 0:
                resultados = liststudent()

                resultados_json = jsonify(resultados)

                return resultados_json
            else:
                return {'message': 'No tienes los permisos suficientes'}
            
        except jwt.ExpiredSignatureError:
            return {'payload': None, 'error': 'Token Expirado'}
        except jwt.InvalidTokenError:
            return {'payload': None, 'error': 'Token Invalido'}
#
@namespace1.route('/roles')
class Roles(Resource):
    def put(self):
        data = request.headers.get('Authorization')
        token = data.split()[1]
        try:
            payload = jwt.decode(token, key, algorithms='HS256')
            role = payload.get('role')

            if role == 0:
                data = request.get_json()
                id_user = data.get('id')
                role_user = data.get('role')
                if id_user:
                    res= roles(id_user, role_user)
                    return res
                else:
                    return {'message':'No existe la elusuario en la base de datos'}
                    

        except jwt.ExpiredSignatureError:
            return {'payload': None, 'error': 'Token Expirado'}
        except jwt.InvalidTokenError:
            return {'payload': None, 'error': 'Token Invalido'}

@namespace1.route('/teachers')
class List(Resource):
    def get(self):
        data = request.headers.get('Authorization')
        token = data.split()[1]
        try:
            payload = jwt.decode(token, key, algorithms='HS256')
            role = payload.get('role')
            

            if role == 0:
                resultados = listteacher()

                resultados_json = jsonify(resultados)

                return resultados_json
            else:
                return {'message': 'No tienes los permisos suficientes'}
            
        except jwt.ExpiredSignatureError:
            return {'payload': None, 'error': 'Token Expirado'}
        except jwt.InvalidTokenError:
            return {'payload': None, 'error': 'Token Invalido'}
#
@namespace1.route('/commissions')
class List(Resource):
    def get(self):
        data = request.headers.get('Authorization')
        token = data.split()[1]
        try:
            payload = jwt.decode(token, key, algorithms='HS256')
            role = payload.get('role')
            
            if role == 0:
                resultados = listcommissions()

                resultados_json = jsonify(resultados)

                return resultados_json
            else:
                return {'message': 'No tienes los permisos suficientes'}
            
        except jwt.ExpiredSignatureError:
            return {'payload': None, 'error': 'Token Expirado'}
        except jwt.InvalidTokenError:
            return {'payload': None, 'error': 'Token Invalido'}
#
@namespace1.route('/delete')
class Delete(Resource):
    def delete(self):
        data = request.get_json()
        id = data.get('id')
        if id:
            resp = limpiar_candidatos(id)
            return resp
        else:
            return {'menssage':'No existe el usuario con esa id'}
        

#
namespace2 = api.namespace('user', description='End Point Candidates')
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
