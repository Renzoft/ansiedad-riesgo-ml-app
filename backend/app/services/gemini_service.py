# ==========================================
# Servicio Gemini
# Genera recomendaciones inteligentes
# para la evaluación de ansiedad
# ==========================================

import os
import json
import google.generativeai as genai


class GeminiService:

    def __init__(self):

        # ==========================================
        # Obtener API Key desde .env
        # ==========================================
        api_key = os.getenv("GEMINI_API_KEY")

        if not api_key:
            raise ValueError(
                "No se encontró GEMINI_API_KEY en las variables de entorno."
            )

        # ==========================================
        # Configurar Gemini
        # ==========================================
        genai.configure(api_key=api_key)

        # ==========================================
        # Modelo configurable desde .env
        #
        # Ejemplo:
        # GEMINI_MODEL=gemini-2.5-flash
        # GEMINI_MODEL=gemini-2.5-pro
        # ==========================================
        modelo = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")

        self.model = genai.GenerativeModel(modelo)

    def generar_reporte(self, nivel_riesgo, probabilidad, variables):
        """
        Genera un reporte personalizado usando Gemini
        a partir del nivel de riesgo calculado por ML
        y las 15 variables de entrada.
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

            # ==========================================
            # Solicitud a Gemini
            # ==========================================
            response = self.model.generate_content(prompt)

            texto = response.text.strip()

            # ==========================================
            # Limpieza por si Gemini devuelve markdown
            # ==========================================
            texto = texto.replace("```json", "")
            texto = texto.replace("```", "")
            texto = texto.strip()

            # ==========================================
            # Convertir respuesta JSON a dict
            # ==========================================
            return json.loads(texto)

        except json.JSONDecodeError as e:

            # ==========================================
            # Gemini respondió texto inválido
            # ==========================================
            return {
                "resumen": "Gemini devolvió una respuesta con formato inválido.",
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

            # ==========================================
            # Error general (API, red, cuota, etc.)
            # ==========================================
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


# ==========================================
# Instancia global
# ==========================================
gemini_service = GeminiService()
