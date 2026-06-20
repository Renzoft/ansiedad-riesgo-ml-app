"""
Controller de Evaluaciones - Maneja requests de evaluación ML (MVC Controller)
"""
import json
import logging

from flask import current_app
from app.models.usuario import db, Usuario
from app.models.evaluacion import Evaluacion
from app.models.resultado_ml import ResultadoML
from app.models.recomendacion import Recomendacion
from app.services.ml_service import predictor
from app.views.evaluacion_view import EvaluacionView

logger = logging.getLogger(__name__)


class EvaluacionController:
    """Controller: Recibe request, orquesta Model + View"""

    @staticmethod
    def realizar_evaluacion(usuario_id, data):
        """Procesa una evaluación completa"""
        try:
            # Verificar que el usuario existe
            usuario = Usuario.query.get(usuario_id)
            if not usuario:
                return EvaluacionView.render_error("Usuario no encontrado", 404)

            if not data:
                return EvaluacionView.render_error(
                    "No se enviaron datos en el cuerpo de la petición"
                )

            # Validar y crear evaluación (lógica en el Model)
            try:
                nueva_evaluacion = Evaluacion.crear_desde_data(usuario_id, data)
            except ValueError as e:
                return EvaluacionView.render_error(str(e))

            db.session.add(nueva_evaluacion)
            db.session.flush()

            # Ejecutar predicción ML
            vector = nueva_evaluacion.to_vector()
            probabilidad = predictor.predecir(vector)

            # Categorizar riesgo (lógica en el Model)
            nivel_riesgo, explicacion = ResultadoML.categorizar_riesgo(probabilidad)

            # Generar reporte con Gemini
            reporte_ia = EvaluacionController._generar_reporte_gemini(
                nivel_riesgo, probabilidad, nueva_evaluacion.to_dict_variables()
            )

            # Guardar resultado ML
            reporte_ia_json = json.dumps(reporte_ia) if reporte_ia else None
            nuevo_resultado = ResultadoML(
                id_evaluacion=nueva_evaluacion.id_evaluacion,
                id_usuario=usuario_id,
                probabilidad_ansiedad=probabilidad,
                nivel_riesgo=nivel_riesgo,
                reporte_ia=reporte_ia_json
            )
            db.session.add(nuevo_resultado)
            db.session.flush()

            # Asociar recomendaciones
            recomendaciones = Recomendacion.query.filter_by(
                categoria=nivel_riesgo
            ).all()
            for recomendacion in recomendaciones:
                nuevo_resultado.recomendaciones.append(recomendacion)

            db.session.commit()

            # Construir respuesta
            respuesta = {
                "id_evaluacion": nueva_evaluacion.id_evaluacion,
                "probabilidad_ansiedad": probabilidad,
                "nivel_riesgo": nivel_riesgo,
                "explicacion": explicacion,
                "fecha_realizacion": nueva_evaluacion.fecha_realizacion.isoformat(),
                "recomendaciones": [r.to_dict() for r in recomendaciones],
                "reporte_ia": reporte_ia,
            }

            return EvaluacionView.render_resultado(respuesta)

        except Exception as e:
            db.session.rollback()
            return EvaluacionView.render_error_interno(str(e))

    @staticmethod
    def historial_evaluaciones(usuario_id):
        """Obtiene el historial de evaluaciones del usuario"""
        try:
            evaluaciones = Evaluacion.obtener_historial(usuario_id)
            resultado = [e.to_dict() for e in evaluaciones]
            return EvaluacionView.render_historial(resultado)
        except Exception as e:
            return EvaluacionView.render_error_interno(str(e))

    @staticmethod
    def _generar_reporte_gemini(nivel_riesgo, probabilidad, variables):
        """Genera reporte con Gemini si está disponible"""
        gemini_service = current_app.extensions.get("gemini")

        if not gemini_service:
            logger.warning("Gemini service NO encontrado")
            return {
                "resumen": "Servicio de recomendaciones de IA no disponible temporalmente.",
                "fortalezas": [],
                "factores_preocupantes": [],
                "recomendaciones": [],
                "plan_7_dias": [],
                "temas_videos": [],
                "temas_lectura": [],
                "prioridad_intervencion": "NO DISPONIBLE",
                "mensaje_motivacional": "Continúa cuidando tu bienestar."
            }

        try:
            logger.info("Intentando generar reporte con Gemini...")
            reporte = gemini_service.generar_reporte(
                nivel_riesgo=nivel_riesgo,
                probabilidad=probabilidad,
                variables=variables
            )
            logger.info("Reporte generado exitosamente")
            return reporte
        except Exception as e:
            logger.error(f"Error al generar reporte con Gemini: {str(e)}", exc_info=True)
            return {
                "resumen": "Error al generar reporte de IA.",
                "fortalezas": [],
                "factores_preocupantes": [],
                "recomendaciones": [],
                "plan_7_dias": [],
                "temas_videos": [],
                "temas_lectura": [],
                "prioridad_intervencion": "ERROR",
                "mensaje_motivacional": "Continúa cuidando tu bienestar.",
                "error": str(e)
            }