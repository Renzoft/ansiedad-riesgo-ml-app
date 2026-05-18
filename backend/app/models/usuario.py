"""
Modelo de usuario
"""
from flask_sqlalchemy import SQLAlchemy #Permite definir tablas de base de datos
from flask_bcrypt import  Bcrypt #Permite encriptar contraseñas
from datetime import datetime #Permite manejar fechas

db = SQLAlchemy() #Instancia de la base de datos
bcrypt = Bcrypt()  # Instancia de la encriptación de contraseñas


class Usuario(db.Model):
    """
    Clase de usuario
    """

    __tablename__ = 'usuario'#Nombre de la tabla

    id_usuario = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    rol = db.Column(db.String(20), nullable=False)
    correo = db.Column(db.String(100), unique = True, nullable=False)
    contrasena = db.Column(db.String(255), nullable=False)
    facultad = db.Column(db.String(100))
    ciclo = db.Column(db.Integer)
    fecha_registro = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # VARIABLES ACADÉMICAS Y PSICOSOCIALES
    # =========================
    phq9 = db.Column(db.Integer, default=0)
    gad7 = db.Column(db.Integer, default=0)
    online_stress = db.Column(db.Integer, default=0)
    financial_stress = db.Column(db.Integer, default=0)
    academic_stress = db.Column(db.Integer, default=0)
    gpa = db.Column(db.Float, default=0.0)
    family_support = db.Column(db.Integer, default=0)
    self_efficacy = db.Column(db.Integer, default=0)
    peer_relationship = db.Column(db.Integer, default=0)

    # =========================
    # MÉTODOS AUTH
    # =========================
    def establecer_contrasena(self, contrasena):
        """
        Encripta la contraseña
        """
        self.contrasena = bcrypt.generate_password_hash(contrasena).decode('utf-8')

    def verificar_contrasena(self, contrasena):
        """
        Verifica si la contraseña ingresada coincide con el hash
        """

        return bcrypt.check_password_hash(self.contrasena,contrasena)
