from flask import Flask, request
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
    <h2>🔍 بحث عن المستخدمين (نسخة ضعيفة)</h2>
    <form action="/search" method="GET">
        <input type="text" name="username" placeholder="اكتب اسم المستخدم">
        <button type="submit">بحث</button>
    </form>
    """

# صفحة البحث - هنا الضعف
@app.route('/search')
def search():
    username = request.args.get('username', '')
    
    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        # ⚠️⚠️⚠️ الكارثة: دمج المدخلات مباشرة في الاستعلام
        query = f"SELECT id, username, password, role FROM users WHERE username = '{username}'"
        
        print(f"\n📝 الاستعلام المنفذ: {query}\n")

        cursor.execute(query)
        results = cursor.fetchall()

        if results:
            html = f"<h3>نتائج البحث عن: {username}</h3>"
            html += "<table border='1' cellpadding='5'>"
            html += "<tr><th>ID</th><th>Username</th><th>Password</th><th>Role</th></tr>"
            for row in results:
                html += f"<tr><td>{row[0]}</td><td>{row[1]}</td><td>{row[2]}</td><td>{row[3]}</td></tr>"
            html += "</table>"
            html += "<br><a href='/'>رجوع</a>"
            return html
        else:
            return f"<h3>لا توجد نتائج لـ: {username}</h3><a href='/'>رجوع</a>"

    except Error as e:
        # ⚠️ إظهار تفاصيل الخطأ للمستخدم
        return f"<h3>خطأ في قاعدة البيانات:</h3><pre>{e}</pre><a href='/'>رجوع</a>"

    finally:
        if 'connection' in locals() and connection.is_connected():
            cursor.close()
            connection.close()

if __name__ == '__main__':
    app.run(debug=True, port=5000)