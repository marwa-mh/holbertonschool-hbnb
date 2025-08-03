const API_BASE_URL = window.location.origin + '/api/v1';
function getPlaceIdFromURL() {
  const params = new URLSearchParams(window.location.search);
  
  return params.get('id'); 
}
document.addEventListener('DOMContentLoaded', () => {
  const placeId = getPlaceIdFromURL();
  if (placeId) {
    fetchPlaceDetails(placeId);
    fetchReviews(placeId);
  }
});

async function fetchPlaceDetails(placeId) {
  try {
    const response = await fetch(`${API_BASE_URL}/places/${placeId}`);
    if (!response.ok) throw new Error('Failed to fetch place details');
    const data = await response.json();
    displayPlaceDetails(data);
  } catch (error) {
    console.error('Error fetching place:', error);
  }
}

function displayPlaceDetails(place) {
  const container = document.querySelector('.place-details');
    container.innerHTML = '';
  container.innerHTML = `
    <h2>${place.title}</h2>
    <img src="${place.image_url || 'https://via.placeholder.com/600x400'}" alt="${place.title}" class="place-image">
    <p>${place.description}</p>
    <p><strong>Price:</strong> $${place.price}</p>
    <p><strong>City:</strong> ${place.city || 'N/A'}</p>
    <p><strong>Amenities:</strong> ${place.amenities.map(a => a.name).join(', ')}</p>
  `;
}



async function fetchReviews(placeId) {
  try {
    const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`);
    if (!response.ok) throw new Error('Failed to fetch reviews');
    const reviews = await response.json();
    displayReviews(reviews);
  } catch (error) {
    console.error('Error fetching reviews:', error);
  }
}

function displayReviews(reviews) {
  const container = document.querySelector('.reviews');
  if (reviews.length === 0) {
    container.innerHTML += `<h3>Reviews</h3><p>No reviews yet.</p>`;
    return;
  }

  const reviewHTML = reviews.map(review => `
    <div class="review">
      <p><strong>${review.user_name || 'Anonymous'}:</strong> ${review.text}</p>
      <small>${new Date(review.created_at).toLocaleDateString()}</small>
    </div>
  `).join('');

  container.innerHTML += `
    <h3>Reviews</h3>
    ${reviewHTML}
  `;
}
