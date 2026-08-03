// frontend/lib/screens/learning_screen.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class LearningScreen extends StatefulWidget {
  const LearningScreen({super.key});

  @override
  State<LearningScreen> createState() => _LearningScreenState();
}

class _LearningScreenState extends State<LearningScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _professionController = TextEditingController();
  final TextEditingController _weaknessController = TextEditingController();
  List<dynamic> _plans = [];
  Map<String, dynamic>? _activePlan;
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadPlans();
  }

  Future<void> _loadPlans() async {
    try {
      final plans = await _apiService.listLearningPlans();
      setState(() {
        _plans = plans;
      });
    } catch (e) {
      // Handle error
    }
  }

  Future<void> _generatePlan() async {
    setState(() {
      _isLoading = true;
    });

    try {
      final plan = await _apiService.generateLearningPlan({
        'profession': _professionController.text.trim().isEmpty ? 'Fachinformatiker' : _professionController.text.trim(),
        'weaknesses': [_weaknessController.text.trim().isEmpty ? 'Datenbanken' : _weaknessController.text.trim()],
      });
      setState(() {
        _activePlan = plan;
      });
      await _loadPlans();
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

  Future<void> _updateProgress(String topic, String status) async {
    if (_activePlan == null) return;

    try {
      await _apiService.updateLearningProgress({
        'plan_id': _activePlan!['plan_id'],
        'topic': topic,
        'status': status,
      });
      final plans = await _apiService.listLearningPlans();
      final updated = plans.firstWhere((p) => p['plan_id'] == _activePlan!['plan_id'], orElse: () => _activePlan);
      setState(() {
        _activePlan = updated;
        _plans = plans;
      });
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
        title: const Text('Lernpläne & Schwächenanalyse'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (_activePlan == null) ...[
              TextField(
                controller: _professionController,
                decoration: const InputDecoration(
                  labelText: 'Ausbildungsberuf (z.B. Fachinformatiker)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 12),
              TextField(
                controller: _weaknessController,
                decoration: const InputDecoration(
                  labelText: 'Hauptschwäche (z.B. SQL, Netzwerke)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 12),
              ElevatedButton(
                onPressed: _isLoading ? null : _generatePlan,
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('Individuellen Lernplan generieren'),
              ),
              const Divider(height: 32),
              const Text('Vorhandene Lernpläne', style: TextStyle(fontWeight: FontWeight.bold)),
              Expanded(
                child: ListView.builder(
                  itemCount: _plans.length,
                  itemBuilder: (context, index) {
                    final p = _plans[index];
                    return ListTile(
                      title: Text(p['title']),
                      subtitle: Text(p['summary'] ?? ''),
                      onTap: () {
                        setState(() {
                          _activePlan = p;
                        });
                      },
                    );
                  },
                ),
              ),
            ] else ...[
              Row(
                mainAxisAlignment: MainAxisAlignment.between,
                children: [
                  Text(_activePlan!['title'], style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold)),
                  TextButton(
                    onPressed: () {
                      setState(() {
                        _activePlan = null;
                      });
                    },
                    child: const Text('Zurück'),
                  ),
                ],
              ),
              const SizedBox(height: 8),
              Text(_activePlan!['summary'] ?? ''),
              const SizedBox(height: 16),
              const Text('Themen & Aktionen:', style: TextStyle(fontWeight: FontWeight.bold)),
              const SizedBox(height: 8),
              Expanded(
                child: ListView(
                  children: ((_activePlan!['items'] as List?) ?? []).map<Widget>((item) {
                    return Card(
                      child: ListTile(
                        title: Text(item['topic']),
                        subtitle: Text('Priorität: ${item['priority']} | Status: ${item['status']}'),
                        trailing: PopupMenuButton<String>(
                          onSelected: (status) => _updateProgress(item['topic'], status),
                          itemBuilder: (context) => [
                            const PopupMenuItem(value: 'open', child: Text('Offen')),
                            const PopupMenuItem(value: 'in_progress', child: Text('In Bearbeitung')),
                            const PopupMenuItem(value: 'completed', child: Text('Erledigt')),
                          ],
                        ),
                      ),
                    );
                  }).toList(),
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}