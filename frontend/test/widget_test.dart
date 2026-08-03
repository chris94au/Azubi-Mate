// frontend/test/widget_test.dart
import 'package:flutter_test/flutter_test.dart';
import 'package:azubi_mate/main.dart';

void main() {
  testWidgets('App starts and shows dashboard title', (WidgetTester tester) async {
    await tester.pumpWidget(const AzubiMateApp());

    expect(find.text('Azubi-Mate Dashboard'), findsOneWidget);
  });
}