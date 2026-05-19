"""
Servicio de Machine Learning para estimar riesgo de ansiedad
"""
import os
import logging

try:
    import numpy as np
except ImportError:
    np = None

try:
    import joblib
except ImportError:
    joblib = None

class AnxietyPredictorService:
    """
    Clase para manejar las predicciones de ansiedad utilizando modelos de ML preentrenados.
    """
    def __init__(self):
        self.logistic_regression = None
        self.catboost_model = None
        self.random_forest = None
        self.modelos_cargados = False
        self._cargar_modelos()

    def _cargar_modelos(self):
        """
        Intenta cargar los modelos desde app/static/models/
        """
        if joblib is None or np is None:
            logging.warning("Librerías numpy o joblib no instaladas. Se usará el fallback de forma automática.")
            self.modelos_cargados = False
            return

        try:
            # Asumiendo que la ruta es backend/app/services, vamos a buscar la carpeta static
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            models_dir = os.path.join(base_dir, 'static', 'models')
            
            # Crear directorio si no existe (para evitar errores en la carga inicial)
            if not os.path.exists(models_dir):
                os.makedirs(models_dir)

            ruta_lr = os.path.join(models_dir, 'logistic_regression.pkl')
            ruta_cb = os.path.join(models_dir, 'catboost_model.pkl')
            ruta_rf = os.path.join(models_dir, 'random_forest.pkl')

            # Solo intentar cargar si los archivos realmente existen
            if os.path.exists(ruta_lr) and os.path.exists(ruta_cb) and os.path.exists(ruta_rf):
                self.logistic_regression = joblib.load(ruta_lr)
                self.catboost_model = joblib.load(ruta_cb)
                self.random_forest = joblib.load(ruta_rf)
                self.modelos_cargados = True
                logging.info("Modelos de ML cargados exitosamente.")
            else:
                logging.warning("No se encontraron los archivos .pkl en static/models. Activando fallback.")
                self.modelos_cargados = False

        except Exception as e:
            logging.warning(f"No se pudieron cargar los modelos de ML. Se usará el fallback. Error: {str(e)}")
            self.modelos_cargados = False

    def predecir(self, vector):
        """
        Realiza la predicción del riesgo de ansiedad.
        vector: lista o array de 15 características en orden estricto.
        """
        if len(vector) != 15:
            raise ValueError(f"El vector debe contener exactamente 15 características. Recibido: {len(vector)}")

        # Extraer variables para el fallback (phq9 es index 0, gad7 es index 1)
        phq9 = vector[0]
        gad7 = vector[1]

        if self.modelos_cargados and np is not None and joblib is not None:
            try:
                # Convertir a array de NumPy
                X = np.array(vector).reshape(1, -1)

                # Obtener probabilidades (se asume que la Clase 0 es riesgo de ansiedad)
                prob_lr = self.logistic_regression.predict_proba(X)[0][0]
                prob_cb = self.catboost_model.predict_proba(X)[0][0]
                prob_rf = self.random_forest.predict_proba(X)[0][0]

                # Ensamble por Votación Suave (Promedio simple)
                probabilidad_final = (prob_lr + prob_cb + prob_rf) / 3.0
                return probabilidad_final
            except Exception as e:
                logging.error(f"Error al predecir con los modelos: {str(e)}. Activando fallback.")
                return self._fallback(phq9, gad7)
        else:
            return self._fallback(phq9, gad7)

    def _fallback(self, phq9, gad7):
        """
        Lógica temporal de cálculo de probabilidad de riesgo.
        """
        probabilidad = (phq9 / 27.0) * 0.6 + (gad7 / 21.0) * 0.4
        
        # Asegurar que esté entre 0 y 1
        if probabilidad > 1.0:
            probabilidad = 1.0
        elif probabilidad < 0.0:
            probabilidad = 0.0
            
        return float(probabilidad)

# Instancia global para ser importada
predictor = AnxietyPredictorService()
