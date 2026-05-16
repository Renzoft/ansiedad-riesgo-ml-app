"""
Rutas de autenticación
"""

from flask import Blueprint, request, jsonify #Enrutamiento modular
from flask_jwt_extended import create_access_token#Generación de tokens
from app.models.usuario import db, Usuario #Modelo de usuario

auth_bp = Blueprint("auth", __name__)

# =====================================
# REGISTER
# =====================================

@auth_bp.route('/registro', methods=['POST'])
def registrar_usuario():
    """
    Ruta para registrar un nuevo usuario
    """
    data = request.get_json()
    nombre = data.get("nombre")
    correo = data.get("correo")
    contrasena = data.get("contrasena")
    facultad = data.get("facultad")
    ciclo = data.get("ciclo")

    # =========================
    # VALIDAR CAMPOS
    # =========================
    if not nombre or not correo or not contrasena:
        return jsonify({"message": "Todos los campos son obligatorios"}), 400
    # =========================
    # VALIDAR CORREO ÚNICO
    # =========================
    usuario_existente = Usuario.query.filter_by(correo=correo).first()
    if usuario_existente:

        return jsonify({"mensaje": "El correo ya está registrado"}), 400
    # =========================
    # CREAR USUARIO
    # =========================
    nuevo_usuario = Usuario(
        nombre=nombre, correo=correo, facultad=facultad, ciclo=ciclo
    )

    # HASH PASSWORD
    nuevo_usuario.establecer_contrasena(contrasena)
    # GUARDAR EN BD
    db.session.add(nuevo_usuario)
    db.session.commit()
    return jsonify({"message": "Usuario registrado correctamente"}), 201

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
    token = create_access_token(identity=usuario.id_usuario)

    return jsonify({"mensaje": "Login exitoso", "token": token}), 200
