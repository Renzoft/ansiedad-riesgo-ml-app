/// Modelo que representa a un Usuario del sistema
class Usuario {
  final int idUsuario;
  final String nombre;
  final String correo;
  final String? facultad;
  final int? ciclo;
  final String rol;

  Usuario({
    required this.idUsuario,
    required this.nombre,
    required this.correo,
    this.facultad,
    this.ciclo,
    required this.rol,
  });

  factory Usuario.fromJson(Map<String, dynamic> json) {
    return Usuario(
      idUsuario: json['id_usuario'] ?? 0,
      nombre: json['nombre'] ?? '',
      correo: json['correo'] ?? '',
      facultad: json['facultad'],
      ciclo: json['ciclo'],
      rol: json['rol'] ?? 'Estudiante',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_usuario': idUsuario,
      'nombre': nombre,
      'correo': correo,
      'facultad': facultad,
      'ciclo': ciclo,
      'rol': rol,
    };
  }
}