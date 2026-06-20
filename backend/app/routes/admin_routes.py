"""
Rutas administrativas - Acceso exclusivo para ROLE_ADMIN (MVC Route)
Blueprint: admin_bp (prefijo /api/v1/admin)
"""
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.utils.roles import ROLE_ADMIN
from app.utils.decorators import role_required
from app.controllers.admin_controller import AdminController

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


@admin_bp.route('/usuarios', methods=['POST'])
@jwt_required()
@role_required(ROLE_ADMIN)
def crear_usuario():
    data = request.get_json()
    return AdminController.crear_usuario(data)


@admin_bp.route('/usuarios', methods=['GET'])
@jwt_required()
@role_required(ROLE_ADMIN)
def listar_usuarios():
    return AdminController.listar_usuarios()


@admin_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
@jwt_required()
@role_required(ROLE_ADMIN)
def detalle_usuario(id_usuario):
    return AdminController.detalle_usuario(id_usuario)


@admin_bp.route('/usuarios/<int:id_usuario>/rol', methods=['PUT'])
@jwt_required()
@role_required(ROLE_ADMIN)
def cambiar_rol(id_usuario):
    data = request.get_json()
    admin_id = int(get_jwt_identity())
    return AdminController.cambiar_rol(id_usuario, data, admin_id)


@admin_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@jwt_required()
@role_required(ROLE_ADMIN)
def editar_usuario(id_usuario):
    data = request.get_json()
    return AdminController.editar_usuario(id_usuario, data)


@admin_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@jwt_required()
@role_required(ROLE_ADMIN)
def eliminar_usuario(id_usuario):
    admin_id = int(get_jwt_identity())
    return AdminController.eliminar_usuario(id_usuario, admin_id)


@admin_bp.route('/usuarios/estadisticas', methods=['GET'])
@jwt_required()
@role_required(ROLE_ADMIN)
def estadisticas():
    return AdminController.estadisticas()


@admin_bp.route('/evaluaciones/<int:id_evaluacion>', methods=['DELETE'])
@jwt_required()
@role_required(ROLE_ADMIN)
def eliminar_evaluacion(id_evaluacion):
    return AdminController.eliminar_evaluacion(id_evaluacion)