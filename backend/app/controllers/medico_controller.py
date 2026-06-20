"""
Controller de Médico - Maneja requests del panel médico (MVC Controller)
"""
from app.models.usuario import Usuario
from app.models.evaluacion import Evaluacion
from app.models.resultado_ml import ResultadoML
from app.views.medico_view import MedicoView


class MedicoController:
    """Controller: Recibe request, orquesta Model + View"""

    @staticmethod
    def listar_pacientes():
        """Lista todos los pacientes (estudiantes)"""
        try:
            pacientes = Usuario.query.filter_by(rol='Estudiante')\
                                      .order_by(Usuario.fecha_registro.desc()).all()

            resultado = []
            for p in pacientes:
                data = p.to_dict()
                ultima_eval = Evaluacion.obtener_ultima(p.id_usuario)
                if ultima_eval and ultima_eval.resultado:
                    data["ultimo_riesgo"] = ultima_eval.resultado.nivel_riesgo
                    data["ultima_probabilidad"] = ultima_eval.resultado.probabilidad_ansiedad
                    data["ultima_evaluacion_fecha"] = (
                        ultima_eval.fecha_realizacion.isoformat()
                        if ultima_eval.fecha_realizacion else None
                    )
                else:
                    data["ultimo_riesgo"] = None
                    data["ultima_probabilidad"] = None
                    data["ultima_evaluacion_fecha"] = None

                resultado.append(data)

            return MedicoView.render_lista_pacientes(resultado)
        except Exception as e:
            return MedicoView.render_error_interno(str(e))

    @staticmethod
    def estadisticas():
        """Obtiene estadísticas para el médico"""
        try:
            total_pacientes = Usuario.query.filter_by(rol='Estudiante').count()
            total_evaluaciones = Evaluacion.query.count()

            riesgo_bajo = ResultadoML.query.filter_by(nivel_riesgo='BAJO').count()
            riesgo_medio = ResultadoML.query.filter_by(nivel_riesgo='MEDIO').count()
            riesgo_alto = ResultadoML.query.filter_by(nivel_riesgo='ALTO').count()

            return MedicoView.render_estadisticas({
                "total_pacientes": total_pacientes,
                "total_evaluaciones": total_evaluaciones,
                "distribucion_riesgo": {
                    "bajo": riesgo_bajo,
                    "medio": riesgo_medio,
                    "alto": riesgo_alto
                }
            })
        except Exception as e:
            return MedicoView.render_error_interno(str(e))

    @staticmethod
    def evaluaciones_recientes():
        """Obtiene las últimas 20 evaluaciones"""
        try:
            evaluaciones = Evaluacion.obtener_recientes(20)

            resultado = []
            for eval in evaluaciones:
                item = {
                    "id_evaluacion": eval.id_evaluacion,
                    "id_usuario": eval.id_usuario,
                    "nombre_paciente": eval.usuario.nombre,
                    "correo_paciente": eval.usuario.correo,
                    "fecha_realizacion": (
                        eval.fecha_realizacion.isoformat()
                        if eval.fecha_realizacion else None
                    ),
                }
                if eval.resultado:
                    item["nivel_riesgo"] = eval.resultado.nivel_riesgo
                    item["probabilidad_ansiedad"] = eval.resultado.probabilidad_ansiedad
                    item["fecha_prediccion"] = (
                        eval.resultado.fecha_prediccion.isoformat()
                        if eval.resultado.fecha_prediccion else None
                    )
                else:
                    item["nivel_riesgo"] = None
                    item["probabilidad_ansiedad"] = None
                    item["fecha_prediccion"] = None

                resultado.append(item)

            return MedicoView.render_evaluaciones_recientes(resultado)
        except Exception as e:
            return MedicoView.render_error_interno(str(e))

    @staticmethod
    def detalle_paciente(id_usuario):
        """Obtiene detalle completo de un paciente"""
        try:
            usuario = Usuario.query.get(id_usuario)
            if not usuario:
                return MedicoView.render_error("Paciente no encontrado", 404)

            if usuario.rol != 'Estudiante':
                return MedicoView.render_error(
                    "El usuario no es un paciente", 403
                )

            data = usuario.to_dict()
            evaluaciones = Evaluacion.obtener_historial(id_usuario)
            data["evaluaciones"] = [e.to_dict() for e in evaluaciones]
            data["total_evaluaciones"] = len(evaluaciones)

            return MedicoView.render_detalle_paciente(data)
        except Exception as e:
            return MedicoView.render_error_interno(str(e))