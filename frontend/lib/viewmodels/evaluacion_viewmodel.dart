import 'package:flutter/foundation.dart';
import '../config/api_config.dart';
import '../models/evaluacion.dart';
import '../models/recomendacion.dart';
import '../models/resultado_ml.dart';
import '../services/api_service.dart';

/// ViewModel encargado de las evaluaciones de riesgo de ansiedad
class EvaluacionViewModel extends ChangeNotifier {
  final ApiService _apiService;

  EvaluacionViewModel(this._apiService);

  // ==========================================
  // ESTADOS
  // ==========================================
  bool _isLoading = false;
  String? _error;
  double? _probabilidad;
  String? _nivelRiesgo;
  String? _explicacion;
  List<Recomendacion> _recomendaciones = [];
  List<Evaluacion> _historial = [];
  ResultadoMl? _ultimoResultado;

  bool get isLoading => _isLoading;
  String? get error => _error;
  double? get probabilidad => _probabilidad;
  String? get nivelRiesgo => _nivelRiesgo;
  String? get explicacion => _explicacion;
  List<Recomendacion> get recomendaciones => _recomendaciones;
  List<Evaluacion> get historial => _historial;
  ResultadoMl? get ultimoResultado => _ultimoResultado;

  // ==========================================
  // EVALUAR RIESGO (POST)
  // ==========================================
  Future<bool> evaluarRiesgo(Map<String, double> variables) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.post(
        ApiConfig.evaluar,
        body: variables,
      );

      _probabilidad = (response['probabilidad_ansiedad'] as num?)?.toDouble();
      _nivelRiesgo = response['nivel_riesgo'] as String?;
      _explicacion = response['explicacion'] as String?;

      if (response['recomendaciones'] != null) {
        _recomendaciones =
            (response['recomendaciones'] as List<dynamic>)
                .map((r) => Recomendacion.fromJson(r))
                .toList();
      }

      _ultimoResultado = ResultadoMl.fromJson({
        'id_resultado': response['id_evaluacion'] ?? 0,
        'id_evaluacion': response['id_evaluacion'] ?? 0,
        'id_usuario': 0,
        'probabilidad_ansiedad': _probabilidad ?? 0,
        'nivel_riesgo': _nivelRiesgo ?? '',
        'recomendaciones': response['recomendaciones'] ?? [],
      });

      _isLoading = false;
      notifyListeners();
      return true;
    } catch (e) {
      _error = e.toString().contains('ApiException')
          ? e.toString()
          : 'Error de conexión con el servidor';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  // ==========================================
  // OBTENER HISTORIAL (GET)
  // ==========================================
  Future<void> obtenerHistorial() async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final data = await _apiService.getList(ApiConfig.historialEvaluaciones);
      _historial =
          data.map((json) => Evaluacion.fromJson(json)).toList();
      _isLoading = false;
      notifyListeners();
    } catch (e) {
      _error = e.toString().contains('ApiException')
          ? e.toString()
          : 'Error de conexión con el servidor';
      _isLoading = false;
      notifyListeners();
    }
  }

  // ==========================================
  // LIMPIAR
  // ==========================================
  void limpiarResultado() {
    _probabilidad = null;
    _nivelRiesgo = null;
    _explicacion = null;
    _recomendaciones = [];
    _ultimoResultado = null;
    notifyListeners();
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }
}