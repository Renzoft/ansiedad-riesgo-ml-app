import 'recomendacion.dart';

/// Modelo que representa el resultado de la predicción del modelo ML
class ResultadoMl {
  final int idResultado;
  final int idEvaluacion;
  final int idUsuario;
  final double probabilidadAnsiedad;
  final String nivelRiesgo; // 'BAJO', 'MEDIO', 'ALTO'
  final String? fechaPrediccion;
  final List<Recomendacion> recomendaciones;

  ResultadoMl({
    required this.idResultado,
    required this.idEvaluacion,
    required this.idUsuario,
    required this.probabilidadAnsiedad,
    required this.nivelRiesgo,
    this.fechaPrediccion,
    this.recomendaciones = const [],
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
    };
  }
}