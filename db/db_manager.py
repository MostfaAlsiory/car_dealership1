from db.connection import get_db_connection
import pymysql
from flask import Flask, render_template, request, redirect, flash, session

def insert_record(table, data):
    """إضافة سجل إلى الجدول المحدد"""
    placeholders = ', '.join(['%s'] * len(data))
    columns = ', '.join(data.keys())
    sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    values = tuple(data.values())

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, values)
            connection.commit()
    finally:
        connection.close()

def update_record(table, data, where_clause):
    """تحديث سجل في الجدول المحدد"""
    set_clause = ', '.join([f"{key} = %s" for key in data.keys()])
    sql = f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    values = tuple(data.values())

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            print(f" sql:  {sql}")
            print(f" value:  {values}")
            print(f"{cursor.execute(sql, values)}")
 
            connection.commit()
           
    finally:
        connection.close()

def delete_record(table, where_clause):
    """حذف سجل من الجدول المحدد"""
    sql = f"DELETE FROM {table} WHERE {where_clause}"

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            connection.commit()
    finally:
        connection.close()

def fetch_records(table, where_clause=None):
    """استرجاع سجلات من الجدول المحدد"""
    sql = f"SELECT * FROM {table}"
    if where_clause:
        sql += f" WHERE {where_clause}"

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetchall()
    finally:
        connection.close()

def search_records(table, where_clause=None):
    
    """
    البحث عن سجلات في جدول معين بناءً على شروط محددة.
    :param table: اسم الجدول.
    :param where_clause: جملة شرطية لتحديد النتائج (اختياري).
    :return: قائمة من السجلات.
    """
    sql = f"SELECT * FROM {table}"
    if where_clause:
        sql += f" WHERE {where_clause}"

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        return results
    finally:
        connection.close()




def fetch_records_level(table, where_clause=None):



    """استرجاع سجلات من الجدول المحدد"""
    sql = f"SELECT  L_id , L_name from {table} WHERE L_id in (SELECT l_id FROM con_l_d  "
    if where_clause:
        sql += f" WHERE {where_clause})"
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return cursor.fetchall()
    finally:
        connection.close()       






def fetch_records_students(table, where_clause=None):



    """استرجاع سجلات من الجدول المحدد"""
    sql = f"SELECT S_id , S_name,S_phone FROM {table} WHERE S_id in (SELECT s_id FROM con_s_l "
    if where_clause:
        sql += f" WHERE {where_clause})"
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)
        return cursor.fetchall()
    finally:
        connection.close()       









def register_account(username,email,hashed_password):
    connection = get_db_connection()
    try:
            with connection.cursor() as cursor:
                # التحقق إذا كان المستخدم أو البريد الإلكتروني موجودًا
                check_sql = "SELECT * FROM users WHERE username = %s OR email = %s"
                cursor.execute(check_sql, (username, email))
                existing_user = cursor.fetchone()

                if existing_user:
                    flash("اسم المستخدم أو البريد الإلكتروني موجود بالفعل.", "warning")
                    return redirect('/register')

                # إضافة المستخدم الجديد إلى قاعدة البيانات
                insert_sql = "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)"
                cursor.execute(insert_sql, (username, email, hashed_password))
                connection.commit()
                flash("تم التسجيل بنجاح! يمكنك تسجيل الدخول الآن.", "success")
                return redirect('/login')
    except pymysql.MySQLError as e:

        flash("حدث خطأ أثناء التسجيل: " + str(e), "danger")


    '''
    لتسجيل الدخول بهذة الدالة يجب اتباع بعض التعديلات
    1- تعديل اسم الجدول للمستخدمين على حسب المشروع الهدف
    2- تغيير حقول التحقق
    3-تغيير الحقول المراد اضافتها بعد التحقق من عدم تكرارها 
    4- تغيير توجية الصفحات على حسب المشروع 
    
    
    '''
        







def db_insert_function(table_name, data):

    """
    دالة لإدخال البيانات في قاعدة البيانات وإرجاع المفتاح الرئيسي للسجل الجديد.
   
    Args:
        table_name (str): اسم الجدول.
        data (dict): قاموس يحتوي على أسماء الأعمدة والقيم.

    Returns:
        int: المفتاح الرئيسي للسجل الجديد.
    """
    connection=get_connection()
    try:
        with connection.cursor() as cursor:
            # بناء استعلام الإدخال
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['%s'] * len(data))
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
           
            # تنفيذ الاستعلام
            cursor.execute(query, list(data.values()))
           
            # حفظ التغييرات
            connection.commit()
           
            # الحصول على المفتاح الرئيسي للسجل الجديد
            return cursor.lastrowid
    except Exception as e:
        print(f"Database error: {str(e)}")
        return None
    finally:
        connection.close()





def db_fetch_images(table_name, conditions=None):
    """
    دالة عامة لاسترجاع الصور من قاعدة البيانات بناءً على شروط محددة.

    Args:
        table_name (str): اسم الجدول.
        conditions (dict, optional): قاموس يحتوي على أسماء الأعمدة والقيم للشروط.
                                     افتراضيًا يعيد جميع الصور.

    Returns:
        list: قائمة بالقيم المسترجعة أو قائمة فارغة إذا لم يوجد بيانات.
    """
    connection = get_connection()
    try:
        with connection.cursor(pymysql.cursors.DictCursor) as cursor:
            # بناء استعلام SELECT
            query = f"SELECT * FROM {table_name}"
            if conditions:
                condition_strings = [f"{col} = %s" for col in conditions.keys()]
                query += " WHERE " + " AND ".join(condition_strings)
                cursor.execute(query, list(conditions.values()))
            else:
                cursor.execute(query)

            # جلب جميع النتائج
            return cursor.fetchall()
    except Exception as e:
        print(f"Database error: {str(e)}")
        return []
    finally:
        connection.close()




