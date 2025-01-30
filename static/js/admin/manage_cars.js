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
            // إنشاء كافة الصفوف دفعة واحدة لتفادي التكرار
            const rows = cars.map(car => {
                return `
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
            }).join(""); // دمج جميع الصفوف في نص واحد

            // إضافة الصفوف المدمجة
            tableBody.innerHTML = rows;
        })
        .catch(error => console.error("❌ خطأ في جلب السيارات:", error));
}



document.addEventListener("DOMContentLoaded", function () {
    document.getElementById("car-form").addEventListener("submit", async function (event) {
        event.preventDefault(); // 🔴 منع إعادة تحميل الصفحة

        let formData = new FormData(this); // 🔹 جمع بيانات النموذج

        // ✅ 1. رفع الصورة أولًا قبل إرسال باقي البيانات
        let imageFile = formData.get("image");
        if (imageFile && imageFile.name) {
            let imageUploadForm = new FormData();
            imageUploadForm.append("image", imageFile);

            try {
                let imageResponse = await fetch("/upload_image", {
                    method: "POST",
                    body: imageUploadForm
                });

                let imageData = await imageResponse.json();
                if (!imageData.success) {
                    showMessage(imageData.message, false);
                    return;
                }

                formData.append("image_url", imageData.filename);
            } catch (error) {
                console.error("❌ خطأ أثناء رفع الصورة:", error);
                showMessage("حدث خطأ أثناء رفع الصورة", false);
                return;
            }
        }

        // ✅ 2. إرسال بيانات السيارة إلى السيرفر بعد رفع الصورة
        try {
            let response = await fetch("/add_car", {
                method: "POST",
                body: formData
            });

            let data = await response.json();
            console.log("📡 Response:", data);

            showMessage(data.message, data.success);

            if (data.success) {
                document.getElementById("car-form").reset();
                addCarToTable(data.car); // ✅ إضافة السيارة مباشرة إلى الجدول
            }
        } catch (error) {
            console.error("❌ خطأ أثناء الإرسال:", error);
            showMessage("حدث خطأ أثناء إضافة السيارة", false);
        }
    });

    // ✅ تحميل السيارات عند فتح الصفحة
    fetchCars();
});


// ✅ تحديث الجدول مع مسحه أولًا لتجنب التكرار
function updateTable(cars) {
    const tableBody = document.getElementById("car-list");
    tableBody.innerHTML = ""; // 🔴 مسح البيانات القديمة قبل التحديث

    cars.forEach(car => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td>${car.id}</td>
            <td>${car.brand}</td>
            <td>${car.model}</td>
            <td>${car.year}</td>
            <td>${car.price}</td>
            <td>${car.fuel_type}</td>
            <td>${car.engine_power} HP</td>
            <td>${car.fuel_efficiency} كم/لتر</td>
            <td><img src="${car.image_url}" alt="صورة السيارة" width="50"></td>
            <td>${car.category}</td>
        `;
        tableBody.appendChild(row);
    });
}
// ✅ دالة لإضافة السيارة الجديدة مباشرة إلى الجدول دون إعادة تحميل القائمة كاملة
function addCarToTable(car) {
    const tableBody = document.getElementById("car-list");

    // بدلاً من استخدام innerHTML، سنستخدم appendChild مع العنصر المضاف بشكل ديناميكي.
    const row = document.createElement("tr");

    row.innerHTML = `
        <td>${car.id}</td>
        <td>${car.brand}</td>
        <td>${car.model}</td>
        <td>${car.year}</td>
        <td>${car.price}</td>
        <td>${car.fuel_type}</td>
        <td>${car.engine_power} HP</td>
        <td>${car.fuel_efficiency} كم/لتر</td>
        <td><img src="${car.image_url}" alt="صورة السيارة" width="50"></td>
        <td>${car.category}</td>
    `;

    // إضافة الصف الجديد إلى الجدول
    tableBody.appendChild(row);
}


// ✅ دالة لعرض الرسائل للمستخدم
function showMessage(message, isSuccess) {
    let messageBox = document.getElementById("message-box");
    messageBox.textContent = message;
    messageBox.style.display = "block";
    messageBox.style.color = isSuccess ? "green" : "red";
    messageBox.style.border = isSuccess ? "2px solid green" : "2px solid red";
    messageBox.style.backgroundColor = isSuccess ? "#d4edda" : "#f8d7da";
}

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
























document.getElementById('imageInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('fileLabel').textContent = `تم اختيار الصورة: ${file.name}`;
    } else {
        document.getElementById('fileLabel').textContent = "لم يتم اختيار صورة";
    }
});

document.getElementById('car-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    // رفع الصورة أولًا
    const imageResponse = await fetch('/upload_image', {
        method: 'POST',
        body: formData
    });

    const imageResult = await imageResponse.json();
    if (!imageResult.success) {
        alert(imageResult.message);
        return;
    }

    // إضافة اسم الصورة إلى البيانات وإرسالها إلى السيرفر
    formData.append('image_url', imageResult.filename);

    const carResponse = await fetch('/add_car', {
        method: 'POST',
        body: formData
    });

    const carResult = await carResponse.json();
    alert(carResult.message);
});









document.getElementById('imageInput').addEventListener('change', function (event) {
    const file = event.target.files[0];
    if (file) {
        document.getElementById('fileLabel').textContent = `تم اختيار الصورة: ${file.name}`;
    } else {
        document.getElementById('fileLabel').textContent = "لم يتم اختيار صورة";
    }
});

document.getElementById('car-form').addEventListener('submit', async function (event) {
    event.preventDefault();

    const formData = new FormData(this);

    // رفع الصورة أولًا
    const imageResponse = await fetch('/upload_image', {
        method: 'POST',
        body: formData
    });

    const imageResult = await imageResponse.json();
    if (!imageResult.success) {
        alert(imageResult.message);
        return;
    }

    // إضافة اسم الصورة إلى البيانات وإرسالها إلى السيرفر
    formData.append('image_url', imageResult.filename);

    const carResponse = await fetch('/add_car', {
        method: 'POST',
        body: formData
    });

    const carResult = await carResponse.json();
    alert(carResult.message);
});










