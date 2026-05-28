import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../viewmodels/evaluacion_viewmodel.dart';
import '../../widgets/custom_button.dart';

/// Pantalla con el formulario de las 15 variables para evaluar el riesgo
class EvaluacionScreen extends StatefulWidget {
  const EvaluacionScreen({super.key});

  @override
  State<EvaluacionScreen> createState() => _EvaluacionScreenState();
}

class _EvaluacionScreenState extends State<EvaluacionScreen> {
  final _formKey = GlobalKey<FormState>();

  // Controladores para las 15 variables
  final _phq9 = TextEditingController(text: '0');
  final _gad7 = TextEditingController(text: '0');
  final _sleepHours = TextEditingController(text: '7');
  final _exerciseFreq = TextEditingController(text: '3');
  final _socialActivity = TextEditingController(text: '5');
  final _onlineStress = TextEditingController(text: '5');
  final _gpa = TextEditingController(text: '3.0');
  final _familySupport = TextEditingController(text: '5');
  final _screenTime = TextEditingController(text: '5');
  final _academicStress = TextEditingController(text: '5');
  final _dietQuality = TextEditingController(text: '5');
  final _selfEfficacy = TextEditingController(text: '5');
  final _peerRelationship = TextEditingController(text: '5');
  final _financialStress = TextEditingController(text: '5');
  final _sleepQuality = TextEditingController(text: '5');

  @override
  void dispose() {
    for (final c in [
      _phq9, _gad7, _sleepHours, _exerciseFreq, _socialActivity,
      _onlineStress, _gpa, _familySupport, _screenTime, _academicStress,
      _dietQuality, _selfEfficacy, _peerRelationship, _financialStress, _sleepQuality,
    ]) {
      c.dispose();
    }
    super.dispose();
  }

  Future<void> _handleEvaluar() async {
    if (!_formKey.currentState!.validate()) return;

    final variables = {
      'phq9_score': double.parse(_phq9.text),
      'gad7_score': double.parse(_gad7.text),
      'sleep_hours': double.parse(_sleepHours.text),
      'exercise_freq': double.parse(_exerciseFreq.text),
      'social_activity': double.parse(_socialActivity.text),
      'online_stress': double.parse(_onlineStress.text),
      'gpa': double.parse(_gpa.text),
      'family_support': double.parse(_familySupport.text),
      'screen_time': double.parse(_screenTime.text),
      'academic_stress': double.parse(_academicStress.text),
      'diet_quality': double.parse(_dietQuality.text),
      'self_efficacy': double.parse(_selfEfficacy.text),
      'peer_relationship': double.parse(_peerRelationship.text),
      'financial_stress': double.parse(_financialStress.text),
      'sleep_quality': double.parse(_sleepQuality.text),
    };

    final evaluacionVM = context.read<EvaluacionViewModel>();
    final success = await evaluacionVM.evaluarRiesgo(variables);

    if (success && mounted) {
      Navigator.pushNamed(context, '/resultado');
    }
  }

  Widget _buildSlider({
    required String label,
    required String descripcion,
    required TextEditingController controller,
    required double min,
    required double max,
    required String unidad,
  }) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(fontWeight: FontWeight.bold)),
            if (descripcion.isNotEmpty)
              Text(descripcion, style: const TextStyle(fontSize: 12, color: Colors.grey)),
            const SizedBox(height: 8),
            Row(
              children: [
                SizedBox(
                  width: 60,
                  child: TextFormField(
                    controller: controller,
                    keyboardType: TextInputType.number,
                    textAlign: TextAlign.center,
                    decoration: const InputDecoration(
                      border: OutlineInputBorder(),
                      contentPadding: EdgeInsets.symmetric(vertical: 8),
                    ),
                    validator: (v) {
                      if (v == null || v.isEmpty) return 'Req.';
                      final val = double.tryParse(v);
                      if (val == null) return 'Núm.';
                      if (val < min || val > max) return '$min-$max';
                      return null;
                    },
                  ),
                ),
                const SizedBox(width: 8),
                Text(unidad, style: const TextStyle(color: Colors.grey)),
                const Spacer(),
                Text('$min-$max', style: const TextStyle(fontSize: 12, color: Colors.grey)),
              ],
            ),
          ],
        ),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Evaluar Riesgo')),
      body: SingleChildScrollView(
        padding: const EdgeInsets.all(16),
        child: Form(
          key: _formKey,
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const Text(
                'Completa los siguientes indicadores',
                style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 4),
              const Text(
                'Todas las respuestas son anónimas y confidenciales.',
                style: TextStyle(color: Colors.grey),
              ),
              const SizedBox(height: 16),

              _buildSlider(
                label: 'PHQ-9',
                descripcion: 'Nivel de depresión (0=ninguno, 27=severo)',
                controller: _phq9, min: 0, max: 27, unidad: '',
              ),
              _buildSlider(
                label: 'GAD-7',
                descripcion: 'Nivel de ansiedad (0=ninguno, 21=severo)',
                controller: _gad7, min: 0, max: 21, unidad: '',
              ),
              _buildSlider(
                label: 'Horas de sueño',
                descripcion: 'Promedio de horas que duermes al día',
                controller: _sleepHours, min: 3, max: 10, unidad: 'hrs',
              ),
              _buildSlider(
                label: 'Frecuencia de ejercicio',
                descripcion: 'Días a la semana que haces ejercicio',
                controller: _exerciseFreq, min: 0, max: 7, unidad: 'días/sem',
              ),
              _buildSlider(
                label: 'Actividad social',
                descripcion: 'Nivel de interacción social (0=bajo, 10=alto)',
                controller: _socialActivity, min: 0, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'Estrés online',
                descripcion: 'Estrés por redes/internet (1=bajo, 10=alto)',
                controller: _onlineStress, min: 1, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'GPA / Promedio',
                descripcion: 'Promedio académico',
                controller: _gpa, min: 0, max: 5, unidad: '',
              ),
              _buildSlider(
                label: 'Apoyo familiar',
                descripcion: 'Apoyo familiar percibido (1=bajo, 10=alto)',
                controller: _familySupport, min: 1, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'Tiempo de pantalla',
                descripcion: 'Horas frente a pantalla al día',
                controller: _screenTime, min: 1, max: 12, unidad: 'hrs',
              ),
              _buildSlider(
                label: 'Estrés académico',
                descripcion: 'Estrés por estudios (1=bajo, 10=alto)',
                controller: _academicStress, min: 1, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'Calidad de alimentación',
                descripcion: 'Calidad de tu dieta (1=mala, 10=excelente)',
                controller: _dietQuality, min: 1, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'Autoeficacia',
                descripcion: 'Confianza en ti mismo (1=baja, 10=alta)',
                controller: _selfEfficacy, min: 1, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'Relaciones con pares',
                descripcion: 'Relación con compañeros (1=mala, 10=excelente)',
                controller: _peerRelationship, min: 1, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'Estrés financiero',
                descripcion: 'Preocupación económica (1=baja, 10=alta)',
                controller: _financialStress, min: 1, max: 10, unidad: '',
              ),
              _buildSlider(
                label: 'Calidad del sueño',
                descripcion: 'Calidad general del sueño (0=mala, 10=excelente)',
                controller: _sleepQuality, min: 0, max: 10, unidad: '',
              ),

              const SizedBox(height: 24),

              Consumer<EvaluacionViewModel>(
                builder: (context, evVM, _) {
                  if (evVM.error != null) {
                    WidgetsBinding.instance.addPostFrameCallback((_) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(
                          content: Text(evVM.error!), backgroundColor: Colors.red,
                        ),
                      );
                      evVM.clearError();
                    });
                  }

                  return CustomButton(
                    text: 'Evaluar Riesgo',
                    isLoading: evVM.isLoading,
                    onPressed: _handleEvaluar,
                  );
                },
              ),
              const SizedBox(height: 32),
            ],
          ),
        ),
      ),
    );
  }
}