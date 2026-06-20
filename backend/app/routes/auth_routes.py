"""
Rutas de autenticación (MVC Route - solo mapea URL a Controller)
"""
from flask import Blueprint, request
from app.controllers.auth_controller import AuthController

auth_bp = Blueprint("auth", __name__)


@auth_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    """Registrar un nuevo usuario"""
    data = request.get_json()
    return AuthController.registrar(data)


@auth_bp.route('/login', methods=['POST'])
def login():
    """Iniciar sesión"""
    data = request.get_json()
    return AuthController.login(data)