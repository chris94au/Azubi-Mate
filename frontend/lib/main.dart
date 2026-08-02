import 'package:flutter/material.dart';

void main() {
  runApp(const AzubiMateApp());
}

class AzubiMateApp extends StatelessWidget {
  const AzubiMateApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Azubi-Mate',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: const Color(0xFF0D47A1)),
        useMaterial3: true,
      ),
      home: const DashboardScreen(),
    );
  }
}

class DashboardScreen extends StatelessWidget {
  const DashboardScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Azubi-Mate Dashboard'),
      ),
      body: const Center(
        child: Text('Willkommen bei Azubi-Mate!'),
      ),
    );
  }
}