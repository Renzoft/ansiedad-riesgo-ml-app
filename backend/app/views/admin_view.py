"""
View de Administración - Serializa modelos a JSON (MVC View)
"""
from flask import jsonify


class AdminView:
    """View: Convierte modelos de administración en respuestas JSON"""

    @staticmethod
    def render_usuario(usuario_dict, mensaje=None):
        if mensaje:
            return jsonify({"mensaje": mensaje, "usuario": usuario_dict}), 200
        return jsonify(usuario_dict), 200

    @staticmethod
    def render_usuario_creado(usuario_dict):
        return jsonify({
            "mensaje": "Usuario creado correctamente",
            "usuario": usuario_dict
        }), 201

    @staticmethod
    def render_lista_usuarios(usuarios_dict):
        return jsonify(usuarios_dict), 200

    @staticmethod
    def render_estadisticas(estadisticas_dict):
        return jsonify(estadisticas_dict), 200

    @staticmethod
    def render_mensaje(mensaje, status_code=200):
        return jsonify({"mensaje": mensaje}), status_code

    @staticmethod
    def render_error(mensaje, status_code=400):
        return jsonify({"error": "Error", "mensaje": mensaje}), status_code

    @staticmethod
    def render_error_interno(mensaje):
        return jsonify({"error": "Error interno", "mensaje": str(mensaje)}), 500