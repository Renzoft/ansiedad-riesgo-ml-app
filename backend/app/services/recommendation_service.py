"""
Servicio de recomendaciones personalizadas
"""

class RecommendationService:
    """
    Genera recomendaciones basadas en:
    - nivel de riesgo
    - hábitos débiles
    """

    def generar_recomendaciones(self, categoria, habito):
        recomendaciones = []

        # ======================================
        # RECOMENDACIONES SEGÚN RIESGO
        # ======================================

        if categoria == "BAJO":
            recomendaciones.append({
                "tipo": "bienestar",
                "titulo": "Mantén tus hábitos saludables",
                "descripcion": "Continúa con tus rutinas positivas de descanso y organización.",
                "link": "https://medlineplus.gov/spanish/mentalhealth.html" # Enlace a recursos de salud mental en español
            })

        elif categoria == "MEDIO":
            recomendaciones.append({
                "tipo": "respiracion",
                "titulo": "Practica respiración consciente",
                "descripcion": "Dedica 5 minutos diarios a ejercicios de respiración.",
                "link": "https://www.youtube.com/watch?v=SEfs5TJZ6Nk" # Enlace a video de respiración consciente
            })

        elif categoria == "ALTO":
            recomendaciones.append({
                "tipo": "apoyo",
                "titulo": "Contacta bienestar universitario",
                "descripcion": "Se recomienda orientación psicológica profesional.",
                "link": "https://bienestaruniversitario.pe" # Enlace a bienestar universitario de la UNMSM
            })

        # ======================================
        # RECOMENDACIONES SEGÚN HÁBITOS
        # ======================================

        if habito.sleep_hours < 6:
            recomendaciones.append({
                "tipo": "sueno",
                "titulo": "Mejora tus horas de sueño",
                "descripcion": "Dormir menos de 6 horas incrementa el estrés emocional.",
                "link": "https://www.sleepfoundation.org" # Enlace a recursos sobre sueño
            })

        if habito.exercise_freq < 2:
            recomendaciones.append({
                "tipo": "ejercicio",
                "titulo": "Incrementa tu actividad física",
                "descripcion": "Caminar o ejercitarte reduce síntomas de ansiedad.",
                "link": "https://www.who.int/es/news-room/fact-sheets/detail/physical-activity" # Enlace a recomendaciones de actividad física de la OMS
            })

        if habito.screen_time > 8:
            recomendaciones.append({
                "tipo": "pantalla",
                "titulo": "Reduce tiempo frente a pantallas",
                "descripcion": "El exceso de pantallas puede afectar el sueño y la ansiedad.",
                "link": "https://www.apa.org" # Enlace a recursos de la APA sobre tecnología y salud mental
            })

        if habito.social_activity < 4:
            recomendaciones.append({
                "tipo": "social",
                "titulo": "Fortalece tus relaciones sociales",
                "descripcion": "Interactuar con amigos y familiares mejora el bienestar emocional.",
                "link": "https://www.mind.org.uk" # Enlace a recursos de Mind sobre apoyo social y salud mental
            })

        return recomendaciones


recommendation_service = RecommendationService()