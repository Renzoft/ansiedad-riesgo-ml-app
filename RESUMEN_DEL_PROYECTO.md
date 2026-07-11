# RESUMEN COMPLETO DEL PROYECTO

## Ansiedad Riesgo ML App

> Aplicación móvil multiplataforma con Machine Learning para la estimación del riesgo de ansiedad en estudiantes universitarios.
> **Universidad Nacional Mayor de San Marcos · 2026**

---

## 1. DESCRIPCIÓN GENERAL

Este proyecto propone el diseño y evaluación de una aplicación móvil basada en técnicas de **Machine Learning** para la **detección temprana del riesgo de ansiedad** en estudiantes universitarios. A partir del análisis de **15 indicadores** psicoeducativos, académicos y de estilo de vida (calidad del sueño, rendimiento académico, estrés financiero, actividad social, etc.), el sistema estima el nivel de riesgo del estudiante y le proporciona recomendaciones preventivas personalizadas de forma inmediata.

La solución integra un **backend robusto basado en Flask (Python)** con un **ensamble multimodelo** (6 modelos predictivos coordinados mediante Soft Voting) y un **cliente móvil multiplataforma desarrollado en Flutter (Dart)**, garantizando confidencialidad, persistencia de datos local (SQLite) y una interfaz de usuario interactiva y en español.

### Roles de Usuario

| Rol               | Descripción                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| **Estudiante**    | Realiza evaluaciones de riesgo, visualiza su historial y recibe recomendaciones personalizadas |
| **Médico**        | Consulta pacientes asignados, revisa evaluaciones y estadísticas de riesgo                     |
| **Administrador** | Gestiona usuarios (CRUD), asigna roles, visualiza estadísticas globales del sistema            |

### Integrantes

| Nombre                            | Código   |
| --------------------------------- | -------- |
| Benites Meza, Marco Fabricio      | 21200257 |
| Coronado Córtez, Jeferson         | 20200131 |
| Munayco Vivanco, Renzo Alexander  | 22200107 |
| Morales Mallqui, Denilson Teófilo | 22200263 |
| Torres Mariluz, Josué Armando     | 21200251 |

---

## 2. ARQUITECTURA DEL PROYECTO

El sistema adopta un modelo de arquitectura **Cliente-Servidor (REST API)** con comunicación vía HTTP autenticada con **tokens JWT**.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        CLIENTE (Flutter)                             │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    PATRÓN MVVM                                 │   │
│  │                                                               │   │
│  │  ┌──────────────┐   ┌──────────────┐   ┌──────────────┐      │   │
│  │  │    Vistas     │   │  ViewModels  │   │   Servicios   │      │   │
│  │  │   (Screens)   │──▶│  (Provider)  │──▶│ (API Service) │      │   │
│  │  │  (Widgets)    │   │ (State Mgmt) │   │  (HTTP Client)│      │   │
│  │  └──────────────┘   └──────────────┘   └──────┬───────┘      │   │
│  │                                                 │              │   │
│  │  ┌──────────────┐                              │              │   │
│  │  │    Modelos    │◀─────────────────────────────┘              │   │
│  │  │  (Dart data)  │                                            │   │
│  │  └──────────────┘                                             │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                │ HTTP (JWT)                         │
└────────────────────────────────┼────────────────────────────────────┘
                                 │
┌────────────────────────────────┼────────────────────────────────────┐
│                    SERVIDOR (Flask)  ▼                               │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                    PATRÓN MVC                                  │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │              ROUTES (Blueprints)                         │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐     │  │   │
│  │  │  │   Auth   │ │Eval ML   │ │  Admin  │ │ Médico  │     │  │   │
│  │  │  └────┬─────┘ └────┬─────┘ └────┬────┘ └────┬────┘     │  │   │
│  │  └───────┼─────────────┼────────────┼───────────┼──────────┘  │   │
│  │          │             │            │           │              │   │
│  │  ┌───────┴─────────────┴────────────┴───────────┴──────────┐  │   │
│  │  │              CONTROLLERS                                 │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐     │  │   │
│  │  │  │   Auth   │ │Eval ML   │ │  Admin  │ │ Médico  │     │  │   │
│  │  │  └──────────┘ └──────────┘ └─────────┘ └─────────┘     │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  │          │             │            │           │              │   │
│  │  ┌───────┴─────────────┴────────────┴───────────┴──────────┐  │   │
│  │  │              MODELS (SQLAlchemy)                         │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐     │  │   │
│  │  │  │ Usuario  │ │Evaluación│ │Resultado│ │Recomend.│     │  │   │
│  │  │  └──────────┘ └──────────┘ └─────────┘ └─────────┘     │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  │                                                               │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │              VIEWS (Formateo de Respuestas)              │  │   │
│  │  │  ┌──────────┐ ┌──────────┐ ┌─────────┐ ┌─────────┐     │  │   │
│  │  │  │   Auth   │ │Eval ML   │ │  Admin  │ │ Médico  │     │  │   │
│  │  │  └──────────┘ └──────────┘ └─────────┘ └─────────┘     │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              SERVICIOS                                         │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │  ML Service (Ensamble 6 modelos + Fallback)              │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  │  ┌─────────────────────────────────────────────────────────┐  │   │
│  │  │  Gemini Service (IA Generativa para reportes)            │  │   │
│  │  └─────────────────────────────────────────────────────────┘  │   │
│  └──────────────────────────────────────────────────────────────┘   │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │              BASE DE DATOS (SQLite / PostgreSQL)               │   │
│  │                                                               │   │
│  │  usuarios ── evaluacion ── resultados_ml ── recomendaciones   │   │
│  │                         └── resultado_recomendaciones (M:N)   │   │
│  └──────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 3. ARQUITECTURA MVC DEL BACKEND (Flask)

El backend implementa el patrón **Modelo-Vista-Controlador (MVC)** de la siguiente manera:

### 3.1. Modelos (Models)

Representan las entidades de la base de datos mediante **SQLAlchemy ORM**. Cada modelo es una clase de Python que mapea a una tabla en SQLite/PostgreSQL.

| Archivo            | Tabla             | Propósito                                                   |
| ------------------ | ----------------- | ----------------------------------------------------------- |
| `usuario.py`       | `usuarios`        | Cuentas de usuario con perfil, rol y autenticación (bcrypt) |
| `evaluacion.py`    | `evaluacion`      | Resultados de cada test con las 15 variables del modelo ML  |
| `resultado_ml.py`  | `resultados_ml`   | Predicciones del modelo ML (probabilidad y nivel de riesgo) |
| `recomendacion.py` | `recomendaciones` | Catálogo de recomendaciones precargadas por nivel de riesgo |

### 3.2. Vistas (Views)

Son responsables de **formatear las respuestas HTTP** que se envían al cliente. Cada vista contiene métodos estáticos que construyen diccionarios JSON con la estructura adecuada.

| Archivo              | Propósito                                                         |
| -------------------- | ----------------------------------------------------------------- |
| `auth_view.py`       | Formatea respuestas de login, registro y errores de autenticación |
| `evaluacion_view.py` | Formatea respuestas de evaluación ML, historial y resultados      |
| `admin_view.py`      | Formatea respuestas de gestión de usuarios y estadísticas         |
| `medico_view.py`     | Formatea respuestas de listado de pacientes y detalle             |

### 3.3. Controladores (Controllers)

Contienen la **lógica de negocio**. Reciben los datos del request (a través de las rutas), interactúan con los modelos (base de datos) y delegan el formateo de la respuesta a las vistas.

| Archivo                    | Propósito                                                                                          |
| -------------------------- | -------------------------------------------------------------------------------------------------- |
| `auth_controller.py`       | Lógica de registro, login, validación de credenciales y generación de JWT                          |
| `evaluacion_controller.py` | Lógica de procesamiento de evaluaciones, invocación al servicio ML y asociación de recomendaciones |
| `admin_controller.py`      | Lógica CRUD de usuarios, cambio de roles y estadísticas globales                                   |
| `medico_controller.py`     | Lógica de consulta de pacientes asignados, detalle y estadísticas médicas                          |

### 3.4. Rutas (Routes / Blueprints)

Definen los **endpoints de la API REST** y conectan las URL con los controladores. Flask organiza las rutas en Blueprints modulares.

| Archivo                  | Prefijo URL            | Propósito                               |
| ------------------------ | ---------------------- | --------------------------------------- |
| `auth_routes.py`         | `/` (raíz)             | Endpoints `/registro` y `/login`        |
| `evaluaciones_routes.py` | `/api/v1/evaluaciones` | Endpoints de evaluación ML e historial  |
| `admin_routes.py`        | `/api/v1/admin`        | Endpoints de administración de usuarios |
| `medico_routes.py`       | `/api/v1/medico`       | Endpoints para médicos                  |

### 3.5. Servicios (Services)

Capas adicionales que encapsulan lógica especializada fuera del patrón MVC clásico.

| Archivo             | Propósito                                                                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------------------------------ |
| `ml_service.py`     | Servicio de Machine Learning: carga los 6 modelos .pkl, ejecuta el ensamble Soft Voting y proporciona fallback basado en PHQ-9/GAD-7 |
| `gemini_service.py` | Servicio de IA Generativa: integración con Google Gemini API para generar reportes descriptivos personalizados                       |

### 3.6. Utilidades (Utils)

| Archivo         | Propósito                                                                                    |
| --------------- | -------------------------------------------------------------------------------------------- |
| `decorators.py` | Decoradores personalizados como `role_required` para proteger rutas según el rol del usuario |
| `roles.py`      | Constantes de roles (`ROLE_ESTUDIANTE`, `ROLE_MEDICO`, `ROLE_ADMIN`)                         |

### 3.7. Punto de Entrada

| Archivo       | Propósito                                                                                                                                                                                                  |
| ------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `__init__.py` | **Application Factory**: crea y configura la app Flask, inicializa extensiones (db, bcrypt, JWT, CORS, Migrate, Gemini), registra los Blueprints y define comandos CLI (`init-db`, `init-recomendaciones`) |
| `run.py`      | Script de arranque del servidor Flask                                                                                                                                                                      |

---

## 4. ARQUITECTURA MVVM DEL FRONTEND (Flutter)

El frontend implementa el patrón **Modelo-Vista-ViewModel (MVVM)** utilizando **Provider** para la gestión de estado.

### 4.1. Modelos (Models)

Clases Dart que representan los datos que viajan entre el frontend y el backend. Contienen la estructura de datos y métodos de serialización/deserialización JSON.

| Archivo              | Propósito                                                                  |
| -------------------- | -------------------------------------------------------------------------- |
| `usuario.dart`       | Modelo de Usuario con campos: id, nombre, correo, rol, facultad, ciclo     |
| `evaluacion.dart`    | Modelo de Evaluación con las 15 variables del cuestionario                 |
| `resultado_ml.dart`  | Modelo de Resultado ML con probabilidad, nivel de riesgo y recomendaciones |
| `recomendacion.dart` | Modelo de Recomendación con categoría, título y descripción                |

### 4.2. Vistas (Views / Screens)

Son los **widgets de Flutter** que conforman la interfaz de usuario. Cada pantalla es un `StatefulWidget` o `StatelessWidget` que se suscribe a los ViewModels mediante `Consumer` o `context.watch()`.

| Archivo                              | Ruta           | Propósito                                                             |
| ------------------------------------ | -------------- | --------------------------------------------------------------------- |
| `onboarding_screen.dart`             | `/onboarding`  | Pantalla de bienvenida inicial                                        |
| `login_screen.dart`                  | `/login`       | Inicio de sesión                                                      |
| `registro_screen.dart`               | (modal)        | Registro de nuevo usuario                                             |
| `home_screen.dart`                   | `/home`        | Dashboard principal con indicadores de bienestar                      |
| `evaluacion_screen.dart`             | `/evaluacion`  | Cuestionario interactivo paso a paso (15 variables)                   |
| `resultado_screen.dart`              | `/resultado`   | Resultados de la evaluación con indicador de riesgo y recomendaciones |
| `historial_screen.dart`              | `/historial`   | Historial de evaluaciones realizadas                                  |
| `perfil_screen.dart`                 | `/perfil`      | Perfil del usuario                                                    |
| `admin_home_screen.dart`             | `/admin-home`  | Panel de administración (gestión de usuarios)                         |
| `admin_user_detail_screen.dart`      | (detalle)      | Detalle de un usuario para administrador                              |
| `admin_user_form.dart`               | (formulario)   | Formulario de creación/edición de usuario                             |
| `medico_home_screen.dart`            | `/medico-home` | Panel del médico con lista de pacientes                               |
| `medico_paciente_detail_screen.dart` | (detalle)      | Detalle completo de un paciente para el médico                        |

### 4.3. ViewModels

Clases que extienden `ChangeNotifier` y contienen la **lógica de presentación**. Gestionan el estado de la UI, realizan llamadas al `ApiService` y notifican a las vistas cuando hay cambios.

| Archivo                     | Propósito                                                                 |
| --------------------------- | ------------------------------------------------------------------------- |
| `auth_viewmodel.dart`       | Gestiona estado de autenticación: login, registro, token, sesión          |
| `evaluacion_viewmodel.dart` | Gestiona estado de la evaluación: preguntas, envío, resultados, historial |
| `medico_viewmodel.dart`     | Gestiona estado del médico: lista de pacientes, detalle, estadísticas     |
| `theme_viewmodel.dart`      | Gestiona el tema de la app (claro/oscuro)                                 |

### 4.4. Servicios (Services)

| Archivo            | Propósito                                                                                                      |
| ------------------ | -------------------------------------------------------------------------------------------------------------- |
| `api_service.dart` | Cliente HTTP genérico con métodos GET, POST, PUT, DELETE. Maneja autenticación JWT automática y errores de API |

### 4.5. Configuración y Constantes

| Archivo           | Propósito                                                                   |
| ----------------- | --------------------------------------------------------------------------- |
| `api_config.dart` | Configuración de la URL base de la API (para emulador o dispositivo físico) |
| `app_colors.dart` | Paleta de colores para tema claro y oscuro (usando Theme Extensions)        |
| `app_icons.dart`  | Definición de iconos personalizados                                         |

### 4.6. Widgets Reutilizables

| Archivo                     | Propósito                                             |
| --------------------------- | ----------------------------------------------------- |
| `animated_bar_chart.dart`   | Gráfico de barras animado para visualizar resultados  |
| `animated_counter.dart`     | Contador numérico animado                             |
| `animated_donut_chart.dart` | Gráfico de dona animado para estadísticas             |
| `custom_button.dart`        | Botón personalizado con estilos de la app             |
| `custom_textfield.dart`     | Campo de texto personalizado con validación           |
| `risk_indicator.dart`       | Indicador visual de nivel de riesgo (bajo/medio/alto) |

### 4.7. Punto de Entrada

| Archivo     | Propósito                                                                                                                                                           |
| ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `main.dart` | Punto de entrada de la app Flutter. Inicializa `ApiConfig`, configura `MultiProvider` con los 4 ViewModels, define el tema (claro/oscuro) y las rutas de navegación |

---

## 5. ESTRUCTURA COMPLETA DEL PROYECTO (ÁRBOL DE ARCHIVOS IMPORTANTES)

```
ansiedad-riesgo-ml-app/
│
├── README.md                              # Documentación principal del proyecto
├── RESUMEN_DEL_PROYECTO.md                # Este archivo
├── Procfile                               # Configuración de despliegue (Render)
├── INFORME DE CONFIGURACION DEL PROYECTO EN JIRA.md
│
├── backend/                               # ─── BACKEND (Flask - Python) ───
│   ├── run.py                             # Punto de entrada del servidor Flask
│   ├── requirements.txt                   # Dependencias de Python
│   ├── .env                               # Variables de entorno (JWT_SECRET_KEY, GEMINI_API_KEY)
│   ├── INFORME_BACKEND_ML.md              # Informe técnico del backend y ML
│   ├── init_recomendaciones.py            # Script para precargar recomendaciones
│   ├── regenerar_reportes.py              # Script para regenerar reportes con Gemini
│   ├── test_gemini.py                     # Script de prueba de integración Gemini
│   ├── check_recomendaciones.py           # Script de verificación de recomendaciones
│   ├── test_model.py                      # Script de prueba de modelos ML
│   │
│   ├── app/                               # Módulo principal de la aplicación Flask
│   │   ├── __init__.py                    # Application Factory: configura app, BD, JWT, CORS, Blueprints
│   │   │
│   │   ├── config/
│   │   │   └── config.py                  # Configuraciones de Flask (clases Config, Development, Production)
│   │   │
│   │   ├── models/                        # ─── CAPA MODELO (MVC) ───
│   │   │   ├── usuario.py                 # Modelo Usuario: SQLAlchemy + Flask-Bcrypt (hash de contraseñas)
│   │   │   ├── evaluacion.py              # Modelo Evaluación: 15 variables del cuestionario ML
│   │   │   ├── resultado_ml.py            # Modelo ResultadoML: predicción, probabilidad, nivel de riesgo
│   │   │   └── recomendacion.py           # Modelo Recomendación + tabla pivote resultado_recomendaciones (M:N)
│   │   │
│   │   ├── views/                         # ─── CAPA VISTA (MVC) ───
│   │   │   ├── auth_view.py               # Formatea respuestas de autenticación (login, registro, errores)
│   │   │   ├── evaluacion_view.py         # Formatea respuestas de evaluación ML y resultados
│   │   │   ├── admin_view.py              # Formatea respuestas de administración (usuarios, estadísticas)
│   │   │   └── medico_view.py             # Formatea respuestas del módulo médico (pacientes, detalle)
│   │   │
│   │   ├── controllers/                   # ─── CAPA CONTROLADOR (MVC) ───
│   │   │   ├── auth_controller.py         # Lógica de registro, login, validación y generación de JWT
│   │   │   ├── evaluacion_controller.py   # Lógica de evaluación: procesa cuestionario, invoca ML, asocia recomendaciones
│   │   │   ├── admin_controller.py        # Lógica CRUD de usuarios, cambio de roles, estadísticas globales
│   │   │   └── medico_controller.py       # Lógica de consulta de pacientes, detalle y estadísticas médicas
│   │   │
│   │   ├── routes/                        # ─── RUTAS / BLUEPRINTS ───
│   │   │   ├── auth_routes.py             # Endpoints: POST /registro, POST /login
│   │   │   ├── evaluaciones_routes.py     # Endpoints: POST /api/v1/evaluaciones/, GET /historial
│   │   │   ├── admin_routes.py            # Endpoints: CRUD /api/v1/admin/usuarios, estadísticas
│   │   │   └── medico_routes.py           # Endpoints: GET /api/v1/medico/pacientes, detalle, estadísticas
│   │   │
│   │   ├── services/                      # ─── SERVICIOS ESPECIALIZADOS ───
│   │   │   ├── ml_service.py              # Servicio ML: carga 6 modelos .pkl, ensamble Soft Voting, fallback PHQ-9/GAD-7
│   │   │   └── gemini_service.py          # Servicio Gemini: integración con Google Gemini API para reportes IA
│   │   │
│   │   ├── utils/                         # ─── UTILIDADES ───
│   │   │   ├── decorators.py              # Decorador @role_required para proteger rutas por rol
│   │   │   └── roles.py                   # Constantes: ROLE_ESTUDIANTE, ROLE_MEDICO, ROLE_ADMIN
│   │   │
│   │   └── static/models/                 # Modelos ML preentrenados (.pkl)
│   │       ├── logistic_regression_model.pkl
│   │       ├── knn_model.pkl
│   │       ├── lightgbm_model.pkl
│   │       ├── random_forest_model.pkl
│   │       ├── xgboost_weighted_model.pkl
│   │       └── catboost_weighted_model.pkl
│   │
│   ├── instance/
│   │   └── base_datos.db                  # Base de datos SQLite persistente
│   │
│   └── migrations/                        # Migraciones de base de datos (Alembic)
│       ├── alembic.ini                    # Configuración de Alembic
│       ├── env.py                         # Entorno de migraciones
│       └── versions/
│           └── add_reporte_ia_to_resultados_ml.py  # Migración: añade campo reporte_ia a resultados_ml
│
├── frontend/                              # ─── FRONTEND (Flutter - Dart) ───
│   ├── pubspec.yaml                       # Dependencias de Flutter/Dart
│   ├── README.md                          # Documentación del frontend
│   │
│   └── lib/                               # Código fuente de Flutter
│       ├── main.dart                      # Punto de entrada: MultiProvider, rutas, tema claro/oscuro
│       │
│       ├── config/
│       │   └── api_config.dart            # Configuración de URL base de la API
│       │
│       ├── constants/
│       │   ├── app_colors.dart            # Paleta de colores (tema claro y oscuro)
│       │   └── app_icons.dart             # Definición de iconos personalizados
│       │
│       ├── models/                        # ─── MODELOS (MVVM) ───
│       │   ├── usuario.dart               # Modelo Usuario (Dart): serialización/deserialización JSON
│       │   ├── evaluacion.dart            # Modelo Evaluación (Dart): 15 variables del cuestionario
│       │   ├── resultado_ml.dart          # Modelo ResultadoML (Dart): predicción, riesgo, recomendaciones
│       │   └── recomendacion.dart         # Modelo Recomendación (Dart): categoría, título, descripción
│       │
│       ├── services/                      # ─── SERVICIOS ───
│       │   └── api_service.dart           # Cliente HTTP: GET, POST, PUT, DELETE con autenticación JWT
│       │
│       ├── viewmodels/                    # ─── VIEWMODELS (MVVM) ───
│       │   ├── auth_viewmodel.dart        # ViewModel de autenticación: login, registro, sesión
│       │   ├── evaluacion_viewmodel.dart  # ViewModel de evaluación: preguntas, envío, resultados, historial
│       │   ├── medico_viewmodel.dart      # ViewModel del médico: pacientes, detalle, estadísticas
│       │   └── theme_viewmodel.dart       # ViewModel del tema: alternar claro/oscuro
│       │
│       ├── views/                         # ─── VISTAS / PANTALLAS (MVVM) ───
│       │   ├── onboarding/
│       │   │   └── onboarding_screen.dart # Pantalla de bienvenida inicial
│       │   ├── auth/
│       │   │   ├── login_screen.dart      # Pantalla de inicio de sesión
│       │   │   └── registro_screen.dart   # Pantalla de registro de usuario
│       │   ├── home/
│       │   │   └── home_screen.dart       # Dashboard principal con indicadores de bienestar
│       │   ├── evaluacion/
│       │   │   ├── evaluacion_screen.dart # Cuestionario interactivo paso a paso (15 variables)
│       │   │   ├── resultado_screen.dart  # Resultados con indicador de riesgo y recomendaciones
│       │   │   └── historial_screen.dart  # Historial de evaluaciones realizadas
│       │   ├── perfil/
│       │   │   └── perfil_screen.dart     # Perfil del usuario
│       │   ├── admin/
│       │   │   ├── admin_home_screen.dart         # Panel de administración (lista de usuarios)
│       │   │   ├── admin_user_detail_screen.dart  # Detalle de usuario para admin
│       │   │   └── admin_user_form.dart           # Formulario crear/editar usuario
│       │   └── medico/
│       │       ├── medico_home_screen.dart              # Panel del médico (lista de pacientes)
│       │       └── medico_paciente_detail_screen.dart   # Detalle completo de paciente
│       │
│       └── widgets/                       # ─── WIDGETS REUTILIZABLES ───
│           ├── animated_bar_chart.dart     # Gráfico de barras animado
│           ├── animated_counter.dart       # Contador numérico animado
│           ├── animated_donut_chart.dart   # Gráfico de dona animado
│           ├── custom_button.dart          # Botón personalizado
│           ├── custom_textfield.dart       # Campo de texto personalizado
│           └── risk_indicator.dart         # Indicador visual de nivel de riesgo
│
└── (archivos raíz)
    ├── .gitignore
    └── Procfile
```

---

## 6. STACK TECNOLÓGICO COMPLETO

### Backend (Flask - Python)

| Tecnología              | Versión | Propósito                            |
| ----------------------- | ------- | ------------------------------------ |
| Flask                   | 3.1.3   | Framework web REST API               |
| SQLAlchemy              | 2.0.49  | ORM para base de datos               |
| Flask-Migrate (Alembic) | 4.1.0   | Migraciones de base de datos         |
| Flask-JWT-Extended      | 4.7.4   | Autenticación JWT                    |
| Flask-Bcrypt            | 1.0.1   | Encriptación de contraseñas          |
| Flask-CORS              | 6.0.2   | Soporte CORS                         |
| SQLite                  | -       | Base de datos local (desarrollo)     |
| PostgreSQL              | -       | Base de datos en producción (Render) |

### Frontend (Flutter - Dart)

| Tecnología        | Versión     | Propósito                      |
| ----------------- | ----------- | ------------------------------ |
| Flutter (Dart)    | SDK ^3.11.5 | Framework multiplataforma      |
| Provider          | ^6.1.5      | Gestión de estado (MVVM)       |
| HTTP              | ^1.6.0      | Cliente HTTP para API REST     |
| SharedPreferences | ^2.5.5      | Almacenamiento local de sesión |
| Phosphor Flutter  | ^2.1.0      | Iconografía moderna            |

### Machine Learning (Ensamble de 6 Modelos)

| Modelo              | Archivo                         | Features    | Propósito                           |
| ------------------- | ------------------------------- | ----------- | ----------------------------------- |
| Regresión Logística | `logistic_regression_model.pkl` | 15 features | Captura relaciones lineales base    |
| K-Nearest Neighbors | `knn_model.pkl`                 | 7 features  | Clasificación por vecindad          |
| LightGBM            | `lightgbm_model.pkl`            | 7 features  | Gradient Boosting ultrarrápido      |
| Random Forest       | `random_forest_model.pkl`       | 7 features  | Ensamble de árboles de decisión     |
| XGBoost Ponderado   | `xgboost_weighted_model.pkl`    | 7 features  | Clasificador con regularización     |
| CatBoost Ponderado  | `catboost_weighted_model.pkl`   | 15 features | Gradient Boosting de alto desempeño |

### Método de Ensamble: **Soft Voting** (Promedio simple de probabilidades)

### Tolerancia a Fallos: **Fallback** basado en PHQ-9 y GAD-7

---

## 7. MODELO DE DATOS (SQLite)

### Tablas

| Tabla                       | Descripción                                                           |
| --------------------------- | --------------------------------------------------------------------- |
| `usuarios`                  | Cuentas de usuarios con perfil (nombre, correo, rol, facultad, ciclo) |
| `evaluacion`                | Resultados de cada test con las 15 variables del modelo ML            |
| `resultados_ml`             | Predicciones del modelo ML (probabilidad y nivel de riesgo)           |
| `recomendaciones`           | Catálogo de recomendaciones precargadas por nivel de riesgo           |
| `resultado_recomendaciones` | Tabla pivote M:N entre resultados y recomendaciones                   |

### Vector de Características (15 variables para el ML)

| #   | Variable            | Descripción                        | Rango      |
| --- | ------------------- | ---------------------------------- | ---------- |
| 1   | `phq9_score`        | Nivel de depresión (PHQ-9)         | 0 – 27     |
| 2   | `gad7_score`        | Nivel de ansiedad (GAD-7)          | 0 – 21     |
| 3   | `sleep_hours`       | Horas de sueño al día              | 3.0 – 10.0 |
| 4   | `exercise_freq`     | Días de ejercicio a la semana      | 0 – 7      |
| 5   | `social_activity`   | Nivel de actividad social          | 0 – 10     |
| 6   | `online_stress`     | Estrés generado por internet       | 1 – 10     |
| 7   | `gpa`               | Promedio académico acumulado       | 0.0 – 5.0  |
| 8   | `family_support`    | Nivel de apoyo familiar            | 1 – 10     |
| 9   | `screen_time`       | Horas frente a pantallas al día    | 1.0 – 12.0 |
| 10  | `academic_stress`   | Estrés por exigencia de estudios   | 1 – 10     |
| 11  | `diet_quality`      | Calidad de la dieta diaria         | 1 – 10     |
| 12  | `self_efficacy`     | Nivel de autoeficacia y seguridad  | 1 – 10     |
| 13  | `peer_relationship` | Calidad de relación con compañeros | 1 – 10     |
| 14  | `financial_stress`  | Estrés por finanzas personales     | 1 – 10     |
| 15  | `sleep_quality`     | Calidad general de descanso        | 0 – 10     |

### Categorización del Riesgo

| Nivel     | Probabilidad | Acción Recomendada                        |
| --------- | ------------ | ----------------------------------------- |
| **BAJO**  | < 0.35       | Mantener hábitos saludables               |
| **MEDIO** | 0.35 – 0.70  | Reforzar estrategias de manejo del estrés |
| **ALTO**  | > 0.70       | Buscar apoyo profesional urgentemente     |

---

## 8. API REST - ENDPOINTS

### Autenticación

| Método | Endpoint    | Descripción                  |
| ------ | ----------- | ---------------------------- |
| `POST` | `/registro` | Registrar un nuevo usuario   |
| `POST` | `/login`    | Iniciar sesión (retorna JWT) |

### Evaluaciones (Requiere JWT)

| Método | Endpoint                         | Descripción                                       |
| ------ | -------------------------------- | ------------------------------------------------- |
| `POST` | `/api/v1/evaluaciones/`          | Enviar evaluación y obtener predicción ML         |
| `GET`  | `/api/v1/evaluaciones/historial` | Historial de evaluaciones del usuario autenticado |

### Administrador (Requiere rol ADMIN)

| Método   | Endpoint                              | Descripción                         |
| -------- | ------------------------------------- | ----------------------------------- |
| `GET`    | `/api/v1/admin/usuarios`              | Listar todos los usuarios           |
| `POST`   | `/api/v1/admin/usuarios`              | Crear un nuevo usuario              |
| `GET`    | `/api/v1/admin/usuarios/<id>`         | Detalle de usuario con evaluaciones |
| `PUT`    | `/api/v1/admin/usuarios/<id>`         | Editar datos de un usuario          |
| `PUT`    | `/api/v1/admin/usuarios/<id>/rol`     | Cambiar rol de un usuario           |
| `DELETE` | `/api/v1/admin/usuarios/<id>`         | Eliminar un usuario                 |
| `GET`    | `/api/v1/admin/usuarios/estadisticas` | Estadísticas globales del sistema   |
| `DELETE` | `/api/v1/admin/evaluaciones/<id>`     | Eliminar una evaluación             |

### Médico (Requiere rol MEDICO)

| Método | Endpoint                                | Descripción                         |
| ------ | --------------------------------------- | ----------------------------------- |
| `GET`  | `/api/v1/medico/pacientes`              | Listar pacientes asignados          |
| `GET`  | `/api/v1/medico/pacientes/<id>/detalle` | Detalle completo de un paciente     |
| `GET`  | `/api/v1/medico/estadisticas`           | Estadísticas de pacientes           |
| `GET`  | `/api/v1/medico/evaluaciones-recientes` | Evaluaciones recientes de pacientes |
