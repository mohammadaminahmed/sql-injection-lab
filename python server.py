import mysql.connector
from mysql.connector import Error

try:
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # ⚠️ غيرها لكلمة مرورك
        database="cybersecurity_lab7"
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # 1. حذف الجدول القديم بالكامل
        cursor.execute("DROP TABLE IF EXISTS users")
        print("🗑️ تم حذف الجدول القديم.")

        # 2. إنشاء جدول جديد نظيف
        cursor.execute("""
        CREATE TABLE users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            password VARCHAR(100) NOT NULL,
            role VARCHAR(50) NOT NULL
        )
        """)
        print("🆕 تم إنشاء جدول جديد.")

        # 3. إضافة المستخدمين مرة واحدة فقط
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('admin', 'SuperSecret123', 'admin')")
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('ahmed', 'password123', 'user')")
        cursor.execute("INSERT INTO users (username, password, role) VALUES ('sara', 'qwerty', 'user')")

        connection.commit()
        print("✅ تمت إعادة تعيين قاعدة البيانات بنجاح! لديك الآن 3 مستخدمين فقط.")

except Error as e:
    print(f"❌ حدث خطأ: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("🔒 تم إغلاق الاتصال.")