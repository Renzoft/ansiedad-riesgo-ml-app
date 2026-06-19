# ==========================================
# Servicio Gemini (Flask Extension Pattern)
# Genera recomendaciones inteligentes para la evaluación de ansiedad
# ==========================================

import json
import logging
from flask import current_app

logger = logging.getLogger(__name__)


class GeminiService:
    """
    Extensión personalizada de Flask para interactuar con la API de Gemini.
    Sigue el patrón de diseño oficial de Extensiones de Flask, lo que
    evita ejecuciones en tiempo de importación y permite una configuración centralizada.
    """

    def __init__(self, app=None):
        self.app = app
        self._model = None
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """
        Inicializa la extensión vinculándola con la aplicación Flask actual.
        """
        # Registrar esta extensión en el diccionario de extensiones de Flask
        if not hasattr(app, "extensions"):
            app.extensions = {}
        app.extensions["gemini"] = self

        # Leer configuración desde el objeto app.config (Application Factory)
        api_key = app.config.get("GEMINI_API_KEY")
        modelo = app.config.get("GEMINI_MODEL", "gemini-2.5-flash")

        if not api_key:
            # Alerta crítica si no está configurada, ideal para ambientes de producción
            raise ValueError(
                "La configuración 'GEMINI_API_KEY' es obligatoria en app.config para inicializar GeminiService."
            )

        try:
            import google.generativeai as genai

            genai.configure(api_key=api_key)
            self._model = genai.GenerativeModel(modelo)
            logger.info(
                f"Servicio de Gemini inicializado correctamente usando el modelo: {modelo}"
            )
        except Exception as e:
            logger.error(
                f"Error al configurar el cliente de Google Generative AI: {str(e)}"
            )
            raise e

    @property
    def model(self):
        """
        Retorna la instancia del modelo Generativo de forma segura.
        """
        if self._model is None:
            raise RuntimeError(
                "GeminiService no ha sido inicializado. Asegúrate de llamar a init_app(app)."
            )
        return self._model

    def generar_reporte(self, nivel_riesgo, probabilidad, variables):
        """
        Genera un reporte personalizado usando Gemini
        a partir del nivel de riesgo calculado por ML y las 15 variables de entrada.
        """
        prompt = f"""
Eres un especialista en bienestar emocional universitario.

Analiza la siguiente evaluación.

Nivel de riesgo:
{nivel_riesgo}

Probabilidad de ansiedad:
{round(probabilidad * 100, 2)}%

Variables:
{json.dumps(variables, indent=2)}

Genera únicamente JSON válido con la siguiente estructura:

{{
    "resumen":"",

    "fortalezas":[],

    "factores_preocupantes":[],

    "recomendaciones":[],

    "plan_7_dias":[],

    "temas_videos":[],

    "temas_lectura":[],

    "prioridad_intervencion":"",

    "mensaje_motivacional":""
}}

Reglas:

- Máximo 5 fortalezas
- Máximo 5 factores_preocupantes
- Máximo 5 recomendaciones
- Máximo 7 acciones para plan_7_dias
- Máximo 3 temas_videos
- Máximo 3 temas_lectura

IMPORTANTE:

- Responde SOLO JSON.
- No uses markdown.
- No uses ```json.
- No agregues texto antes ni después del JSON.
"""
        try:
            # Solicitud a Gemini
            response = self.model.generate_content(prompt)
            texto = response.text.strip()

            # Limpieza por si Gemini devuelve markdown a pesar del prompt
            texto = texto.replace("```json", "")
            texto = texto.replace("```", "")
            texto = texto.strip()

            # Convertir respuesta JSON a dict
            return json.loads(texto)

        except json.JSONDecodeError as e:
            logger.error(f"Respuesta de Gemini no fue un JSON válido: {str(e)}")
            return {
                "resumen": "Gemini debolvió una respuesta con formato inválido.",
                "fortalezas": [],
                "factores_preocupantes": [],
                "recomendaciones": [],
                "plan_7_dias": [],
                "temas_videos": [],
                "temas_lectura": [],
                "prioridad_intervencion": "NO DISPONIBLE",
                "mensaje_motivacional": "Continúa cuidando tu bienestar.",
                "error": f"JSON inválido: {str(e)}",
            }

        except Exception as e:
            logger.error(f"Error general en GeminiService: {str(e)}")
            return {
                "resumen": "No fue posible generar recomendaciones personalizadas.",
                "fortalezas": [],
                "factores_preocupantes": [],
                "recomendaciones": [],
                "plan_7_dias": [],
                "temas_videos": [],
                "temas_lectura": [],
                "prioridad_intervencion": "NO DISPONIBLE",
                "mensaje_motivacional": "Continúa cuidando tu bienestar.",
                "error": str(e),
            }
