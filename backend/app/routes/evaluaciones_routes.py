"""
Rutas para Evaluación y Riesgo Emocional
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.usuario import db, Usuario
from app.models.habito import Habito
from app.models.evaluacion import EvaluacionRiesgo
from app.services.ml_service import predictor
from flask import request
from datetime import datetime, timedelta, timezone

evaluaciones_bp = Blueprint("evaluaciones", __name__, url_prefix="/api/v1")

@evaluaciones_bp.route('/evaluaciones/evaluar', methods=['POST'])
@jwt_required()
def evaluar_riesgo():
    """
    Estima el riesgo de ansiedad del usuario actual (HU-11)
    """
    try:
        # 1. Obtener usuario_id desde el token
        usuario_id = int(get_jwt_identity())

        # 2. Consultar usuario
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"error": "No encontrado", "mensaje": "Usuario no encontrado"}), 404

        # 3. Consultar el último registro de hábito
        ultimo_habito = Habito.query.filter_by(usuario_id=usuario_id).order_by(Habito.fecha.desc()).first()

        # 4. Validación Crítica
        if not ultimo_habito:
            return jsonify({
                "error": "Datos insuficientes", 
                "mensaje": "Debes registrar tus indicadores de estilo de vida de al menos un día para poder realizar la estimación de riesgo emocional."
            }), 400

        # 5. Construir el vector de 15 características en el ORDEN ESTRICTO:
        # [phq9, gad7, sleep_hours, exercise_freq, social_activity, online_stress,
        #  gpa, family_support, screen_time, academic_stress, diet_quality,
        #  self_efficacy, peer_relationship, financial_stress, sleep_quality]
        vector_caracteristicas = [
            float(usuario.phq9),
            float(usuario.gad7),
            float(ultimo_habito.sleep_hours),
            float(ultimo_habito.exercise_freq),
            float(ultimo_habito.social_activity),
            float(usuario.online_stress),
            float(usuario.gpa),
            float(usuario.family_support),
            float(ultimo_habito.screen_time),
            float(usuario.academic_stress),
            float(ultimo_habito.diet_quality),
            float(usuario.self_efficacy),
            float(usuario.peer_relationship),
            float(usuario.financial_stress),
            float(ultimo_habito.sleep_quality)
        ]

        # 6. Invocar predecir
        probabilidad = predictor.predecir(vector_caracteristicas)

        # 7. Categorización (TR15)
        if probabilidad < 0.35:
            categoria = 'BAJO'
            explicacion = "Tus indicadores muestran un equilibrio saludable. Continúa manteniendo estas rutinas."
        elif 0.35 <= probabilidad <= 0.70:
            categoria = 'MEDIO'
            explicacion = "Se detectan ciertos niveles de alerta. Revisa tus horas de sueño y pausas activas."
        else:
            categoria = 'ALTO'
            explicacion = "Alta predisposición a ansiedad. Busca orientación en el departamento de bienestar estudiantil."

        # 8. Guardar en base de datos
        nueva_evaluacion = EvaluacionRiesgo(
            usuario_id=usuario_id,
            probabilidad_ansiedad=probabilidad,
            categoria_riesgo=categoria,
            explicacion=explicacion
        )

        db.session.add(nueva_evaluacion)
        db.session.commit()

        return jsonify(nueva_evaluacion.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "mensaje": str(e)}), 500


@evaluaciones_bp.route("/evaluaciones/historial", methods=["GET"])
@jwt_required()
def historial_evaluaciones():
    """
    Retorna historial emocional para gráficas
    """

    try:
        usuario_id = int(get_jwt_identity())

        periodo = request.args.get("periodo", "mes")

        fecha_limite = datetime.now(timezone.utc)

        if periodo == "mes":
            fecha_limite = fecha_limite - timedelta(days=30)

        elif periodo == "trimestre":
            fecha_limite = fecha_limite - timedelta(days=90)

        elif periodo == "anio":
            fecha_limite = fecha_limite - timedelta(days=365)

        evaluaciones = (
            EvaluacionRiesgo.query.filter(
                EvaluacionRiesgo.usuario_id == usuario_id,
                EvaluacionRiesgo.created_at >= fecha_limite,
            )
            .order_by(EvaluacionRiesgo.created_at.asc())
            .all()
        )

        resultado = []

        for evaluacion in evaluaciones:

            habito = Habito.query.filter_by(
                usuario_id=usuario_id, fecha=evaluacion.fecha
            ).first()

            resultado.append(
                {
                    "fecha": evaluacion.fecha.isoformat(),
                    "probabilidad_ansiedad": evaluacion.probabilidad_ansiedad,
                    "categoria_riesgo": evaluacion.categoria_riesgo,
                    "explicacion": evaluacion.explicacion,
                    # TOOLTIP DATA
                    "habitos": {
                        "sleep_hours": habito.sleep_hours if habito else None,
                        "exercise_freq": habito.exercise_freq if habito else None,
                        "screen_time": habito.screen_time if habito else None,
                        "diet_quality": habito.diet_quality if habito else None,
                        "sleep_quality": habito.sleep_quality if habito else None,
                    },
                }
            )

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
