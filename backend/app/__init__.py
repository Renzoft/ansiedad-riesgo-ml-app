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
from flask_migrate import Migrate

from app.models.habito import Habito # Importar modelo para que SQLAlchemy/Migrate lo detecte
from app.routes.habitos_routes import habitos_bp #Rutas de hábitos
from app.models.evaluacion import EvaluacionRiesgo # Modelo Evaluacion de Riesgo
from app.routes.evaluaciones_routes import evaluaciones_bp # Rutas Evaluacion de Riesgo
migrate = Migrate() #Manejo de migraciones
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
    migrate.init_app(app,db) #Inicialización de migraciones
    # ==========================================
    # CREACIÓN DE TABLAS
    # ==========================================
    app.register_blueprint(auth_bp)
    app.register_blueprint(habitos_bp)
    app.register_blueprint(evaluaciones_bp)

    # Comando CLI para inicializar la base de datos manualmente
    @app.cli.command("init-db")
    def init_db():
        """Inicializa la base de datos creando las tablas"""
        db.create_all()
        print("Tablas creadas correctamente.")

    return app
