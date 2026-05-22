# Ansiedad Riesgo ML App

> Aplicación móvil con Machine Learning para la estimación del riesgo de ansiedad en estudiantes universitarios.

---

## Descripción

Este proyecto propone el diseño y evaluación de una aplicación móvil basada en técnicas de **Machine Learning** para la **detección temprana del riesgo de ansiedad** en estudiantes universitarios. A partir del análisis de indicadores psicoeducativos, académicos y de estilo de vida (calidad del sueño, rendimiento académico, estrés financiero, entre otros), el sistema estima el nivel de riesgo del estudiante y le proporciona recomendaciones preventivas personalizadas.

La solución integra modelos de clasificación supervisada (Regresión Logística, Random Forest, LightGBM) con una arquitectura cliente-servidor construida sobre **Flutter** y **Flask**, buscando ofrecer una herramienta accesible, precisa y orientada al bienestar emocional del estudiante.

---

## Integrantes

| Nombre | Código |
|---|---|
| Benites Meza, Marco Fabricio | 21200257 |
| Coronado Córtez, Jeferson | 20200131 |
| Munayco Vivanco, Renzo Alexander | 22200107 |
| Morales Mallqui, Denilson Teófilo | 22200263 |
| Torres Mariluz, Josué Armando | 21200251 |

---

## Guía de Configuración Local (Para Desarrolladores)

Si acabas de clonar este repositorio y estás usando **Windows**, sigue estos pasos para levantar el backend en tu máquina local:

1. **Entrar a la carpeta del backend:**
   ```bash
   cd backend
   ```
2. **Crear y activar tu entorno virtual:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate  # Si usas Git Bash
   # .\venv\Scripts\activate      # Si usas CMD o PowerShell
   ```
3. **Instalar las dependencias:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Definir la variable de entorno de Flask (Git Bash):**
   *(Este paso es opcional si ya tienes el archivo `.env`, pero recomendado)*
   ```bash
   export FLASK_APP=run.py
   ```
5. **Inicializar y actualizar la base de datos (SQLite local):**
   ```bash
   flask db upgrade
   flask init-recomendaciones
   ```
6. **Levantar el servidor:**
   ```bash
   flask run
   ```
   *El servidor quedará corriendo en `http://127.0.0.1:5000`.*

---

## Stack tecnológico

- **Frontend móvil:** Flutter
- **Backend:** Flask (Python)
- **Base de datos:** PostgreSQL
- **Machine Learning:** scikit-learn · LightGBM
- **Entorno de entrenamiento:** Google Colab / Jupyter Notebook

---

Proyecto académico — Universidad Nacional Mayor de San Marcos · 2026.
