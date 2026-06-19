import 'recomendacion.dart';

/// ==========================================
/// NUEVO
/// Modelo para el reporte generado por Gemini
/// ==========================================
class ReporteIA {
  final String resumen;
  final List<String> fortalezas;
  final List<String> factoresPreocupantes;
  final List<String> recomendaciones;
  final List<String> plan7Dias;
  final List<String> temasVideos;
  final List<String> temasLectura;
  final String prioridadIntervencion;
  final String mensajeMotivacional;

  ReporteIA({
    required this.resumen,
    required this.fortalezas,
    required this.factoresPreocupantes,
    required this.recomendaciones,
    required this.plan7Dias,
    required this.temasVideos,
    required this.temasLectura,
    required this.prioridadIntervencion,
    required this.mensajeMotivacional,
  });

  factory ReporteIA.fromJson(Map<String, dynamic> json) {
    return ReporteIA(
      resumen: json['resumen'] ?? '',

      fortalezas: List<String>.from(json['fortalezas'] ?? []),

      factoresPreocupantes: List<String>.from(
        json['factores_preocupantes'] ?? [],
      ),

      recomendaciones: List<String>.from(json['recomendaciones'] ?? []),

      plan7Dias: List<String>.from(json['plan_7_dias'] ?? []),

      temasVideos: List<String>.from(json['temas_videos'] ?? []),

      temasLectura: List<String>.from(json['temas_lectura'] ?? []),

      prioridadIntervencion: json['prioridad_intervencion'] ?? '',

      mensajeMotivacional: json['mensaje_motivacional'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'resumen': resumen,
      'fortalezas': fortalezas,
      'factores_preocupantes': factoresPreocupantes,
      'recomendaciones': recomendaciones,
      'plan_7_dias': plan7Dias,
      'temas_videos': temasVideos,
      'temas_lectura': temasLectura,
      'prioridad_intervencion': prioridadIntervencion,
      'mensaje_motivacional': mensajeMotivacional,
    };
  }
}

/// ==========================================
/// Modelo Resultado ML
/// ==========================================
class ResultadoMl {
  final int idResultado;
  final int idEvaluacion;
  final int idUsuario;
  final double probabilidadAnsiedad;
  final String nivelRiesgo;
  final String? fechaPrediccion;
  final List<Recomendacion> recomendaciones;

  /// ==========================================
  /// NUEVO
  /// Reporte generado por Gemini
  /// ==========================================
  final ReporteIA? reporteIA;

  ResultadoMl({
    required this.idResultado,
    required this.idEvaluacion,
    required this.idUsuario,
    required this.probabilidadAnsiedad,
    required this.nivelRiesgo,
    this.fechaPrediccion,
    this.recomendaciones = const [],

    /// NUEVO
    this.reporteIA,
  });

  factory ResultadoMl.fromJson(Map<String, dynamic> json) {
    return ResultadoMl(
      idResultado: json['id_resultado'] ?? 0,

      idEvaluacion: json['id_evaluacion'] ?? 0,

      idUsuario: json['id_usuario'] ?? 0,

      probabilidadAnsiedad: (json['probabilidad_ansiedad'] ?? 0).toDouble(),

      nivelRiesgo: json['nivel_riesgo'] ?? 'BAJO',

      fechaPrediccion: json['fecha_prediccion'],

      recomendaciones:
          (json['recomendaciones'] as List<dynamic>?)
              ?.map((r) => Recomendacion.fromJson(r))
              .toList() ??
          [],

      /// ==========================================
      /// NUEVO
      /// Parsear reporte generado por Gemini
      /// ==========================================
      reporteIA: json['reporte_ia'] != null
          ? ReporteIA.fromJson(json['reporte_ia'])
          : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_resultado': idResultado,
      'id_evaluacion': idEvaluacion,
      'id_usuario': idUsuario,
      'probabilidad_ansiedad': probabilidadAnsiedad,
      'nivel_riesgo': nivelRiesgo,
      'fecha_prediccion': fechaPrediccion,

      /// NUEVO
      'reporte_ia': reporteIA?.toJson(),

      'recomendaciones': recomendaciones.map((r) => r.toJson()).toList(),
    };
  }
}
