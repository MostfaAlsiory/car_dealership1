function deleteCar(carId) {
    if (!confirm("⚠️ هل أنت متأكد من أنك تريد حذف هذه السيارة؟")) return;

    fetch(`/delete_car/${carId}`, {
        method: "POST"
    })
        .then(response => response.json())
        .then(data => {
            console.log("📡 Response:", data); // ✅ طباعة الاستجابة في الكونسول

            let messageBox = document.getElementById("message-box");
            messageBox.textContent = data.message;
            messageBox.style.display = "block";
            messageBox.style.color = data.success ? "green" : "red";
            messageBox.style.border = data.success ? "2px solid green" : "2px solid red";
            messageBox.style.backgroundColor = data.success ? "#d4edda" : "#f8d7da";

            if (data.success) {
                fetchCars(); // ✅ تحديث الجدول مباشرة بعد الحذف
            }
        })
        .catch(error => console.error("❌ خطأ أثناء الحذف:", error));
}





function editCar(id) {
    fetch(`/get_car1/${id}`)
        .then(response => response.json())
        .then(car => {
            // ملء جميع الحقول
            document.getElementById('edit-car-id').value = car.id;
            document.getElementById('edit-brand').value = car.brand;
            document.getElementById('edit-model').value = car.model;
            document.getElementById('edit-year').value = car.year;
            document.getElementById('edit-price').value = car.price;
            document.getElementById('edit-fuel_type').value = car.fuel_type;
            document.getElementById('edit-engine_power').value = car.engine_power;
            document.getElementById('edit-fuel_efficiency').value = car.fuel_efficiency;
            document.getElementById('edit-image_url').value = car.image_url;
            document.getElementById('edit-description').value = car.description;
            document.getElementById('edit-category').value = car.category;

            // إظهار النموذج
            document.getElementById('edit-form-container').style.display = 'flex';
        })
        .catch(error => console.error('Error:', error));
}

document.getElementById('edit-car-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const carData = {
        id: document.getElementById('edit-car-id').value,
        brand: document.getElementById('edit-brand').value,
        model: document.getElementById('edit-model').value,
        year: document.getElementById('edit-year').value,
        price: document.getElementById('edit-price').value,
        fuel_type: document.getElementById('edit-fuel_type').value,
        engine_power: document.getElementById('edit-engine_power').value,
        fuel_efficiency: document.getElementById('edit-fuel_efficiency').value,
        image_url: document.getElementById('edit-image_url').value,
        description: document.getElementById('edit-description').value,
        category: document.getElementById('edit-category').value
    };

    fetch(`/update_car/${carData.id}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(carData)
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                alert("تم التعديل بنجاح");
                fetchCars();
                cancelEdit();
            } else {
                alert("فشل في التعديل");
            }
        })
        .catch(error => console.error('Error:', error));
});

// إلغاء التعديل
function cancelEdit() {
    document.getElementById('edit-form-container').style.display = 'none';
}

// إرسال التعديل
document.getElementById('edit-car-form').addEventListener('submit', function (e) {
    e.preventDefault();

    const carId = document.getElementById('edit-car-id').value;
    const brand = document.getElementById('edit-brand').value;
    const model = document.getElementById('edit-model').value;
    const year = document.getElementById('edit-year').value;
    const price = document.getElementById('edit-price').value;

    fetch(`/update_car/${carId}`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ brand, model, year, price })
    })
        .then(response => response.json())
        .then(result => {
            if (result.success) {
                alert("تم التعديل بنجاح");
                fetchCars();
                cancelEdit();
            } else {
                alert("فشل التعديل");
            }
        });
});

// جلب السيارات عند تحميل الصفحة
async function fetchCars() {
    const tableBody = document.getElementById('car-list');
    tableBody.innerHTML = ''; // 🔹 تفريغ الجدول قبل التحديث

    fetch('/get_cars')
        .then(response => response.json())
        .then(cars => {
            cars.forEach(car => {
                const row = `
                    <tr>
                        <td>${car.brand}</td>
                        <td>${car.model}</td>
                        <td>${car.year}</td>
                        <td>${car.price} $</td>
                        <td><img src="static/upload/${car.image_url}" class="car-image" alt="Car Image"></td>
                        <td>
                            <button onclick="editCar(${car.id})">تعديل</button>
                            <button onclick="deleteCar(${car.id})" class="delete-btn">حذف</button>
                        </td>
                    </tr>
                `;
                tableBody.innerHTML += row;
            });
        })
        .catch(error => console.error("❌ خطأ في جلب السيارات:", error));
}
fetchCars();




document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("car-form").addEventListener("submit", function (event) {
        event.preventDefault(); // 🔴 منع إعادة تحميل الصفحة

        let formData = new FormData(this); // 🔹 جمع بيانات النموذج

        fetch("/add_car", {
            method: "POST",
            body: formData
        })
            .then(response => response.json()) // 🔹 تحويل الاستجابة إلى JSON
            .then(data => {
                console.log("📡 Response:", data); // ✅ طباعة الاستجابة في الكونسول

                let messageBox = document.getElementById("message-box");
                messageBox.textContent = data.message;
                messageBox.style.display = "block";
                messageBox.style.color = data.success ? "green" : "red";
                messageBox.style.border = data.success ? "2px solid green" : "2px solid red";
                messageBox.style.backgroundColor = data.success ? "#d4edda" : "#f8d7da";

                if (data.success) {
                    document.getElementById("car-form").reset(); // 🔹 إعادة تعيين النموذج
                    fetchCars(); // ✅ تحديث الجدول مباشرة بعد الإضافة
                }
            })
            .catch(error => console.error("❌ خطأ أثناء الإرسال:", error));
    });

    // ✅ تحميل السيارات عند فتح الصفحة
    fetchCars();
});
// التحكم في الشريط الجانبي
const sidebar = document.querySelector('.sidebar');
const hamburger = document.querySelector('.hamburger');

function toggleSidebar() {
    sidebar.classList.toggle('active');
}

// أحداث النقر
hamburger.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleSidebar();
});

document.addEventListener('click', (e) => {
    if (window.innerWidth <= 768 &&
        !sidebar.contains(e.target) &&
        !hamburger.contains(e.target)) {
        sidebar.classList.remove('active');
    }
});

// إغلاق القائمة عند تغيير حجم النافذة
window.addEventListener('resize', () => {
    if (window.innerWidth > 768) {
        sidebar.classList.remove('active');
    }
});

// تبديل المحتوى
function chiked(num) {
    const contents = document.querySelectorAll('[class^="main-content"]');
    contents.forEach(content => {
        content.style.display = 'none';
        content.classList.remove('active');
    });
    document.getElementById(`m${num}`).style.display = 'block';

    if (window.innerWidth <= 768) {
        sidebar.classList.remove('active');
    }
}

// تهيئة أولية
chiked(1);