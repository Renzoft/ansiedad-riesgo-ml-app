"""
Modelo de Evaluacion de Riesgo
"""
from app.models.usuario import db
from datetime import datetime, date

class EvaluacionRiesgo(db.Model):
    """
    Clase de Evaluacion de Riesgo
    """
    __tablename__ = 'evaluacion_riesgo'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario', ondelete='CASCADE'), nullable=False)
    fecha = db.Column(db.Date, default=date.today)
    probabilidad_ansiedad = db.Column(db.Float)
    categoria_riesgo = db.Column(db.String(20))
    explicacion = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """
        Convierte el objeto a un diccionario para JSON
        """
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "probabilidad_ansiedad": self.probabilidad_ansiedad,
            "categoria_riesgo": self.categoria_riesgo,
            "explicacion": self.explicacion,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
