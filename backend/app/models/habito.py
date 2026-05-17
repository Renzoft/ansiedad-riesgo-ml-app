"""
Modelo de Habito (Indicadores de estilo de vida)
"""
from app.models.usuario import db
from datetime import datetime

class Habito(db.Model):
    """
    Clase de Habito (Indicadores de Estilo de Vida)
    """
    __tablename__ = 'habito'

    id = db.Column(db.Integer, primary_key=True)
    usuario_id = db.Column(db.Integer, db.ForeignKey('usuario.id_usuario'), nullable=False)
    fecha = db.Column(db.Date, nullable=False)
    
    # Indicadores
    sleep_hours = db.Column(db.Float, nullable=False)
    exercise_freq = db.Column(db.Integer, nullable=False)
    social_activity = db.Column(db.Float, nullable=False)
    screen_time = db.Column(db.Float, nullable=False)
    diet_quality = db.Column(db.Float, nullable=False)
    sleep_quality = db.Column(db.Float, nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Restricción: Un solo registro de hábito por usuario por día
    __table_args__ = (
        db.UniqueConstraint('usuario_id', 'fecha', name='uq_usuario_fecha'),
    )

    def to_dict(self):
        """
        Convierte el objeto a un diccionario para JSON
        """
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "fecha": self.fecha.isoformat() if self.fecha else None,
            "sleep_hours": self.sleep_hours,
            "exercise_freq": self.exercise_freq,
            "social_activity": self.social_activity,
            "screen_time": self.screen_time,
            "diet_quality": self.diet_quality,
            "sleep_quality": self.sleep_quality,
            "created_at": self.created_at.isoformat() if self.created_at else None
        }
