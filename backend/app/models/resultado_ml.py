"""
Modelo de Resultado ML - Almacena la predicción del modelo de Machine Learning.
"""
from app.models.usuario import db
from datetime import datetime


class ResultadoML(db.Model):
    """
    Cada registro almacena el resultado de una predicción de riesgo de ansiedad,
    vinculado a una evaluación específica y al usuario.
    """
    __tablename__ = 'resultados_ml'

    id_resultado = db.Column(db.Integer, primary_key=True, autoincrement=True)
    id_evaluacion = db.Column(db.Integer,
                              db.ForeignKey('evaluacion.id_evaluacion', ondelete='CASCADE'),
                              nullable=False, unique=True)
    id_usuario = db.Column(db.Integer,
                           db.ForeignKey('usuarios.id_usuario', ondelete='CASCADE'),
                           nullable=False)
    probabilidad_ansiedad = db.Column(db.Float, nullable=False)
    nivel_riesgo = db.Column(db.String(20), nullable=False)  # 'BAJO', 'MEDIO', 'ALTO'
    fecha_prediccion = db.Column(db.DateTime, default=datetime.utcnow)

    # =========================
    # RELACIÓN M:N CON RECOMENDACIONES
    # =========================
    recomendaciones = db.relationship(
        'Recomendacion',
        secondary='resultado_recomendaciones',
        backref=db.backref('resultados', lazy='dynamic'),
        lazy='joined'
    )

    def to_dict(self):
        """
        Convierte el objeto a un diccionario para JSON.
        Incluye la lista de recomendaciones anidadas.
        """
        return {
            "id_resultado": self.id_resultado,
            "id_evaluacion": self.id_evaluacion,
            "id_usuario": self.id_usuario,
            "probabilidad_ansiedad": self.probabilidad_ansiedad,
            "nivel_riesgo": self.nivel_riesgo,
            "fecha_prediccion": self.fecha_prediccion.isoformat() if self.fecha_prediccion else None,
            "recomendaciones": [r.to_dict() for r in self.recomendaciones]
        }
