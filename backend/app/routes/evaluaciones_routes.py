"""
Rutas para Evaluación de Riesgo de Ansiedad (MVC Route - solo mapea URL a Controller)
Blueprint: evaluaciones_bp (prefijo /api/v1/evaluaciones)
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.roles import ROLE_ESTUDIANTE
from app.utils.decorators import role_required
from app.controllers.evaluacion_controller import EvaluacionController

evaluaciones_bp = Blueprint("evaluaciones", __name__, url_prefix="/api/v1/evaluaciones")


@evaluaciones_bp.route('/', methods=['POST'])
@jwt_required()
@role_required(ROLE_ESTUDIANTE)
def realizar_evaluacion():
    """Recibe las 15 variables, ejecuta el modelo ML y retorna resultado"""
    usuario_id = int(get_jwt_identity())
    data = request.get_json()
    return EvaluacionController.realizar_evaluacion(usuario_id, data)


@evaluaciones_bp.route('/historial', methods=['GET'])
@jwt_required()
@role_required(ROLE_ESTUDIANTE)
def historial_evaluaciones():
    """Retorna el historial de evaluaciones del usuario autenticado"""
    usuario_id = int(get_jwt_identity())
    return EvaluacionController.historial_evaluaciones(usuario_id)