// frontend/lib/screens/report_screen.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ReportScreen extends StatefulWidget {
  const ReportScreen({super.key});

  @override
  State<ReportScreen> createState() => _ReportScreenState();
}

class _ReportScreenState extends State<ReportScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _bulletController = TextEditingController();
  List<String> _bulletPoints = [];
  List<dynamic> _reports = [];
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadReports();
  }

  Future<void> _loadReports() async {
    try {
      final reports = await _apiService.listReports();
      setState(() {
        _reports = reports;
      });
    } catch (e) {
      // Handle error silently
    }
  }

  void _addBulletPoint() {
    if (_bulletController.text.trim().isNotEmpty) {
      setState(() {
        _bulletPoints.add(_bulletController.text.trim());
        _bulletController.clear();
      });
    }
  }

  Future<void> _generateReport() async {
    if (_bulletPoints.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Bitte mindestens einen Stichpunkt eingeben.')),
      );
      return;
    }

    setState(() {
      _isLoading = true;
    });

    try {
      await _apiService.generateReport({
        'report_type': 'wochenbericht',
        'bullet_points': _bulletPoints,
      });
      setState(() {
        _bulletPoints.clear();
      });
      await _loadReports();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Ausbildungsnachweis erfolgreich generiert!')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Fehler: $e')),
        );
      }
    } finally {
      setState(() {
        _isLoading = false;
      });
    }
  }

  Future<void> _confirmReport(String reportId) async {
    try {
      await _apiService.confirmReport(reportId);
      await _loadReports();
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Bericht bestätigt!')),
        );
      }
    } catch (e) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(content: Text('Fehler: $e')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Ausbildungsnachweise'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            const Text(
              'Neue Tätigkeiten als Stichpunkte eingeben:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _bulletController,
                    decoration: const InputDecoration(
                      hintText: 'z.B. API entwickelt',
                      border: OutlineInputBorder(),
                    ),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _addBulletPoint,
                  child: const Text('Hinzufügen'),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Wrap(
              spacing: 8.0,
              children: _bulletPoints
                  .map((bp) => Chip(
                        label: Text(bp),
                        onDeleted: () {
                          setState(() {
                            _bulletPoints.remove(bp);
                          });
                        },
                      ))
                  .toList(),
            ),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: _isLoading ? null : _generateReport,
              child: _isLoading
                  ? const CircularProgressIndicator(color: Colors.white)
                  : const Text('Bericht mit KI generieren'),
            ),
            const Divider(height: 32),
            const Text(
              'Vorhandene Berichte',
              style: TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 8),
            Expanded(
              child: _reports.isEmpty
                  ? const Center(child: Text('Keine Berichte vorhanden.'))
                  : ListView.builder(
                      itemCount: _reports.length,
                      itemBuilder: (context, index) {
                        final report = _reports[index];
                        return Card(
                          child: ListTile(
                            title: Text(report['title'] ?? 'Bericht'),
                            subtitle: Text('Typ: ${report['report_type']} | Status: ${report['status']}'),
                            trailing: report['status'] == 'draft'
                                ? IconButton(
                                    icon: const Icon(Icons.check, color: Colors.green),
                                    onPressed: () => _confirmReport(report['id']),
                                    tooltip: 'Bestätigen',
                                  )
                                : const Icon(Icons.verified, color: Colors.blue),
                          ),
                        );
                      },
                    ),
            ),
          ],
        ),
      ),
    );
  }
}