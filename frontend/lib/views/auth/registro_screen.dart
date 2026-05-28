import 'package:flutter/material.dart';
import 'package:provider/provider.dart';
import '../../viewmodels/auth_viewmodel.dart';
import '../../widgets/custom_button.dart';
import '../../widgets/custom_textfield.dart';

class RegistroScreen extends StatefulWidget {
  const RegistroScreen({super.key});

  @override
  State<RegistroScreen> createState() => _RegistroScreenState();
}

class _RegistroScreenState extends State<RegistroScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nombreController = TextEditingController();
  final _correoController = TextEditingController();
  final _contrasenaController = TextEditingController();
  final _confirmarController = TextEditingController();
  final _facultadController = TextEditingController();
  final _cicloController = TextEditingController();
  bool _obscurePassword = true;

  @override
  void dispose() {
    _nombreController.dispose();
    _correoController.dispose();
    _contrasenaController.dispose();
    _confirmarController.dispose();
    _facultadController.dispose();
    _cicloController.dispose();
    super.dispose();
  }

  Future<void> _handleRegistro() async {
    if (!_formKey.currentState!.validate()) return;

    final authVM = context.read<AuthViewModel>();
    final success = await authVM.registrar(
      nombre: _nombreController.text.trim(),
      correo: _correoController.text.trim(),
      contrasena: _contrasenaController.text,
      facultad: _facultadController.text.trim(),
      ciclo: int.tryParse(_cicloController.text.trim()),
    );

    if (success && mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Registro exitoso. Ahora inicia sesión.'),
          backgroundColor: Colors.green,
        ),
      );
      Navigator.pop(context); // Regresa al login
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Registro')),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(24),
          child: Form(
            key: _formKey,
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                const Text(
                  'Crear cuenta',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
                const SizedBox(height: 24),

                CustomTextField(
                  controller: _nombreController,
                  label: 'Nombre completo',
                  hint: 'Ej: Juan Pérez',
                  prefixIcon: Icons.person_outlined,
                  validator: (v) =>
                      (v == null || v.trim().isEmpty) ? 'Ingrese su nombre' : null,
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _correoController,
                  label: 'Correo electrónico',
                  hint: 'ejemplo@correo.com',
                  keyboardType: TextInputType.emailAddress,
                  prefixIcon: Icons.email_outlined,
                  validator: (v) {
                    if (v == null || v.trim().isEmpty) return 'Ingrese su correo';
                    if (!v.contains('@')) return 'Correo inválido';
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _contrasenaController,
                  label: 'Contraseña',
                  hint: 'Mínimo 6 caracteres',
                  obscureText: _obscurePassword,
                  prefixIcon: Icons.lock_outlined,
                  suffixIcon: IconButton(
                    icon: Icon(_obscurePassword
                        ? Icons.visibility_off
                        : Icons.visibility),
                    onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                  ),
                  validator: (v) {
                    if (v == null || v.isEmpty) return 'Ingrese una contraseña';
                    if (v.length < 6) return 'Mínimo 6 caracteres';
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _confirmarController,
                  label: 'Confirmar contraseña',
                  obscureText: true,
                  prefixIcon: Icons.lock_outlined,
                  validator: (v) {
                    if (v != _contrasenaController.text) return 'Las contraseñas no coinciden';
                    return null;
                  },
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _facultadController,
                  label: 'Facultad (opcional)',
                  hint: 'Ej: Ingeniería',
                  prefixIcon: Icons.school_outlined,
                ),
                const SizedBox(height: 16),

                CustomTextField(
                  controller: _cicloController,
                  label: 'Ciclo (opcional)',
                  hint: 'Ej: 5',
                  keyboardType: TextInputType.number,
                  prefixIcon: Icons.numbers_outlined,
                ),
                const SizedBox(height: 24),

                Consumer<AuthViewModel>(
                  builder: (context, authVM, _) {
                    if (authVM.error != null) {
                      WidgetsBinding.instance.addPostFrameCallback((_) {
                        ScaffoldMessenger.of(context).showSnackBar(
                          SnackBar(
                            content: Text(authVM.error!),
                            backgroundColor: Colors.red,
                          ),
                        );
                        authVM.clearError();
                      });
                    }

                    return CustomButton(
                      text: 'Registrarse',
                      isLoading: authVM.isLoading,
                      onPressed: _handleRegistro,
                    );
                  },
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}