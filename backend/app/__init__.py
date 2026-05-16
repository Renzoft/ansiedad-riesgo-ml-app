"""
Módulo principal
"""
import os #Manejo de variables de entorno
from flask import Flask #Clase principal para crear la app
from flask_jwt_extended import JWTManager #Manejo de JWT(JSON Web Tokens)
from datetime import timedelta #Expiración de tokens

from app.models.usuario import db,bcrypt #Modelo de usuario
from app.routes.auth_routes import auth_bp #Rutas de autenticación
from dotenv import load_dotenv #Manejo de variables de entorno

jwt = JWTManager() #Manejo de JWT(JSON Web Tokens)

def crear_app():
    """
    Función para crear la app
    """
    load_dotenv()#Carga las variables de entorno
    app = Flask(__name__)
    # ==========================================
    # CONFIGURACIÓN DE LA BASE DE DATOS
    # ==========================================
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_datos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ==========================================
    # CONFIGURACIÓN DE JWT (TOKENS)
    # ==========================================
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")#Clave de encriptación
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

    # ==========================================
    # INICIALIZACIÓN DE EXTENSIONES
    # ==========================================
    db.init_app(app) #Inicialización de la base de datos
    bcrypt.init_app(app) #Inicialización de la encriptación de contraseñas
    jwt.init_app(app) #Inicialización de JWT(JSON Web Tokens)

    # ==========================================
    # CREACIÓN DE TABLAS
    # ==========================================

    with app.app_context():
        db.create_all()
    
    app.register_blueprint(auth_bp)
    return app
