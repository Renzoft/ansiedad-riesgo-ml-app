"""
Script para inicializar las recomendaciones base en la base de datos
"""
from app import crear_app
from app.models.recomendacion import Recomendacion

app = crear_app()

with app.app_context():
    # Verificar si ya existen recomendaciones
    existentes = Recomendacion.query.count()
    if existentes > 0:
        print(f"Ya existen {existentes} recomendaciones en la base de datos. No se insertaron nuevas.")
        exit(0)
    
    recomendaciones_base = [
        Recomendacion(
            categoria="BAJO",
            titulo="Mantén tus hábitos saludables",
            descripcion="Tus indicadores muestran un equilibrio saludable. "
                        "Continúa con tus rutinas de sueño, ejercicio y alimentación. "
                        "Considera practicar mindfulness para mantener tu bienestar."
        ),
        Recomendacion(
            categoria="MEDIO",
            titulo="Refuerza tus estrategias de manejo del estrés",
            descripcion="Se detectan ciertos niveles de alerta en tus indicadores. "
                        "Revisa tus horas de sueño, incorpora pausas activas durante el estudio "
                        "y busca apoyo en tus compañeros o familiares. "
                        "Considera consultar con el servicio de bienestar estudiantil."
        ),
        Recomendacion(
            categoria="ALTO",
            titulo="Busca apoyo profesional",
            descripcion="Tus indicadores sugieren una alta predisposición a ansiedad. "
                        "Es importante que acudas al departamento de bienestar estudiantil "
                        "o a un profesional de salud mental. No estás solo/a, "
                        "hay recursos disponibles para apoyarte."
        ),
    ]
    
    try:
        from app.models.usuario import db
        db.session.add_all(recomendaciones_base)
        db.session.commit()
        print("3 recomendaciones base insertadas correctamente (BAJO, MEDIO, ALTO).")
    except Exception as e:
        db.session.rollback()
        print(f"Error al insertar recomendaciones: {str(e)}")