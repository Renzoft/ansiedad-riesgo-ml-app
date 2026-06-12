import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// Services
import 'services/api_service.dart';

// ViewModels
import 'viewmodels/auth_viewmodel.dart';
import 'viewmodels/evaluacion_viewmodel.dart';
import 'viewmodels/medico_viewmodel.dart';
import 'viewmodels/theme_viewmodel.dart';

// Theme
import 'constants/app_colors.dart';

// Screens
import 'views/onboarding/onboarding_screen.dart';
import 'views/auth/login_screen.dart';
import 'views/home/home_screen.dart';
import 'views/admin/admin_home_screen.dart';
import 'views/medico/medico_home_screen.dart';
import 'views/evaluacion/evaluacion_screen.dart';
import 'views/evaluacion/resultado_screen.dart';
import 'views/evaluacion/historial_screen.dart';
import 'views/perfil/perfil_screen.dart';

void main() {
  runApp(const AnsiedadApp());
}

class AnsiedadApp extends StatelessWidget {
  const AnsiedadApp({super.key});

  @override
  Widget build(BuildContext context) {
    final apiService = ApiService();

    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => ThemeNotifier()),
        ChangeNotifierProvider(create: (_) => AuthViewModel(apiService)),
        ChangeNotifierProvider(create: (_) => EvaluacionViewModel(apiService)),
        ChangeNotifierProvider(create: (_) => MedicoViewModel(apiService)),
      ],
      child: Consumer<ThemeNotifier>(
        builder: (context, themeNotifier, _) {
          return MaterialApp(
            title: 'Evaluación de Riesgo',
            debugShowCheckedModeBanner: false,
            themeMode: themeNotifier.themeMode,
            theme: ThemeData(
              brightness: Brightness.light,
              colorScheme: const ColorScheme.light(
                primary: Color(0xFF6366F1),
                secondary: Color(0xFF6366F1),
                surface: Colors.white,
              ),
              useMaterial3: true,
              appBarTheme: const AppBarTheme(
                centerTitle: true,
                elevation: 1,
                backgroundColor: Colors.white,
                foregroundColor: Color(0xFF1E293B),
              ),
              scaffoldBackgroundColor: const Color(0xFFF8FAFC),
              extensions: [AppColors.light],
            ),
            darkTheme: ThemeData(
              brightness: Brightness.dark,
              colorScheme: const ColorScheme.dark(
                primary: Color(0xFF818CF8),
                secondary: Color(0xFF818CF8),
                surface: Color(0xFF1E293B),
              ),
              useMaterial3: true,
              appBarTheme: const AppBarTheme(
                centerTitle: true,
                elevation: 0,
                backgroundColor: Color(0xFF0F172A),
                foregroundColor: Color(0xFFF1F5F9),
              ),
              scaffoldBackgroundColor: const Color(0xFF0F172A),
              extensions: [AppColors.dark],
            ),
            initialRoute: '/onboarding',
            routes: {
              '/onboarding': (context) => const OnboardingScreen(),
              '/login': (context) => const LoginScreen(),
              '/home': (context) => const HomeScreen(),
              '/admin-home': (context) => const AdminHomeScreen(),
              '/medico-home': (context) => const MedicoHomeScreen(),
              '/evaluacion': (context) => const EvaluacionScreen(),
              '/resultado': (context) => const ResultadoScreen(),
              '/historial': (context) => const HistorialScreen(),
              '/perfil': (context) => const PerfilScreen(),
            },
          );
        },
      ),
    );
  }
}