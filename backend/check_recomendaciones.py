from app import crear_app
from app.models.recomendacion import Recomendacion

app = crear_app()

with app.app_context():
    recs = Recomendacion.query.all()
    print(f'Recomendaciones en BD: {len(recs)}')
    for r in recs:
        print(f'  - {r.categoria}: {r.titulo}')