import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../viewmodels/auth_viewmodel.dart';

class HomeScreen extends StatelessWidget {
  const HomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Inicio'),
        actions: [
          IconButton(
            icon: const Icon(Icons.logout),
            onPressed: () {
              context.read<AuthViewModel>().logout();
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ],
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            // Tarjeta de bienvenida
            Card(
              child: Padding(
                padding: const EdgeInsets.all(20),
                child: Column(
                  children: [
                    const Icon(Icons.psychology, size: 48, color: Colors.indigo),
                    const SizedBox(height: 8),
                    Text(
                      'Sistema de Evaluación de Riesgo',
                      style: Theme.of(context).textTheme.titleLarge,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 4),
                    const Text(
                      'Evalúa tu nivel de riesgo de ansiedad y recibe recomendaciones personalizadas.',
                      textAlign: TextAlign.center,
                      style: TextStyle(color: Colors.grey),
                    ),
                  ],
                ),
              ),
            ),
            const SizedBox(height: 24),

            // Menú de opciones
            Expanded(
              child: GridView.count(
                crossAxisCount: 2,
                mainAxisSpacing: 12,
                crossAxisSpacing: 12,
                children: [
                  _MenuButton(
                    icon: Icons.assignment,
                    label: 'Evaluar Riesgo',
                    color: Colors.indigo,
                    onTap: () => Navigator.pushNamed(context, '/evaluacion'),
                  ),
                  _MenuButton(
                    icon: Icons.history,
                    label: 'Historial',
                    color: Colors.teal,
                    onTap: () => Navigator.pushNamed(context, '/historial'),
                  ),
                  _MenuButton(
                    icon: Icons.favorite,
                    label: 'Registrar Hábito',
                    color: Colors.orange,
                    onTap: () => Navigator.pushNamed(context, '/registrar-habito'),
                  ),
                  _MenuButton(
                    icon: Icons.person,
                    label: 'Mi Perfil',
                    color: Colors.purple,
                    onTap: () => Navigator.pushNamed(context, '/perfil'),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _MenuButton extends StatelessWidget {
  final IconData icon;
  final String label;
  final Color color;
  final VoidCallback onTap;

  const _MenuButton({
    required this.icon,
    required this.label,
    required this.color,
    required this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      elevation: 2,
      child: InkWell(
        onTap: onTap,
        borderRadius: BorderRadius.circular(12),
        child: Padding(
          padding: const EdgeInsets.all(16),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(icon, size: 40, color: color),
              const SizedBox(height: 8),
              Text(
                label,
                textAlign: TextAlign.center,
                style: const TextStyle(fontWeight: FontWeight.w500),
              ),
            ],
          ),
        ),
      ),
    );
  }
}