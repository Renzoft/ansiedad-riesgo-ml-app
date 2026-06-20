"""
Módulo principal - Punto de entrada del servidor Flask
"""
import os
from app import crear_app

app = crear_app()

# Crear tablas automáticamente al iniciar (solo en desarrollo/pruebas)
# En producción con disco persistente, usar flask db upgrade
with app.app_context():
    from app.models.usuario import db
    from sqlalchemy import inspect
    inspector = inspect(db.engine)
    if not inspector.has_table('usuarios'):
        print("⚠️  No se encontraron tablas. Creando tablas automáticamente...")
        db.create_all()
        print("✅ Tablas creadas correctamente")
    else:
        print("✅ Tablas ya existen")

if __name__ == "__main__":
    # Obtener puerto desde variable de entorno o usar 5000 por defecto
    puerto = int(os.getenv("PORT", 5000))
    # Escuchar en 0.0.0.0 para aceptar conexiones desde cualquier IP
    # (localhost, red local, contenedores Docker, etc.)
    app.run(host="0.0.0.0", port=puerto, debug=True)
