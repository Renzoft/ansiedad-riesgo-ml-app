# Informe del Backend y Modelos de Machine Learning

Este documento explica el funcionamiento técnico de la capa de backend de la aplicación, su arquitectura relacional y el ensamble predictivo de Machine Learning implementado para la estimación del riesgo de ansiedad en estudiantes universitarios (HU-11).

---

## 1. Arquitectura del Backend

El backend está desarrollado utilizando **Python** y el framework **Flask**, con una arquitectura modular orientada a *Blueprints* para asegurar la separación de responsabilidades, la legibilidad y la escalabilidad del código.

### Tecnologías Clave
- **Flask:** Microframework web encargado del enrutamiento de la API REST.
- **SQLAlchemy:** ORM (Object-Relational Mapping) para interactuar de forma segura con la base de datos mediante clases de Python, eliminando la escritura de SQL crudo y previniendo inyecciones SQL.
- **Flask-Migrate (Alembic):** Control de versiones y migraciones estructuradas del esquema de base de datos.
- **Flask-Bcrypt:** Encriptación de contraseñas de usuarios mediante hashing seguro de una vía.
- **Flask-JWT-Extended:** Autenticación de sesiones mediante JSON Web Tokens para la protección de endpoints restringidos a nivel de roles.

### Base de Datos y Persistencia Local (SQLite)
La aplicación almacena toda su información en una base de datos relacional local **SQLite**.
- **Archivo Físico de Persistencia:** Los datos se escriben directamente en el disco duro en el archivo localizado en:
  `backend/instance/base_datos.db`
- **Garantía de Persistencia:** Debido a que SQLite escribe de forma síncrona en un archivo del sistema de archivos de Windows, **los datos de usuarios, evaluaciones e historiales persisten indefinidamente**. Si cierras las terminales de VSCode, apagas tu computadora o detienes el servidor, ningún dato se perderá. Al reiniciar la app, los registros se cargarán de forma íntegra.

---

## 2. Sistema Predictivo y Machine Learning (HU-11)

El propósito central de la aplicación es identificar a estudiantes universitarios con riesgo de ansiedad de manera temprana, basándose en variables psicoeducativas y de estilo de vida.

### Vector de Características
El modelo predice el riesgo combinando **15 características estrictas**, las cuales son recolectadas de manera interactiva por el estudiante mediante el cuestionario paso a paso de Flutter:

1. `phq9_score` (Nivel de depresión, rango 0-27)
2. `gad7_score` (Nivel de ansiedad, rango 0-21)
3. `sleep_hours` (Horas de sueño al día, rango 3.0-10.0)
4. `exercise_freq` (Días de ejercicio a la semana, rango 0-7)
5. `social_activity` (Nivel de actividad social, rango 0-10)
6. `online_stress` (Estrés generado por internet, rango 1-10)
7. `gpa` (Promedio académico acumulado, rango 0.0-5.0)
8. `family_support` (Nivel de apoyo familiar, rango 1-10)
9. `screen_time` (Horas frente a pantallas al día, rango 1.0-12.0)
10. `academic_stress` (Estrés por exigencia de estudios, rango 1-10)
11. `diet_quality` (Calidad de la dieta diaria, rango 1-10)
12. `self_efficacy` (Nivel de autoeficacia y seguridad, rango 1-10)
13. `peer_relationship` (Calidad de relación con compañeros, rango 1-10)
14. `financial_stress` (Estrés por finanzas personales, rango 1-10)
15. `sleep_quality` (Calidad general de descanso, rango 0-10)

Estas variables se registran de manera transaccional en la tabla `evaluacion` por cada intento antes de ser procesadas por el estimador.

---

## 3. Enfoque de Modelado: Ensamble por Votación Suave (Soft Voting)

Para garantizar la mayor precisión y robustez predictiva, reduciendo los falsos negativos comunes en modelos individuales, el sistema implementa un **ensamble de 6 modelos preentrenados** de clasificación binaria (Clase 0: Con Riesgo de Ansiedad, Clase 1: Saludable):

1. **Regresión Logística (`logistic_regression_model.pkl`):** Captura dependencias y pesos lineales base. Espera el vector completo de 15 variables.
2. **K-Nearest Neighbors (`knn_model.pkl`):** Clasifica en base a vecindad de características. Espera 7 variables clave.
3. **LightGBM (`lightgbm_model.pkl`):** Algoritmo de Gradient Boosting ultrarrápido optimizado en árbol. Espera 7 variables clave.
4. **Random Forest (`random_forest_model.pkl`):** Ensamble de árboles de decisión que previene el sobreajuste. Espera 7 variables clave.
5. **XGBoost Ponderado (`xgboost_weighted_model.pkl`):** Potente clasificador con regularización. Espera 7 variables clave.
6. **CatBoost Ponderado (`catboost_weighted_model.pkl`):** Algoritmo de Gradient Boosting de alto desempeño para manejar relaciones complejas. Espera el vector de 15 variables.

La clase `AnxietyPredictorService` en `ml_service.py` recibe el vector del usuario, adapta su tamaño automáticamente según las necesidades de cada modelo (7 o 15 variables) mediante el mapeo interno, invoca la inferencia probabilística de cada uno y realiza un **Promedio Simple de las Probabilidades (Soft Voting)** para generar la estimación final robusta.

---

## 4. Tolerancia a Fallos y Desarrollo Continuo (Fallback)

Debido a que librerías pesadas como `numpy`, `joblib` u otras necesarias para la carga de modelos de Machine Learning pueden no estar presentes durante despliegues rápidos en el frontend, el backend implementa un **mecanismo automático de respaldo (Fallback)**.

Si las librerías científicas fallan al importarse o alguno de los modelos `.pkl` en `app/static/models/` está ausente, el servidor de Flask **no crasheará ni interrumpirá el servicio**. En su lugar, registrará una advertencia y recurrirá a un algoritmo de aproximación clínica estándar que estima la probabilidad basándose puramente en las escalas estandarizadas del test:

```python
probabilidad = (phq9 / 27.0) * 0.6 + (gad7 / 21.0) * 0.4
```

Esto garantiza el desarrollo continuo y permite probar la base de datos y flujos de usuario sin depender de dependencias de IA.

---

## 5. Categorización de Resultados y Recomendaciones

La probabilidad de riesgo resultante (rango de 0.0 a 1.0) es clasificada automáticamente en el backend en una de tres categorías de alerta:
- **Riesgo Bajo (Probabilidad < 0.35):** Indica equilibrio emocional. Vincula recomendaciones de mantenimiento y hábitos saludables.
- **Riesgo Medio (Probabilidad de 0.35 a 0.70):** Indica alertas en el descanso o estrés académico. Sugiere pausas activas y autoevaluación de tiempos.
- **Riesgo Alto (Probabilidad > 0.70):** Alerta crítica de susceptibilidad a ansiedad severa. Recomienda de forma urgente consultar con el departamento de bienestar estudiantil o psicólogos profesionales.

El endpoint asocia dinámicamente estas recomendaciones (almacenadas de forma inicial en SQLite) mediante una relación de muchos a muchos (`ResultadoML.recomendaciones`) y las retorna al cliente en formato JSON listo para visualizar.
