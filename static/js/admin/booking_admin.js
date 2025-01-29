

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
        let statusClass = booking.status === 'pending' ? 'status-pending' :
            booking.status === 'confirmed' ? 'status-confirmed' : 'status-cancelled';

        tableBody.innerHTML += `
            <tr>
                <td data-label="رقم الحجز">${booking.id}</td>
                <td data-label="اسم العميل">${booking.customer_name}</td>
                <td data-label="السيارة">${booking.car_model}</td>
                <td data-label="التاريخ">${booking.booking_date}</td>
                <td data-label="الحالة" class="${statusClass}">${booking.status}</td>
                <td data-label="الإجراءات" class="actions">
                    <button onclick="updateStatus(${booking.id}, 'confirmed')">تأكيد</button>
                    <button onclick="updateStatus(${booking.id}, 'cancelled')">إلغاء</button>
                </td>
            </tr>
        `;
    });
}

async function updateStatus(id, status) {
    await fetch('/update_booking_status', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ id, status })
    });
    fetchBookings();
}

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('searchInput').addEventListener('input', fetchBookings);
    document.getElementById('statusFilter').addEventListener('change', fetchBookings);
    fetchBookings();
});