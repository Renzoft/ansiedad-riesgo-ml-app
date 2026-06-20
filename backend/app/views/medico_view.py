"""
View de Médico - Serializa modelos a JSON (MVC View)
"""
from flask import jsonify


class MedicoView:
    """View: Convierte modelos del médico en respuestas JSON"""

    @staticmethod
    def render_lista_pacientes(pacientes_dict):
        return jsonify(pacientes_dict), 200

    @staticmethod
    def render_detalle_paciente(detalle_dict):
        return jsonify(detalle_dict), 200

    @staticmethod
    def render_estadisticas(estadisticas_dict):
        return jsonify(estadisticas_dict), 200

    @staticmethod
    def render_evaluaciones_recientes(lista_dict):
        return jsonify(lista_dict), 200

    @staticmethod
    def render_error(mensaje, status_code=400):
        return jsonify({"error": "Error", "mensaje": mensaje}), status_code

    @staticmethod
    def render_error_interno(mensaje):
        return jsonify({"error": "Error interno", "mensaje": str(mensaje)}), 500