import plotly.graph_objects as go
import plotly.io as pio
import plotly.express as px
from flask import Flask, render_template, request, redirect, url_for, session, jsonify, flash, send_from_directory
import psycopg2
import os
from werkzeug.utils import secure_filename
import cloudinary
import cloudinary.uploader
import cloudinary.api

app = Flask(__name__)
app.secret_key = 'your_secret_key'
UPLOAD_FOLDER = 'static/upload'


# تهيئة Cloudinary
cloudinary.config(
    cloud_name="due2rm5cb",  # استبدل بـ cloud_name الخاص بك
    api_key="494883843628169",        # استبدل بـ api_key الخاص بك
    api_secret="TnEHyxax7uSePlBh4EwS8QjJdBs"   # استبدل بـ api_secret الخاص بك
)

# مجلد مؤقت لحفظ الصور المرفوعة (اختياري، يمكن حذفه إذا لم يكن مطلوبًا)
UPLOAD_FOLDER = 'static/upload'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# التحقق من الامتداد المسموح به
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# تعديل الاتصال بقاعدة البيانات لاستخدام PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        host="dpg-cv1obhtsvqrc738pkmh0-a.oregon-postgres.render.com",
        dbname="car_dealership_tgov",  # اسم قاعدة البيانات
        user="car_dealership_tgov_user",  # اسم المستخدم
        password="MLk96kZaKtjJR60PlOnlfmiDDgO25y5s",  # كلمة المرور
        port="5432"  # أو رقم المنفذ الذي تستخدمه
    )
    return conn

def get_db_connection1():
    conn = psycopg2.connect(host="localhost", dbname="car_dealership", user="postgres", password="root", port="5432")
    return conn

@app.after_request
def add_header(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

def login_user(username, password):
    """تسجيل الدخول."""
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            # التحقق من المستخدم بالاسم
            sql = "SELECT * FROM users WHERE username = %s"
            cursor.execute(sql, (username,))
            user = cursor.fetchone()
            if user and user[3] == password:  # user[3] هو الحقل الذي يحتوي على كلمة المرور
                session['id'] = user[0]
                session['username'] = user[1]
                return True, "تم تسجيل الدخول بنجاح!"
            else:
                return False, "البريد الإلكتروني أو كلمة المرور غير صحيحة."
    except Exception as e:
        return False, f"حدث خطأ أثناء تسجيل الدخول: {str(e)}"

@app.route('/sitemap.xml')
def sitemap():
    return send_from_directory('.', 'sitemap.xml')

@app.route('/robots.txt')
def robots():
    return Response("User-agent: *\nDisallow:", mimetype="text/plain")

@app.route('/')
def home():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM cars")
        featured_cars = cursor.fetchall()
    conn.close()
    return render_template('home.html', featured_cars=featured_cars)

@app.route('/car/<int:car_id>')
def car_details(car_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        cursor.execute("SELECT * FROM reviews WHERE car_id = %s", (car_id,))
        reviews = cursor.fetchall()
    conn.close()
    return render_template('car_details.html', car=car, reviews=reviews)

@app.route('/compare')
def compare():
    car_ids = request.args.get('car_ids')
    if car_ids:
        try:
            ids_list = tuple(map(int, car_ids.split(',')))  # تحويل القيم إلى أعداد صحيحة
            placeholders = ','.join(['%s'] * len(ids_list))
            query = f"SELECT id, brand, model, price, engine_power, fuel_efficiency FROM cars WHERE id IN ({placeholders})"
            conn = get_db_connection()
            with conn.cursor() as cursor:
                cursor.execute(query, ids_list)
                cars = cursor.fetchall()
            conn.close()
            car_list = []
            for car in cars:
                car_dict = {
                    "id": car[0],
                    "brand": car[1],
                    "model": car[2],
                    "price": car[3],
                    "engine_power": car[4],
                    "fuel_efficiency": car[5]
                }
                car_list.append(car_dict)
        except Exception as e:
            print(f"خطأ أثناء جلب البيانات: {e}")
            car_list = []
    else:
        car_list = []
    return render_template('compare.html', cars=car_list)

@app.route('/bookings')
def booking():
    car_id = request.args.get("car_id")
    car_name = request.args.get("car_name")
    return render_template("booking.html", car_id=car_id, car_name=car_name)

@app.route('/get_cars4', methods=['GET'])
def get_cars4():
    brand = request.args.get('brand', '').strip()
    max_price = request.args.get('max_price', '').strip()
    fuel_type = request.args.get('fuel_type', '').strip()
    sort_by = request.args.get('sort_by', 'price')  # الترتيب الافتراضي
    sort_order = request.args.get('sort_order', 'asc')  # الترتيب تصاعدي افتراضيًا
    query = "SELECT id, brand, model, year, price, fuel_type, image_url FROM cars WHERE 1=1"
    params = []
    if brand:
        query += " AND brand LIKE %s"
        params.append(f"%{brand}%")
    if max_price:
        query += " AND price <= %s"
        params.append(max_price)
    if fuel_type:
        query += " AND fuel_type = %s"
        params.append(fuel_type)
    if sort_by in ['price', 'year']:
        query += f" ORDER BY {sort_by} {sort_order}"
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    rows = cursor.fetchall()
    cars = []
    for row in rows:
        car = {
            'id': row[0],
            'brand': row[1],
            'model': row[2],
            'year': row[3],
            'price': row[4],
            'fuel_type': row[5],
            'image_url': row[6]
        }
        cars.append(car)
    cursor.close()
    conn.close()
    return jsonify(cars)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    try:
        data = request.json
        if not all(k in data for k in ('car_id', 'user_name', 'rating', 'review_text')):
            return jsonify({"success": False, "message": "بيانات غير مكتملة"}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        sql = """
            INSERT INTO reviews (car_id, user_name, rating, review_text, created_at)
            VALUES (%s, %s, %s, %s, NOW())
            RETURNING id, car_id, user_name, rating, review_text, created_at
        """
        cursor.execute(sql, (data['car_id'], data['user_name'], data['rating'], data['review_text']))
        review = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({
            "success": True,
            "message": "تم إرسال التقييم بنجاح!",
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"حدث خطأ: {str(e)}"}), 500

@app.route('/reviews/<int:car_id>')
def reviews_page(car_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id, user_name, rating, review_text, created_at FROM reviews WHERE car_id = %s", (car_id,))
        reviews = cursor.fetchall()
        cursor.execute("SELECT brand, model FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
        if not car:
            return "السيارة غير موجودة!", 404
        return render_template('reviews.html', car=car, reviews=reviews, car_id=car_id)
    except Exception as e:
        return f"حدث خطأ: {str(e)}", 500
    finally:
        cursor.close()
        conn.close()

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    sql = """
        INSERT INTO bookings (customer_name, customer_email, phone_number, car_id, booking_date, booking_time, status, created_at)
        VALUES (%s, %s, %s, %s, %s, %s, 'pending', NOW())
    """
    values = (
        data['customer_name'],
        data['customer_email'],
        data['phone_number'],
        data['car_id'],
        data['booking_date'],
        data['booking_time']
    )
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    return jsonify({"message": "تم حجز السيارة بنجاح!"})

@app.route("/login_page")
def login_page():
    return render_template("admin/login.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        success, message = login_user(username, password)
        flash(message, "success" if success else "danger")
        return redirect('/admin' if success else '/login')
    return render_template('admin/login.html')

@app.route('/admin')
def admin_dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('SELECT COUNT(*) FROM cars')
        num_cars = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM bookings')
        num_bookings = cursor.fetchone()[0]
        cursor.execute('SELECT COUNT(*) FROM reviews')
        num_reviews = cursor.fetchone()[0]
    conn.close()
    return render_template('admin/dashboard.html', num_cars=num_cars, num_bookings=num_bookings, num_reviews=num_reviews)

@app.route('/get_bookings')
def get_bookings():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT bookings.id, bookings.customer_name, cars.brand, cars.model, bookings.customer_email, bookings.phone_number, bookings.booking_date, bookings.status
            FROM bookings
            JOIN cars ON bookings.car_id = cars.id
        """)
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        bookings = [dict(zip(columns, row)) for row in result]
        conn.close()
        return jsonify(bookings)

@app.route('/update_booking_status', methods=['POST'])
def update_booking_status():
    conn = get_db_connection()
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("UPDATE bookings SET status=%s WHERE id=%s", (data['status'], data['id']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Booking status updated successfully'})

@app.route('/get_cars')
def get_cars():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, brand, model, year, price, fuel_type, image_url, category FROM cars")
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        cars = [dict(zip(columns, row)) for row in result]
        conn.close()
        return jsonify(cars)

@app.route('/upload_image', methods=['POST'])
def upload_image():
    if 'image' not in request.files:
        return jsonify({"success": False, "message": "لا توجد صورة مرفوعة"})
    file = request.files['image']
    if file.filename == '':
        return jsonify({"success": False, "message": "يجب اختيار صورة"})
    if file and allowed_file(file.filename):
        # رفع الصورة إلى Cloudinary
        response = cloudinary.uploader.upload(file)
        image_url = response['secure_url']  # الحصول على رابط الصورة
        return jsonify({"success": True, "image_url": image_url})
    return jsonify({"success": False, "message": "صيغة الملف غير مدعومة"})

@app.route('/add_car', methods=['POST'])
def add_car():
    conn = get_db_connection()
    try:
        brand = request.form['brand']
        model = request.form['model']
        year = request.form['year']
        price = request.form['price']
        fuel_type = request.form['fuel_type']
        engine_power = request.form['engine_power']
        fuel_efficiency = request.form['fuel_efficiency']
        image_url = request.form.get('image_url', '')  # رابط الصورة من Cloudinary
        description = request.form['description']
        category = request.form['category']
        with conn.cursor() as cursor:
            sql = """INSERT INTO cars (brand, model, year, price, fuel_type, engine_power, fuel_efficiency, image_url, description, category) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s) RETURNING id"""
            cursor.execute(sql, (brand, model, year, price, fuel_type, engine_power, fuel_efficiency, image_url, description, category))
            car_id = cursor.fetchone()[0]
            conn.commit()
        return jsonify({
            "success": True,
            "message": "تمت إضافة السيارة بنجاح!",
            "car": {
                "id": car_id,
                "brand": brand,
                "model": model,
                "year": year,
                "price": price,
                "fuel_type": fuel_type,
                "engine_power": engine_power,
                "fuel_efficiency": fuel_efficiency,
                "image_url": image_url,
                "description": description,
                "category": category
            }
        })
    except Exception as e:
        return jsonify({"success": False, "message": f"حدث خطأ: {str(e)}"})
    finally:
        conn.close()

@app.route('/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM cars WHERE id = %s"
            cursor.execute(sql, (car_id,))
            if cursor.rowcount > 0:
                conn.commit()
                return jsonify({"success": True, "message": "Car deleted successfully!"})
            else:
                return jsonify({"success": False, "message": "Car not found!"})
    except Exception as e:
        return jsonify({"success": False, "message": f"Error: {str(e)}"})
    finally:
        conn.close()

@app.route('/get_car1/<int:car_id>')
def get_car1(car_id):
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
        car = cursor.fetchone()
    conn.close()
    if car:
        return jsonify({
            'id': car[0],
            'brand': car[1],
            'model': car[2],
            'year': car[3],
            'price': car[4],
            'fuel_type': car[5],
            'engine_power': car[6],
            'fuel_efficiency': car[7],
            'image_url': car[8],
            'description': car[10],
            'category': car[11]
        })
    return jsonify({'error': 'Car not found'}), 404

@app.route('/update_car/<int:car_id>', methods=['POST'])
def update_car(car_id):
    data = request.get_json()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """UPDATE cars SET 
                    brand=%s, model=%s, year=%s, price=%s,
                    fuel_type=%s, engine_power=%s, fuel_efficiency=%s, image_url=%s,
                    description=%s, category=%s
                    WHERE id=%s"""
            cursor.execute(sql, (
                data['brand'],
                data['model'],
                data['year'],
                data['price'],
                data['fuel_type'],
                data['engine_power'],
                data['fuel_efficiency'],
                data['image_url'],
                data['description'],
                data['category'],
                car_id
            ))
            conn.commit()
        return jsonify({'success': True})
    except Exception as e:
        print(e)
        return jsonify({'success': False}), 500
    finally:
        conn.close()



@app.route('/get_reviews')
def get_reviews():
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM reviews")
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]
        reviews = [dict(zip(columns, row)) for row in result]
        conn.close()
        return jsonify(reviews)


@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO reviews (car_id, user_name, rating, review_text, created_at) VALUES (%s, %s, %s, %s, NOW())",
                           (data['car_id'], data['user_name'], data['rating'], data['review_text']))
            conn.commit()
            return jsonify({'message': 'Review added successfully!'})
    finally:
        conn.close()



@app.route('/delete_review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
            conn.commit()
            return jsonify({'message': 'Review deleted successfully!'})
    finally:
        conn.close()

@app.route('/call')
def call():
    return render_template("call.html")

# تسجيل الخروج
@app.route('/logout')
def logout():

    session.clear()
    flash("تم تسجيل الخروج بنجاح.", "info")
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True)




