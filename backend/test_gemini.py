"""
Script de prueba para verificar que GeminiService funciona correctamente
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app import crear_app
from app.services.gemini_service import GeminiService

# Crear la aplicación Flask
app = crear_app()

# Probar GeminiService
with app.app_context():
    print("=" * 60)
    print("PRUEBA DE GEMINI SERVICE")
    print("=" * 60)
    
    # Verificar que el servicio está registrado
    gemini_service = app.extensions.get("gemini")
    if not gemini_service:
        print("❌ ERROR: GeminiService no está registrado en app.extensions")
        sys.exit(1)
    
    print("✅ GeminiService encontrado en app.extensions")
    
    # Probar generación de reporte
    print("\n📝 Generando reporte de prueba...")
    try:
        reporte = gemini_service.generar_reporte(
            nivel_riesgo="MEDIO",
            probabilidad=0.65,
            variables={
                "phq9_score": 15,
                "gad7_score": 12,
                "sleep_hours": 5.5,
                "exercise_freq": 2,
                "social_activity": 4,
                "online_stress": 7,
                "gpa": 3.2,
                "family_support": 6,
                "screen_time": 8.5,
                "academic_stress": 8,
                "diet_quality": 5,
                "self_efficacy": 6,
                "peer_relationship": 7,
                "financial_stress": 6,
                "sleep_quality": 5
            }
        )
        
        print("✅ Reporte generado exitosamente")
        print(f"\n📊 Tipo: {type(reporte)}")
        print(f"\n📋 Resumen: {reporte.get('resumen', 'N/A')[:100]}...")
        print(f"\n💡 Recomendaciones: {len(reporte.get('recomendaciones', []))}")
        
        if reporte.get('recomendaciones'):
            print("\nPrimera recomendación:")
            rec = reporte['recomendaciones'][0]
            print(f"  - Título: {rec.get('titulo', 'N/A')}")
            print(f"  - Descripción: {rec.get('descripcion', 'N/A')[:100]}...")
        
        print("\n" + "=" * 60)
        print("✅ PRUEBA EXITOSA - Gemini está funcionando correctamente")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ ERROR al generar reporte: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)