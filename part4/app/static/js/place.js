document.addEventListener('DOMContentLoaded', () => {
  const placeId = getQueryParam('id'); // getQueryParam is from shared.js
  const token = getCookie('token');
  const errorBox = document.getElementById('errorBox');

  if (placeId) {
    fetchPlaceDetails(placeId, token);
    fetchReviews(placeId, token);

    // Listen for the custom event dispatched when a new review is submitted
    document.addEventListener('reviewSubmitted', () => {
      // Refresh the reviews list to show the new one
      fetchReviews(placeId, token);
    });
  } else {
    if (errorBox) {
      errorBox.textContent = 'No place ID found in URL.';
      errorBox.style.display = 'block';
    }
  }
});

async function fetchPlaceDetails(placeId, token) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/places/${placeId}`, {
      headers,
    });
    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ error: 'Failed to fetch place details' }));
      throw new Error(errorData.error);
    }
    const data = await response.json();
    displayPlaceDetails(data);
  } catch (error) {
    console.error('Error fetching place:', error);
    const errorBox = document.getElementById('errorBox');
    if (errorBox) {
      errorBox.textContent = error.message;
      errorBox.style.display = 'block';
    }
  }
}

function displayPlaceDetails(place) {
  const container = document.querySelector('.place-details');
  if (!container) return;

  const amenities =
    place.amenities && place.amenities.length > 0
      ? place.amenities.map((a) => a.name).join(', ')
      : 'No amenities listed.';
   // Pick random image
  var randomImage = images[Math.floor(Math.random() * images.length)];
  container.innerHTML = `
    <h2>${place.title}</h2>
    <img src="${randomImage}" alt="${place.title}" class="place-image">
    <p>${place.description}</p>
    <p><strong>Price:</strong> $${place.price.toFixed(2)}</p>
    <p><strong>City:</strong> ${place.city || 'N/A'}</p>
    <p><strong>Amenities:</strong> ${amenities}</p>
  `;
}

async function fetchReviews(placeId, token) {
  const headers = { 'Content-Type': 'application/json' };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
      headers,
    });
    if (!response.ok) {
      const errorData = await response
        .json()
        .catch(() => ({ error: 'Failed to fetch reviews' }));
      throw new Error(errorData.error);
    }
    const reviews = await response.json();
    displayReviews(reviews);
  } catch (error) {
    console.error('Error fetching reviews:', error);
    // Optionally, display this error in the reviews section
    const reviewsContainer = document.querySelector('.reviews');
    if (reviewsContainer) {
      reviewsContainer.innerHTML =
        '<h3>Reviews</h3><p class="error">Could not load reviews.</p>';
    }
  }
}
function displayReviews(reviews) {
  const container = document.querySelector('.reviews');
  container.innerHTML = `<h2>Reviews</h2>`;

  reviews.forEach(review => {
    const stars = '★'.repeat(review.rating) + '☆'.repeat(5 - review.rating);

    const reviewCard = document.createElement('div');
    reviewCard.className = 'review-card';
    reviewCard.innerHTML = `
      <div class="review-author">${review.user_name || 'Anonymous'}</div>
      <div class="star-rating">${stars}</div>
      <div class="review-text">${review.text}</div>
    `;
    container.appendChild(reviewCard);
  });
}

document.addEventListener('DOMContentLoaded', () => {
  const stars = document.querySelectorAll('.star-rating span');
  const ratingInput = document.getElementById('rating-value');

  stars.forEach(star => {
    star.addEventListener('click', () => {
      // Remove previous selection
      stars.forEach(s => s.classList.remove('selected'));
      // Add selected class up to clicked star
      star.classList.add('selected');
      let current = star;
      while (current.nextElementSibling) {
        current = current.nextElementSibling;
        current.classList.add('selected');
      }
      // Set hidden input value
      ratingInput.value = star.getAttribute('data-value');
    });
  });
});
