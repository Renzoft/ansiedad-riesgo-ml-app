"""
Script para crear el admin
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import crear_app
from app.models.usuario import db, Usuario
from app.utils.roles import ROLE_ADMIN


app = crear_app()

with app.app_context():

    admin = Usuario.query.filter_by(correo="admin@sistema.com").first()

    if not admin:

        admin = Usuario(
            nombre="Admin",
            correo="admin@sistema.com",
            facultad="Sistema",
            ciclo=0,
            rol=ROLE_ADMIN,
        )

        admin.establecer_contrasena("admin123")

        db.session.add(admin)
        db.session.commit()

        print("Admin creado")
    else:
        print("Admin ya existe")
