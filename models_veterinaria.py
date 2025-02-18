from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Dueño(db.Model, UserMixin):
    __tablename__ = 'dueños'
    id = db.Column(db.Integer, primary_key=True)
    cedula = db.Column(db.String(20), unique=True, nullable=False)  # Campo cédula
    nombre = db.Column(db.String(100))
    correo = db.Column(db.String(100))
    telefono = db.Column(db.String(50))
    password_hash = db.Column(db.String(128))  # Contraseña hasheada
    is_admin = db.Column(db.Boolean, default=False)  # Para distinguir si es admin
    rol = db.Column(db.String(20))  # <-- Nuevo campo para rol

    # Relación con las mascotas
    mascotas = db.relationship('Mascota', backref='dueño', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def is_admin_user(self):
        return self.is_admin

    def __repr__(self):
        return f"<Dueño {self.nombre}, {self.cedula}>"



class Mascota(db.Model):
    __tablename__ = 'mascotas'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especie = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    dueño_id = db.Column(db.Integer, db.ForeignKey('dueños.id'), nullable=False)
    veterinario_id = db.Column(db.Integer, db.ForeignKey('veterinarios.id'), nullable=False)

    # Relación con Veterinario
    veterinario = db.relationship('Veterinario', backref='mascotas')

    def __repr__(self):
        return f"<Mascota {self.nombre}, {self.especie}, {self.edad} años>"

class Veterinario(db.Model):
    __tablename__ = 'veterinarios'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    
    # Relación con tratamientos
    tratamientos = db.relationship('Tratamiento', backref='veterinario', lazy=True)

    def __repr__(self):
        return f"<Veterinario {self.nombre}>"

class Tratamiento(db.Model):
    __tablename__ = 'tratamientos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100))
    descripcion = db.Column(db.String(255))
    veterinario_id = db.Column(db.Integer, db.ForeignKey('veterinarios.id'), nullable=False)

    def __repr__(self):
        return f"<Tratamiento {self.nombre}>"
