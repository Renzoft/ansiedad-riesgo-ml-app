"""
Modelo de Evaluación - Almacena las 15 variables del test por cada evaluación rendida.
"""
from app.models.usuario import db
from datetime import datetime


class Evaluacion(db.Model):
    """
    Cada registro representa un test completo rendido por un estudiante.
    Contiene las 15 variables numéricas que alimentan el modelo de ML.
    """
    __tablename__ = 'evaluacion'

    id_evaluacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'),
                           nullable=False)
    fecha_realizacion = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # 15 VARIABLES DEL MODELO ML
    # =========================
    phq9_score = db.Column(db.Float, nullable=False)         # Rango: 0-27
    gad7_score = db.Column(db.Float, nullable=False)         # Rango: 0-21
    sleep_hours = db.Column(db.Float, nullable=False)        # Rango: 3.0-10.0
    exercise_freq = db.Column(db.Float, nullable=False)      # Rango: 0-7
    social_activity = db.Column(db.Float, nullable=False)    # Rango: 0-10
    online_stress = db.Column(db.Float, nullable=False)      # Rango: 1-10
    gpa = db.Column(db.Float, nullable=False)                # Rango: 0.0-5.0
    family_support = db.Column(db.Float, nullable=False)     # Rango: 1-10
    screen_time = db.Column(db.Float, nullable=False)        # Rango: 1.0-12.0
    academic_stress = db.Column(db.Float, nullable=False)    # Rango: 1-10
    diet_quality = db.Column(db.Float, nullable=False)       # Rango: 1-10
    self_efficacy = db.Column(db.Float, nullable=False)      # Rango: 1-10
    peer_relationship = db.Column(db.Float, nullable=False)  # Rango: 1-10
    financial_stress = db.Column(db.Float, nullable=False)   # Rango: 1-10
    sleep_quality = db.Column(db.Float, nullable=False)      # Rango: 0-10

    # =========================
    # RELACIÓN 1:1 CON RESULTADO ML
    # =========================
    resultado = db.relationship('ResultadoML', backref='evaluacion', uselist=False,
                                cascade='all, delete-orphan')

    def to_vector(self):
        """
        Retorna las 15 variables como lista en el ORDEN ESTRICTO
        requerido por el modelo de ML.
        """
        return [
            self.phq9_score,
            self.gad7_score,
            self.sleep_hours,
            self.exercise_freq,
            self.social_activity,
            self.online_stress,
            self.gpa,
            self.family_support,
            self.screen_time,
            self.academic_stress,
            self.diet_quality,
            self.self_efficacy,
            self.peer_relationship,
            self.financial_stress,
            self.sleep_quality
        ]

    def to_dict(self):
        """
        Convierte el objeto a un diccionario para JSON.
        Incluye el resultado ML anidado si existe.
        """
        data = {
            "id_evaluacion": self.id_evaluacion,
            "id_usuario": self.id_usuario,
            "fecha_realizacion": self.fecha_realizacion.isoformat() if self.fecha_realizacion else None,
            "phq9_score": self.phq9_score,
            "gad7_score": self.gad7_score,
            "sleep_hours": self.sleep_hours,
            "exercise_freq": self.exercise_freq,
            "social_activity": self.social_activity,
            "online_stress": self.online_stress,
            "gpa": self.gpa,
            "family_support": self.family_support,
            "screen_time": self.screen_time,
            "academic_stress": self.academic_stress,
            "diet_quality": self.diet_quality,
            "self_efficacy": self.self_efficacy,
            "peer_relationship": self.peer_relationship,
            "financial_stress": self.financial_stress,
            "sleep_quality": self.sleep_quality,
            "resultado": self.resultado.to_dict() if self.resultado else None
        }
        return data
