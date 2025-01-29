
import plotly.express as px
from flask import Flask, render_template, request, redirect, url_for, session,jsonify
import pymysql
import plotly.graph_objects as go
import plotly.io as pio

app = Flask(__name__)
app.secret_key = 'your_secret_key'






conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="car_dealership"
)
cursor = conn.cursor(pymysql.cursors.DictCursor)










def get_db_connection1():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='car_dealership',
        cursorclass=pymysql.cursors.DictCursor
    )


def get_db_connection():
    return pymysql.connect(
        host='localhost',
        user='root',
        password='',
        database='car_dealership',
        
    )

@app.route("/login")
def index():
    return render_template("admin/login.html")
    
# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        # Check username and password (this should be replaced with actual validation)
        if username == 'admin' and password == 'admin123':
            session['logged_in'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return 'Invalid credentials, please try again.'

    return render_template('admin/login.html')




@app.route('/admin')
def admin_dashboard():
    conn=get_db_connection()
    with conn.cursor() as cursor:


        cursor.execute('SELECT COUNT(*) FROM cars')
        num_cars = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM bookings')
        num_bookings = cursor.fetchone()[0]

        cursor.execute('SELECT COUNT(*) FROM reviews')
        num_reviews = cursor.fetchone()[0]

    # إعداد الرسم البياني مع جعل الحجم تلقائيًا
        fig = go.Figure(data=[
            go.Bar(name='السيارات', x=['السيارات'], y=[num_cars]),
            go.Bar(name='الحجوزات', x=['الحجوزات'], y=[num_bookings]),
            go.Bar(name='المراجعات', x=['المراجعات'], y=[num_reviews])
        ])

        fig.update_layout(
        title='إحصائيات لوحة التحكم',
        autosize=True,
        margin=dict(l=20, r=20, t=50, b=20),
        xaxis_title='الفئات',
        yaxis_title='العدد',
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
    )

    # تمرير الرسم البياني للواجهة الأمامية
        graph_html = pio.to_html(fig, full_html=False, config={'responsive': True})
        conn.close()

    

        return render_template('admin/dashboard.html', graph_html=graph_html, num_cars=num_cars, num_bookings=num_bookings, num_reviews=num_reviews)





@app.route('/get_bookings')
def get_bookings():
    conn1=get_db_connection1()

    with conn1.cursor() as cursor:

        cursor.execute("SELECT b.id, b.customer_name, c.model AS car_model, b.booking_date, b.status FROM bookings b JOIN cars c ON b.car_id = c.id")
        bookings = cursor.fetchall()
        conn1.close()
        print(bookings)

        return jsonify(bookings)



@app.route('/update_booking_status', methods=['POST'])
def update_booking_status():

    conn=get_db_connection()
  
    data = request.json
    with conn.cursor() as cursor:
        cursor.execute("UPDATE bookings SET status=%s WHERE id=%s", (data['status'], data['id']))
        conn.commit()
        conn.close()
        return jsonify({'message': 'تم التحديث بنجاح'})




@app.route('/get_cars')
def get_cars():

    conn=get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT id, brand, model, year, price, fuel_type, image_url, category FROM cars")
        result = cursor.fetchall()
        columns = [col[0] for col in cursor.description]  # استخراج أسماء الأعمدة
        cars = [dict(zip(columns, row)) for row in result]  # دمج القيم مع أسماء الأعمدة
        conn.close()
        return jsonify(cars)
    
  

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
        image_url = request.form['image_url']
        description = request.form['description']
        category = request.form['category']

        with conn.cursor() as cursor:
            sql = """INSERT INTO cars (brand, model, year, price, fuel_type, engine_power, fuel_efficiency, image_url, description, category) 
                     VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"""
            cursor.execute(sql, (brand, model, year, price, fuel_type, engine_power, fuel_efficiency, image_url, description, category))
            conn.commit()
            car_id = cursor.lastrowid  # 🔹 جلب ID السيارة المضافة حديثًا

        return jsonify({
            "success": True,
            "message": "🚀 تمت إضافة السيارة بنجاح!",
            "car": {
                "id": car_id,
                "brand": brand,
                "model": model,
                "year": year,
                "price": price,
                "fuel_type": fuel_type,
                "engine_power": engine_power,
                "fuel_efficiency": fuel_efficiency,
                "image_url": f"static/upload/{image_url}",
                "description": description,
                "category": category
            }
        })

    except Exception as e:
        return jsonify({"success": False, "message": f" X خطأ: {str(e)}"})

    finally:
        conn.close()

# حذف سيارة
@app.route('/delete_car/<int:car_id>', methods=['POST'])
def delete_car(car_id):
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = "DELETE FROM cars WHERE id = %s"
            cursor.execute(sql, (car_id,))
            if cursor.rowcount > 0:
                conn.commit()
                return jsonify({"success": True, "message": " تم حذف السيارة بنجاح!"})
            else:
                return jsonify({"success": False, "message": " السيارة غير موجودة!"})

    except Exception as e:
        return jsonify({"success": False, "message": f" خطأ: {str(e)}"})

    finally:
        conn.close()






# جلب بيانات سيارة محددة
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
            'description': car[9],
            'category': car[10]
        })
    return jsonify({'error': 'Car not found'}), 404

# تحديث بيانات السيارة
@app.route('/update_car/<int:car_id>', methods=['POST'])
def update_car(car_id):
    data = request.get_json()
    conn = get_db_connection()
    try:
        with conn.cursor() as cursor:
            sql = """UPDATE cars SET 
                    brand=%s, model=%s, year=%s, price=%s,
                    fuel_type=%s, engine_power=%s, fuel_efficiency=%s,
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
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM reviews")
            result = cursor.fetchall()

            columns = [col[0] for col in cursor.description]  # استخراج أسماء الأعمدة
            reviews = [dict(zip(columns, row)) for row in result]  # دمج القيم مع أسماء الأعمدة
            return jsonify(reviews)
    finally:
        connection.close()

@app.route('/add_review', methods=['POST'])
def add_review():
    data = request.json
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO reviews (car_id, user_name, rating, review_text, created_at) VALUES (%s, %s, %s, %s, NOW())",
                           (data['car_id'], data['user_name'], data['rating'], data['review_text']))
            connection.commit()
            return jsonify({'message': 'تمت الإضافة بنجاح!'})
    finally:
        connection.close()

@app.route('/delete_review/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("DELETE FROM reviews WHERE id = %s", (review_id,))
            connection.commit()
            return jsonify({'message': 'تم الحذف بنجاح!'})
    finally:
        connection.close()


   






























@app.route('/')
def home():
    cursor.execute("SELECT * FROM cars")
    featured_cars = cursor.fetchall()
    return render_template('home.html', featured_cars=featured_cars)



@app.route('/car/<int:car_id>')
def car_details(car_id):
    cursor.execute("SELECT * FROM cars WHERE id = %s", (car_id,))
    car = cursor.fetchone()
    
    cursor.execute("SELECT * FROM reviews WHERE car_id = %s", (car_id,))
    reviews = cursor.fetchall()
    
    return render_template('car_details.html', car=car, reviews=reviews)


@app.route('/compare')
def compare():
    car_ids = request.args.get('car_ids')
    
    if car_ids:
        ids_list = car_ids.split(',')
        placeholders = ','.join(['%s'] * len(ids_list))
        query = f"SELECT * FROM cars WHERE id IN ({placeholders})"
        cursor.execute(query, ids_list)
        cars = cursor.fetchall()
    else:
        cars = []

    return render_template('compare.html', cars=cars)



@app.route('/bookings')
def booking():
    return render_template("booking.html")

@app.route('/get_cars4', methods=['GET'])
def get_cars4():
    brand = request.args.get('brand', '').strip()
    max_price = request.args.get('max_price', '').strip()
    fuel_type = request.args.get('fuel_type', '').strip()
    sort_by = request.args.get('sort_by', 'price')  # الترتيب الافتراضي بالسعر
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

    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute(query, params)
    cars = cursor.fetchall()
    
    return jsonify(cars)


# معالجة إرسال الحجز
@app.route('/submit_review', methods=['POST'])
def submit_review():
    data = request.json
    cursor = conn.cursor()

    sql = """
        INSERT INTO reviews (car_id, user_name, rating, review_text, created_at)
        VALUES (%s, %s, %s, %s, NOW())
    """
    values = (data['car_id'], data['user_name'], data['rating'], data['review_text'])

    cursor.execute(sql, values)
    conn.commit()

    return jsonify({"message": "تم إرسال التقييم بنجاح!"})



@app.route('/reviews/<int:car_id>')
def reviews_page(car_id):
    cursor.execute("SELECT * FROM reviews WHERE car_id = %s", (car_id,))
    reviews = cursor.fetchall()

    cursor.execute("SELECT brand, model FROM cars WHERE id = %s", (car_id,))
    car = cursor.fetchone()

    return render_template('reviews.html', car=car, reviews=reviews, car_id=car_id)












if __name__ == '__main__':
    app.run(debug=True)






