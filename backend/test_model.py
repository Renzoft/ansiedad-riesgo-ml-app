import sys, logging
logging.basicConfig(level=logging.WARNING)
sys.path.insert(0, '.')

from app.services.ml_service import predictor

vector = [8, 6, 7.5, 3, 6, 6, 3.5, 7, 5, 7, 7, 6, 6, 5, 7]
prob = predictor.predecir(vector)

print('modelos_cargados:', predictor.modelos_cargados)
print('prediccion:', prob)
