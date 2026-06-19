"""
Módulo principal - Punto de entrada del servidor Flask
"""
import os
from app import crear_app

app = crear_app()

if __name__ == "__main__":
    # Obtener puerto desde variable de entorno o usar 5000 por defecto
    puerto = int(os.getenv("PORT", 5000))
    # Escuchar en 0.0.0.0 para aceptar conexiones desde cualquier IP
    # (localhost, red local, contenedores Docker, etc.)
    app.run(host="0.0.0.0", port=puerto, debug=True)
