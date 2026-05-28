import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../viewmodels/auth_viewmodel.dart';

class PerfilScreen extends StatelessWidget {
  const PerfilScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Mi Perfil')),
      body: Consumer<AuthViewModel>(
        builder: (context, authVM, _) {
          final usuario = authVM.usuario;
          final rol = authVM.rol ?? 'Estudiante';
          final nombre = authVM.nombre ?? 'Usuario';
          final correo = authVM.correo ?? '';
          final facultad = usuario?['facultad'] as String?;
          final ciclo = usuario?['ciclo'];

          return SingleChildScrollView(
            padding: const EdgeInsets.all(24),
            child: Column(
              children: [
                // Avatar con color según rol
                CircleAvatar(
                  radius: 44,
                  backgroundColor: _getRolColor(rol).withValues(alpha: 0.15),
                  child: Icon(
                    _getRolIcon(rol),
                    size: 44,
                    color: _getRolColor(rol),
                  ),
                ),
                const SizedBox(height: 16),
                Text(
                  nombre,
                  style: Theme.of(context).textTheme.titleLarge?.copyWith(
                    fontWeight: FontWeight.bold,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  correo,
                  style: const TextStyle(color: Color(0xFF94A3B8)),
                ),
                const SizedBox(height: 8),
                Container(
                  padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 6),
                  decoration: BoxDecoration(
                    color: _getRolColor(rol).withValues(alpha: 0.1),
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Text(
                    rol,
                    style: TextStyle(
                      color: _getRolColor(rol),
                      fontWeight: FontWeight.w600,
                      fontSize: 13,
                    ),
                  ),
                ),
                const SizedBox(height: 28),

                // Info cards
                _buildInfoCard(
                  icon: Icons.school_outlined,
                  label: 'Facultad',
                  value: facultad ?? 'No especificada',
                ),
                if (ciclo != null) ...[
                  const SizedBox(height: 12),
                  _buildInfoCard(
                    icon: Icons.calendar_today_outlined,
                    label: 'Ciclo',
                    value: '$ciclo',
                  ),
                ],
                const SizedBox(height: 12),
                _buildInfoCard(
                  icon: Icons.email_outlined,
                  label: 'Correo',
                  value: correo,
                ),

                const SizedBox(height: 32),

                // Logout button
                Card(
                  child: ListTile(
                    leading: const Icon(Icons.logout, color: Colors.red),
                    title: const Text('Cerrar Sesión'),
                    onTap: () {
                      authVM.logout();
                      Navigator.pushNamedAndRemoveUntil(
                        context, '/login', (route) => false,
                      );
                    },
                  ),
                ),
              ],
            ),
          );
        },
      ),
    );
  }

  Widget _buildInfoCard({
    required IconData icon,
    required String label,
    required String value,
  }) {
    return Container(
      width: double.infinity,
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: Colors.white,
        borderRadius: BorderRadius.circular(14),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 10,
            offset: const Offset(0, 2),
          ),
        ],
      ),
      child: Row(
        children: [
          Container(
            width: 40,
            height: 40,
            decoration: BoxDecoration(
              color: const Color(0xFFF1F5F9),
              borderRadius: BorderRadius.circular(10),
            ),
            child: Icon(icon, size: 20, color: const Color(0xFF64748B)),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  label,
                  style: const TextStyle(
                    fontSize: 12,
                    color: Color(0xFF94A3B8),
                  ),
                ),
                const SizedBox(height: 2),
                Text(
                  value,
                  style: const TextStyle(
                    fontSize: 15,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF1E293B),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Color _getRolColor(String rol) {
    switch (rol) {
      case 'Admin':
        return const Color(0xFF6366F1);
      case 'Medico':
        return const Color(0xFFF59E0B);
      default:
        return const Color(0xFF3B82F6);
    }
  }

  IconData _getRolIcon(String rol) {
    switch (rol) {
      case 'Admin':
        return Icons.admin_panel_settings;
      case 'Medico':
        return Icons.local_hospital;
      default:
        return Icons.school;
    }
  }
}