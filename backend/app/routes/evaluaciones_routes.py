"""
Rutas para Evaluación de Riesgo de Ansiedad
Blueprint: evaluaciones_bp (prefijo /api/v1/evaluaciones)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.usuario import db, Usuario
from app.models.evaluacion import Evaluacion
from app.models.resultado_ml import ResultadoML
from app.models.recomendacion import Recomendacion
from app.services.ml_service import predictor

evaluaciones_bp = Blueprint("evaluaciones", __name__, url_prefix="/api/v1/evaluaciones")

# =========================
# RANGOS VÁLIDOS PARA LAS 15 VARIABLES
# =========================
RANGOS_VARIABLES = {
    "phq9_score":        (0, 27),
    "gad7_score":        (0, 21),
    "sleep_hours":       (3.0, 10.0),
    "exercise_freq":     (0, 7),
    "social_activity":   (0, 10),
    "online_stress":     (1, 10),
    "gpa":               (0.0, 5.0),
    "family_support":    (1, 10),
    "screen_time":       (1.0, 12.0),
    "academic_stress":   (1, 10),
    "diet_quality":      (1, 10),
    "self_efficacy":     (1, 10),
    "peer_relationship": (1, 10),
    "financial_stress":  (1, 10),
    "sleep_quality":     (0, 10),
}

# Orden estricto de las variables para el vector ML
ORDEN_VARIABLES = [
    "phq9_score", "gad7_score", "sleep_hours", "exercise_freq",
    "social_activity", "online_stress", "gpa", "family_support",
    "screen_time", "academic_stress", "diet_quality", "self_efficacy",
    "peer_relationship", "financial_stress", "sleep_quality"
]


def _validar_variables(data):
    """
    Valida que las 15 variables estén presentes, sean numéricas y dentro de rango.
    Retorna (valores_dict, None) si es válido, o (None, error_response) si falla.
    """
    valores = {}
    for variable, (minimo, maximo) in RANGOS_VARIABLES.items():
        valor = data.get(variable)

        # Validar presencia
        if valor is None:
            return None, (
                jsonify({"error": "Campo faltante", "mensaje": f"El campo '{variable}' es obligatorio"}),
                400
            )

        # Validar tipo numérico
        try:
            valor = float(valor)
        except (ValueError, TypeError):
            return None, (
                jsonify({"error": "Tipo inválido", "mensaje": f"El campo '{variable}' debe ser numérico"}),
                400
            )

        # Validar rango
        if not (minimo <= valor <= maximo):
            return None, (
                jsonify({
                    "error": "Fuera de rango",
                    "mensaje": f"'{variable}' debe estar entre {minimo} y {maximo}. Recibido: {valor}"
                }),
                400
            )

        valores[variable] = valor

    return valores, None


def _categorizar_riesgo(probabilidad):
    """
    Clasifica la probabilidad en nivel de riesgo y genera explicación.
    """
    if probabilidad < 0.35:
        nivel = 'BAJO'
        explicacion = "Tus indicadores muestran un equilibrio saludable. Continúa manteniendo estas rutinas."
    elif probabilidad <= 0.70:
        nivel = 'MEDIO'
        explicacion = "Se detectan ciertos niveles de alerta. Revisa tus horas de sueño y pausas activas."
    else:
        nivel = 'ALTO'
        explicacion = "Alta predisposición a ansiedad. Busca orientación en el departamento de bienestar estudiantil."

    return nivel, explicacion


# ==========================================
# POST /  →  Realizar evaluación completa
# ==========================================
@evaluaciones_bp.route('/', methods=['POST'])
@jwt_required()
def realizar_evaluacion():
    """
    Recibe las 15 variables, las persiste en 'evaluacion', ejecuta el modelo ML,
    guarda el resultado en 'resultados_ml' y asocia las recomendaciones.
    """
    try:
        # 1. Obtener usuario_id desde el JWT
        usuario_id = int(get_jwt_identity())

        # 2. Verificar que el usuario existe
        usuario = Usuario.query.get(usuario_id)
        if not usuario:
            return jsonify({"error": "No encontrado", "mensaje": "Usuario no encontrado"}), 404

        # 3. Obtener y validar datos del JSON
        data = request.get_json()
        if not data:
            return jsonify({"error": "Sin datos", "mensaje": "No se enviaron datos en el cuerpo de la petición"}), 400

        valores, error = _validar_variables(data)
        if error:
            return error

        # 4. Crear y guardar registro en tabla 'evaluacion'
        nueva_evaluacion = Evaluacion(
            id_usuario=usuario_id,
            **valores
        )
        db.session.add(nueva_evaluacion)
        db.session.flush()  # Obtener id_evaluacion sin commit

        # 5. Construir vector y ejecutar predicción ML
        vector = nueva_evaluacion.to_vector()
        probabilidad = predictor.predecir(vector)

        # 6. Categorizar riesgo
        nivel_riesgo, explicacion = _categorizar_riesgo(probabilidad)

        # 7. Crear y guardar registro en tabla 'resultados_ml'
        nuevo_resultado = ResultadoML(
            id_evaluacion=nueva_evaluacion.id_evaluacion,
            id_usuario=usuario_id,
            probabilidad_ansiedad=probabilidad,
            nivel_riesgo=nivel_riesgo
        )
        db.session.add(nuevo_resultado)
        db.session.flush()  # Obtener id_resultado para asociar recomendaciones

        # 8. Buscar recomendaciones que coincidan con el nivel de riesgo y asociar
        recomendaciones = Recomendacion.query.filter_by(categoria=nivel_riesgo).all()
        for recomendacion in recomendaciones:
            nuevo_resultado.recomendaciones.append(recomendacion)

        # 9. Commit de toda la transacción
        db.session.commit()

        # 10. Construir respuesta
        respuesta = {
            "id_evaluacion": nueva_evaluacion.id_evaluacion,
            "probabilidad_ansiedad": probabilidad,
            "nivel_riesgo": nivel_riesgo,
            "explicacion": explicacion,
            "fecha_realizacion": nueva_evaluacion.fecha_realizacion.isoformat(),
            "recomendaciones": [r.to_dict() for r in recomendaciones]
        }

        return jsonify(respuesta), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno del servidor", "mensaje": str(e)}), 500


# ==========================================
# GET /historial  →  Historial de evaluaciones
# ==========================================
@evaluaciones_bp.route('/historial', methods=['GET'])
@jwt_required()
def historial_evaluaciones():
    """
    Retorna todas las evaluaciones del usuario autenticado con sus
    resultados ML y recomendaciones anidadas, en orden descendente.
    """
    try:
        usuario_id = int(get_jwt_identity())

        # Consultar evaluaciones ordenadas por fecha descendente
        evaluaciones = Evaluacion.query.filter_by(id_usuario=usuario_id)\
                                       .order_by(Evaluacion.fecha_realizacion.desc()).all()

        resultado = [evaluacion.to_dict() for evaluacion in evaluaciones]
        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": "Error interno del servidor", "mensaje": str(e)}), 500
