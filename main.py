from flask import Flask, render_template,request,jsonify
import pymysql

app = Flask(__name__)

# الاتصال بقاعدة البيانات
conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="car_dealership"
)
cursor = conn.cursor(pymysql.cursors.DictCursor)

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

@app.route('/get_cars', methods=['GET'])
def get_cars():
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




