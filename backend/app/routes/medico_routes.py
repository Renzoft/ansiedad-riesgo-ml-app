"""
Rutas para el rol Médico - Acceso exclusivo para ROLE_MEDICO y ROLE_ADMIN
Blueprint: medico_bp (prefijo /api/v1/medico)
"""
from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.usuario import db, Usuario
from app.models.evaluacion import Evaluacion
from app.models.resultado_ml import ResultadoML
from app.utils.roles import ROLE_MEDICO, ROLE_ADMIN
from app.utils.decorators import role_required

medico_bp = Blueprint("medico", __name__, url_prefix="/api/v1/medico")


# ==========================================
# GET /pacientes  →  Lista de pacientes (estudiantes)
# ==========================================
@medico_bp.route('/pacientes', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def listar_pacientes():
    """
    Retorna la lista de pacientes (usuarios con rol Estudiante)
    con información básica y su última evaluación si existe.
    """
    try:
        pacientes = Usuario.query.filter_by(rol='Estudiante')\
                                  .order_by(Usuario.fecha_registro.desc()).all()

        resultado = []
        for p in pacientes:
            data = p.to_dict()
            # Obtener última evaluación
            ultima_eval = Evaluacion.query.filter_by(id_usuario=p.id_usuario)\
                                           .order_by(Evaluacion.fecha_realizacion.desc()).first()
            if ultima_eval and ultima_eval.resultado:
                data["ultimo_riesgo"] = ultima_eval.resultado.nivel_riesgo
                data["ultima_probabilidad"] = ultima_eval.resultado.probabilidad_ansiedad
                data["ultima_evaluacion_fecha"] = ultima_eval.fecha_realizacion.isoformat() if ultima_eval.fecha_realizacion else None
            else:
                data["ultimo_riesgo"] = None
                data["ultima_probabilidad"] = None
                data["ultima_evaluacion_fecha"] = None

            resultado.append(data)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# GET /estadisticas  →  Estadísticas del médico
# ==========================================
@medico_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def estadisticas():
    """
    Retorna estadísticas generales para el panel del médico:
    - Total de pacientes (estudiantes)
    - Total de evaluaciones realizadas
    - Distribución de niveles de riesgo
    """
    try:
        total_pacientes = Usuario.query.filter_by(rol='Estudiante').count()
        total_evaluaciones = Evaluacion.query.count()

        riesgo_bajo = ResultadoML.query.filter_by(nivel_riesgo='BAJO').count()
        riesgo_medio = ResultadoML.query.filter_by(nivel_riesgo='MEDIO').count()
        riesgo_alto = ResultadoML.query.filter_by(nivel_riesgo='ALTO').count()

        return jsonify({
            "total_pacientes": total_pacientes,
            "total_evaluaciones": total_evaluaciones,
            "distribucion_riesgo": {
                "bajo": riesgo_bajo,
                "medio": riesgo_medio,
                "alto": riesgo_alto
            }
        }), 200

    except Exception as e:
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# GET /evaluaciones-recientes  →  Últimas evaluaciones de todos los pacientes
# ==========================================
@medico_bp.route('/evaluaciones-recientes', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def evaluaciones_recientes():
    """
    Retorna las últimas 20 evaluaciones realizadas por cualquier paciente,
    incluyendo nombre del paciente, nivel de riesgo, probabilidad y fecha.
    """
    try:
        evaluaciones = Evaluacion.query\
            .join(Usuario, Evaluacion.id_usuario == Usuario.id_usuario)\
            .order_by(Evaluacion.fecha_realizacion.desc())\
            .limit(20).all()

        resultado = []
        for eval in evaluaciones:
            item = {
                "id_evaluacion": eval.id_evaluacion,
                "id_usuario": eval.id_usuario,
                "nombre_paciente": eval.usuario.nombre,
                "correo_paciente": eval.usuario.correo,
                "fecha_realizacion": eval.fecha_realizacion.isoformat() if eval.fecha_realizacion else None,
            }
            if eval.resultado:
                item["nivel_riesgo"] = eval.resultado.nivel_riesgo
                item["probabilidad_ansiedad"] = eval.resultado.probabilidad_ansiedad
                item["fecha_prediccion"] = eval.resultado.fecha_prediccion.isoformat() if eval.resultado.fecha_prediccion else None
            else:
                item["nivel_riesgo"] = None
                item["probabilidad_ansiedad"] = None
                item["fecha_prediccion"] = None

            resultado.append(item)

        return jsonify(resultado), 200

    except Exception as e:
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# GET /pacientes/<id>/detalle  →  Detalle completo de un paciente
# ==========================================
@medico_bp.route('/pacientes/<int:id_usuario>/detalle', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def detalle_paciente(id_usuario):
    """
    Retorna la información detallada de un paciente específico,
    incluyendo el historial completo de evaluaciones con resultados ML.
    """
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return jsonify({"error": "No encontrado", "mensaje": "Paciente no encontrado"}), 404

        if usuario.rol != 'Estudiante':
            return jsonify({"error": "Acceso denegado", "mensaje": "El usuario no es un paciente"}), 403

        data = usuario.to_dict()

        evaluaciones = Evaluacion.query.filter_by(id_usuario=id_usuario)\
                                       .order_by(Evaluacion.fecha_realizacion.desc()).all()
        data["evaluaciones"] = [e.to_dict() for e in evaluaciones]
        data["total_evaluaciones"] = len(evaluaciones)

        return jsonify(data), 200

    except Exception as e:
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500