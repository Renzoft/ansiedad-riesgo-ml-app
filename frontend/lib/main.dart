import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

// Services
import 'services/api_service.dart';

// ViewModels
import 'viewmodels/auth_viewmodel.dart';
import 'viewmodels/evaluacion_viewmodel.dart';

// Screens
import 'views/auth/login_screen.dart';

import 'views/home/home_screen.dart';
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
    // Instancia compartida de ApiService
    final apiService = ApiService();

    return MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (_) => AuthViewModel(apiService),
        ),
        ChangeNotifierProvider(
          create: (_) => EvaluacionViewModel(apiService),
        ),
      ],
      child: MaterialApp(
        title: 'Evaluación de Riesgo',
        debugShowCheckedModeBanner: false,
        theme: ThemeData(
          primarySwatch: Colors.indigo,
          useMaterial3: true,
          appBarTheme: const AppBarTheme(
            centerTitle: true,
            elevation: 1,
          ),
        ),
        initialRoute: '/login',
        routes: {
          '/login': (context) => const LoginScreen(),
          '/home': (context) => const HomeScreen(),
          '/evaluacion': (context) => const EvaluacionScreen(),
          '/resultado': (context) => const ResultadoScreen(),
          '/historial': (context) => const HistorialScreen(),
          '/perfil': (context) => const PerfilScreen(),
        },
      ),
    );
  }
}