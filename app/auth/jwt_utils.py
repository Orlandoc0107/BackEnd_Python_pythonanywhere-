import jwt
from datetime import datetime, timedelta
from flask import current_app

def generate_token(user_data):
    expiration_time = datetime.utcnow() + timedelta(days=1)
    payload = {
        'user_id': user_data.get('id'),
        'role': user_data.get('role'),
        'email': user_data.get('email'),
        'exp': expiration_time
    }
    jwt_token = jwt.encode(payload, current_app.config['SECRET_KEY'], algorithm='HS256')
    return jwt_token

def decode_token(token):
    try:
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
