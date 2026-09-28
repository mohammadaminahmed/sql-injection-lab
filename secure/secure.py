from flask import Flask, request
from markupsafe import escape
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)

# دالة الاتصال بقاعدة البيانات
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="cybersecurity_lab7"
    )

# الصفحة الرئيسية
@app.route('/')
def home():
    return """
    <h2>🔍 بحث عن المستخدمين (نسخة محمية)</h2>
    <form action="/search" method="GET">
        <input type="text" name="username" placeholder="اكتب اسم المستخدم">
        <button type="submit">بحث</button>
    </form>
    """

# صفحة البحث - هنا الحماية
@app.route('/search')
def search():
    username = request.args.get('username', '')
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # ✅✅✅ الحماية: Prepared Statement
        query = "SELECT id, username, password, role FROM users WHERE username = %s"
        
        print(f"\n📝 الاستعلام المنفذ: {query}")
        print(f"📦 القيمة المرسلة منفصلة: {username}\n")

        cursor.execute(query, (username,))
        results = cursor.fetchall()

        if results:
            # ✅ تنظيف المدخلات قبل عرضها في HTML (حماية من XSS)
            safe_username = escape(username)
            html = f"<h3>نتائج البحث عن: {safe_username}</h3>"
            html += "<table border='1' cellpadding='5'>"
            html += "<tr><th>ID</th><th>Username</th><th>Password</th><th>Role</th></tr>"
            for row in results:
                html += f"<tr><td>{row[0]}</td><td>{escape(str(row[1]))}</td><td>***</td><td>{escape(str(row[3]))}</td></tr>"
            html += "</table>"
            html += "<br><a href='/'>رجوع</a>"
            return html
        else:
            return f"<h3>لا توجد نتائج</h3><a href='/'>رجوع</a>"

    except Error as e:
        # ✅ لا نكشف تفاصيل الخطأ
        print(f"⚠️ خطأ داخلي: {e}")  # يظهر في الشاشة السوداء فقط
        return f"<h3>حدث خطأ في المعالجة، حاول لاحقًا</h3><a href='/'>رجوع</a>"

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5001)