"""
Rutas administrativas - Acceso exclusivo para ROLE_ADMIN
Blueprint: admin_bp (prefijo /api/v1/admin)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.usuario import db, Usuario
from app.models.evaluacion import Evaluacion
from app.models.resultado_ml import ResultadoML
from app.utils.roles import ROLE_ADMIN, ROLE_ESTUDIANTE, ROLE_MEDICO
from app.utils.decorators import role_required

admin_bp = Blueprint("admin", __name__, url_prefix="/api/v1/admin")


# ==========================================
# POST /usuarios  →  Crear un nuevo usuario
# ==========================================
@admin_bp.route('/usuarios', methods=['POST'])
@jwt_required()
@role_required(ROLE_ADMIN)
def crear_usuario():
    """
    Crea un nuevo usuario en el sistema.
    Body (JSON):
    {
        "nombre": "Juan Pérez",
        "correo": "juan@universidad.edu",
        "contrasena": "123456",
        "rol": "Estudiante",
        "facultad": "Ingeniería",
        "ciclo": 5
    }
    """
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Datos inválidos", "mensaje": "Se requiere JSON"}), 400

        # Validar campos obligatorios
        campos_requeridos = ['nombre', 'correo', 'contrasena']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                return jsonify({
                    "error": "Datos inválidos",
                    "mensaje": f"El campo '{campo}' es obligatorio"
                }), 400

        # Verificar si el correo ya existe
        if Usuario.query.filter_by(correo=data['correo']).first():
            return jsonify({
                "error": "Correo duplicado",
                "mensaje": "Ya existe un usuario con ese correo"
            }), 409

        # Crear usuario
        nuevo_usuario = Usuario(
            nombre=data['nombre'],
            correo=data['correo'],
            rol=data.get('rol', ROLE_ESTUDIANTE),
            facultad=data.get('facultad'),
            ciclo=data.get('ciclo'),
        )
        nuevo_usuario.establecer_contrasena(data['contrasena'])

        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({
            "mensaje": "Usuario creado correctamente",
            "usuario": nuevo_usuario.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# GET /usuarios  →  Listar todos los usuarios
# ==========================================
@admin_bp.route('/usuarios', methods=['GET'])
@jwt_required()
@role_required(ROLE_ADMIN)
def listar_usuarios():
    """
    Retorna la lista completa de usuarios registrados en el sistema.
    Solo accesible para administradores.
    """
    try:
        usuarios = Usuario.query.order_by(Usuario.fecha_registro.desc()).all()
        resultado = [u.to_dict() for u in usuarios]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# GET /usuarios/<id>  →  Ver detalle de un usuario
# ==========================================
@admin_bp.route('/usuarios/<int:id_usuario>', methods=['GET'])
@jwt_required()
@role_required(ROLE_ADMIN)
def detalle_usuario(id_usuario):
    """
    Retorna la información detallada de un usuario específico,
    incluyendo sus evaluaciones y resultados ML.
    Solo accesible para administradores.
    """
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return jsonify({"error": "No encontrado", "mensaje": "Usuario no encontrado"}), 404

        # Datos básicos del usuario
        data = usuario.to_dict()

        # Evaluaciones del usuario
        evaluaciones = Evaluacion.query.filter_by(id_usuario=id_usuario)\
                                       .order_by(Evaluacion.fecha_realizacion.desc()).all()
        data["evaluaciones"] = [e.to_dict() for e in evaluaciones]
        data["total_evaluaciones"] = len(evaluaciones)

        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# PUT /usuarios/<id>/rol  →  Cambiar rol de un usuario
# ==========================================
@admin_bp.route('/usuarios/<int:id_usuario>/rol', methods=['PUT'])
@jwt_required()
@role_required(ROLE_ADMIN)
def cambiar_rol(id_usuario):
    """
    Permite cambiar el rol de un usuario (Estudiante, Medico, Admin).
    Solo accesible para administradores.

    Body (JSON):
    {
        "rol": "Medico"
    }
    """
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return jsonify({"error": "No encontrado", "mensaje": "Usuario no encontrado"}), 404

        data = request.get_json()
        if not data or "rol" not in data:
            return jsonify({"error": "Datos inválidos", "mensaje": "El campo 'rol' es obligatorio"}), 400

        nuevo_rol = data["rol"]
        roles_validos = [ROLE_ESTUDIANTE, ROLE_MEDICO, ROLE_ADMIN]

        if nuevo_rol not in roles_validos:
            return jsonify({
                "error": "Rol inválido",
                "mensaje": f"El rol debe ser uno de: {', '.join(roles_validos)}"
            }), 400

        # No permitir que un admin se quite sus propios privilegios
        admin_id = int(get_jwt_identity())
        if id_usuario == admin_id and nuevo_rol != ROLE_ADMIN:
            return jsonify({
                "error": "Acción no permitida",
                "mensaje": "No puedes cambiarte el rol a ti mismo"
            }), 403

        usuario.rol = nuevo_rol
        db.session.commit()

        return jsonify({
            "mensaje": "Rol actualizado correctamente",
            "usuario": usuario.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# PUT /usuarios/<id>  →  Editar datos de un usuario
# ==========================================
@admin_bp.route('/usuarios/<int:id_usuario>', methods=['PUT'])
@jwt_required()
@role_required(ROLE_ADMIN)
def editar_usuario(id_usuario):
    """
    Editar datos de un usuario (nombre, correo, facultad, ciclo).
    No permite cambiar la contraseña desde aquí por seguridad.
    Body (JSON):
    {
        "nombre": "Juan Pérez Actualizado",
        "correo": "juan@universidad.edu",
        "facultad": "Ingeniería",
        "ciclo": 6
    }
    """
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return jsonify({"error": "No encontrado", "mensaje": "Usuario no encontrado"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Datos inválidos", "mensaje": "Se requiere JSON"}), 400

        # Actualizar solo los campos enviados
        if 'nombre' in data:
            usuario.nombre = data['nombre']
        if 'correo' in data:
            # Verificar que el correo no esté en uso por otro usuario
            existente = Usuario.query.filter_by(correo=data['correo']).first()
            if existente and existente.id_usuario != id_usuario:
                return jsonify({
                    "error": "Correo duplicado",
                    "mensaje": "Ya existe otro usuario con ese correo"
                }), 409
            usuario.correo = data['correo']
        if 'facultad' in data:
            usuario.facultad = data['facultad']
        if 'ciclo' in data:
            usuario.ciclo = data['ciclo']

        db.session.commit()

        return jsonify({
            "mensaje": "Usuario actualizado correctamente",
            "usuario": usuario.to_dict()
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# DELETE /usuarios/<id>  →  Eliminar un usuario
# ==========================================
@admin_bp.route('/usuarios/<int:id_usuario>', methods=['DELETE'])
@jwt_required()
@role_required(ROLE_ADMIN)
def eliminar_usuario(id_usuario):
    """
    Elimina un usuario y todos sus datos asociados (evaluaciones, resultados, etc.)
    gracias a las relaciones CASCADE en la base de datos.
    Solo accesible para administradores.
    """
    try:
        usuario = Usuario.query.get(id_usuario)
        if not usuario:
            return jsonify({"error": "No encontrado", "mensaje": "Usuario no encontrado"}), 404

        # No permitir que un admin se elimine a sí mismo
        admin_id = int(get_jwt_identity())
        if id_usuario == admin_id:
            return jsonify({
                "error": "Acción no permitida",
                "mensaje": "No puedes eliminarte a ti mismo"
            }), 403

        db.session.delete(usuario)
        db.session.commit()

        return jsonify({"mensaje": "Usuario eliminado correctamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500


# ==========================================
# GET /usuarios/estadisticas  →  Estadísticas del sistema
# ==========================================
@admin_bp.route('/usuarios/estadisticas', methods=['GET'])
@jwt_required()
@role_required(ROLE_ADMIN)
def estadisticas():
    """
    Retorna estadísticas generales del sistema:
    - Total de usuarios por rol
    - Total de evaluaciones realizadas
    - Distribución de niveles de riesgo
    Solo accesible para administradores.
    """
    try:
        # Conteo de usuarios por rol
        total_estudiantes = Usuario.query.filter_by(rol=ROLE_ESTUDIANTE).count()
        total_medicos = Usuario.query.filter_by(rol=ROLE_MEDICO).count()
        total_admins = Usuario.query.filter_by(rol=ROLE_ADMIN).count()

        # Total de evaluaciones
        total_evaluaciones = Evaluacion.query.count()

        # Distribución de niveles de riesgo
        riesgo_bajo = ResultadoML.query.filter_by(nivel_riesgo='BAJO').count()
        riesgo_medio = ResultadoML.query.filter_by(nivel_riesgo='MEDIO').count()
        riesgo_alto = ResultadoML.query.filter_by(nivel_riesgo='ALTO').count()

        return jsonify({
            "total_usuarios": total_estudiantes + total_medicos + total_admins,
            "usuarios_por_rol": {
                "estudiantes": total_estudiantes,
                "medicos": total_medicos,
                "admins": total_admins
            },
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
# DELETE /evaluaciones/<id>  →  Eliminar evaluación (admin)
# ==========================================
@admin_bp.route('/evaluaciones/<int:id_evaluacion>', methods=['DELETE'])
@jwt_required()
@role_required(ROLE_ADMIN)
def eliminar_evaluacion(id_evaluacion):
    """
    Elimina una evaluación específica y sus resultados ML asociados.
    Solo accesible para administradores.
    """
    try:
        evaluacion = Evaluacion.query.get(id_evaluacion)
        if not evaluacion:
            return jsonify({"error": "No encontrado", "mensaje": "Evaluación no encontrada"}), 404

        db.session.delete(evaluacion)
        db.session.commit()

        return jsonify({"mensaje": "Evaluación eliminada correctamente"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error interno", "mensaje": str(e)}), 500