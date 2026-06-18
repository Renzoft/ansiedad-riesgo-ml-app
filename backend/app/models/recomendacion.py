"""
Modelo de Recomendación y tabla asociativa resultado_recomendaciones.
"""
from app.models.usuario import db


# =========================
# TABLA ASOCIATIVA (Muchos a Muchos)
# =========================
resultado_recomendaciones = db.Table(
    'resultado_recomendaciones',
    db.Column('id_resultado', db.Integer,
              db.ForeignKey('resultados_ml.id_resultado', ondelete='CASCADE'),
              primary_key=True),
    db.Column('id_recomendacion', db.Integer,
              db.ForeignKey('recomendaciones.id_recomendacion', ondelete='CASCADE'),
              primary_key=True)
)


class Recomendacion(db.Model):
    """
    Catálogo de recomendaciones pre-cargadas, agrupadas por categoría
    (BAJO, MEDIO, ALTO) para vincular con los resultados del modelo ML.
    """
    __tablename__ = 'recomendaciones'

    id_recomendacion = db.Column(db.Integer, primary_key=True, autoincrement=True)
    categoria = db.Column(db.String(50), nullable=False)   # 'BAJO', 'MEDIO', 'ALTO'
    titulo = db.Column(db.String(150), nullable=False)
    descripcion = db.Column(db.Text, nullable=False)

    def to_dict(self):
        """
        Convierte el objeto a un diccionario para JSON
        """
        return {
            "id_recomendacion": self.id_recomendacion,
            "categoria": self.categoria,
            "titulo": self.titulo,
            "descripcion": self.descripcion
        }
