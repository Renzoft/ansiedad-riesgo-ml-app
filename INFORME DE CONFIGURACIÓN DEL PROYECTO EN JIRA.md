# **INFORME DE CONFIGURACIÓN DEL PROYECTO EN JIRA**

Proyecto: Aplicación de Evaluación de Riesgo de Ansiedad para Estudiantes    
Metodología: Scrum    
Total de Sprints: 4    
Fechas: 13 de mayo de 2026 – 11 de julio de 2026    
Total de Puntos de Historia: 84  

\---

## **1\. ÉPICAS (5)**

| Código | Nombre |
| :---- | :---- |
| SCRUM-5 | Registro y perfil del estudiante |
| SCRUM-6 | Evaluación y riesgo emocional |
| SCRUM-7 | Seguimiento histórico y visual |
| SCRUM-24 | Administración del sistema |
| SCRUM-25 | Acceso y usabilidad móvil |

\---

## **2\. SPRINTS Y DISTRIBUCIÓN DE HISTORIAS DE USUARIO**

### **SPRINT 1**  

Duración: 13/05/2026 – 26/05/2026 (2 semanas)    
Meta: Permitir que los estudiantes se registren, configuren su perfil, registren hábitos y obtengan una primera estimación de riesgo.    
Puntos totales: 21  

| Código | Historia de Usuario | Puntos | Épica |
| :---- | :---- | :---- | :---- |
| HU-08 | Registrar perfil multidimensional | 5 | SCRUM-5 |
| HU-09 | Registrar indicadores de estilo de vida | 5 | SCRUM-5 |
| HU-10 | Inicio de sesión seguro | 3 | SCRUM-5 |
| HU-11 | Estimar riesgo de ansiedad | 8 | SCRUM-6 |

\---

### **SPRINT 2**  

Duración: 27/05/2026 – 09/06/2026 (2 semanas)    
Meta: Implementar alertas preventivas, recomendaciones personalizadas, visualización de historial y permitir edición del perfil.    
Puntos totales: 21  

| Código | Historia de Usuario | Puntos | Épica |
| :---- | :---- | :---- | :---- |
| HU-12 | Recibir alertas preventivas | 5 | SCRUM-6 |
| HU-13 | Recomendaciones personalizadas | 8 | SCRUM-6 |
| HU-14 | Ver historial emocional y gráficas | 5 | SCRUM-7 |
| HU-21 | Editar perfil y datos personales | 3 | SCRUM-5 |

\---

### **SPRINT 3**  

Duración: 10/06/2026 – 23/06/2026 (2 semanas)    
Meta: Añadir funcionalidades de respaldo, métricas administrativas, mejora de la interfaz móvil y exportación de datos.    
Puntos totales: 26  

| Código | Historia de Usuario | Puntos | Épica |
| :---- | :---- | :---- | :---- |
| HU-15 | Generar respaldos automáticos | 8 | SCRUM-24 |
| HU-16 | Ver métricas globales anonimizadas | 5 | SCRUM-24 |
| HU-17 | Interfaz móvil en Flutter | 8 | SCRUM-25 |
| HU-20 | Exportar historial emocional | 5 | SCRUM-7 |

\---

### **SPRINT 4**  

Duración: 24/06/2026 – 11/07/2026 (18 días)    
Meta: Completar la experiencia de usuario con descarga de la app, manual integrado, recursos de ayuda y configuración de alertas.    
Puntos totales: 16  

| Código | Historia de Usuario | Puntos | Épica |
| :---- | :---- | :---- | :---- |
| HU-18 | Descargar e instalar la aplicación móvil | 3 | SCRUM-25 |
| HU-19 | Manual de usuario integrado | 5 | SCRUM-25 |
| HU-22 | Recursos de ayuda y contacto de emergencia | 3 | SCRUM-25 |
| HU-23 | Personalizar frecuencia y tipo de alertas | 5 | SCRUM-6 |

\---

## **3\. DETALLE DE HISTORIAS DE USUARIO (Descripción y Criterios de Aceptación)**

### **HU-08 – Registrar perfil multidimensional**

Descripción:    
Como estudiante, quiero registrar mis datos académicos y personales (nombre, correo, edad, carrera, semestre) para generar mi perfil de evaluación.

Criterios de aceptación:  

1. El formulario incluye campos: nombre completo, correo electrónico (único), contraseña, edad (16-70), carrera (lista desplegable), semestre (1-10).  
2. Todos los campos son obligatorios y se validan (correo único, edad numérica).  
3. La contraseña se almacena de forma segura (hash bcrypt).  
4. Al enviar, se crea el perfil en la base de datos y se redirige a la pantalla de login.

Subtareas técnicas (TR):  

* TR8: Diseño de base de datos (tablas y relaciones)  
* TR9: Creación de base de datos en SQLite  
* TR13: Creación de API para registro de perfil multidimensional (Flask)  
* TR20: Creación de formularios de registro en Flutter (parte perfil)

\---

### **HU-09 – Registrar indicadores de estilo de vida**

Descripción:    
Como estudiante, quiero registrar mis hábitos diarios (horas de sueño, actividad física, tiempo de pantalla, nivel de estrés) para que el sistema evalúe mi bienestar emocional.

Criterios de aceptación:  

1. Formulario con campos: fecha (selector), horas de sueño (0-24), ejercicio (sí/no), tiempo en pantalla (0-12 h), nivel de estrés (1-10).  
2. Los datos se guardan asociados al usuario autenticado y con fecha.  
3. El sistema permite registrar hábitos una vez al día (no duplicados en misma fecha).  
4. Se muestra mensaje de confirmación.

Subtareas técnicas (TR):  

* TR14: Creación de API para registro de indicadores (Flask)  
* TR20: Creación de formularios en Flutter (parte hábitos)  
* (Adicional) TR9 ya usada para BD

\---

### **HU-10 – Inicio de sesión seguro**

Descripción:    
Como usuario, quiero iniciar sesión con correo y contraseña para proteger mi información personal.

Criterios de aceptación:  

1. Pantalla de login con campos correo y contraseña.  
2. Las credenciales se validan contra la base de datos (contraseña hasheada).  
3. Al éxito, se genera un token JWT con expiración de 30 minutos y se almacena localmente (flutter\_secure\_storage).  
4. El token se incluye automáticamente en todas las peticiones autenticadas.  
5. Opción de cerrar sesión que elimina el token.

Subtareas técnicas (TR):  

* TR23: Implementación de validación de credenciales  
* TR24: Implementación de seguridad y confidencialidad (JWT, bcrypt)

\---

### **HU-11 – Estimar riesgo de ansiedad**

Descripción:    
Como estudiante, quiero conocer mi nivel de riesgo emocional (bajo, medio, alto) basado en mis respuestas para comprender mi estado de ansiedad.

Criterios de aceptación:  

1. El sistema procesa los datos del perfil \+ los últimos hábitos registrados usando un modelo de machine learning (o reglas lógicas).  
2. Devuelve una categoría de riesgo y una breve explicación.  
3. El resultado se muestra en pantalla y se guarda en el historial con fecha.  
4. Si no hay hábitos suficientes, se muestra un mensaje pidiendo registrar al menos un día.

Subtareas técnicas (TR):  

* TR11: Implementación del modelo de Machine Learning (Python con scikit-learn)  
* TR12: Integración del modelo ML con el backend Flask  
* TR15: Implementación del motor de categorización de riesgo  
* TR27: Pruebas de integración del modelo ML  
* TR30: Optimización del modelo

\---

### **HU-12 – Recibir alertas preventivas**

Descripción:    
Como usuario, quiero recibir notificaciones inteligentes cuando mi estado emocional empeore para identificar posibles cambios a tiempo.

Criterios de aceptación:  

1. Si el nivel de riesgo aumenta respecto a la última evaluación, se envía una notificación push (o correo electrónico simulado).  
2. La alerta incluye un mensaje de apoyo y sugerencia de acción.  
3. El usuario puede activar/desactivar las alertas desde configuración (asociado a HU-23).  
4. Las alertas se registran en el sistema.

Subtareas técnicas (TR):  

* TR17: Implementación del sistema de notificaciones inteligentes (Flask \+ Firebase Cloud Messaging o correo)

\---

### **HU-13 – Recomendaciones personalizadas**

Descripción:    
Como estudiante, quiero recibir recomendaciones de bienestar (ejercicios, hábitos, recursos) basadas en mi perfil y nivel de riesgo para mejorar mi salud emocional.

Criterios de aceptación:  

1. Las recomendaciones se generan según el nivel de riesgo y los hábitos débiles (ej. poco sueño, alto estrés).  
2. Se muestran en el dashboard principal después de cada evaluación.  
3. Incluyen enlaces a contenido útil (técnicas de respiración, contacto con bienestar universitario).  
4. Se actualizan cada vez que se registran nuevos hábitos.

Subtareas técnicas (TR):  

* TR18: Desarrollo del módulo de recomendaciones personalizadas (backend con reglas)

\---

### **HU-14 – Ver historial emocional y gráficas**

Descripción:    
Como estudiante, quiero visualizar mi evolución en el tiempo mediante gráficas de progreso para monitorear cambios en mi estado emocional.

Criterios de aceptación:  

1. Gráfico de líneas que muestra el nivel de riesgo vs fecha (últimas 10 evaluaciones o por rango).  
2. Posibilidad de filtrar por último mes, trimestre o año.  
3. Cada punto muestra detalles (fecha, nivel de riesgo, hábitos asociados) en un tooltip.  
4. La gráfica es interactiva y se actualiza automáticamente.

Subtareas técnicas (TR):  

* TR16: Desarrollo del módulo de reportes históricos (backend)  
* TR22: Implementación de gráficas de progreso en Flutter (fl\_chart)

\---

### **HU-15 – Generar respaldos automáticos**

Descripción:    
Como administrador, quiero programar copias de seguridad automáticas de la base de datos para evitar pérdida de información.

Criterios de aceptación:  

1. Respaldo diario programado a las 2:00 AM (archivo .sql o .db comprimido en ZIP).  
2. Los backups se almacenan en una carpeta segura (o en la nube, simulado localmente).  
3. El administrador puede restaurar desde un backup mediante una interfaz simple (opcional).  
4. Se registra un log de cada respaldo.

Subtareas técnicas (TR):  

* TR25: Implementación de copias de seguridad programadas (APScheduler en Flask)  
* TR33: Despliegue del sistema en servidor (asociado parcial)

\---

### **HU-16 – Ver métricas globales anonimizadas**

Descripción:    
Como administrador, quiero visualizar estadísticas agregadas (ej. % estudiantes con riesgo alto por carrera) para mejorar los servicios de bienestar.

Criterios de aceptación:  

1. Panel con gráficos de barras y pastel (niveles de riesgo por carrera, semestre, rango de edad).  
2. No se muestra información individual identificable (datos anonimizados).  
3. Los datos se pueden exportar a CSV.  
4. Solo accesible para usuarios con rol administrador.

Subtareas técnicas (TR):  

* TR36: Desarrollo de panel de administración con métricas agregadas (nueva TR)

\---

### **HU-17 – Interfaz móvil en Flutter**

Descripción:    
Como usuario, quiero usar una aplicación móvil intuitiva en mi teléfono (Android/iOS) para interactuar fácilmente con el sistema.

Criterios de aceptación:  

1. La app incluye todas las pantallas: login, registro, dashboard, registro de hábitos, historial, gráficas, recomendaciones, configuración.  
2. Navegación mediante menú inferior o tabs.  
3. Diseño responsive, accesible (contraste, tamaños de botón).  
4. La app consume correctamente todas las API del backend.

Subtareas técnicas (TR):  

* TR19: Desarrollo de interfaz móvil en Flutter (estructura base)  
* TR21: Implementación de conexión entre Flutter y backend (Dio, interceptores)  
* TR26: Pruebas unitarias del sistema (parcial)  
* TR28: Pruebas funcionales de la aplicación móvil  
* TR29: Pruebas de rendimiento del sistema

\---

### **HU-18 – Descargar e instalar la aplicación móvil**

Descripción:    
Como usuario, quiero descargar e instalar la aplicación desde un enlace directo (APK o TestFlight) para acceder al sistema sin usar un navegador.

Criterios de aceptación:  

1. El sistema proporciona un código QR o enlace de descarga (generación del APK).  
2. Instrucciones claras para instalar en Android (permisos de fuentes desconocidas) o iOS (TestFlight).  
3. La aplicación se abre y funciona sin errores críticos.

Subtareas técnicas (TR):  

* TR31: Implementación de portabilidad en múltiples plataformas (build para Android)  
* TR34: Publicación de la aplicación móvil (generar APK/AAB)

\---

### **HU-19 – Manual de usuario integrado**

Descripción:    
Como usuario, quiero disponer de un manual de uso dentro de la propia aplicación para comprender cada funcionalidad.

Criterios de aceptación:  

1. Sección "Ayuda" con tutoriales paso a paso (texto e imágenes).  
2. Tooltips opcionales en la primera visita a cada pantalla.  
3. Manual descargable en PDF.  
4. Acceso rápido desde el menú principal.

Subtareas técnicas (TR):  

* TR32: Elaboración del manual de usuario (contenido en Markdown/PDF)  
* TR35: Evaluación final del sistema (parcial)

\---

### **HU-20 – Exportar historial emocional**

Descripción:    
Como estudiante, quiero exportar mi historial de evaluaciones y gráficas a PDF o CSV para compartirlo con un profesional de salud o guardarlo como respaldo personal.

Criterios de aceptación:  

1. Botón "Exportar" en la pantalla de historial.  
2. El archivo exportado incluye: fechas, nivel de riesgo, hábitos registrados y recomendaciones asociadas.  
3. Formatos disponibles: PDF (legible) y CSV (para análisis externo).  
4. La exportación se genera en el backend y se descarga automáticamente.

Subtareas técnicas (TR):  

* TR37: Implementar exportación a PDF/CSV del historial (Flask \+ reportlab / csv)

\---

### **HU-21 – Editar perfil y datos personales**

Descripción:    
Como estudiante, quiero modificar mis datos personales (nombre, correo, contraseña, carrera, semestre) después de haberme registrado para mantener actualizada mi información.

Criterios de aceptación:  

1. Pantalla "Mi perfil" accesible desde el menú principal.  
2. Permite cambiar: nombre, correo (validar unicidad), contraseña (con confirmación), carrera, semestre.  
3. Los cambios se reflejan inmediatamente en el sistema sin perder el historial.  
4. Requiere autenticación y verificación de contraseña actual para cambios sensibles.

Subtareas técnicas (TR):  

* TR38: Desarrollar API y pantalla para edición de perfil (Flask \+ Flutter)

\---

### **HU-22 – Recursos de ayuda y contacto de emergencia**

Descripción:    
Como estudiante, quiero acceder a un botón de "Ayuda inmediata" que muestre contactos de servicios de bienestar universitario o líneas de crisis para recibir apoyo profesional en caso de necesitarlo.

Criterios de aceptación:  

1. Botón flotante o en menú visible en todas las pantallas.  
2. Al presionarlo, muestra: teléfono de atención psicológica de la universidad, chat de crisis (si existe), y consejos de regulación emocional.  
3. No requiere inicio de sesión (acceso rápido).  
4. Incluye un mensaje de que no es una línea de emergencia médica.

Subtareas técnicas (TR):  

* TR39: Crear sección con botón de ayuda, contactos de emergencia y consejos rápidos (Flutter, sin backend)

\---

### **HU-23 – Personalizar frecuencia y tipo de alertas**

Descripción:    
Como estudiante, quiero elegir cada cuánto y cómo quiero recibir notificaciones (push, correo, o ninguna) para no sentirme abrumado por las alertas.

Criterios de aceptación:  

1. Pantalla de configuración con opciones: “Alertas de riesgo alto” (siempre activas), “Alertas semanales de resumen”, “Desactivar todas”.  
2. El usuario puede elegir recibir recomendaciones semanales por correo.  
3. Los cambios se guardan en el perfil del usuario y se respetan al generar alertas.  
4. La configuración persiste entre sesiones.

Subtareas técnicas (TR):  

* TR40: Implementar pantalla de configuración de notificaciones en Flutter y backend para guardar preferencias

\---

## **4\. RESUMEN DE TAREAS TÉCNICAS (TR) POR SPRINT**

| Sprint | TRs involucradas |
| :---- | :---- |
| Sprint 1 | TR8, TR9, TR13, TR20, TR14, TR23, TR24, TR11, TR12, TR15, TR27, TR30 |
| Sprint 2 | TR17, TR18, TR16, TR22, TR38 |
| Sprint 3 | TR25, TR33, TR36, TR19, TR21, TR26, TR28, TR29, TR37 |
| Sprint 4 | TR31, TR34, TR32, TR35, TR39, TR40 |

Nota: TR1 a TR7 (planificación inicial) se mantienen en documentación externa fuera de JIRA.

\---

## **5\. CONCLUSIONES**

El proyecto ha sido completamente configurado en JIRA siguiendo la metodología Scrum. Se definieron 5 épicas, 4 sprints, 15 historias de usuario con sus respectivos criterios de aceptación y 40 tareas técnicas (incluyendo 5 nuevas TR). La distribución de puntos (84) es equilibrada y permite un desarrollo incremental con entregas de valor al final de cada sprint.