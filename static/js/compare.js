// تأثيرات عند تحميل الصفحة
document.addEventListener("DOMContentLoaded", function () {
    const rows = document.querySelectorAll('.compare-table td');
    rows.forEach(cell => {
        cell.addEventListener('mouseover', () => {
            cell.style.backgroundColor = "#f39c12";
        });
        cell.addEventListener('mouseout', () => {
            cell.style.backgroundColor = "";
        });
    });
});





// إضافة السيارات إلى المقارنة
function addToCompare(id, brand, model) {
    let cars = JSON.parse(localStorage.getItem('compareCars')) || [];

    // التحقق من عدم إضافة السيارة مرتين
    if (cars.find(car => car.id === id)) {
        alert("تمت إضافة السيارة مسبقًا إلى المقارنة!");
        return;
    }

    cars.push({ id, brand, model });
    localStorage.setItem('compareCars', JSON.stringify(cars));
    updateCompareBar();
}

// تحديث شريط المقارنة
function updateCompareBar() {
    let cars = JSON.parse(localStorage.getItem('compareCars')) || [];
    let countSpan = document.getElementById('compare-count');
    let compareLink = document.getElementById('compare-link');

    if (cars.length > 0) {
        countSpan.innerText = `تم اختيار ${cars.length} سيارة`;
        compareLink.classList.remove('hidden');

        // إنشاء رابط المقارنة مع الـ ID المختارة
        let compareIds = cars.map(car => `car_id=${car.id}`).join('&');
        compareLink.href = `/compare?${compareIds}`;
    } else {
        countSpan.innerText = "لم يتم اختيار سيارات";
        compareLink.classList.add('hidden');
    }
}

// تحميل البيانات عند فتح الصفحة
document.addEventListener('DOMContentLoaded', updateCompareBar);




