"""
View de Evaluaciones - Serializa modelos a JSON (MVC View)
"""
from flask import jsonify


class EvaluacionView:
    """View: Convierte modelos de evaluación en respuestas JSON"""

    @staticmethod
    def render_resultado(resultado_dict):
        return jsonify(resultado_dict), 201

    @staticmethod
    def render_historial(evaluaciones_dict):
        return jsonify(evaluaciones_dict), 200

    @staticmethod
    def render_error(mensaje, status_code=400):
        return jsonify({"error": "Error", "mensaje": mensaje}), status_code

    @staticmethod
    def render_error_interno(mensaje):
        return jsonify({"error": "Error interno del servidor", "mensaje": str(mensaje)}), 500