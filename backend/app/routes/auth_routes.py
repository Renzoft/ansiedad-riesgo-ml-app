"""
Rutas de autenticación
"""

from flask import Blueprint, request, jsonify #Enrutamiento modular
from flask_jwt_extended import create_access_token#Generación de tokens
from app.models.usuario import db, Usuario #Modelo de usuario
from app.utils.roles import ROLE_ESTUDIANTE #Roles

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
    
    # Nuevas variables académicas y psicosociales
    phq9 = data.get("phq9")
    gad7 = data.get("gad7")
    online_stress = data.get("online_stress")
    financial_stress = data.get("financial_stress")
    academic_stress = data.get("academic_stress")
    gpa = data.get("gpa")
    family_support = data.get("family_support")
    self_efficacy = data.get("self_efficacy")
    peer_relationship = data.get("peer_relationship")

    # =========================
    # VALIDAR CAMPOS BÁSICOS
    # =========================
    if not nombre or not correo or not contrasena:
        return jsonify({"message": "Todos los campos básicos son obligatorios"}), 400

    # =========================
    # VALIDAR NUEVOS CAMPOS (Obligatorios, Tipo y Rango)
    # =========================
    nuevos_campos = {
        "phq9": phq9, "gad7": gad7, "online_stress": online_stress, 
        "financial_stress": financial_stress, "academic_stress": academic_stress, 
        "gpa": gpa, "family_support": family_support, 
        "self_efficacy": self_efficacy, "peer_relationship": peer_relationship
    }
    
    for campo, valor in nuevos_campos.items():
        if valor is None:
            return jsonify({"error": f"El campo {campo} es obligatorio"}), 400

    try:
        phq9 = int(phq9)
        if not (0 <= phq9 <= 27):
            return jsonify({"error": "phq9 debe estar entre 0 y 27"}), 400
            
        gad7 = int(gad7)
        if not (0 <= gad7 <= 21):
            return jsonify({"error": "gad7 debe estar entre 0 y 21"}), 400
            
        online_stress = int(online_stress)
        if not (1 <= online_stress <= 10):
            return jsonify({"error": "online_stress debe estar entre 1 y 10"}), 400
            
        financial_stress = int(financial_stress)
        if not (1 <= financial_stress <= 10):
            return jsonify({"error": "financial_stress debe estar entre 1 y 10"}), 400
            
        academic_stress = int(academic_stress)
        if not (1 <= academic_stress <= 10):
            return jsonify({"error": "academic_stress debe estar entre 1 y 10"}), 400
            
        gpa = float(gpa)
        if not (0.0 <= gpa <= 5.0):
            return jsonify({"error": "gpa debe estar entre 0.0 y 5.0"}), 400
            
        family_support = int(family_support)
        if not (1 <= family_support <= 10):
            return jsonify({"error": "family_support debe estar entre 1 y 10"}), 400
            
        self_efficacy = int(self_efficacy)
        if not (1 <= self_efficacy <= 10):
            return jsonify({"error": "self_efficacy debe estar entre 1 y 10"}), 400
            
        peer_relationship = int(peer_relationship)
        if not (1 <= peer_relationship <= 10):
            return jsonify({"error": "peer_relationship debe estar entre 1 y 10"}), 400
    except ValueError:
        return jsonify({"error": "Uno o más campos tienen un formato numérico inválido"}), 400
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
        nombre=nombre, correo=correo, facultad=facultad, ciclo=ciclo, rol=ROLE_ESTUDIANTE,
        phq9=phq9, gad7=gad7, online_stress=online_stress, financial_stress=financial_stress,
        academic_stress=academic_stress, gpa=gpa, family_support=family_support,
        self_efficacy=self_efficacy, peer_relationship=peer_relationship
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
    token = create_access_token(
        identity=str(usuario.id_usuario), additional_claims={"rol": usuario.rol}
    )

    return jsonify({"mensaje": "Login exitoso", "token": token}), 200
