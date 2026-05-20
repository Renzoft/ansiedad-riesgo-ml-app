from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.models.usuario import Usuario
from app.models.habito import Habito
from app.models.evaluacion import EvaluacionRiesgo

from app.services.recommendation_service import recommendation_service

recomendaciones_bp = Blueprint(
    "recomendaciones",
    __name__,
    url_prefix="/api/v1"
)


@recomendaciones_bp.route('/recomendaciones', methods=['GET'])
@jwt_required()
def obtener_recomendaciones():
    try:
        usuario_id = int(get_jwt_identity())

        # Última evaluación
        ultima_evaluacion = (
            EvaluacionRiesgo.query
            .filter_by(usuario_id=usuario_id)
            .order_by(EvaluacionRiesgo.created_at.desc())
            .first()
        )

        if not ultima_evaluacion:
            return jsonify({
                "mensaje": "Aún no tienes evaluaciones emocionales"
            }), 404

        # Último hábito
        ultimo_habito = (
            Habito.query
            .filter_by(usuario_id=usuario_id)
            .order_by(Habito.fecha.desc())
            .first()
        )

        recomendaciones = recommendation_service.generar_recomendaciones(
            ultima_evaluacion.categoria_riesgo,
            ultimo_habito
        )

        return jsonify({
            "categoria_riesgo": ultima_evaluacion.categoria_riesgo,
            "recomendaciones": recomendaciones
        }), 200

    except Exception as e:
        return jsonify({
            "error": str(e)
        }), 500