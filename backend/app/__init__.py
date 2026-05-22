"""
Módulo principal - Application Factory
"""
import os  # Manejo de variables de entorno
from flask import Flask  # Clase principal para crear la app
from flask_jwt_extended import JWTManager  # Manejo de JWT(JSON Web Tokens)
from datetime import timedelta  # Expiración de tokens

from app.models.usuario import db, bcrypt  # Modelo de usuario + extensiones
from app.routes.auth_routes import auth_bp  # Rutas de autenticación
from dotenv import load_dotenv  # Manejo de variables de entorno
from flask_migrate import Migrate

# Importar modelos para que SQLAlchemy/Migrate los detecte
from app.models.evaluacion import Evaluacion
from app.models.resultado_ml import ResultadoML
from app.models.recomendacion import Recomendacion, resultado_recomendaciones

from app.routes.evaluaciones_routes import evaluaciones_bp  # Rutas de evaluaciones
from app.routes.admin_routes import admin_bp  # Rutas administrativas

migrate = Migrate()  # Manejo de migraciones
jwt = JWTManager()  # Manejo de JWT(JSON Web Tokens)


def crear_app():
    """
    Función para crear la app
    """
    load_dotenv()  # Carga las variables de entorno
    app = Flask(__name__)

    # ==========================================
    # CONFIGURACIÓN DE LA BASE DE DATOS
    # ==========================================
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///base_datos.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ==========================================
    # CONFIGURACIÓN DE JWT (TOKENS)
    # ==========================================
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")  # Clave de encriptación
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)

    # ==========================================
    # INICIALIZACIÓN DE EXTENSIONES
    # ==========================================
    db.init_app(app)  # Inicialización de la base de datos
    bcrypt.init_app(app)  # Inicialización de la encriptación de contraseñas
    jwt.init_app(app)  # Inicialización de JWT(JSON Web Tokens)
    migrate.init_app(app, db)  # Inicialización de migraciones

    # ==========================================
    # REGISTRO DE BLUEPRINTS
    # ==========================================
    app.register_blueprint(auth_bp)
    app.register_blueprint(evaluaciones_bp)
    app.register_blueprint(admin_bp)

    # ==========================================
    # COMANDOS CLI
    # ==========================================
    @app.cli.command("init-db")
    def init_db():
        """Inicializa la base de datos creando las tablas"""
        db.create_all()
        print("Tablas creadas correctamente.")

    @app.cli.command("init-recomendaciones")
    def init_recomendaciones():
        """Precarga la tabla 'recomendaciones' con 3 registros base (BAJO, MEDIO, ALTO)"""
        from app.models.recomendacion import Recomendacion as Rec

        # Verificar si ya existen recomendaciones
        existentes = Rec.query.count()
        if existentes > 0:
            print(f"Ya existen {existentes} recomendaciones en la base de datos. No se insertaron nuevas.")
            return

        recomendaciones_base = [
            Rec(
                categoria="BAJO",
                titulo="Mantén tus hábitos saludables",
                descripcion="Tus indicadores muestran un equilibrio saludable. "
                            "Continúa con tus rutinas de sueño, ejercicio y alimentación. "
                            "Considera practicar mindfulness para mantener tu bienestar."
            ),
            Rec(
                categoria="MEDIO",
                titulo="Refuerza tus estrategias de manejo del estrés",
                descripcion="Se detectan ciertos niveles de alerta en tus indicadores. "
                            "Revisa tus horas de sueño, incorpora pausas activas durante el estudio "
                            "y busca apoyo en tus compañeros o familiares. "
                            "Considera consultar con el servicio de bienestar estudiantil."
            ),
            Rec(
                categoria="ALTO",
                titulo="Busca apoyo profesional",
                descripcion="Tus indicadores sugieren una alta predisposición a ansiedad. "
                            "Es importante que acudas al departamento de bienestar estudiantil "
                            "o a un profesional de salud mental. No estás solo/a, "
                            "hay recursos disponibles para apoyarte."
            ),
        ]

        try:
            db.session.add_all(recomendaciones_base)
            db.session.commit()
            print("3 recomendaciones base insertadas correctamente (BAJO, MEDIO, ALTO).")
        except Exception as e:
            db.session.rollback()
            print(f"Error al insertar recomendaciones: {str(e)}")

    return app
