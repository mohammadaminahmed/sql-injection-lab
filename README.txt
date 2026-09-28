# SQL Injection Lab 🧪

مختبر تعليمي لفهم هجمات SQL Injection وطرق الحماية منها.

## المحتويات

- `vulnerable/app.py`: نسخة ضعيفة من تطبيق Flask (للتعلم).
- `secure/app_secure.py`: نسخة محمية باستخدام Prepared Statements.
- `detector.py`: أداة كشف الحقن.
- `extractor.py`: أداة استخراج البيانات.
- `blind_extractor.py`: أداة الاستخراج الأعمى.

## كيف يعمل؟

1. شغّل قاعدة البيانات MySQL.
2. شغّل `vulnerable/app.py` على المنفذ 5000.
3. شغّل `secure/app_secure.py` على المنفذ 5001.
4. جرب الاختراق على النسخة الضعيفة، وقارن مع النسخة المحمية.

## اختبار سريع

في حقل البحث اكتب:
