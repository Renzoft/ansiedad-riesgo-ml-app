"""
Servicio de Machine Learning para estimar riesgo de ansiedad
Utiliza 6 modelos preentrenados y combina sus predicciones mediante ensamble.
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
    Clase para manejar las predicciones de ansiedad utilizando 6 modelos de ML
    preentrenados almacenados en app/static/models/.
    """

    # Nombres exactos de los archivos .pkl que deben estar en static/models/
    NOMBRES_MODELOS = [
        "logistic_regression_model.pkl",   # Regresión Logística (usa 15 features)
        "knn_model.pkl",                   # K-Nearest Neighbors (usa 7 features)
        "lightgbm_model.pkl",              # LightGBM              (usa 7 features)
        "random_forest_model.pkl",         # Random Forest         (usa 7 features)
        "xgboost_weighted_model.pkl",      # XGBoost ponderado     (usa 7 features)
        "catboost_weighted_model.pkl",     # CatBoost ponderado    (usa 15 features)
    ]

    # Subconjunto de 7 variables que usan algunos modelos (KNN, LightGBM, RF, XGBoost)
    # Mapeo: nombre esperado -> índice en el vector de 15
    INDICES_7_FEATURES = {
        "PHQ9": 0,              # phq9_score         (índice 0)
        "GAD7": 1,              # gad7_score         (índice 1)
        "SleepHours": 2,        # sleep_hours        (índice 2)
        "ExerciseFreq": 3,      # exercise_freq      (índice 3)
        "SocialActivity": 4,    # social_activity    (índice 4)
        "OnlineStress": 5,      # online_stress      (índice 5)
        "FinancialStress": 13,  # financial_stress   (índice 13)
    }

    def __init__(self):
        """Inicializa el servicio e intenta cargar los modelos."""
        self.modelos = {}           # dict: nombre -> modelo cargado
        self.modelos_info = {}      # dict: nombre -> {'n_features': int, 'feature_names': list or None}
        self.modelos_cargados = False
        self._cargar_modelos()

    def _cargar_modelos(self):
        """
        Intenta cargar los 6 modelos desde app/static/models/.
        Si alguno falla o no existe, activa el fallback.
        """
        if joblib is None or np is None:
            logging.warning(
                "Librerías numpy o joblib no instaladas. "
                "Se usará el fallback de forma automática."
            )
            self.modelos_cargados = False
            return

        try:
            # Ruta base: backend/app/ → se sube a backend/app/static/models/
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            models_dir = os.path.join(base_dir, "static", "models")

            # Crear directorio si no existe
            if not os.path.exists(models_dir):
                os.makedirs(models_dir)
                logging.info(f"Directorio creado: {models_dir}")

            modelos_temp = {}
            info_temp = {}
            todos_existen = True

            for nombre in self.NOMBRES_MODELOS:
                ruta = os.path.join(models_dir, nombre)
                if os.path.exists(ruta):
                    try:
                        modelo = joblib.load(ruta)
                        modelos_temp[nombre] = modelo

                        # Detectar cuántas features espera el modelo
                        n_features = self._detectar_n_features(modelo)
                        info_temp[nombre] = {
                            'n_features': n_features,
                            'feature_names': self._detectar_feature_names(modelo)
                        }
                        logging.info(
                            f"Modelo cargado: {nombre} "
                            f"(espera {n_features} features)"
                        )
                    except Exception as e:
                        logging.warning(
                            f"Error al cargar {nombre}: {str(e)}. "
                            "Se usará fallback."
                        )
                        todos_existen = False
                        break
                else:
                    logging.warning(
                        f"Archivo no encontrado: {nombre}. "
                        "Se usará fallback."
                    )
                    todos_existen = False
                    break

            if todos_existen and len(modelos_temp) == len(self.NOMBRES_MODELOS):
                self.modelos = modelos_temp
                self.modelos_info = info_temp
                self.modelos_cargados = True
                logging.info(
                    f"Los 6 modelos de ML se cargaron exitosamente desde {models_dir}."
                )
            else:
                self.modelos_cargados = False

        except Exception as e:
            logging.warning(
                f"No se pudieron cargar los modelos de ML. "
                f"Se usará el fallback. Error: {str(e)}"
            )
            self.modelos_cargados = False

    # ------------------------------------------------------------------
    # MÉTODOS AUXILIARES PARA DETECTAR ESTRUCTURA DE CADA MODELO
    # ------------------------------------------------------------------

    @staticmethod
    def _detectar_n_features(modelo):
        """
        Intenta determinar cuántas features espera el modelo.
        Retorna 0 si no se puede determinar.
        """
        # Para modelos sklearn (RandomForest, KNN, LogisticRegression)
        if hasattr(modelo, 'n_features_in_'):
            return modelo.n_features_in_

        # Para pipelines de sklearn
        if hasattr(modelo, 'steps') and hasattr(modelo, 'n_features_in_'):
            return modelo.n_features_in_

        # Para XGBoost
        if hasattr(modelo, '_Booster'):
            try:
                return modelo._Booster.num_features()
            except Exception:
                pass
        if hasattr(modelo, 'n_features_in_'):
            return modelo.n_features_in_

        # Para LightGBM
        if hasattr(modelo, 'n_features_'):
            return modelo.n_features_

        # CatBoost
        if hasattr(modelo, 'feature_count_'):
            return modelo.feature_count_

        return 0

    @staticmethod
    def _detectar_feature_names(modelo):
        """
        Intenta obtener los nombres de las features si están disponibles.
        """
        if hasattr(modelo, 'feature_names_in_'):
            return list(modelo.feature_names_in_)
        if hasattr(modelo, 'feature_name_') and modelo.feature_name_:
            return list(modelo.feature_name_)
        return None

    # ------------------------------------------------------------------
    # ADAPTACIÓN DEL VECTOR SEGÚN EL MODELO
    # ------------------------------------------------------------------

    def _adaptar_vector(self, vector_completo, n_features, feature_names):
        """
        Adapta el vector de 15 features al número de features que espera el modelo.

        - Si el modelo espera 15 features → usa el vector completo.
        - Si el modelo espera 7 features  → extrae el subconjunto según INDICES_7_FEATURES.
        - Si el modelo espera otro número  → usa el fallback.
        """
        if n_features == 15 or n_features == 0:
            # Usar vector completo
            return np.array(vector_completo).reshape(1, -1)

        elif n_features == 7:
            # Extraer solo las 7 variables que esperan estos modelos
            indices = list(self.INDICES_7_FEATURES.values())
            vector_7 = [vector_completo[i] for i in indices]
            return np.array(vector_7).reshape(1, -1)

        else:
            # No sabemos cómo adaptar, devolvemos el completo
            logging.warning(
                f"El modelo espera {n_features} features, "
                "no se sabe cómo adaptar. Usando vector completo."
            )
            return np.array(vector_completo).reshape(1, -1)

    # ------------------------------------------------------------------
    # PREDICCIÓN
    # ------------------------------------------------------------------

    def predecir(self, vector):
        """
        Realiza la predicción del riesgo de ansiedad.

        Parámetros
        ----------
        vector : list or array
            Lista de 15 características en el orden estricto definido
            en evaluaciones_routes.py.

        Retorna
        -------
        float
            Probabilidad de riesgo de ansiedad entre 0.0 y 1.0.
        """
        if len(vector) != 15:
            raise ValueError(
                f"El vector debe contener exactamente 15 características. "
                f"Recibido: {len(vector)}"
            )

        # Extraer variables para el fallback (phq9 es índice 0, gad7 es índice 1)
        phq9 = vector[0]
        gad7 = vector[1]

        if self.modelos_cargados and np is not None and joblib is not None:
            try:
                probabilidades = []

                for nombre, modelo in self.modelos.items():
                    try:
                        info = self.modelos_info.get(nombre, {})
                        n_features = info.get('n_features', 0)
                        feature_names = info.get('feature_names')

                        # Adaptar el vector al número de features del modelo
                        X = self._adaptar_vector(
                            vector, n_features, feature_names
                        )

                        # predict_proba retorna [[prob_clase_0, prob_clase_1]]
                        # Tomamos la probabilidad de la clase 0 (riesgo de ansiedad)
                        prob = modelo.predict_proba(X)[0][0]
                        probabilidades.append(prob)

                    except Exception as e:
                        logging.error(
                            f"Error al predecir con {nombre}: {str(e)}"
                        )
                        # Si un modelo falla, usamos el fallback como respaldo
                        prob_fallback = self._fallback(phq9, gad7)
                        probabilidades.append(prob_fallback)

                # Ensamble por Votación Suave (Promedio simple de los 6 modelos)
                probabilidad_final = float(np.mean(probabilidades))

                # Asegurar que esté entre 0 y 1
                probabilidad_final = max(0.0, min(1.0, probabilidad_final))

                return probabilidad_final

            except Exception as e:
                logging.error(
                    f"Error al predecir con los modelos: {str(e)}. "
                    "Activando fallback."
                )
                return self._fallback(phq9, gad7)
        else:
            return self._fallback(phq9, gad7)

    # ------------------------------------------------------------------
    # FALLBACK
    # ------------------------------------------------------------------

    @staticmethod
    def _fallback(phq9, gad7):
        """
        Fórmula de respaldo cuando los modelos ML no están disponibles.
        Usa solo PHQ-9 (60%) y GAD-7 (40%) para estimar la probabilidad.
        """
        probabilidad = (phq9 / 27.0) * 0.6 + (gad7 / 21.0) * 0.4

        # Asegurar que esté entre 0 y 1
        if probabilidad > 1.0:
            probabilidad = 1.0
        elif probabilidad < 0.0:
            probabilidad = 0.0

        return float(probabilidad)


# Instancia global para ser importada desde otros módulos
predictor = AnxietyPredictorService()