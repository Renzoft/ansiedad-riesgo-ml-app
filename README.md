# Ansiedad Riesgo ML App

> Aplicación móvil con Machine Learning para la estimación del riesgo de ansiedad en estudiantes universitarios.

---

## Descripción

Este proyecto propone el diseño y evaluación de una aplicación móvil basada en técnicas de **Machine Learning** para la **detección temprana del riesgo de ansiedad** en estudiantes universitarios. A partir del análisis de indicadores psicoeducativos, académicos y de estilo de vida (calidad del sueño, rendimiento académico, estrés financiero, entre otros), el sistema estima el nivel de riesgo del estudiante y le proporciona recomendaciones preventivas personalizadas de forma inmediata.

La solución integra un backend robusto basado en **Flask** con un ensamble multimodelo (6 modelos predictivos coordinados) y un cliente móvil multiplataforma desarrollado en **Flutter**, garantizando confidencialidad, persistencia de datos local (SQLite) y una interfaz de usuario interactiva y en español.

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

## Arquitectura del Proyecto

El sistema adopta un modelo de arquitectura **Cliente-Servidor (REST API)**:
- **Cliente (Frontend):** Desarrollado en **Flutter** bajo el patrón **MVVM** (Model-View-ViewModel). Se comunica con la API mediante peticiones HTTP asíncronas seguras con tokens JWT.
- **Servidor (Backend):** Desarrollado en **Flask (Python)** mediante *Blueprints* modulares. Implementa persistencia local en una base de datos relacional SQLite y contiene el microservicio de evaluación con modelos de Machine Learning.

---

## Guía de Configuración Local Paso a Paso (Windows)

Asegúrate de realizar los pasos desde una terminal de **Git Bash** dentro de VSCode.

### Parte 1: Levantar el Backend (Flask)

1. **Navega a la carpeta del backend:**
   ```bash
   cd backend
   ```
2. **Crea y activa el entorno virtual de Python:**
   ```bash
   python -m venv venv
   source venv/Scripts/activate
   ```
   *(Verás que la terminal ahora indica `(venv)` al inicio de la línea de comandos).*
3. **Instala las dependencias necesarias:**
   ```bash
   pip install -r requirements.txt
   ```
   *(Opcional: Si quieres habilitar el ensamble predictivo real completo de ML en lugar de la fórmula matemática de respaldo, instala también `pip install numpy joblib scikit-learn lightgbm xgboost catboost`).*
4. **Inicializa y actualiza la Base de Datos (SQLite local):**
   ```bash
   flask db upgrade
   flask init-recomendaciones
   ```
   *Nota: Las recomendaciones y los usuarios se guardan en el archivo físico `backend/instance/base_datos.db`. Los datos persisten indefinidamente incluso si cierras la terminal o apagas tu computadora.*
5. **Enciende el servidor de Flask:**
   ```bash
   flask run
   ```
   *El servidor quedará corriendo en http://127.0.0.1:5000. No cierres esta pestaña de la terminal.*

---

### Parte 2: Configurar y Levantar el Frontend (Flutter)

Abre una **segunda pestaña** de la terminal de Git Bash y sigue estos pasos:

1. **Navega a la carpeta del frontend:**
   ```bash
   cd frontend
   ```
2. **Descarga los paquetes de Flutter:**
   ```bash
   flutter pub get
   ```
3. **Encender el Celular Virtual (Emulador):**
   * Abre las **Variables de Entorno** de tu Windows y asegúrate de crear la variable de usuario `ANDROID_HOME` apuntando al SDK (`C:\Android`).
   * En la variable `Path` de usuario, agrega las rutas: `C:\Android\platform-tools`, `C:\Android\emulator` y `C:\Android\cmdline-tools\latest\bin`.
   * En VSCode, presiona `Ctrl + Shift + P`, escribe `Flutter: Launch Emulator`, presiona Enter y selecciona tu dispositivo creado (ej. `Pixel_5_API_34`). El celular aparecerá flotando en tu pantalla.
4. **Ejecutar la Aplicación:**
   ```bash
   flutter run
   ```
   *(Flutter detectará el emulador y cargará la aplicación en el celular virtual para que realices tus pruebas en español).*

---

## Stack Tecnológico

- **Frontend móvil:** Flutter (Dart) - Patrón MVVM + Provider.
- **Backend:** Flask (Python) - SQLAlchemy, Flask-Migrate, Flask-JWT-Extended.
- **Base de datos:** SQLite (Desarrollo local persistente).
- **Machine Learning (Ensamble de 6 Modelos):** Regresión Logística, KNN, LightGBM, Random Forest, XGBoost y CatBoost.
- **Entorno de entrenamiento:** Google Colab / Jupyter Notebook.

---

Proyecto académico — Universidad Nacional Mayor de San Marcos · 2026.
