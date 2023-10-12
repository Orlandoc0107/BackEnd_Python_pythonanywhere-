from flask import Flask, request,jsonify, Blueprint, render_template
from app.config.config import SECRET, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME  
from app.db.db_init import create_tables
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from marshmallow import Schema, fields

app = Flask(__name__ , template_folder='app/templates')

app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



db = SQLAlchemy(app)
ma = Marshmallow(app)
app.secret_key = SECRET

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), nullable=True)
    first_name = db.Column(db.String(255), nullable=True)
    last_name = db.Column(db.String(255), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    google_auth_id = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    profile_photo = db.Column(db.String(255), nullable=True)
    rol = db.Column(db.String(255), default='candidate' , nullable=True)
    
    def __init__(self, username=None, first_name=None, last_name=None, age=None, email=None, google_auth_id=None, password=None, profile_photo=None, rol='candidate'):        
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.email = email
        self.google_auth_id = google_auth_id
        self.password = password
        self.profile_photo = profile_photo
        self.rol = rol

class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    creation = db.Column(db.Date)
    administrador_id = db.Column(db.Integer)
    teacher_id = db.Column(db.Integer, nullable=True)
    student_id = db.Column(db.Integer, nullable=True)

    def __init__(self, name=None, creation=None, administrador_id=None, teacher_id=None, student_id=None):
        self.name = name
        self.creation = creation
        self.administrador_id = administrador_id
        self.teacher_id = teacher_id
        self.student_id = student_id

class Subject(db.Model):
    __tablename__ = 'subject'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=True)
    total_notes = db.Column(db.Integer, nullable=True)
    teacher_id = db.Column(db.Integer, nullable=True)
    
    def __init__(self, name=None, total_notes=None):
        self.name = name
        self.total_notes = total_notes

class Note(db.Model):
    __tablename__ = 'note'
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=True)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    note = db.Column(db.Integer, nullable=True)
    subject = db.relationship('Subject', backref='notes')
    student = db.relationship('User', backref='notes')
    
    def __init__(self, subject_id=None, student_id=None, note=None):
        self.subject_id = subject_id
        self.student_id = student_id
        self.note = note
    

class UserSchema(Schema):
    class Meta:
        fields = ("id", "username", "first_name", "last_name", "age", "email", "google_auth_id", "profile_photo", "rol")

class ComisionSchema(Schema):
    class Meta:
        fields = ("id", "name", "creation", "administrador_id", "teacher_id", "student_id")
        
class SubjectSchema(Schema):
    class Meta:
        fields = ("id", "name", "total_notes", "teacher_id")
        
class NotaSchema(Schema):
    class Meta:
        fields = ("id", "subject_id", "student_id", "note")




# Ruta de inicio
@app.route('/')
def index():
    return 'Hola!'

# Registrrar
@app.route('/register', methods=['GET', 'POST'])
def register_user():
    if request.method == 'POST':
        data = request.form

        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return render_template('register.html', error='Todos los campos son obligatorios'), 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return render_template('register.html', error='El correo ya está registrado'), 400
  
        new_user = User(email=email, password=password)

        db.session.add(new_user)
        db.session.commit()

        return render_template('register.html', message='Usuario registrado con éxito')

    return render_template('register.html')


if __name__ == '__main__':
    create_tables()
    app.run(debug=True, port=0)
