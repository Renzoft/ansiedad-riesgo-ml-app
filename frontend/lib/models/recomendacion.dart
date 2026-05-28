/// Modelo que representa una Recomendación asociada a un nivel de riesgo
class Recomendacion {
  final int idRecomendacion;
  final String categoria; // 'BAJO', 'MEDIO', 'ALTO'
  final String titulo;
  final String descripcion;

  Recomendacion({
    required this.idRecomendacion,
    required this.categoria,
    required this.titulo,
    required this.descripcion,
  });

  factory Recomendacion.fromJson(Map<String, dynamic> json) {
    return Recomendacion(
      idRecomendacion: json['id_recomendacion'] ?? 0,
      categoria: json['categoria'] ?? '',
      titulo: json['titulo'] ?? '',
      descripcion: json['descripcion'] ?? '',
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id_recomendacion': idRecomendacion,
      'categoria': categoria,
      'titulo': titulo,
      'descripcion': descripcion,
    };
  }
}