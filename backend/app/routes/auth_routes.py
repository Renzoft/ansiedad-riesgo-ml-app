"""
Rutas de autenticación
"""

from flask import Blueprint, request, jsonify  # Enrutamiento modular
from flask_jwt_extended import create_access_token  # Generación de tokens
from app.models.usuario import db, Usuario  # Modelo de usuario
from app.utils.roles import ROLE_ESTUDIANTE  # Roles

auth_bp = Blueprint("auth", __name__)

# =====================================
# REGISTER
# =====================================

@auth_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    """
    Ruta para registrar un nuevo usuario.
    Solo recibe datos de perfil (sin variables ML).
    """
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    facultad = data.get("facultad")
    ciclo = data.get("ciclo")

    # =========================
    # VALIDAR CAMPOS OBLIGATORIOS
    # =========================
    if not nombre or not correo or not contrasena:
        return jsonify({"mensaje": "Los campos nombre, correo y contraseña son obligatorios"}), 400

    # =========================
    # VALIDAR CICLO (si se envía)
    # =========================
    if ciclo is not None:
        try:
            ciclo = int(ciclo)
        except (ValueError, TypeError):
            return jsonify({"mensaje": "El campo ciclo debe ser un número entero"}), 400

    # =========================
    # VALIDAR CORREO ÚNICO
    # =========================
    usuario_existente = Usuario.query.filter_by(correo=correo).first()
    if usuario_existente:
        return jsonify({"mensaje": "El correo ya está registrado"}), 400

    # =========================
    # CREAR USUARIO
    # =========================
    try:
        nuevo_usuario = Usuario(
            nombre=nombre,
            correo=correo,
            facultad=facultad,
            ciclo=ciclo,
            rol=ROLE_ESTUDIANTE
        )

        # HASH PASSWORD
        nuevo_usuario.establecer_contrasena(contrasena)

        # GUARDAR EN BD
        db.session.add(nuevo_usuario)
        db.session.commit()

        return jsonify({"mensaje": "Usuario registrado correctamente"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al registrar usuario", "mensaje": str(e)}), 500

# ==========================================
# LOGIN
# ==========================================

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Ruta para iniciar sesión
    """
    data = request.get_json()
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    # ==========================================
    # VALIDAR CAMPOS
    # ==========================================
    if not correo or not contrasena:
        return jsonify({"mensaje": "Correo y contraseña son obligatorios"}), 400

    # ==========================================
    # BUSCAR USUARIO
    # ==========================================
    usuario = Usuario.query.filter_by(correo=correo).first()

    if not usuario:
        return jsonify({"mensaje": "Usuario no encontrado"}), 404
    # ==========================================
    # VERIFICAR CONTRASEÑA
    # ==========================================
    if not usuario.verificar_contrasena(contrasena):
        return jsonify({"mensaje": "Contraseña incorrecta"}), 401
    # ==========================================
    # GENERAR TOKEN JWT
    # ==========================================
    token = create_access_token(
        identity=str(usuario.id_usuario), additional_claims={"rol": usuario.rol}
    )

    return jsonify({"mensaje": "Login exitoso", "token": token}), 200
