from flask import Flask
from app.routes.auth_routes import init_app
from app.db.db_init import create_tables
from flask_restx import Api

app = Flask(__name__)
app.config.from_object('app.config.config')
app.secret_key = 'SECRET'

api = init_app(app)

if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=0)
