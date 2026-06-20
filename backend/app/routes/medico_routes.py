"""
Rutas para el rol Médico - Acceso exclusivo para ROLE_MEDICO y ROLE_ADMIN (MVC Route)
Blueprint: medico_bp (prefijo /api/v1/medico)
"""
from flask import Blueprint
from flask_jwt_extended import jwt_required
from app.utils.roles import ROLE_MEDICO, ROLE_ADMIN
from app.utils.decorators import role_required
from app.controllers.medico_controller import MedicoController

medico_bp = Blueprint("medico", __name__, url_prefix="/api/v1/medico")


@medico_bp.route('/pacientes', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def listar_pacientes():
    return MedicoController.listar_pacientes()


@medico_bp.route('/estadisticas', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def estadisticas():
    return MedicoController.estadisticas()


@medico_bp.route('/evaluaciones-recientes', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def evaluaciones_recientes():
    return MedicoController.evaluaciones_recientes()


@medico_bp.route('/pacientes/<int:id_usuario>/detalle', methods=['GET'])
@jwt_required()
@role_required(ROLE_MEDICO, ROLE_ADMIN)
def detalle_paciente(id_usuario):
    return MedicoController.detalle_paciente(id_usuario)