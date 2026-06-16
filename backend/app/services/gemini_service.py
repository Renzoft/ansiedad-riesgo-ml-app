# ==========================================
# Servicio Gemini
# Genera recomendaciones inteligentes
# ==========================================

import os
import json
# import google.generativeai as genai


class GeminiService:

    def __init__(self):

        # ==========================================
        # Configuración Gemini
        # ==========================================
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

        self.model = genai.GenerativeModel("gemini-2.5-flash")

    def generar_reporte(self, nivel_riesgo, probabilidad, variables):

        prompt = f"""
Eres un especialista en bienestar emocional universitario.

Analiza la siguiente evaluación.

Nivel de riesgo:
{nivel_riesgo}

Probabilidad de ansiedad:
{round(probabilidad * 100, 2)}%

Variables:
{json.dumps(variables, indent=2)}

Genera únicamente JSON válido.

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

- máximo 5 fortalezas
- máximo 5 factores_preocupantes
- máximo 5 recomendaciones
- máximo 7 acciones para plan_7_dias
- máximo 3 temas_videos
- máximo 3 temas_lectura

Responde SOLO JSON.
No uses markdown.
No uses ```json.
"""

        try:

            response = self.model.generate_content(prompt)

            texto = response.text.strip()

            texto = texto.replace("```json", "")
            texto = texto.replace("```", "")

            return json.loads(texto)

        except Exception as e:

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
