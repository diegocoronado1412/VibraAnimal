import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///vibra_animal.db'  # Puedes cambiarlo a PostgreSQL o MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)  # Para manejar sesiones seguras


