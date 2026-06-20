"""
Controller de Administración - Maneja requests CRUD de usuarios (MVC Controller)
"""
from app.models.usuario import db, Usuario
from app.models.evaluacion import Evaluacion
from app.models.resultado_ml import ResultadoML
from app.utils.roles import ROLE_ESTUDIANTE, ROLE_MEDICO, ROLE_ADMIN
from app.views.admin_view import AdminView


class AdminController:
    """Controller: Recibe request, orquesta Model + View"""

    @staticmethod
    def crear_usuario(data):
        """Crea un nuevo usuario"""
        if not data:
            return AdminView.render_error("Se requiere JSON")

        campos_requeridos = ['nombre', 'correo', 'contrasena']
        for campo in campos_requeridos:
            if campo not in data or not data[campo]:
                return AdminView.render_error(
                    f"El campo '{campo}' es obligatorio"
                )

        if Usuario.existe_correo(data['correo']):
            return AdminView.render_error(
                "Ya existe un usuario con ese correo", 409
            )

        try:
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
            return AdminView.render_usuario_creado(nuevo_usuario.to_dict())
        except Exception as e:
            db.session.rollback()
            return AdminView.render_error_interno(str(e))

    @staticmethod
    def listar_usuarios():
        """Lista todos los usuarios"""
        try:
            usuarios = Usuario.listar_todos()
            return AdminView.render_lista_usuarios(usuarios)
        except Exception as e:
            return AdminView.render_error_interno(str(e))

    @staticmethod
    def detalle_usuario(id_usuario):
        """Obtiene detalle de un usuario con sus evaluaciones"""
        try:
            usuario = Usuario.query.get(id_usuario)
            if not usuario:
                return AdminView.render_error("Usuario no encontrado", 404)

            data = usuario.to_dict()
            evaluaciones = Evaluacion.obtener_historial(id_usuario)
            data["evaluaciones"] = [e.to_dict() for e in evaluaciones]
            data["total_evaluaciones"] = len(evaluaciones)

            return AdminView.render_usuario(data)
        except Exception as e:
            return AdminView.render_error_interno(str(e))

    @staticmethod
    def cambiar_rol(id_usuario, data, admin_id):
        """Cambia el rol de un usuario"""
        try:
            usuario = Usuario.query.get(id_usuario)
            if not usuario:
                return AdminView.render_error("Usuario no encontrado", 404)

            if not data or "rol" not in data:
                return AdminView.render_error(
                    "El campo 'rol' es obligatorio"
                )

            nuevo_rol = data["rol"]
            roles_validos = [ROLE_ESTUDIANTE, ROLE_MEDICO, ROLE_ADMIN]

            if nuevo_rol not in roles_validos:
                return AdminView.render_error(
                    f"El rol debe ser uno de: {', '.join(roles_validos)}"
                )

            if id_usuario == admin_id and nuevo_rol != ROLE_ADMIN:
                return AdminView.render_error(
                    "No puedes cambiarte el rol a ti mismo", 403
                )

            usuario.rol = nuevo_rol
            db.session.commit()

            return AdminView.render_usuario(
                usuario.to_dict(),
                "Rol actualizado correctamente"
            )
        except Exception as e:
            db.session.rollback()
            return AdminView.render_error_interno(str(e))

    @staticmethod
    def editar_usuario(id_usuario, data):
        """Edita datos de un usuario"""
        try:
            usuario = Usuario.query.get(id_usuario)
            if not usuario:
                return AdminView.render_error("Usuario no encontrado", 404)

            if not data:
                return AdminView.render_error("Se requiere JSON")

            if 'nombre' in data:
                usuario.nombre = data['nombre']
            if 'correo' in data:
                if Usuario.existe_correo(data['correo'], excluir_id=id_usuario):
                    return AdminView.render_error(
                        "Ya existe otro usuario con ese correo", 409
                    )
                usuario.correo = data['correo']
            if 'facultad' in data:
                usuario.facultad = data['facultad']
            if 'ciclo' in data:
                usuario.ciclo = data['ciclo']
            if 'rol' in data:
                usuario.rol = data['rol']
                if data['rol'] != ROLE_ESTUDIANTE:
                    usuario.facultad = None
                    usuario.ciclo = None

            db.session.commit()
            return AdminView.render_usuario(
                usuario.to_dict(),
                "Usuario actualizado correctamente"
            )
        except Exception as e:
            db.session.rollback()
            return AdminView.render_error_interno(str(e))

    @staticmethod
    def eliminar_usuario(id_usuario, admin_id):
        """Elimina un usuario"""
        try:
            usuario = Usuario.query.get(id_usuario)
            if not usuario:
                return AdminView.render_error("Usuario no encontrado", 404)

            if id_usuario == admin_id:
                return AdminView.render_error(
                    "No puedes eliminarte a ti mismo", 403
                )

            db.session.delete(usuario)
            db.session.commit()
            return AdminView.render_mensaje("Usuario eliminado correctamente")
        except Exception as e:
            db.session.rollback()
            return AdminView.render_error_interno(str(e))

    @staticmethod
    def estadisticas():
        """Obtiene estadísticas del sistema"""
        try:
            total_estudiantes = Usuario.query.filter_by(rol=ROLE_ESTUDIANTE).count()
            total_medicos = Usuario.query.filter_by(rol=ROLE_MEDICO).count()
            total_admins = Usuario.query.filter_by(rol=ROLE_ADMIN).count()
            total_evaluaciones = Evaluacion.query.count()

            riesgo_bajo = ResultadoML.query.filter_by(nivel_riesgo='BAJO').count()
            riesgo_medio = ResultadoML.query.filter_by(nivel_riesgo='MEDIO').count()
            riesgo_alto = ResultadoML.query.filter_by(nivel_riesgo='ALTO').count()

            return AdminView.render_estadisticas({
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
            })
        except Exception as e:
            return AdminView.render_error_interno(str(e))

    @staticmethod
    def eliminar_evaluacion(id_evaluacion):
        """Elimina una evaluación"""
        try:
            evaluacion = Evaluacion.query.get(id_evaluacion)
            if not evaluacion:
                return AdminView.render_error("Evaluación no encontrada", 404)

            db.session.delete(evaluacion)
            db.session.commit()
            return AdminView.render_mensaje("Evaluación eliminada correctamente")
        except Exception as e:
            db.session.rollback()
            return AdminView.render_error_interno(str(e))