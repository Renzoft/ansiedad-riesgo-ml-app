"""
View de Autenticación - Serializa modelos a JSON (MVC View)
"""
from flask import jsonify


class AuthView:
    """View: Convierte modelos de autenticación en respuestas JSON"""

    @staticmethod
    def render_registro_exitoso():
        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    @staticmethod
    def render_login_exitoso(token, usuario_dict):
        return jsonify({
            "mensaje": "Login exitoso",
            "token": token,
            "usuario": usuario_dict,
        }), 200

    @staticmethod
    def render_error(mensaje, status_code=400):
        return jsonify({"mensaje": mensaje}), status_code

    @staticmethod
    def render_error_interno(mensaje):
        return jsonify({"error": "Error al registrar usuario", "mensaje": mensaje}), 500