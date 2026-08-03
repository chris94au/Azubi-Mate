// frontend/lib/screens/exam_screen.dart
import 'package:flutter/material.dart';
import '../services/api_service.dart';

class ExamScreen extends StatefulWidget {
  const ExamScreen({super.key});

  @override
  State<ExamScreen> createState() => _ExamScreenState();
}

class _ExamScreenState extends State<ExamScreen> {
  final ApiService _apiService = ApiService();
  final TextEditingController _topicController = TextEditingController();
  Map<String, dynamic>? _activeSession;
  Map<String, dynamic>? _progress;
  int _currentQuestionIndex = 0;
  final TextEditingController _answerController = TextEditingController();
  bool _isLoading = false;

  @override
  void initState() {
    super.initState();
    _loadProgress();
  }

  Future<void> _loadProgress() async {
    try {
      final prog = await _apiService.getExamProgress();
      setState(() {
        _progress = prog;
      });
    } catch (e) {
      // Handle error
    }
  }

  Future<void> _generateExam() async {
    final topic = _topicController.text.trim().isEmpty ? 'Python Grundlagen' : _topicController.text.trim();
    setState(() {
      _isLoading = true;
    });

    try {
      final session = await _apiService.generateExam({
        'topic': topic,
        'question_type': 'multiple_choice',
        'count': 3,
      });
      setState(() {
        _activeSession = session;
        _currentQuestionIndex = 0;
        _answerController.clear();
      });
      await _loadProgress();
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

  Future<void> _submitAnswer(String questionId) async {
    if (_activeSession == null || _answerController.text.trim().isEmpty) return;

    try {
      final eval = await _apiService.submitExamAnswer(
        _activeSession!['session_id'],
        {
          'question_id': questionId,
          'answer': _answerController.text.trim(),
        },
      );

      if (mounted) {
        showDialog(
          context: context,
          builder: (context) => AlertDialog(
            title: Text(eval['correct'] ? 'Richtig!' : 'Falsch / Ausgewertet'),
            content: Text(eval['feedback'] ?? ''),
            actions: [
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                  setState(() {
                    _answerController.clear();
                    if (_currentQuestionIndex + 1 < (_activeSession!['questions'] as List).length) {
                      _currentQuestionIndex++;
                    } else {
                      _activeSession = null;
                      _loadProgress();
                    }
                  });
                },
                child: const Text('Weiter'),
              ),
            ],
          ),
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
        title: const Text('Prüfungstrainer'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            if (_progress != null)
              Card(
                child: Padding(
                  padding: const EdgeInsets.all(12.0),
                  child: Text(
                    'Statistik: Beantwortet: ${_progress!['total_answered']} | Richtig: ${_progress!['correct_answers']} | Schnitt: ${(_progress!['average_score'] * 100).toStringAsFixed(1)}%',
                    style: const TextStyle(fontWeight: FontWeight.bold),
                  ),
                ),
              ),
            const SizedBox(height: 16),
            if (_activeSession == null) ...[
              TextField(
                controller: _topicController,
                decoration: const InputDecoration(
                  labelText: 'Thema (z.B. Netzwerke, Python)',
                  border: OutlineInputBorder(),
                ),
              ),
              const SizedBox(height: 12),
              ElevatedButton(
                onPressed: _isLoading ? null : _generateExam,
                child: _isLoading
                    ? const CircularProgressIndicator(color: Colors.white)
                    : const Text('Prüfungssitzung starten'),
              ),
            ] else ...[
              Text(
                _activeSession!['title'],
                style: const TextStyle(fontSize: 18, fontWeight: FontWeight.bold),
              ),
              const SizedBox(height: 16),
              Builder(builder: (context) {
                final questions = _activeSession!['questions'] as List;
                if (_currentQuestionIndex >= questions.length) {
                  return const Text('Sitzung beendet!');
                }
                final q = questions[_currentQuestionIndex];
                final options = (q['options'] as List?) ?? [];

                return Card(
                  child: Padding(
                    padding: const EdgeInsets.all(16.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        Text(
                          'Frage ${_currentQuestionIndex + 1} von ${questions.length}',
                          style: const TextStyle(color: Colors.grey),
                        ),
                        const SizedBox(height: 8),
                        Text(
                          q['question_text'],
                          style: const TextStyle(fontSize: 16, fontWeight: FontWeight.bold),
                        ),
                        const SizedBox(height: 12),
                        if (options.isNotEmpty) ...[
                          const Text('Optionen:', style: TextStyle(fontWeight: FontWeight.bold)),
                          ...options.map<Widget>((opt) => RadioListTile<String>(
                                title: Text(opt),
                                value: opt,
                                groupValue: _answerController.text,
                                onChanged: (val) {
                                  setState(() {
                                    _answerController.text = val!;
                                  });
                                },
                              )),
                        ],
                        const SizedBox(height: 12),
                        TextField(
                          controller: _answerController,
                          decoration: const InputDecoration(
                            labelText: 'Deine Antwort eingeben oder auswählen',
                            border: OutlineInputBorder(),
                          ),
                        ),
                        const SizedBox(height: 16),
                        ElevatedButton(
                          onPressed: () => _submitAnswer(q['id']),
                          child: const Text('Antwort einreichen'),
                        ),
                      ],
                    ),
                  ),
                );
              }),
            ],
          ],
        ),
      ),
    );
  }
}