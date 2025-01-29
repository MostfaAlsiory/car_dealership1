async function fetchReviews() {
    const response = await fetch('/get_reviews');
    const reviews = await response.json();
    const reviewsList = document.getElementById('reviews-list');
    reviewsList.innerHTML = '';
    reviews.forEach(review => {
        reviewsList.innerHTML += `
            <tr>
                <td>${review.id}</td>
                <td>${review.car_id}</td>
                <td>${review.user_name}</td>
                <td>${review.rating}</td>
                <td>${review.review_text}</td>
                <td>${review.created_at}</td>
                <td><button class="delete-btn" style="width:100%" onclick="deleteReview(${review.id})">حذف</button></td>
            </tr>
        `;
    });
}

async function addReview() {
    const carId = document.getElementById('car_id').value;
    const userName = document.getElementById('user_name').value;
    const rating = document.getElementById('rating').value;
    const reviewText = document.getElementById('review_text').value;

    if (!carId || !userName || !rating || !reviewText) {
        alert('يرجى ملء جميع الحقول');
        return;
    }

    const response = await fetch('/add_review', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ car_id: carId, user_name: userName, rating: rating, review_text: reviewText })
    });
    const result = await response.json();
    alert(result.message);
    fetchReviews();
}

async function deleteReview(id) {
    if (confirm('هل أنت متأكد من حذف هذا التقييم؟')) {
        await fetch(`/delete_review/${id}`, { method: 'DELETE' });
        fetchReviews();
    }
}

fetchReviews();