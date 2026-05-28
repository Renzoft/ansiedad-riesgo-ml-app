/// Configuración de la API del backend
class ApiConfig {
  // Para emulador Android usar 10.0.2.2
  // Para dispositivo físico usar la IP local del servidor
  static const String baseUrl = 'http://10.0.2.2:5000';

  // ==========================================
  // ENDPOINTS DE AUTENTICACIÓN
  // ==========================================
  static const String registro = '$baseUrl/registro';
  static const String login = '$baseUrl/login';

  // ==========================================
  // ENDPOINTS DE EVALUACIONES
  // ==========================================
  static const String evaluar = '$baseUrl/api/v1/evaluaciones/';
  static const String historialEvaluaciones =
      '$baseUrl/api/v1/evaluaciones/historial';

  // ==========================================
  // ENDPOINTS DE HÁBITOS
  // ==========================================
  static const String habitos = '$baseUrl/habitos';
  static const String ultimoHabito = '$baseUrl/habitos/ultimo';

  // ==========================================
  // ENDPOINTS DE ADMIN
  // ==========================================
  static const String adminUsuarios = '$baseUrl/api/v1/admin/usuarios';
  static const String adminEstadisticas = '$baseUrl/api/v1/admin/usuarios/estadisticas';
}
