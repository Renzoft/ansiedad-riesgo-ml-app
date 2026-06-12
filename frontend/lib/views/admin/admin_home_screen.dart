import 'package:flutter/material.dart';
import 'package:phosphor_flutter/phosphor_flutter.dart';
import 'package:provider/provider.dart';
import '../../constants/app_icons.dart';
import '../../viewmodels/auth_viewmodel.dart';
import '../../services/api_service.dart';
import '../../config/api_config.dart';

/// Dashboard principal para el rol Admin
class AdminHomeScreen extends StatefulWidget {
  const AdminHomeScreen({super.key});

  @override
  State<AdminHomeScreen> createState() => _AdminHomeScreenState();
}

class _AdminHomeScreenState extends State<AdminHomeScreen> {
  int _currentNavIndex = 0;
  Map<String, dynamic>? _estadisticas;
  List<dynamic> _usuarios = [];
  bool _isLoadingStats = true;
  bool _isLoadingUsers = true;
  String? _error;

  @override
  void initState() {
    super.initState();
    _cargarDatos();
  }

  Future<void> _cargarDatos() async {
    await Future.wait([
      _cargarEstadisticas(),
      _cargarUsuarios(),
    ]);
  }

  Future<void> _cargarEstadisticas() async {
    try {
      final apiService = ApiService();
      final authVM = context.read<AuthViewModel>();
      apiService.setToken(authVM.token);
      final response = await apiService.get(ApiConfig.adminEstadisticas);
      setState(() {
        _estadisticas = response;
        _isLoadingStats = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Error al cargar estadísticas';
        _isLoadingStats = false;
      });
    }
  }

  Future<void> _cargarUsuarios() async {
    try {
      final apiService = ApiService();
      final authVM = context.read<AuthViewModel>();
      apiService.setToken(authVM.token);
      final response = await apiService.getList(ApiConfig.adminUsuarios);
      setState(() {
        _usuarios = response;
        _isLoadingUsers = false;
      });
    } catch (e) {
      setState(() {
        _error = 'Error al cargar usuarios';
        _isLoadingUsers = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: const Color(0xFFF8FAFC),
      body: SafeArea(
        bottom: false,
        child: Column(
          children: [
            Expanded(
              child: _buildCurrentView(),
            ),
            _buildBottomNav(),
          ],
        ),
      ),
    );
  }

  Widget _buildCurrentView() {
    switch (_currentNavIndex) {
      case 0:
        return _buildDashboardView();
      case 1:
        return _buildUsuariosView();
      default:
        return _buildDashboardView();
    }
  }

  // ──────────────────── VISTA DASHBOARD ────────────────────
  Widget _buildDashboardView() {
    return SingleChildScrollView(
      padding: const EdgeInsets.fromLTRB(20, 16, 20, 24),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          _buildHeader(),
          const SizedBox(height: 20),
          _buildStatsGrid(),
          const SizedBox(height: 16),
        ],
      ),
    );
  }

  // ──────────────────── VISTA USUARIOS ────────────────────
  Widget _buildUsuariosView() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Padding(
          padding: const EdgeInsets.fromLTRB(20, 16, 20, 0),
          child: Row(
            children: [
              PhosphorIcon(
                AppIcons.usersFill,
                size: 26,
                color: const Color(0xFF6366F1),
              ),
              const SizedBox(width: 10),
              const Text(
                'Usuarios',
                style: TextStyle(
                  fontSize: 26,
                  fontWeight: FontWeight.bold,
                  color: Color(0xFF1E293B),
                ),
              ),
              const Spacer(),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                decoration: BoxDecoration(
                  color: const Color(0xFFEEF2FF),
                  borderRadius: BorderRadius.circular(12),
                ),
                child: Text(
                  '${_usuarios.length} total',
                  style: const TextStyle(
                    fontSize: 12,
                    fontWeight: FontWeight.w600,
                    color: Color(0xFF6366F1),
                  ),
                ),
              ),
            ],
          ),
        ),
        const SizedBox(height: 16),
        Expanded(child: _buildUsersList()),
      ],
    );
  }

  Widget _buildHeader() {
    final authVM = context.read<AuthViewModel>();
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                PhosphorIcon(
                  AppIcons.dashboardFill,
                  size: 26,
                  color: const Color(0xFF6366F1),
                ),
                const SizedBox(width: 10),
                const Text(
                  'Admin Dashboard',
                  style: TextStyle(
                    fontSize: 26,
                    fontWeight: FontWeight.bold,
                    color: Color(0xFF1E293B),
                  ),
                ),
              ],
            ),
            const SizedBox(height: 4),
            Text(
              'Bienvenido, ${authVM.nombre ?? "Admin"}',
              style: const TextStyle(
                fontSize: 14,
                color: Color(0xFF94A3B8),
              ),
            ),
          ],
        ),
        Container(
          decoration: BoxDecoration(
            color: const Color(0xFFF1F5F9),
            borderRadius: BorderRadius.circular(12),
          ),
          child: IconButton(
            icon: PhosphorIcon(
              AppIcons.signOutIcon,
              color: const Color(0xFF94A3B8),
            ),
            onPressed: () {
              authVM.logout();
              Navigator.pushReplacementNamed(context, '/login');
            },
          ),
        ),
      ],
    );
  }

  Widget _buildStatsGrid() {
    if (_isLoadingStats) {
      return const Center(child: CircularProgressIndicator());
    }

    final stats = _estadisticas;
    final usuariosPorRol = stats?['usuarios_por_rol'] as Map<String, dynamic>?;
    final distribucion = stats?['distribucion_riesgo'] as Map<String, dynamic>?;

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'Estadísticas del Sistema',
          style: TextStyle(
            fontSize: 17,
            fontWeight: FontWeight.bold,
            color: Color(0xFF1E293B),
          ),
        ),
        const SizedBox(height: 14),
        Row(
          children: [
            _buildStatCard(
              icon: AppIcons.usersThree,
              color: const Color(0xFF6366F1),
              bgColor: const Color(0xFFEEF2FF),
              label: 'Usuarios',
              value: '${stats?['total_usuarios'] ?? 0}',
            ),
            const SizedBox(width: 12),
            _buildStatCard(
              icon: AppIcons.clipboardTextFill,
              color: const Color(0xFF059669),
              bgColor: const Color(0xFFECFDF5),
              label: 'Evaluaciones',
              value: '${stats?['total_evaluaciones'] ?? 0}',
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            _buildStatCard(
              icon: AppIcons.student,
              color: const Color(0xFF3B82F6),
              bgColor: const Color(0xFFDBEAFE),
              label: 'Estudiantes',
              value: '${usuariosPorRol?['estudiantes'] ?? 0}',
            ),
            const SizedBox(width: 12),
            _buildStatCard(
              icon: AppIcons.firstAidFill,
              color: const Color(0xFFF59E0B),
              bgColor: const Color(0xFFFEF3C7),
              label: 'Médicos',
              value: '${usuariosPorRol?['medicos'] ?? 0}',
            ),
          ],
        ),
        const SizedBox(height: 12),
        Row(
          children: [
            _buildStatCard(
              icon: AppIcons.smileyFill,
              color: const Color(0xFF059669),
              bgColor: const Color(0xFFECFDF5),
              label: 'Riesgo Bajo',
              value: '${distribucion?['bajo'] ?? 0}',
            ),
            const SizedBox(width: 12),
            _buildStatCard(
              icon: AppIcons.warningFill,
              color: const Color(0xFFF59E0B),
              bgColor: const Color(0xFFFEF3C7),
              label: 'Riesgo Medio',
              value: '${distribucion?['medio'] ?? 0}',
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildStatCard({
    required IconData icon,
    required Color color,
    required Color bgColor,
    required String label,
    required String value,
  }) {
    return Expanded(
      child: Container(
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: Colors.white,
          borderRadius: BorderRadius.circular(16),
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
              width: 42,
              height: 42,
              decoration: BoxDecoration(
                color: bgColor,
                borderRadius: BorderRadius.circular(12),
              ),
              child: PhosphorIcon(icon, size: 22, color: color),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    value,
                    style: const TextStyle(
                      fontSize: 20,
                      fontWeight: FontWeight.bold,
                      color: Color(0xFF1E293B),
                    ),
                  ),
                  Text(
                    label,
                    style: const TextStyle(
                      fontSize: 12,
                      color: Color(0xFF94A3B8),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildUsersList() {
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 20),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (_isLoadingUsers)
            const Center(child: CircularProgressIndicator())
          else if (_usuarios.isEmpty)
            Container(
              width: double.infinity,
              padding: const EdgeInsets.all(40),
              decoration: BoxDecoration(
                color: Colors.white,
                borderRadius: BorderRadius.circular(16),
              ),
              child: Column(
                children: [
                  PhosphorIcon(
                    AppIcons.usersIcon,
                    size: 56,
                    color: const Color(0xFFCBD5E1),
                  ),
                  const SizedBox(height: 12),
                  const Text(
                    'No hay usuarios registrados',
                    style: TextStyle(
                      fontSize: 15,
                      color: Color(0xFF94A3B8),
                    ),
                  ),
                ],
              ),
            )
          else
            Expanded(
              child: ListView.builder(
                padding: EdgeInsets.zero,
                itemCount: _usuarios.length,
                itemBuilder: (context, index) {
                  final usuario = _usuarios[index];
                  final rol = usuario['rol'] ?? 'Estudiante';
                  return Container(
                    margin: const EdgeInsets.only(bottom: 8),
                    padding: const EdgeInsets.all(14),
                    decoration: BoxDecoration(
                      color: Colors.white,
                      borderRadius: BorderRadius.circular(14),
                      boxShadow: [
                        BoxShadow(
                          color: Colors.black.withValues(alpha: 0.03),
                          blurRadius: 8,
                          offset: const Offset(0, 1),
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        CircleAvatar(
                          radius: 20,
                          backgroundColor: _getRolColor(rol).withValues(alpha: 0.15),
                          child: PhosphorIcon(
                            _getRolIcon(rol),
                            size: 20,
                            color: _getRolColor(rol),
                          ),
                        ),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                usuario['nombre'] ?? '',
                                style: const TextStyle(
                                  fontWeight: FontWeight.w600,
                                  color: Color(0xFF1E293B),
                                ),
                              ),
                              Text(
                                usuario['correo'] ?? '',
                                style: const TextStyle(
                                  fontSize: 12,
                                  color: Color(0xFF94A3B8),
                                ),
                              ),
                            ],
                          ),
                        ),
                        Container(
                          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 4),
                          decoration: BoxDecoration(
                            color: _getRolColor(rol).withValues(alpha: 0.1),
                            borderRadius: BorderRadius.circular(12),
                          ),
                          child: Text(
                            rol,
                            style: TextStyle(
                              fontSize: 11,
                              fontWeight: FontWeight.w600,
                              color: _getRolColor(rol),
                            ),
                          ),
                        ),
                      ],
                    ),
                  );
                },
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
        return AppIcons.shieldCheckFill;
      case 'Medico':
        return AppIcons.firstAidFill;
      default:
        return AppIcons.student;
    }
  }

  Widget _buildBottomNav() {
    return Container(
      decoration: BoxDecoration(
        color: Colors.white,
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.06),
            blurRadius: 12,
            offset: const Offset(0, -2),
          ),
        ],
      ),
      child: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 8),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildNavItem(
                index: 0,
                icon: AppIcons.dashboardFill,
                label: 'Dashboard',
              ),
              _buildNavItem(
                index: 1,
                icon: AppIcons.usersFill,
                label: 'Usuarios',
              ),
              _buildNavItem(
                index: 2,
                icon: AppIcons.profileFill,
                label: 'Perfil',
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem({
    required int index,
    required IconData icon,
    required String label,
  }) {
    final isActive = _currentNavIndex == index;
    return GestureDetector(
      onTap: () {
        if (index == 2) {
          Navigator.pushNamed(context, '/perfil');
          return;
        }
        setState(() {
          _currentNavIndex = index;
        });
      },
      child: Container(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 8),
        decoration: isActive
            ? BoxDecoration(
                color: const Color(0xFFEEF2FF),
                borderRadius: BorderRadius.circular(12),
              )
            : null,
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            PhosphorIcon(
              icon,
              size: 24,
              color: isActive ? const Color(0xFF6366F1) : const Color(0xFF94A3B8),
            ),
            const SizedBox(height: 4),
            Text(
              label,
              style: TextStyle(
                fontSize: 11,
                fontWeight: isActive ? FontWeight.w600 : FontWeight.normal,
                color: isActive ? const Color(0xFF6366F1) : const Color(0xFF94A3B8),
              ),
            ),
          ],
        ),
      ),
    );
  }
}