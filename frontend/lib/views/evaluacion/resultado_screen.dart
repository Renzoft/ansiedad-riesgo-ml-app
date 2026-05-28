import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../models/recomendacion.dart';
import '../../viewmodels/evaluacion_viewmodel.dart';
import '../../widgets/risk_indicator.dart';

class ResultadoScreen extends StatelessWidget {
  const ResultadoScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Resultado'),
        actions: [
          IconButton(
            icon: const Icon(Icons.home),
            onPressed: () => Navigator.pushNamedAndRemoveUntil(
              context, '/home', (route) => false,
            ),
          ),
        ],
      ),
      body: Consumer<EvaluacionViewModel>(
        builder: (context, evVM, _) {
          if (evVM.probabilidad == null) {
            return const Center(child: Text('No hay resultados disponibles.'));
          }

          return SingleChildScrollView(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                RiskIndicator(
                  probabilidad: evVM.probabilidad!,
                  nivelRiesgo: evVM.nivelRiesgo ?? '',
                ),
                const SizedBox(height: 16),

                if (evVM.explicacion != null)
                  Card(
                    child: Padding(
                      padding: const EdgeInsets.all(16),
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          const Text(
                            'Explicación',
                            style: TextStyle(fontWeight: FontWeight.bold, fontSize: 16),
                          ),
                          const SizedBox(height: 8),
                          Text(evVM.explicacion!),
                        ],
                      ),
                    ),
                  ),
                const SizedBox(height: 16),

                if (evVM.recomendaciones.isNotEmpty) ...[
                  const Text(
                    'Recomendaciones',
                    style: TextStyle(fontWeight: FontWeight.bold, fontSize: 18),
                  ),
                  const SizedBox(height: 8),
                  ..._buildRecomendaciones(evVM.recomendaciones),
                ],

                const SizedBox(height: 16),

                ElevatedButton.icon(
                  onPressed: () {
                    evVM.limpiarResultado();
                    Navigator.pop(context);
                  },
                  icon: const Icon(Icons.replay),
                  label: const Text('Realizar otra evaluación'),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  List<Widget> _buildRecomendaciones(List<Recomendacion> recomendaciones) {
    return recomendaciones.map((rec) {
      return Card(
        margin: const EdgeInsets.only(bottom: 8),
        child: ListTile(
          leading: const Icon(Icons.lightbulb, color: Colors.amber),
          title: Text(rec.titulo),
          subtitle: Text(rec.descripcion),
        ),
      );
    }).toList();
  }
}