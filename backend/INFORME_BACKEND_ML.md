# Informe del Backend y Modelos de Machine Learning

Este documento explica el funcionamiento técnico de la capa de backend de la aplicación, su arquitectura, y los detalles sobre el modelo predictivo de Machine Learning implementado para estimar el riesgo de ansiedad (HU-11).

## 1. Arquitectura del Backend

El backend está desarrollado utilizando **Python** y el framework **Flask**, con una arquitectura orientada a Blueprints (módulos) para mantener un código limpio, legible y escalable.

### Tecnologías Clave
- **Flask:** Microframework web encargado del enrutamiento.
- **SQLAlchemy:** ORM (Object-Relational Mapping) para interactuar con la base de datos sin escribir SQL crudo.
- **Flask-Migrate (Alembic):** Control de versiones y migraciones de esquemas en la base de datos (se usa el parámetro `render_as_batch=True` internamente para un soporte óptimo de alteraciones de tablas en SQLite).
- **Flask-JWT-Extended:** Autenticación segura y persistencia de sesión a través de JSON Web Tokens para proteger los endpoints.
- **SQLite:** Base de datos relacional ligera utilizada en la fase actual de desarrollo.

### Módulos Principales (Blueprints)
- `/registro` y `/login`: Gestión segura de identidades, perfiles multidimensionales y contraseñas encriptadas (usando bcrypt).
- `/habitos`: Endpoints protegidos para registrar y consultar indicadores de estilo de vida diarios (sueño, dieta, pantallas).
- `/api/v1/evaluaciones`: Endpoints para generar predicciones de riesgo emocional e interrogar el historial de evaluaciones del usuario.

---

## 2. Sistema Predictivo y Machine Learning (HU-11)

El propósito central de la aplicación es identificar a estudiantes universitarios con riesgo de ansiedad de manera temprana, basándose en variables psicoeducativas y de estilo de vida.

### Vector de Características
El modelo predice el riesgo combinando **15 características estrictas**, extraídas de dos fuentes: el perfil del estudiante (9 variables) y su último hábito diario (6 variables).

**Orden estricto procesado por el modelo:**
1. `phq9` (Depresión, 0-27)
2. `gad7` (Ansiedad, 0-21)
3. `sleep_hours` (Horas de sueño)
4. `exercise_freq` (Frecuencia de ejercicio)
5. `social_activity` (Actividad social)
6. `online_stress` (Estrés online)
7. `gpa` (Rendimiento académico)
8. `family_support` (Apoyo familiar)
9. `screen_time` (Tiempo de pantalla)
10. `academic_stress` (Estrés académico)
11. `diet_quality` (Calidad de dieta)
12. `self_efficacy` (Autoeficacia)
13. `peer_relationship` (Relación con compañeros)
14. `financial_stress` (Estrés financiero)
15. `sleep_quality` (Calidad de sueño)

### Proceso de Entrenamiento de los Modelos
El entrenamiento de estos modelos se realizó de forma aislada en un entorno de **Jupyter Notebook / Google Colab** utilizando la librería `scikit-learn` y el framework `CatBoost`. El flujo de trabajo para generar los archivos `.pkl` fue el siguiente:

1. **Recolección y Limpieza de Datos:** 
   - Se utilizó el dataset público de Kaggle centrado en la salud mental, hábitos y rendimiento de estudiantes universitarios.
   - Se aplicó limpieza de datos, eliminando duplicados y manejando valores atípicos (outliers) e imputación de nulos.
2. **Preprocesamiento:**
   - **Escalado:** Las variables numéricas (como `phq9`, `gad7`, `gpa`) fueron estandarizadas mediante `StandardScaler` o `MinMaxScaler` para asegurar que los modelos sensibles a la escala (como Regresión Logística) no tengan sesgos.
   - **Balanceo:** Se aplicaron técnicas de balanceo (como SMOTE o ajuste de pesos) para contrarrestar el desbalance natural de las clases en diagnósticos médicos.
3. **Definición del Target (Variable Objetivo):**
   - Se definió un problema de clasificación binaria estricta donde la **Clase 0** representa "Estudiante en Riesgo de Ansiedad" y la **Clase 1** representa "Saludable".
4. **Entrenamiento y Afinamiento (Hyperparameter Tuning):**
   - El dataset fue dividido en entrenamiento (80%) y prueba (20%).
   - Se empleó Validación Cruzada (K-Fold Cross-Validation) y `GridSearchCV` para encontrar los hiperparámetros óptimos que maximicen el **Recall** (sensibilidad para detectar los positivos reales) y el **F1-Score**.
5. **Exportación de Artefactos:**
   - Una vez validados los tres algoritmos elegidos, los modelos resultantes fueron serializados y comprimidos utilizando la librería `joblib`.
   - Se generaron los archivos binarios `logistic_regression.pkl`, `catboost_model.pkl` y `random_forest.pkl`, los cuales se ubican en `backend/app/static/models/` listos para ser consumidos por el backend de Flask en producción.

### Enfoque de Modelado: Ensamble por Votación Suave (Soft Voting)
Para garantizar el mejor rendimiento predictivo sobre el dataset, se utiliza un ensamble de tres modelos pre-entrenados:
1. **Regresión Logística:** Excelente para capturar linealidades y pesos base.
2. **CatBoost:** Poderoso algoritmo de Gradient Boosting que maneja excepcionalmente bien relaciones complejas y no lineales.
3. **Random Forest:** Conjunto de múltiples árboles de decisión que previene el sobreajuste (overfitting).

En lugar de que un solo modelo tenga la última palabra, la aplicación utiliza **Soft Voting**. La clase `AnxietyPredictorService` recibe las probabilidades individuales de cada modelo y obtiene un promedio ponderado exacto, devolviendo un resultado estadísticamente mucho más robusto.

### Tolerancia a Fallos y Desarrollo Continuo (Fallback)
Dado que las librerías `numpy` y `joblib` (necesarias para inferir modelos `.pkl`) son pesadas y pueden no estar instaladas durante pruebas rápidas de frontend o desarrollo paralelo, el sistema es **altamente tolerante a fallos de importación**.

Si la aplicación detecta que faltan las librerías ML o los archivos de los modelos, no crashea la API. En su lugar, activa automáticamente un **Fallback Matemático** basado en escalas clínicas estándar:
```python
probabilidad = (phq9 / 27.0) * 0.6 + (gad7 / 21.0) * 0.4
```
Esto permite probar las lógicas de categorización y guardado en la base de datos sin depender del despliegue de los modelos.

### Categorización de Resultados y Acción
La probabilidad resultante (entre 0 y 1) se clasifica automáticamente para devolver información amigable y empática al frontend:
- **< 0.35 (BAJO):** Equilibrio saludable.
- **0.35 a 0.70 (MEDIO):** Ciertos niveles de alerta (Requiere revisión de hábitos).
- **> 0.70 (ALTO):** Alta predisposición a la ansiedad. Recomienda orientación inmediata.
