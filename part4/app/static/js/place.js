const API_BASE_URL = window.location.origin + '/api/v1';

function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  return params.get('id');
}

document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  const token = getCookie('token');
  const reviewForm = document.getElementById('review-form');
  const errorBox = document.getElementById('errorBox');

  if (reviewForm) {
    reviewForm.style.display = token ? 'block' : 'none';
  }

  if (placeId) {
    fetchPlaceDetails(placeId, token);
    fetchReviews(placeId, token);
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

  container.innerHTML = `
    <h2>${place.title}</h2>
    <img src="${
      place.picture_url || 'https://via.placeholder.com/600x400'
    }" alt="${place.title}" class="place-image">
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
  if (!container) return;

  let contentHTML = '<h3>Reviews</h3>';
  if (reviews.length === 0) {
    contentHTML += `<p>No reviews yet.</p>`;
  } else {
    const reviewHTML = reviews
      .map(
        (review) => `
      <div class="review">
        <p><strong>${review.user_name || 'Anonymous'}:</strong> ${
          review.text
        }</p>
        <small>${new Date(review.created_at).toLocaleDateString()}</small>
      </div>
    `
      )
      .join('');
    contentHTML += reviewHTML;
  }
  container.innerHTML = contentHTML;
}
