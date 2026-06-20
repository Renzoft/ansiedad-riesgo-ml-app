"""
Controller de Autenticación - Maneja requests de login y registro (MVC Controller)
"""
from app.models.usuario import db, Usuario
from app.utils.roles import ROLE_ESTUDIANTE
from app.views.auth_view import AuthView
from flask_jwt_extended import create_access_token


class AuthController:
    """Controller: Recibe request, orquesta Model + View"""

    @staticmethod
    def registrar(data):
        """Registrar un nuevo usuario"""
        nombre = data.get("nombre")
        correo = data.get("correo")
        contrasena = data.get("contrasena")
        facultad = data.get("facultad")
        ciclo = data.get("ciclo")

        # Validar campos obligatorios
        if not nombre or not correo or not contrasena:
            return AuthView.render_error(
                "Los campos nombre, correo y contraseña son obligatorios"
            )

        # Validar ciclo
        if ciclo is not None:
            try:
                ciclo = int(ciclo)
            except (ValueError, TypeError):
                return AuthView.render_error(
                    "El campo ciclo debe ser un número entero"
                )

        # Validar correo único
        if Usuario.existe_correo(correo):
            return AuthView.render_error("El correo ya está registrado")

        # Crear usuario
        try:
            nuevo_usuario = Usuario(
                nombre=nombre,
                correo=correo,
                facultad=facultad,
                ciclo=ciclo,
                rol=ROLE_ESTUDIANTE
            )
            nuevo_usuario.establecer_contrasena(contrasena)
            db.session.add(nuevo_usuario)
            db.session.commit()
            return AuthView.render_registro_exitoso()
        except Exception as e:
            db.session.rollback()
            return AuthView.render_error_interno(str(e))

    @staticmethod
    def login(data):
        """Iniciar sesión"""
        correo = data.get("correo")
        contrasena = data.get("contrasena")

        if not correo or not contrasena:
            return AuthView.render_error(
                "Correo y contraseña son obligatorios"
            )

        usuario = Usuario.query.filter_by(correo=correo).first()
        if not usuario:
            return AuthView.render_error("Usuario no encontrado", 404)

        if not usuario.verificar_contrasena(contrasena):
            return AuthView.render_error("Contraseña incorrecta", 401)

        token = create_access_token(
            identity=str(usuario.id_usuario),
            additional_claims={"rol": usuario.rol}
        )

        return AuthView.render_login_exitoso(token, usuario.to_dict())