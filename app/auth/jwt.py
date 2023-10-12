import jwt
from app.config.config import SECRET

SECRET_KEY = "SECRET"

def generate_token(user_info):
    return jwt.encode(user_info, SECRET_KEY, algorithm="HS256")

def validate_token(token):
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
    except jwt.ExpiredSignatureError:
        return None  
    except jwt.InvalidTokenError:
        return None  
