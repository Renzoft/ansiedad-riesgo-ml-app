"""
Modelo de Usuario
"""
from flask_sqlalchemy import SQLAlchemy  # Permite definir tablas de base de datos
from flask_bcrypt import Bcrypt  # Permite encriptar contraseñas
from datetime import datetime  # Permite manejar fechas

db = SQLAlchemy()  # Instancia de la base de datos
bcrypt = Bcrypt()  # Instancia de la encriptación de contraseñas


class Usuario(db.Model):
    """
    Clase de Usuario - Tabla principal de cuentas de estudiantes.
    Solo almacena datos de perfil, sin variables ML.
    """

    __tablename__ = 'usuarios'  # Nombre de la tabla (plural, según diagrama oficial)

    id_usuario = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nombre = db.Column(db.String(100), nullable=False)
    correo = db.Column(db.String(100), unique=True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    facultad = db.Column(db.String(100))
    ciclo = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)
    rol = db.Column(db.String(20), default='estudiante')

    # =========================
    # RELACIONES
    # =========================
    evaluaciones = db.relationship('Evaluacion', backref='usuario', lazy=True,
                                   cascade='all, delete-orphan')
    resultados = db.relationship('ResultadoML', backref='usuario', lazy=True,
                                 cascade='all, delete-orphan')

    # =========================
    # MÉTODOS AUTH
    # =========================
    def establecer_contrasena(self, contrasena):
        """
        Encripta la contraseña
        """
        self.contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')

    def verificar_contrasena(self, contrasena):
        """
        Verifica si la contraseña ingresada coincide con el hash
        """
        return bcrypt.check_password_hash(self.contrasena, contrasena)

    def to_dict(self):
        """
        Convierte el objeto a un diccionario para JSON
        """
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "correo": self.correo,
            "facultad": self.facultad,
            "ciclo": self.ciclo,
            "fecha_registro": self.fecha_registro.isoformat() if self.fecha_registro else None,
            "rol": self.rol
        }
