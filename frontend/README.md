# Frontend Ansiedad ML App

> Aplicación móvil multiplataforma desarrollada en **Flutter** para la evaluación del riesgo de ansiedad estudiantil mediante Inteligencia Artificial.

---

## Arquitectura del Cliente

La aplicación está construida sobre el patrón de arquitectura **MVVM (Model-View-ViewModel)** y utiliza **Provider** como gestor de estado reactivo oficial:

* **Model (`lib/models/`):** Define los esquemas de datos locales y el mapeo JSON proveniente de la API del backend (`Usuario`, `Evaluacion`, `ResultadoMl`, `Recomendacion`).
* **View (`lib/views/`):** Contiene la interfaz de usuario en widgets declarativos organizados por flujos (Inicio, Registro, Onboarding, Cuestionario, Historial, Resultados y Perfil). Toda la visualización se encuentra en idioma español.
* **ViewModel (`lib/viewmodels/`):** Sirve como puente de comunicación lógico. Consume los servicios HTTP y expone los estados de carga, error y datos estructurados a las vistas usando `ChangeNotifier` para redibujar la UI ante cualquier cambio.
* **Service (`lib/services/`):** Capa encargada de realizar peticiones de red directas (`api_service.dart`) inyectando cabeceras de autorización JWT dinámicas.

---

## Estructura de Directorios

```text
frontend/
├── android/            # Archivos de configuración nativa de Android
├── assets/             # Fuentes, imágenes y recursos estáticos
├── lib/                # Código fuente de Dart
│   ├── config/         # Configuración del host del servidor y endpoints (api_config.dart)
│   ├── models/         # Clases de entidades/modelos de datos
│   ├── services/       # Lógica del cliente HTTP
│   ├── viewmodels/     # Lógica de estados y negocio de la UI (Auth y Evaluacion)
│   ├── views/          # Pantallas de la aplicación (Onboarding, Login, Home, Test, etc.)
│   ├── widgets/        # Componentes UI reutilizables (Botones, indicadores de riesgo)
│   └── main.dart       # Punto de entrada de la aplicación y registro de rutas/proveedores
└── pubspec.yaml        # Gestión de paquetes y dependencias del proyecto
```

---

## Guía de Configuración Local y Arranque (Windows)

### 1. Requisitos Previos
- Tener instalado el SDK de **Flutter** (versión estable).
- Tener instalado **Android Studio** con las herramientas de desarrollo básicas.

### 2. Configurar Variables de Entorno en Windows
Para que las herramientas de Flutter reconozcan tu celular virtual y compilador:
1. En tu buscador de Windows, abre **Variables de entorno del sistema**.
2. Agrega una variable en **Variables de usuario**:
   - **Nombre:** `ANDROID_HOME`
   - **Valor:** `C:\Android` *(Asegúrate de que este sea el path real de tu SDK instalado)*
3. Selecciona la variable **Path** en variables de usuario y agrégale estas tres rutas nuevas:
   - `C:\Android\platform-tools`
   - `C:\Android\emulator`
   - `C:\Android\cmdline-tools\latest\bin`
4. Cierra y vuelve a abrir tu editor VSCode para que aplique los cambios.

### 3. Descargar Paquetes
En tu terminal Git Bash, ubícate en la carpeta `frontend/` y ejecuta:
```bash
flutter pub get
```

### 4. Lanzar el Celular Virtual desde VSCode
1. Presiona `Ctrl + Shift + P` en VSCode.
2. Escribe **`Flutter: Launch Emulator`** y presiona `Enter`.
3. Selecciona tu emulador creado (por ejemplo, `Pixel_5_API_34`). El celular virtual se encenderá en tu pantalla.

### 5. Ejecutar la Aplicación
Una vez que el celular virtual esté completamente encendido en tu pantalla, ejecuta:
```bash
flutter run
```
*La terminal compilará la aplicación y la abrirá de forma interactiva en tu celular de pantalla.*

---

## Funcionalidades Clave del Frontend

- **Cuestionario paso a paso:** Un cuestionario interactivo de 15 pantallas individuales con transiciones fluidas y controles adaptados al tipo de respuesta (chips, escalas de botones circulares 1-10 y sliders).
- **Control de Estado Vacío:** Los usuarios nuevos son recibidos por una interfaz limpia con una tarjeta de bienvenida, ocultando las gráficas sin mediciones.
- **Gráfica de Tendencia Activa:** Dibuja una gráfica lineal dinámicamente usando las probabilidades exactas obtenidas en el historial de evaluaciones.
