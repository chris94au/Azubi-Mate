// frontend/lib/services/api_service.dart
import 'dart:convert';
import 'package:http/http.dart' as http;

class ApiService {
  final String baseUrl;

  ApiService({this.baseUrl = 'http://localhost:8000/api/v1'});

  Future<Map<String, dynamic>> getStatus() async {
    final response = await http.get(Uri.parse('$baseUrl/status'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to load status');
  }

  Future<Map<String, dynamic>> generateReport(Map<String, dynamic> requestData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/reports/generate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to generate report: ${response.body}');
  }

  Future<Map<String, dynamic>> confirmReport(String reportId) async {
    final response = await http.post(Uri.parse('$baseUrl/reports/$reportId/confirm'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to confirm report');
  }

  Future<List<dynamic>> listReports() async {
    final response = await http.get(Uri.parse('$baseUrl/reports'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to list reports');
  }

  Future<Map<String, dynamic>> generateExam(Map<String, dynamic> requestData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/exams/generate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to generate exam');
  }

  Future<Map<String, dynamic>> submitExamAnswer(String sessionId, Map<String, dynamic> submissionData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/exams/$sessionId/submit'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(submissionData),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to submit exam answer');
  }

  Future<Map<String, dynamic>> getExamProgress() async {
    final response = await http.get(Uri.parse('$baseUrl/exams/progress'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to load exam progress');
  }

  Future<Map<String, dynamic>> generateLearningPlan(Map<String, dynamic> requestData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/learning/plans/generate'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(requestData),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to generate learning plan');
  }

  Future<Map<String, dynamic>> updateLearningProgress(Map<String, dynamic> updateData) async {
    final response = await http.post(
      Uri.parse('$baseUrl/learning/progress'),
      headers: {'Content-Type': 'application/json'},
      body: jsonEncode(updateData),
    );
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to update learning progress');
  }

  Future<List<dynamic>> listLearningPlans() async {
    final response = await http.get(Uri.parse('$baseUrl/learning/plans'));
    if (response.statusCode == 200) {
      return jsonDecode(response.body);
    }
    throw Exception('Failed to list learning plans');
  }
}