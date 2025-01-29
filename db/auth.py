

import hashlib
import pymysql
from flask import session, flash
from db.connection import get_db_connection
# إعداد الاتصال بقاعدة البيانات

def hash_password(password):
    """تشفير كلمة المرور باستخدام SHA256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(employee_id,username, password_hash, role):
    """تسجيل مستخدم جديد."""
    
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # التحقق من وجود المستخدم أو البريد الإلكتروني
            check_sql = "SELECT * FROM users WHERE username = %s "
            cursor.execute(check_sql, (username))
            existing_user = cursor.fetchone()

            if existing_user:
                return False, "اسم المستخدم أو البريد الإلكتروني موجود بالفعل."

            # إدخال المستخدم الجديد
            insert_sql = "INSERT INTO users ( employee_id, username, password_hash, role ) VALUES  (%s, %s, %s,%s)"
            cursor.execute(insert_sql, (employee_id,username, password_hash,role))
            connection.commit()
            return True, "تم التسجيل بنجاح! يمكنك تسجيل الدخول الآن."
    except pymysql.MySQLError as e:
        return False, f"حدث خطأ أثناء التسجيل: {str(e)}"

def login_user(username, password):
    """تسجيل الدخول."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            # التحقق من المستخدم بالبريد الإلكتروني
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username))
            user = cursor.fetchone()


            if user and user["password_hash"] == password:  # user[3] هو الحقل الذي يحتوي على كلمة المرور
                session['user_id'] = user["user_id"]
                session['username'] = user["username"]
                session['role'] = user['role']
               
                return True, "تم تسجيل الدخول بنجاح!"
            else:
                return False, "البريد الإلكتروني أو كلمة المرور غير صحيحة."
    except pymysql.MySQLError as e:
        return False, f"حدث خطأ أثناء تسجيل الدخول: {str(e)}"

def get_user_profile(user_id):
    """جلب بيانات الملف الشخصي."""
    try:
        connection = get_db_connection()
        with connection.cursor() as cursor:
            sql = "SELECT * FROM users WHERE user_id = %s"
            cursor.execute(sql, (user_id,))
            return cursor.fetchone()
    except pymysql.MySQLError as e:
        return None, f"حدث خطأ أثناء جلب البيانات: {str(e)}"

def logout_user():
    """تسجيل الخروج."""
    session.clear()

