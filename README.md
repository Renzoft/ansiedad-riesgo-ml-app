# Ansiedad Riesgo ML App

> Aplicación móvil multiplataforma con Machine Learning para la estimación del riesgo de ansiedad en estudiantes universitarios.

---

## Descripción

Este proyecto propone el diseño y evaluación de una aplicación móvil basada en técnicas de **Machine Learning** para la **detección temprana del riesgo de ansiedad** en estudiantes universitarios. A partir del análisis de indicadores psicoeducativos, académicos y de estilo de vida (calidad del sueño, rendimiento académico, estrés financiero, entre otros), el sistema estima el nivel de riesgo del estudiante y le proporciona recomendaciones preventivas personalizadas de forma inmediata.

La solución integra un **backend robusto basado en Flask (Python)** con un **ensamble multimodelo** (6 modelos predictivos coordinados mediante Soft Voting) y un **cliente móvil multiplataforma desarrollado en Flutter**, garantizando confidencialidad, persistencia de datos local (SQLite) y una interfaz de usuario interactiva y en español.

### Roles de Usuario

| Rol | Descripción |
|-----|-------------|
| **Estudiante** | Realiza evaluaciones de riesgo, visualiza su historial y recibe recomendaciones personalizadas |
| **Médico** | Consulta pacientes asignados, revisa evaluaciones y estadísticas de riesgo |
| **Administrador** | Gestiona usuarios (CRUD), asigna roles, visualiza estadísticas globales del sistema |

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

```
┌─────────────────────────────────────────────────────────────┐
│                    CLIENTE (Flutter)                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐       │
│  │    Vistas     │  │  ViewModels  │  │   Servicios   │       │
│  │   (Screens)   │──│  (Provider)  │──│ (API Service) │       │
│  └──────────────┘  └──────────────┘  └──────┬───────┘       │
│                    Patrón MVVM              │ HTTP (JWT)     │
└─────────────────────────────────────────────┼────────────────┘
                                              │
┌─────────────────────────────────────────────┼────────────────┐
│                    SERVIDOR (Flask)          ▼                │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Blueprints Modulares                     │    │
│  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐   │    │
│  │  │   Auth   │ │Eval ML   │ │  Admin  │ │ Médico  │   │    │
│  │  └──────────┘ └──────────┘ └─────────┘ └─────────┘   │    │
│  └──────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Servicios ML                              │    │
│  │  ┌─────────────────────────────────────────────────┐  │    │
│  │  │  Ensamble Predictivo (6 modelos) + Fallback     │  │    │
│  │  └─────────────────────────────────────────────────┘  │    │
│  └──────────────────────────────────────────────────────┘    │
│  ┌──────────────────────────────────────────────────────┐    │
│  │              Base de Datos (SQLite)                   │    │
│  │  usuarios ── evaluacion ── resultados_ml ── recs    │    │
│  └──────────────────────────────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

### Cliente (Frontend)

- Desarrollado en **Flutter (Dart)** bajo el patrón **MVVM (Model-View-ViewModel)**.
- **Gestión de estado:** Provider para notificar cambios entre ViewModels y vistas.
- Se comunica con la API mediante peticiones HTTP asíncronas autenticadas con **tokens JWT**.
- Interfaz con temática claro/oscuro, animaciones y gráficos interactivos.
- **Pantallas principales:**
  - Onboarding / Login / Registro
  - Home con dashboard de bienestar
  - Evaluación paso a paso (cuestionario interactivo)
  - Resultados con indicadores de riesgo y recomendaciones
  - Historial de evaluaciones
  - Perfil de usuario
  - Panel de administración (gestión de usuarios)
  - Panel de médico (pacientes y estadísticas)

### Servidor (Backend)

- Desarrollado en **Flask (Python)** con *Blueprints* modulares para separación de responsabilidades.
- Autenticación segura con **Flask-JWT-Extended** y encriptación de contraseñas con **Flask-Bcrypt**.
- Persistencia local en **SQLite** con migraciones manejadas por **Flask-Migrate (Alembic)**.
- Contiene el microservicio de evaluación con **6 modelos de Machine Learning** preentrenados.

---

## Stack Tecnológico

### Frontend
| Tecnología | Versión | Propósito |
|---|---|---|
| Flutter (Dart) | SDK ^3.11.5 | Framework multiplataforma |
| Provider | ^6.1.5 | Gestión de estado (MVVM) |
| HTTP | ^1.6.0 | Cliente HTTP para API REST |
| SharedPreferences | ^2.5.5 | Almacenamiento local de sesión |
| Phosphor Flutter | ^2.1.0 | Iconografía moderna |

### Backend
| Tecnología | Versión | Propósito |
|---|---|---|
| Flask | 3.1.3 | Framework web REST API |
| SQLAlchemy | 2.0.49 | ORM para base de datos |
| Flask-Migrate | 4.1.0 | Migraciones de base de datos |
| Flask-JWT-Extended | 4.7.4 | Autenticación JWT |
| Flask-Bcrypt | 1.0.1 | Encriptación de contraseñas |
| Flask-CORS | 6.0.2 | Soporte CORS |

### Machine Learning (Ensamble de 6 Modelos)
| Modelo | Archivo | Features | Propósito |
|---|---|---|---|
| Regresión Logística | `logistic_regression_model.pkl` | 15 features | Captura relaciones lineales base |
| K-Nearest Neighbors | `knn_model.pkl` | 7 features | Clasificación por vecindad |
| LightGBM | `lightgbm_model.pkl` | 7 features | Gradient Boosting ultrarrápido |
| Random Forest | `random_forest_model.pkl` | 7 features | Ensamble de árboles de decisión |
| XGBoost Ponderado | `xgboost_weighted_model.pkl` | 7 features | Clasificador con regularización |
| CatBoost Ponderado | `catboost_weighted_model.pkl` | 15 features | Gradient Boosting de alto desempeño |

---

## Modelo de Datos (SQLite)

### Diagrama Entidad-Relación

```
┌──────────────────┐       ┌──────────────────────┐
│     usuarios      │       │     evaluacion        │
├──────────────────┤       ├──────────────────────┤
│ id_usuario (PK)  │──┐    │ id_evaluacion (PK)   │
│ nombre            │  │    │ id_usuario (FK) ─────┘
│ correo (UNIQUE)   │  │    │ phq9_score            │
│ contrasena (hash) │  │    │ gad7_score            │
│ facultad          │  │    │ sleep_hours           │
│ ciclo             │  │    │ exercise_freq         │
│ fecha_registro    │  │    │ social_activity       │
│ rol               │  │    │ online_stress         │
└──────────────────┘  │    │ gpa                   │
                      │    │ family_support        │
                      │    │ screen_time           │
                      │    │ academic_stress       │
                      │    │ diet_quality          │
                      │    │ self_efficacy         │
┌──────────────────┐  │    │ peer_relationship     │
│   resultados_ml   │  │    │ financial_stress      │
├──────────────────┤  │    │ sleep_quality          │
│ id_resultado(PK)  │  │    │ fecha_realizacion     │
│ id_evaluacion(FK) │──┘    └──────────────────────┘
│ id_usuario (FK) ──┘
│ probabilidad_ansiedad │
│ nivel_riesgo         │       ┌──────────────────────┐
│ fecha_prediccion     │       │   recomendaciones     │
└──────────┬───────────┘       ├──────────────────────┤
           │ *                  │ id_recomendacion(PK)  │
           │                    │ categoria             │
           ▼                    │ titulo                │
┌──────────────────────────┐   │ descripcion           │
│ resultado_recomendaciones │   └──────────────────────┘
│ (Tabla Asociativa M:N)    │
├──────────────────────────┤
│ id_resultado (FK)        │
│ id_recomendacion (FK)    │
└──────────────────────────┘
```

### Tablas

| Tabla | Descripción |
|---|---|
| `usuarios` | Cuentas de usuarios con perfil (nombre, correo, rol, facultad, ciclo) |
| `evaluacion` | Resultados de cada test con las 15 variables del modelo ML |
| `resultados_ml` | Predicciones del modelo ML (probabilidad y nivel de riesgo) |
| `recomendaciones` | Catálogo de recomendaciones precargadas por nivel de riesgo |
| `resultado_recomendaciones` | Tabla pivote M:N entre resultados y recomendaciones |

---

## Machine Learning: Ensamble Predictivo

### Vector de Características (15 variables)

El modelo predice el riesgo combinando **15 características** recolectadas mediante el cuestionario interactivo de Flutter:

| # | Variable | Descripción | Rango |
|---|----------|-------------|-------|
| 1 | `phq9_score` | Nivel de depresión (PHQ-9) | 0 – 27 |
| 2 | `gad7_score` | Nivel de ansiedad (GAD-7) | 0 – 21 |
| 3 | `sleep_hours` | Horas de sueño al día | 3.0 – 10.0 |
| 4 | `exercise_freq` | Días de ejercicio a la semana | 0 – 7 |
| 5 | `social_activity` | Nivel de actividad social | 0 – 10 |
| 6 | `online_stress` | Estrés generado por internet | 1 – 10 |
| 7 | `gpa` | Promedio académico acumulado | 0.0 – 5.0 |
| 8 | `family_support` | Nivel de apoyo familiar | 1 – 10 |
| 9 | `screen_time` | Horas frente a pantallas al día | 1.0 – 12.0 |
| 10 | `academic_stress` | Estrés por exigencia de estudios | 1 – 10 |
| 11 | `diet_quality` | Calidad de la dieta diaria | 1 – 10 |
| 12 | `self_efficacy` | Nivel de autoeficacia y seguridad | 1 – 10 |
| 13 | `peer_relationship` | Calidad de relación con compañeros | 1 – 10 |
| 14 | `financial_stress` | Estrés por finanzas personales | 1 – 10 |
| 15 | `sleep_quality` | Calidad general de descanso | 0 – 10 |

### Método de Ensamble: Soft Voting

El sistema implementa un **ensamble de 6 modelos** de clasificación binaria (Clase 0: Con Riesgo de Ansiedad, Clase 1: Saludable) mediante **Votación Suave (Soft Voting)** — promedio simple de las probabilidades individuales:

```python
probabilidad_final = mean(prob_modelo_1, prob_modelo_2, ..., prob_modelo_6)
```

### Categorización del Riesgo

| Nivel | Probabilidad | Acción Recomendada |
|-------|-------------|-------------------|
| **BAJO** | < 0.35 | Mantener hábitos saludables |
| **MEDIO** | 0.35 – 0.70 | Reforzar estrategias de manejo del estrés |
| **ALTO** | > 0.70 | Buscar apoyo profesional urgentemente |

### Tolerancia a Fallos (Fallback)

Si las librerías `numpy`/`joblib` no están instaladas o los archivos `.pkl` no se encuentran, el sistema **no crashea**. Activa automáticamente un fallback basado en las escalas PHQ-9 y GAD-7:

```python
probabilidad = (phq9 / 27.0) * 0.6 + (gad7 / 21.0) * 0.4
```

---

## API REST - Endpoints

### Autenticación
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/registro` | Registrar un nuevo usuario |
| `POST` | `/login` | Iniciar sesión (retorna JWT) |

### Evaluaciones (Requiere JWT)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/api/v1/evaluaciones/` | Enviar evaluación y obtener predicción ML |
| `GET` | `/api/v1/evaluaciones/historial` | Historial de evaluaciones del usuario autenticado |

### Administrador (Requiere rol ADMIN)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/admin/usuarios` | Listar todos los usuarios |
| `POST` | `/api/v1/admin/usuarios` | Crear un nuevo usuario |
| `GET` | `/api/v1/admin/usuarios/<id>` | Detalle de usuario con evaluaciones |
| `PUT` | `/api/v1/admin/usuarios/<id>` | Editar datos de un usuario |
| `PUT` | `/api/v1/admin/usuarios/<id>/rol` | Cambiar rol de un usuario |
| `DELETE` | `/api/v1/admin/usuarios/<id>` | Eliminar un usuario |
| `GET` | `/api/v1/admin/usuarios/estadisticas` | Estadísticas globales del sistema |
| `DELETE` | `/api/v1/admin/evaluaciones/<id>` | Eliminar una evaluación |

### Médico (Requiere rol MEDICO)
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/api/v1/medico/pacientes` | Listar pacientes asignados |
| `GET` | `/api/v1/medico/pacientes/<id>/detalle` | Detalle completo de un paciente |
| `GET` | `/api/v1/medico/estadisticas` | Estadísticas de pacientes |
| `GET` | `/api/v1/medico/evaluaciones-recientes` | Evaluaciones recientes de pacientes |

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
   *(Para habilitar el ensamble predictivo completo de ML, instala también las dependencias opcionales:*
   ```bash
   pip install numpy joblib scikit-learn lightgbm xgboost catboost
   ```
   *)*

4. **Inicializa y actualiza la Base de Datos (SQLite local):**
   ```bash
   flask db upgrade
   flask init-recomendaciones
   ```
   *Nota: Las recomendaciones y los usuarios se guardan en el archivo físico `backend/instance/base_datos.db`. Los datos persisten indefinidamente incluso si cierras la terminal o apagas tu computadora.*

5. **Crea el archivo `.env`** en la raíz de `backend/` con el siguiente contenido:
   ```
   JWT_SECRET_KEY=tu_clave_secreta_aqui
   ```

6. **Enciende el servidor de Flask:**
   ```bash
   flask run
   ```
   *El servidor quedará corriendo en `http://127.0.0.1:5000`. No cierres esta pestaña de la terminal.*

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

3. **Configura la URL de la API:**
   - Edita el archivo `lib/config/api_config.dart`
   - Para **emulador Android** usa: `http://10.0.2.2:5000`
   - Para **dispositivo físico** usa la IP local del servidor

4. **Encender el Celular Virtual (Emulador):**
   - Abre las **Variables de Entorno** de Windows y asegúrate de crear la variable de usuario `ANDROID_HOME` apuntando al SDK (`C:\Android`).
   - En la variable `Path` de usuario, agrega las rutas: `C:\Android\platform-tools`, `C:\Android\emulator` y `C:\Android\cmdline-tools\latest\bin`.
   - En VSCode, presiona `Ctrl + Shift + P`, escribe `Flutter: Launch Emulator`, presiona Enter y selecciona tu dispositivo creado (ej. `Pixel_5_API_34`). El celular aparecerá flotando en tu pantalla.

5. **Ejecutar la Aplicación:**
   ```bash
   flutter run
   ```
   *(Flutter detectará el emulador y cargará la aplicación en el celular virtual para que realices tus pruebas en español).*

---

## Configuración de Modelos ML (Opcional)

Para habilitar la predicción con los 6 modelos preentrenados:

1. Coloca los archivos `.pkl` en `backend/app/static/models/`:
   - `logistic_regression_model.pkl`
   - `knn_model.pkl`
   - `lightgbm_model.pkl`
   - `random_forest_model.pkl`
   - `xgboost_weighted_model.pkl`
   - `catboost_weighted_model.pkl`

2. Instala las dependencias de ML:
   ```bash
   pip install numpy joblib scikit-learn lightgbm xgboost catboost
   ```

3. Reinicia el servidor Flask. El servicio `AnxietyPredictorService` cargará automáticamente los modelos al iniciar.

---

## Documentación Adicional

- **Informe técnico del Backend y ML:** [backend/INFORME_BACKEND_ML.md](backend/INFORME_BACKEND_ML.md)
- **Informe de configuración en JIRA:** [INFORME DE CONFIGURACION DEL PROYECTO EN JIRA.md](INFORME%20DE%20CONFIGURACION%20DEL%20PROYECTO%20EN%20JIRA.md)
- **Configuración del Frontend:** [frontend/README.md](frontend/README.md)

---

## Estructura del Proyecto

```
ansiedad-riesgo-ml-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py               # Application factory
│   │   ├── config/
│   │   │   └── config.py             # Configuraciones de Flask
│   │   ├── models/
│   │   │   ├── usuario.py            # Modelo Usuario + db/bcrypt
│   │   │   ├── evaluacion.py         # Modelo Evaluación (15 variables)
│   │   │   ├── resultado_ml.py       # Modelo Resultado ML
│   │   │   └── recomendacion.py      # Modelo Recomendación + tabla pivote
│   │   ├── routes/
│   │   │   ├── auth_routes.py        # Endpoints de autenticación
│   │   │   ├── evaluaciones_routes.py # Endpoints de evaluación ML
│   │   │   ├── admin_routes.py       # Endpoints de administración
│   │   │   └── medico_routes.py      # Endpoints para médicos
│   │   ├── services/
│   │   │   └── ml_service.py         # Servicio de ML (ensamble + fallback)
│   │   ├── static/models/            # Modelos .pkl preentrenados
│   │   └── utils/
│   │       ├── decorators.py         # Decoradores (role_required)
│   │       └── roles.py              # Constantes de roles
│   ├── instance/
│   │   └── base_datos.db            # Base de datos SQLite persistente
│   ├── migrations/                   # Migraciones de Alembic
│   ├── requirements.txt
│   ├── run.py                        # Punto de entrada
│   └── INFORME_BACKEND_ML.md
├── frontend/
│   ├── lib/
│   │   ├── main.dart                 # Punto de entrada Flutter
│   │   ├── config/
│   │   │   └── api_config.dart       # Configuración de endpoints API
│   │   ├── constants/
│   │   │   ├── app_colors.dart       # Colores de la app (tema claro/oscuro)
│   │   │   └── app_icons.dart        # Iconos personalizados
│   │   ├── models/
│   │   │   ├── usuario.dart          # Modelo Usuario (Dart)
│   │   │   ├── evaluacion.dart       # Modelo Evaluación (Dart)
│   │   │   ├── resultado_ml.dart     # Modelo Resultado ML (Dart)
│   │   │   └── recomendacion.dart    # Modelo Recomendación (Dart)
│   │   ├── services/
│   │   │   └── api_service.dart      # Servicio HTTP para API
│   │   ├── viewmodels/
│   │   │   ├── auth_viewmodel.dart   # ViewModel de autenticación
│   │   │   ├── evaluacion_viewmodel.dart  # ViewModel de evaluación
│   │   │   ├── medico_viewmodel.dart # ViewModel del médico
│   │   │   └── theme_viewmodel.dart  # ViewModel de tema (claro/oscuro)
│   │   ├── views/
│   │   │   ├── onboarding/           # Pantallas de onboarding
│   │   │   ├── auth/                 # Login y registro
│   │   │   ├── home/                 # Home dashboard
│   │   │   ├── evaluacion/           # Evaluación y resultados
│   │   │   ├── historial/            # Historial de evaluaciones
│   │   │   ├── perfil/               # Perfil de usuario
│   │   │   ├── admin/                # Panel de administración
│   │   │   └── medico/               # Panel del médico
│   │   └── widgets/
│   │       ├── animated_bar_chart.dart    # Gráfico de barras animado
│   │       ├── animated_counter.dart      # Contador animado
│   │       ├── animated_donut_chart.dart  # Gráfico dona animado
│   │       ├── custom_button.dart         # Botón personalizado
│   │       ├── custom_textfield.dart      # Campo de texto personalizado
│   │       └── risk_indicator.dart        # Indicador de riesgo visual
│   ├── pubspec.yaml
│   └── README.md
├── README.md (este archivo)
└── INFORME DE CONFIGURACION DEL PROYECTO EN JIRA.md
```

---

## Aplicaciones Móviles

La aplicación se ha desarrollado con Flutter, lo que permite compilar para **Android**, **iOS**, **Windows**, **macOS** y **Linux** desde un mismo código base.

### Requisitos para desarrollo
- **Flutter SDK** ^3.11.5
- **Dart SDK** ^3.11.5
- **Android Studio** (para emulador Android)
- **Visual Studio Code** (entorno recomendado)

---

Proyecto académico — **Universidad Nacional Mayor de San Marcos** · 2026