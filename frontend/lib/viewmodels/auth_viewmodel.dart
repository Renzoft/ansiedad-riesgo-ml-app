import 'package:flutter/foundation.dart';
import '../config/api_config.dart';
import '../services/api_service.dart';

/// ViewModel encargado de la autenticación (Login y Registro)
class AuthViewModel extends ChangeNotifier {
  final ApiService _apiService;

  AuthViewModel(this._apiService);

  // ==========================================
  // ESTADOS
  // ==========================================
  bool _isLoading = false;
  String? _error;
  String? _token;
  bool _isAuthenticated = false;
  Map<String, dynamic>? _usuario;

  bool get isLoading => _isLoading;
  String? get error => _error;
  String? get token => _token;
  bool get isAuthenticated => _isAuthenticated;
  Map<String, dynamic>? get usuario => _usuario;
  String? get rol => _usuario?['rol'] as String?;
  String? get nombre => _usuario?['nombre'] as String?;
  String? get correo => _usuario?['correo'] as String?;
  int? get idUsuario => _usuario?['id_usuario'] as int?;

  // ==========================================
  // LOGIN
  // ==========================================
  Future<bool> login(String correo, String contrasena) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final response = await _apiService.post(
        ApiConfig.login,
        body: {'correo': correo, 'contrasena': contrasena},
        withAuth: false,
      );

      _token = response['token'] as String?;
      _usuario = response['usuario'] as Map<String, dynamic>?;
      if (_token != null) {
        _apiService.setToken(_token);
        _isAuthenticated = true;
        _isLoading = false;
        notifyListeners();
        return true;
      }

      _error = 'No se recibió token de autenticación';
      _isLoading = false;
      notifyListeners();
      return false;
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
  // REGISTRO
  // ==========================================
  Future<bool> registrar({
    required String nombre,
    required String correo,
    required String contrasena,
    String? facultad,
    int? ciclo,
  }) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      final body = <String, dynamic>{
        'nombre': nombre,
        'correo': correo,
        'contrasena': contrasena,
      };
      if (facultad != null && facultad.isNotEmpty) body['facultad'] = facultad;
      if (ciclo != null) body['ciclo'] = ciclo;

      await _apiService.post(ApiConfig.registro, body: body, withAuth: false);

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
  // CERRAR SESIÓN
  // ==========================================
  void logout() {
    _token = null;
    _isAuthenticated = false;
    _usuario = null;
    _apiService.setToken(null);
    notifyListeners();
  }

  // ==========================================
  // LIMPIAR ERROR
  // ==========================================
  void clearError() {
    _error = null;
    notifyListeners();
  }
}