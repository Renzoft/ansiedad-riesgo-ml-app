"""
Decoradores personalizados para autorización basada en roles (RBAC).
"""
from functools import wraps
from flask import jsonify
from flask_jwt_extended import get_jwt


def role_required(*roles):
    """
    Decorador que verifica que el usuario autenticado tenga uno de los roles
    especificados.

    Uso:
        @jwt_required()
        @role_required(ROLE_ADMIN)
        def mi_endpoint():
            ...

        @jwt_required()
        @role_required(ROLE_MEDICO, ROLE_ADMIN)
        def otro_endpoint():
            ...

    Devuelve 403 Forbidden si el rol no está autorizado.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            # Obtener los claims del JWT (incluye el rol)
            claims = get_jwt()
            rol_usuario = claims.get("rol")

            # Validar que el token tenga un rol
            if not rol_usuario:
                return jsonify({
                    "error": "Acceso denegado",
                    "mensaje": "El token no contiene información de rol"
                }), 403

            # Verificar si el rol del usuario está entre los permitidos
            if rol_usuario not in roles:
                return jsonify({
                    "error": "Acceso denegado",
                    "mensaje": f"Se requiere uno de los siguientes roles: {', '.join(roles)}"
                }), 403

            return fn(*args, **kwargs)
        return wrapper
    return decorator