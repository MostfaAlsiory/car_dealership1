// تغيير الصورة عند النقر على الصورة المصغرة
function changeImage(img) {
    document.getElementById('main-image').src = img.src;
}

// حجز تجربة القيادة
function bookTestDrive() {
    alert("تم إرسال طلب تجربة القيادة بنجاح! سيتم التواصل معك قريبًا.");
}









let selectedCars = JSON.parse(localStorage.getItem('compareCars')) || [];

function toggleCompare(id, brand, model) {
    let button = document.getElementById(`compare-btn-${id}`);

    // التحقق مما إذا كانت السيارة مضافة سابقًا
    let carIndex = selectedCars.findIndex(car => car.id === id);

    if (carIndex === -1) {
        // إضافة السيارة إلى القائمة
        selectedCars.push({ id, brand, model });
        button.classList.add("selected");
        button.innerText = "تمت الإضافة";
    } else {
        // إزالة السيارة من القائمة
        selectedCars.splice(carIndex, 1);
        button.classList.remove("selected");
        button.innerText = "قارن";
    }

    // حفظ القائمة في التخزين المحلي
    localStorage.setItem('compareCars', JSON.stringify(selectedCars));
    updateCompareButton();
}

// تحديث زر التأكيد النهائي
function updateCompareButton() {
    let compareFinalBtn = document.getElementById('compare-final-btn');
    if (selectedCars.length > 0) {
        compareFinalBtn.style.display = "block";
    } else {
        compareFinalBtn.style.display = "none";
    }
}

// تحميل السيارات المخزنة عند فتح الصفحة
document.addEventListener('DOMContentLoaded', () => {
    selectedCars.forEach(car => {
        let button = document.getElementById(`compare-btn-${car.id}`);
        if (button) {
            button.classList.add("selected");
            button.innerText = "تمت الإضافة";
        }
    });
    updateCompareButton();
});







function confirmComparison() {
    let carIds = selectedCars.map(car => car.id).join(",");
    window.location.href = `/compare?car_ids=${carIds}`;
}






















document.addEventListener("DOMContentLoaded", function () {
    const searchForm = document.getElementById("search-form");
    searchForm.addEventListener("submit", function (event) {
        event.preventDefault();
        fetchCars();
    });

    async function fetchCars() {
        const brand = document.getElementById("brand").value;
        const maxPrice = document.getElementById("max_price").value;
        const fuelType = document.getElementById("fuel_type").value;
        const sortBy = document.getElementById("sort_by").value;
        const sortOrder = document.getElementById("sort_order").value;

        const params = new URLSearchParams({
            brand: brand,
            max_price: maxPrice,
            fuel_type: fuelType,
            sort_by: sortBy,
            sort_order: sortOrder
        });

        const response = await fetch(`/get_cars4?${params}`);
        const cars = await response.json();

        updateCarList(cars);
    }






    function updateCarList(cars) {
        const carListContainer = document.querySelector(".car-list");
        carListContainer.innerHTML = ""; // مسح السيارات القديمة

        cars.forEach(car => {
            const carCard = `
                <div class="car-card">
                    <img src="static/upload/${car.image_url}" alt="${car.brand} ${car.model}">
                    <h3>${car.brand} ${car.model}</h3>
                    <p>السعر: $${car.price}</p>
                    <a href="/car/${car.id}" class="btn details-btn">التفاصيل</a>
                    <button class="btn compare-btn" id="compare-btn-${car.id}"
                        data-id="${car.id}" data-brand="${car.brand}" data-model="${car.model}">
                        قارن
                    </button>
                </div>
            `;
            carListContainer.innerHTML += carCard;
        });

        // إعادة ربط الأحداث للأزرار بعد تحميل القائمة
        document.querySelectorAll('.compare-btn').forEach(button => {
            button.addEventListener('click', function () {
                let carId = this.getAttribute('data-id');
                let carBrand = this.getAttribute('data-brand');
                let carModel = this.getAttribute('data-model');
                toggleCompare(carId, carBrand, carModel);
            });
        });

        // استعادة حالة الأزرار من localStorage
        selectedCars.forEach(car => {
            let button = document.getElementById(`compare-btn-${car.id}`);
            if (button) {
                button.classList.add("selected");
                button.innerText = "تمت الإضافة";
            }
        });

        updateCompareButton(); // تحديث زر التأكيد النهائي
    }









    fetchCars(); // تحميل البيانات عند فتح الصفحة
});







//من اجل التقييمات وتحديثها
document.addEventListener('DOMContentLoaded', function () {
    const stars = document.querySelectorAll('.rating-stars span');
    const ratingInput = document.getElementById('rating');

    stars.forEach(star => {
        star.addEventListener('click', function () {
            const selectedValue = this.getAttribute('data-value');

            if (ratingInput.value == selectedValue) {
                // إلغاء التقييم عند النقر مرة أخرى على نفس النجمة
                ratingInput.value = '';
                resetStars();
            } else {
                // تحديد التقييم
                ratingInput.value = selectedValue;
                highlightStars(selectedValue);
            }
        });
    });

    function highlightStars(value) {
        stars.forEach(star => {
            if (star.getAttribute('data-value') <= value) {
                star.classList.add('selected');
            } else {
                star.classList.remove('selected');
            }
        });
    }

    function resetStars() {
        stars.forEach(star => star.classList.remove('selected'));
    }

    // إرسال التقييم
    document.getElementById('review-form').addEventListener('submit', function (event) {
        event.preventDefault();

        const car_id = document.getElementById('car_id').value;
        const user_name = document.getElementById('user_name').value;
        const rating = document.getElementById('rating').value;
        const review_text = document.getElementById('review_text').value;

        if (!rating) {
            alert("يرجى اختيار تقييم!");
            return;
        }

        fetch('/submit_review', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ car_id, user_name, rating, review_text })
        })
            .then(response => response.json())
            .then(data => {
                alert(data.message);
                location.reload();
            })
            .catch(error => console.error('Error:', error));
    });
});