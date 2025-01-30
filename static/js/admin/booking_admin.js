

function searchcars() {
    location.reload();

}



/*
function chiked(n) {
    d1 = document.getElementById("m1");
    d2 = document.getElementById("m2");
    d3 = document.getElementById("m3");
    d4 = document.getElementById("m4");
    if (n == 1) {
        d1.style.display = "block";
        d2.style.display = "none";
        d3.style.display = "none";
        d4.style.display = "none";

    }
    if (n == 2) {
        d1.style.display = "none";
        d2.style.display = "block";
        d3.style.display = "none";
        d4.style.display = "none";


    }
    if (n == 3) {
        d1.style.display = "none";
        d2.style.display = "none";
        d3.style.display = "block";
        d4.style.display = "none";


    }
    if (n == 4) {
        d1.style.display = "none";
        d2.style.display = "none";
        d3.style.display = "none";
        d4.style.display = "block";


    }


}
*/

async function fetchBookings() {
    const response = await fetch('/get_bookings');
    const data = await response.json();
    updateTable(data);
}

function updateTable(data) {
    const searchInput = document.getElementById('searchInput').value.toLowerCase();
    const statusFilter = document.getElementById('statusFilter').value;
    const tableBody = document.getElementById('booking-list');

    tableBody.innerHTML = '';

    data.filter(booking =>
        booking.customer_name.toLowerCase().includes(searchInput) &&
        (statusFilter === '' || booking.status === statusFilter)
    ).forEach(booking => {
        let statusClass = getStatusClass(booking.status);

        tableBody.innerHTML += `
            <tr id="booking-${booking.id}">
                <td data-label="رقم الحجز">${booking.id}</td>
                <td data-label="اسم العميل">${booking.customer_name}</td>
                <td data-label="السيارة">${booking.brand} ${booking.model}</td>
                <td data-label="التاريخ">${booking.booking_date}</td>
                <td data-label="الحالة" class="status ${statusClass}" id="status-${booking.id}">${booking.status}</td>
                <td data-label="الإجراءات" class="actions">
                    <button onclick="updateStatus(${booking.id}, 'confirmed')">تأكيد</button>
                    <button onclick="updateStatus(${booking.id}, 'cancelled')">إلغاء</button>
                </td>
            </tr>
        `;
    });
}

function getStatusClass(status) {
    return status === 'pending' ? 'status-pending' :
        status === 'confirmed' ? 'status-confirmed' :
            'status-cancelled';
}

async function updateStatus(id, status) {
    await fetch('/update_booking_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status })
    });

    // تحديث الحالة فقط بدون إعادة تحميل الجدول بالكامل
    let statusCell = document.getElementById(`status-${id}`);
    if (statusCell) {
        statusCell.textContent = status;
        statusCell.className = `status ${getStatusClass(status)}`;
    }
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchInput').addEventListener('input', fetchBookings);
    document.getElementById('statusFilter').addEventListener('change', fetchBookings);
    fetchBookings();
});
