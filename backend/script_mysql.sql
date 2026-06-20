-- =============================================================
-- SCRIPT DE BASE DE DATOS PARA MYSQL
-- Proyecto: Ansiedad Riesgo ML App
-- Motor: MySQL
-- =============================================================

-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS ansiedad_riesgo_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE ansiedad_riesgo_db;

-- =============================================================
-- 1. TABLA: usuarios
-- =============================================================
CREATE TABLE usuarios (
    id_usuario      INT             NOT NULL AUTO_INCREMENT,
    nombre          VARCHAR(100)    NOT NULL,
    correo          VARCHAR(100)    NOT NULL,
    contrasena      VARCHAR(255)    NOT NULL,
    facultad        VARCHAR(100)    DEFAULT NULL,
    ciclo           INT             DEFAULT NULL,
    fecha_registro  DATETIME        DEFAULT CURRENT_TIMESTAMP,
    rol             VARCHAR(20)     DEFAULT 'estudiante',

    PRIMARY KEY (id_usuario),
    UNIQUE KEY uq_correo (correo)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- 2. TABLA: evaluacion (15 variables del modelo ML)
-- =============================================================
CREATE TABLE evaluacion (
    id_evaluacion       INT         NOT NULL AUTO_INCREMENT,
    id_usuario          INT         NOT NULL,
    fecha_realizacion   DATETIME    DEFAULT CURRENT_TIMESTAMP,

    -- 15 variables del modelo ML
    phq9_score          FLOAT       NOT NULL COMMENT 'Rango: 0-27',
    gad7_score          FLOAT       NOT NULL COMMENT 'Rango: 0-21',
    sleep_hours         FLOAT       NOT NULL COMMENT 'Rango: 3.0-10.0',
    exercise_freq       FLOAT       NOT NULL COMMENT 'Rango: 0-7',
    social_activity     FLOAT       NOT NULL COMMENT 'Rango: 0-10',
    online_stress       FLOAT       NOT NULL COMMENT 'Rango: 1-10',
    gpa                 FLOAT       NOT NULL COMMENT 'Rango: 0.0-5.0',
    family_support      FLOAT       NOT NULL COMMENT 'Rango: 1-10',
    screen_time         FLOAT       NOT NULL COMMENT 'Rango: 1.0-12.0',
    academic_stress     FLOAT       NOT NULL COMMENT 'Rango: 1-10',
    diet_quality        FLOAT       NOT NULL COMMENT 'Rango: 1-10',
    self_efficacy       FLOAT       NOT NULL COMMENT 'Rango: 1-10',
    peer_relationship   FLOAT       NOT NULL COMMENT 'Rango: 1-10',
    financial_stress    FLOAT       NOT NULL COMMENT 'Rango: 1-10',
    sleep_quality       FLOAT       NOT NULL COMMENT 'Rango: 0-10',

    PRIMARY KEY (id_evaluacion),
    KEY fk_evaluacion_usuario (id_usuario),
    CONSTRAINT fk_evaluacion_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- 3. TABLA: resultados_ml (predicciones del modelo)
-- =============================================================
CREATE TABLE resultados_ml (
    id_resultado            INT         NOT NULL AUTO_INCREMENT,
    id_evaluacion           INT         NOT NULL,
    id_usuario              INT         NOT NULL,
    probabilidad_ansiedad   FLOAT       NOT NULL,
    nivel_riesgo            VARCHAR(20) NOT NULL COMMENT 'BAJO, MEDIO, ALTO',
    fecha_prediccion        DATETIME    DEFAULT CURRENT_TIMESTAMP,
    reporte_ia              TEXT        DEFAULT NULL COMMENT 'JSON con el reporte generado por Gemini',

    PRIMARY KEY (id_resultado),
    UNIQUE KEY uq_id_evaluacion (id_evaluacion),
    KEY fk_resultados_usuario (id_usuario),
    CONSTRAINT fk_resultados_evaluacion FOREIGN KEY (id_evaluacion)
        REFERENCES evaluacion (id_evaluacion)
        ON DELETE CASCADE,
    CONSTRAINT fk_resultados_usuario FOREIGN KEY (id_usuario)
        REFERENCES usuarios (id_usuario)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- 4. TABLA: recomendaciones (catálogo)
-- =============================================================
CREATE TABLE recomendaciones (
    id_recomendacion    INT             NOT NULL AUTO_INCREMENT,
    categoria           VARCHAR(50)     NOT NULL COMMENT 'BAJO, MEDIO, ALTO',
    titulo              VARCHAR(150)    NOT NULL,
    descripcion         TEXT            NOT NULL,

    PRIMARY KEY (id_recomendacion),
    KEY idx_categoria (categoria)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- 5. TABLA PIVOTE: resultado_recomendaciones (M:N)
-- =============================================================
CREATE TABLE resultado_recomendaciones (
    id_resultado        INT NOT NULL,
    id_recomendacion    INT NOT NULL,

    PRIMARY KEY (id_resultado, id_recomendacion),
    CONSTRAINT fk_rr_resultado FOREIGN KEY (id_resultado)
        REFERENCES resultados_ml (id_resultado)
        ON DELETE CASCADE,
    CONSTRAINT fk_rr_recomendacion FOREIGN KEY (id_recomendacion)
        REFERENCES recomendaciones (id_recomendacion)
        ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- =============================================================
-- DATOS INICIALES: Recomendaciones base
-- =============================================================
INSERT INTO recomendaciones (categoria, titulo, descripcion) VALUES
(
    'BAJO',
    'Mantén tus hábitos saludables',
    'Tus indicadores muestran un equilibrio saludable. Continúa con tus rutinas de sueño, ejercicio y alimentación. Considera practicar mindfulness para mantener tu bienestar.'
),
(
    'MEDIO',
    'Refuerza tus estrategias de manejo del estrés',
    'Se detectan ciertos niveles de alerta en tus indicadores. Revisa tus horas de sueño, incorpora pausas activas durante el estudio y busca apoyo en tus compañeros o familiares. Considera consultar con el servicio de bienestar estudiantil.'
),
(
    'ALTO',
    'Busca apoyo profesional',
    'Tus indicadores sugieren una alta predisposición a ansiedad. Es importante que acudas al departamento de bienestar estudiantil o a un profesional de salud mental. No estás solo/a, hay recursos disponibles para apoyarte.'
);