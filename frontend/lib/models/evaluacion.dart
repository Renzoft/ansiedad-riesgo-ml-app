import 'resultado_ml.dart';

/// Modelo que representa una Evaluación de riesgo de ansiedad
class Evaluacion {
  final int idEvaluacion;
  final int idUsuario;
  final String? fechaRealizacion;

  // 15 variables del modelo ML
  final double phq9Score;
  final double gad7Score;
  final double sleepHours;
  final double exerciseFreq;
  final double socialActivity;
  final double onlineStress;
  final double gpa;
  final double familySupport;
  final double screenTime;
  final double academicStress;
  final double dietQuality;
  final double selfEfficacy;
  final double peerRelationship;
  final double financialStress;
  final double sleepQuality;

  final ResultadoMl? resultado;

  Evaluacion({
    required this.idEvaluacion,
    required this.idUsuario,
    this.fechaRealizacion,
    required this.phq9Score,
    required this.gad7Score,
    required this.sleepHours,
    required this.exerciseFreq,
    required this.socialActivity,
    required this.onlineStress,
    required this.gpa,
    required this.familySupport,
    required this.screenTime,
    required this.academicStress,
    required this.dietQuality,
    required this.selfEfficacy,
    required this.peerRelationship,
    required this.financialStress,
    required this.sleepQuality,
    this.resultado,
  });

  factory Evaluacion.fromJson(Map<String, dynamic> json) {
    return Evaluacion(
      idEvaluacion: json['id_evaluacion'] ?? 0,
      idUsuario: json['id_usuario'] ?? 0,
      fechaRealizacion: json['fecha_realizacion'],
      phq9Score: (json['phq9_score'] ?? 0).toDouble(),
      gad7Score: (json['gad7_score'] ?? 0).toDouble(),
      sleepHours: (json['sleep_hours'] ?? 0).toDouble(),
      exerciseFreq: (json['exercise_freq'] ?? 0).toDouble(),
      socialActivity: (json['social_activity'] ?? 0).toDouble(),
      onlineStress: (json['online_stress'] ?? 0).toDouble(),
      gpa: (json['gpa'] ?? 0).toDouble(),
      familySupport: (json['family_support'] ?? 0).toDouble(),
      screenTime: (json['screen_time'] ?? 0).toDouble(),
      academicStress: (json['academic_stress'] ?? 0).toDouble(),
      dietQuality: (json['diet_quality'] ?? 0).toDouble(),
      selfEfficacy: (json['self_efficacy'] ?? 0).toDouble(),
      peerRelationship: (json['peer_relationship'] ?? 0).toDouble(),
      financialStress: (json['financial_stress'] ?? 0).toDouble(),
      sleepQuality: (json['sleep_quality'] ?? 0).toDouble(),
      resultado:
          json['resultado'] != null
              ? ResultadoMl.fromJson(json['resultado'])
              : null,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'phq9_score': phq9Score,
      'gad7_score': gad7Score,
      'sleep_hours': sleepHours,
      'exercise_freq': exerciseFreq,
      'social_activity': socialActivity,
      'online_stress': onlineStress,
      'gpa': gpa,
      'family_support': familySupport,
      'screen_time': screenTime,
      'academic_stress': academicStress,
      'diet_quality': dietQuality,
      'self_efficacy': selfEfficacy,
      'peer_relationship': peerRelationship,
      'financial_stress': financialStress,
      'sleep_quality': sleepQuality,
    };
  }
}