async function fetchCars() {
    const response = await fetch('/get_cars');
    const cars = await response.json();
    const carSelect = document.getElementById('car_id');

    cars.forEach(car => {
        let option = document.createElement('option');
        option.value = car.id;
        option.textContent = `${car.brand} ${car.model} - ${car.year}`;
        carSelect.appendChild(option);
    });
}

document.getElementById('booking-form').addEventListener('submit', async (event) => {
    event.preventDefault();

    const bookingData = {
        customer_name: document.getElementById('customer_name').value,
        customer_email: document.getElementById('customer_email').value,
        phone_number: document.getElementById('phone_number').value,
        car_id: document.getElementById('car_id').value,
        booking_date: document.getElementById('booking_date').value,
        booking_time: document.getElementById('booking_time').value
    };

    const response = await fetch('/submit_booking', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(bookingData)
    });

    const result = await response.json();
    alert(result.message);
});

fetchCars();