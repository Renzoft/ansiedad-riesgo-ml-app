"""
Script para regenerar el campo reporte_ia en todos los registros de resultados_ml
que actualmente tienen NULL o tienen el fallback de error, usando el servicio Gemini.
Incluye reintentos automáticos para errores de cuota (429).
"""
import sys
import os
import json
import logging
import time

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import crear_app
from app.models.usuario import db
from app.models.resultado_ml import ResultadoML
from app.models.evaluacion import Evaluacion


def gemini_con_reintento(gemini_service, nivel_riesgo, probabilidad, variables, max_reintentos=5):
    """
    Llama a Gemini y reintenta automáticamente si hay error de cuota (429).
    """
    for intento in range(max_reintentos):
        try:
            reporte = gemini_service.generar_reporte(
                nivel_riesgo=nivel_riesgo,
                probabilidad=probabilidad,
                variables=variables
            )
            # Verificar que el reporte no sea el fallback por error de Gemini
            if reporte.get("resumen") == "No fue posible generar recomendaciones personalizadas." and \
               reporte.get("error") and "429" in str(reporte.get("error", "")):
                logger.warning(f"  Intento {intento + 1}: Error 429 (cuota excedida). Reintentando en 30 seg...")
                time.sleep(30)
                continue
            return reporte
        except Exception as e:
            error_str = str(e)
            if "429" in error_str:
                logger.warning(f"  Intento {intento + 1}: Error 429. Reintentando en 30 seg...")
                time.sleep(30)
                continue
            else:
                logger.error(f"  Error diferente a 429: {error_str}")
                raise
    # Si llegamos aquí, todos los reintentos fallaron
    raise Exception(f"No se pudo generar reporte después de {max_reintentos} intentos por error 429 (cuota excedida).")


def regenerar_reportes():
    """Itera sobre resultados_ml con reporte_ia inválido y genera el reporte con Gemini."""
    app = crear_app()
    
    with app.app_context():
        # Buscar registros que tengan reporte_ia = NULL o que tengan el fallback de error
        resultados_con_error = ResultadoML.query.filter(
            db.or_(
                ResultadoML.reporte_ia.is_(None),
                ResultadoML.reporte_ia.like('%No fue posible generar%'),
                ResultadoML.reporte_ia.like('%Servicio de recomendaciones de IA no disponible%'),
                ResultadoML.reporte_ia.like('%Error al generar reporte de IA%')
            )
        ).all()
        
        logger.info(f"Se encontraron {len(resultados_con_error)} registros con reporte_ia inválido")
        
        if not resultados_con_error:
            logger.info("No hay registros pendientes. Todo está actualizado.")
            return
        
        gemini_service = app.extensions.get("gemini")
        if not gemini_service:
            logger.error("GeminiService no encontrado en app.extensions. Abortando.")
            return
        
        actualizados = 0
        errores = 0
        
        for resultado in resultados_con_error:
            try:
                evaluacion = Evaluacion.query.get(resultado.id_evaluacion)
                if not evaluacion:
                    logger.warning(f"Evaluación {resultado.id_evaluacion} no encontrada. Saltando...")
                    continue
                
                variables = {
                    "phq9_score": evaluacion.phq9_score,
                    "gad7_score": evaluacion.gad7_score,
                    "sleep_hours": evaluacion.sleep_hours,
                    "exercise_freq": evaluacion.exercise_freq,
                    "social_activity": evaluacion.social_activity,
                    "online_stress": evaluacion.online_stress,
                    "gpa": evaluacion.gpa,
                    "family_support": evaluacion.family_support,
                    "screen_time": evaluacion.screen_time,
                    "academic_stress": evaluacion.academic_stress,
                    "diet_quality": evaluacion.diet_quality,
                    "self_efficacy": evaluacion.self_efficacy,
                    "peer_relationship": evaluacion.peer_relationship,
                    "financial_stress": evaluacion.financial_stress,
                    "sleep_quality": evaluacion.sleep_quality,
                }
                
                logger.info(f"Generando reporte para resultado id={resultado.id_resultado}, "
                           f"eval={resultado.id_evaluacion}, riesgo={resultado.nivel_riesgo}")
                
                reporte_ia = gemini_con_reintento(
                    gemini_service,
                    nivel_riesgo=resultado.nivel_riesgo,
                    probabilidad=resultado.probabilidad_ansiedad,
                    variables=variables
                )
                
                resultado.reporte_ia = json.dumps(reporte_ia, ensure_ascii=False)
                db.session.commit()
                
                logger.info(f"✅ Reporte generado correctamente para resultado id={resultado.id_resultado}")
                actualizados += 1
                
                # Pequeña pausa entre requests para no saturar la API
                time.sleep(2)
                
            except Exception as e:
                db.session.rollback()
                logger.error(f"❌ Error al procesar resultado id={resultado.id_resultado}: {str(e)}")
                errores += 1
        
        logger.info(f"\n===== RESUMEN =====")
        logger.info(f"Total procesados: {len(resultados_con_error)}")
        logger.info(f"Actualizados: {actualizados}")
        logger.info(f"Errores: {errores}")


def limpiar_reportes_fallback():
    """
    Revierte los reportes que tienen fallback de error a NULL
    para que el script principal pueda reintentar generarlos.
    """
    app = crear_app()
    with app.app_context():
        resultados = ResultadoML.query.filter(
            db.or_(
                ResultadoML.reporte_ia.like('%No fue posible generar%'),
                ResultadoML.reporte_ia.like('%Servicio de recomendaciones de IA no disponible%'),
                ResultadoML.reporte_ia.like('%Error al generar reporte de IA%')
            )
        ).all()
        
        count = 0
        for r in resultados:
            r.reporte_ia = None
            count += 1
        
        if count > 0:
            db.session.commit()
            logger.info(f"Se revirtieron {count} reportes fallback a NULL para reintentar.")
        else:
            logger.info("No hay reportes fallback que limpiar.")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--limpiar", action="store_true", help="Limpia los reportes fallback a NULL antes de regenerar")
    args = parser.parse_args()
    
    if args.limpiar:
        limpiar_reportes_fallback()
    
    regenerar_reportes()