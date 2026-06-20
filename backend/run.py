"""
Módulo principal - Punto de entrada del servidor Flask
"""
import os
from app import crear_app

app = crear_app()

# Crear tablas, admin y recomendaciones automáticamente al iniciar
with app.app_context():
    from app.models.usuario import db, Usuario
    from app.models.recomendacion import Recomendacion
    from app.utils.roles import ROLE_ADMIN
    from sqlalchemy import inspect
    
    inspector = inspect(db.engine)
    
    # ==========================================
    # 1. CREAR TABLAS SI NO EXISTEN
    # ==========================================
    if not inspector.has_table('usuarios'):
        print("⚠️  No se encontraron tablas. Creando tablas automáticamente...")
        db.create_all()
        print("✅ Tablas creadas correctamente")
    else:
        print("✅ Tablas ya existen")
    
    # ==========================================
    # 2. CREAR USUARIO ADMIN SI NO EXISTE
    # ==========================================
    admin = Usuario.query.filter_by(correo="admin@test.com").first()
    if not admin:
        admin = Usuario(
            nombre="Administrador",
            correo="admin@test.com",
            facultad="Sistema",
            ciclo=1,
            rol=ROLE_ADMIN
        )
        admin.establecer_contrasena("admin123")
        db.session.add(admin)
        db.session.commit()
        print("✅ Usuario admin creado: admin@test.com / admin123")
    else:
        print("ℹ️  Usuario admin ya existe")
    
    # ==========================================
    # 3. INSERTAR RECOMENDACIONES SI NO EXISTEN
    # ==========================================
    if Recomendacion.query.count() == 0:
        recomendaciones = [
            Recomendacion(
                categoria="BAJO",
                titulo="Mantén tus hábitos saludables",
                descripcion="Tus indicadores muestran un equilibrio saludable. "
                            "Continúa con tus rutinas de sueño, ejercicio y alimentación."
            ),
            Recomendacion(
                categoria="MEDIO",
                titulo="Refuerza tus estrategias de manejo del estrés",
                descripcion="Se detectan ciertos niveles de alerta. "
                            "Revisa tus horas de sueño y busca apoyo en tus compañeros."
            ),
            Recomendacion(
                categoria="ALTO",
                titulo="Busca apoyo profesional",
                descripcion="Tus indicadores sugieren una alta predisposición a ansiedad. "
                            "Acude al departamento de bienestar estudiantil."
            ),
        ]
        db.session.add_all(recomendaciones)
        db.session.commit()
        print("✅ Recomendaciones base insertadas (BAJO, MEDIO, ALTO)")
    else:
        print("ℹ️  Recomendaciones ya existen")

if __name__ == "__main__":
    # Obtener puerto desde variable de entorno o usar 5000 por defecto
    puerto = int(os.getenv("PORT", 5000))
    # Escuchar en 0.0.0.0 para aceptar conexiones desde cualquier IP
    # (localhost, red local, contenedores Docker, etc.)
    app.run(host="0.0.0.0", port=puerto, debug=True)
