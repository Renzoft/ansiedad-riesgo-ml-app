"""
Rutas de la API para Hábitos (Indicadores de Estilo de Vida)
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

from app.models.usuario import db
from app.models.habito import Habito

habitos_bp = Blueprint("habitos", __name__)

@habitos_bp.route('/habitos', methods=['POST'])
@jwt_required()
def registrar_habito():
    """
    Ruta para registrar un nuevo hábito para el usuario autenticado
    """
    usuario_id = int(get_jwt_identity())
    data = request.get_json()

    if not data:
        return jsonify({"mensaje": "No se enviaron datos"}), 400

    # Extraer campos
    fecha_str = data.get("fecha")
    sleep_hours = data.get("sleep_hours")
    exercise_freq = data.get("exercise_freq")
    social_activity = data.get("social_activity")
    screen_time = data.get("screen_time")
    diet_quality = data.get("diet_quality")
    sleep_quality = data.get("sleep_quality")

    # Validar campos requeridos
    if fecha_str is None or sleep_hours is None or exercise_freq is None or \
       social_activity is None or screen_time is None or diet_quality is None or sleep_quality is None:
        return jsonify({"mensaje": "Todos los campos son obligatorios"}), 400

    # Validar formato y lógica de fecha
    try:
        fecha_obj = datetime.strptime(fecha_str, "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"mensaje": "Formato de fecha inválido. Debe ser YYYY-MM-DD"}), 400

    if fecha_obj > datetime.now().date():
        return jsonify({"mensaje": "La fecha no puede ser futura"}), 400

    # Validar rangos numéricos
    try:
        sleep_hours = float(sleep_hours)
        exercise_freq = int(exercise_freq)
        social_activity = float(social_activity)
        screen_time = float(screen_time)
        diet_quality = float(diet_quality)
        sleep_quality = float(sleep_quality)

        if not (3.0 <= sleep_hours <= 10.0):
            return jsonify({"mensaje": "sleep_hours debe estar entre 3.0 y 10.0"}), 400
        if not (0 <= exercise_freq <= 7):
            return jsonify({"mensaje": "exercise_freq debe estar entre 0 y 7"}), 400
        if not (0.0 <= social_activity <= 10.0):
            return jsonify({"mensaje": "social_activity debe estar entre 0.0 y 10.0"}), 400
        if not (1.0 <= screen_time <= 12.0):
            return jsonify({"mensaje": "screen_time debe estar entre 1.0 y 12.0"}), 400
        if not (1.0 <= diet_quality <= 10.0):
            return jsonify({"mensaje": "diet_quality debe estar entre 1.0 y 10.0"}), 400
        if not (0.0 <= sleep_quality <= 10.0):
            return jsonify({"mensaje": "sleep_quality debe estar entre 0.0 y 10.0"}), 400
    except ValueError:
        return jsonify({"mensaje": "Los valores proporcionados deben ser numéricos"}), 400

    # Verificar si ya existe un registro para esa fecha y usuario
    habito_existente = Habito.query.filter_by(usuario_id=usuario_id, fecha=fecha_obj).first()
    if habito_existente:
        return jsonify({"mensaje": "Ya existe un registro para esta fecha"}), 409

    # Crear y guardar registro
    nuevo_habito = Habito(
        usuario_id=usuario_id,
        fecha=fecha_obj,
        sleep_hours=sleep_hours,
        exercise_freq=exercise_freq,
        social_activity=social_activity,
        screen_time=screen_time,
        diet_quality=diet_quality,
        sleep_quality=sleep_quality
    )

    db.session.add(nuevo_habito)
    db.session.commit()

    return jsonify({
        "mensaje": "Hábito registrado correctamente",
        "habito": nuevo_habito.to_dict()
    }), 201


@habitos_bp.route('/habitos/ultimo', methods=['GET'])
@jwt_required()
def obtener_ultimo_habito():
    """
    Ruta para obtener el registro de hábitos más reciente del usuario
    """
    usuario_id = int(get_jwt_identity())
    
    ultimo_habito = Habito.query.filter_by(usuario_id=usuario_id)\
                                .order_by(Habito.fecha.desc())\
                                .first()
    
    if not ultimo_habito:
        return jsonify({"mensaje": "No se encontraron registros de hábitos"}), 404

    return jsonify(ultimo_habito.to_dict()), 200


@habitos_bp.route('/habitos', methods=['GET'])
@jwt_required()
def listar_habitos():
    """
    Ruta para listar todos los hábitos del usuario con paginación
    """
    usuario_id = int(get_jwt_identity())
    
    # Parámetros de paginación
    try:
        limit = int(request.args.get('limit', 10))
        offset = int(request.args.get('offset', 0))
    except ValueError:
        return jsonify({"mensaje": "Parámetros limit y offset deben ser enteros"}), 400

    habitos = Habito.query.filter_by(usuario_id=usuario_id)\
                          .order_by(Habito.fecha.desc())\
                          .limit(limit)\
                          .offset(offset)\
                          .all()

    return jsonify([h.to_dict() for h in habitos]), 200
