import jwt
from datetime import datetime, timedelta
from flask import current_app
from app.config.config import SECRET_KEY

key=SECRET_KEY

def generate_token(user_data):
    payload = {
        'user_id': user_data.get('id'),
        'role': user_data.get('role'),
        'email': user_data.get('email'),
    }
    jwt_token = jwt.encode(payload, key, algorithm='HS256')
    
    print('{jwt_token}')
    
    return jwt_token



# def decode_token(token):
#     try:
#         payload = jwt.decode(token, key, algorithms='HS256')
#         id = payload.get('user_id')
#         role = payload.get('role')
#         email = payload.get('email')
#         return (id, role, email)
#     except jwt.ExpiredSignatureError:
#         return {'payload': None, 'error': 'Token Expirado'}
#     except jwt.InvalidTokenError:
#         return {'payload': None, 'error': 'Token Invalido'}
