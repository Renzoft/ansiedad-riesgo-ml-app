import 'package:flutter/foundation.dart';
import '../config/api_config.dart';
import '../services/api_service.dart';

/// ViewModel para el panel del Médico
class MedicoViewModel extends ChangeNotifier {
  final ApiService _apiService;

  MedicoViewModel(this._apiService);

  // ==========================================
  // ESTADOS
  // ==========================================
  bool _isLoadingStats = false;
  bool _isLoadingPacientes = false;
  bool _isLoadingRecientes = false;
  String? _error;

  Map<String, dynamic>? _estadisticas;
  List<dynamic> _pacientes = [];
  List<dynamic> _evaluacionesRecientes = [];

  bool get isLoadingStats => _isLoadingStats;
  bool get isLoadingPacientes => _isLoadingPacientes;
  bool get isLoadingRecientes => _isLoadingRecientes;
  String? get error => _error;
  Map<String, dynamic>? get estadisticas => _estadisticas;
  List<dynamic> get pacientes => _pacientes;
  List<dynamic> get evaluacionesRecientes => _evaluacionesRecientes;

  // ==========================================
  // CARGAR ESTADÍSTICAS
  // ==========================================
  Future<void> cargarEstadisticas() async {
    _isLoadingStats = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.get(ApiConfig.medicoEstadisticas);
      _estadisticas = response;
      _isLoadingStats = false;
      notifyListeners();
    } catch (e) {
      _error = 'Error al cargar estadísticas';
      _isLoadingStats = false;
      notifyListeners();
    }
  }

  // ==========================================
  // CARGAR PACIENTES
  // ==========================================
  Future<void> cargarPacientes() async {
    _isLoadingPacientes = true;
    _error = null;
    notifyListeners();

    try {
      final data = await _apiService.getList(ApiConfig.medicoPacientes);
      _pacientes = data;
      _isLoadingPacientes = false;
      notifyListeners();
    } catch (e) {
      _error = 'Error al cargar pacientes';
      _isLoadingPacientes = false;
      notifyListeners();
    }
  }

  // ==========================================
  // CARGAR EVALUACIONES RECIENTES
  // ==========================================
  Future<void> cargarEvaluacionesRecientes() async {
    _isLoadingRecientes = true;
    _error = null;
    notifyListeners();

    try {
      final data = await _apiService.getList(ApiConfig.medicoEvaluacionesRecientes);
      _evaluacionesRecientes = data;
      _isLoadingRecientes = false;
      notifyListeners();
    } catch (e) {
      _error = 'Error al cargar evaluaciones recientes';
      _isLoadingRecientes = false;
      notifyListeners();
    }
  }

  // ==========================================
  // CARGAR TODO
  // ==========================================
  Future<void> cargarTodo() async {
    await Future.wait([
      cargarEstadisticas(),
      cargarPacientes(),
      cargarEvaluacionesRecientes(),
    ]);
  }

  // ==========================================
  // LIMPIAR ERROR
  // ==========================================
  void clearError() {
    _error = null;
    notifyListeners();
  }
}