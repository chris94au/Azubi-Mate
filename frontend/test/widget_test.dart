import 'package:flutter_test/flutter_test.dart';
import 'package:azubi_mate/main.dart';

void main() {
  testWidgets('App starts and shows welcome message', (WidgetTester tester) async {
    await tester.pumpWidget(const AzubiMateApp());

    expect(find.text('Azubi-Mate Dashboard'), findsOneWidget);
    expect(find.text('Willkommen bei Azubi-Mate!'), findsOneWidget);
  });
}