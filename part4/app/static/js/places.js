const API_BASE_URL = window.location.origin + '/api/v1';

/**
 * Fetches places from the API and renders them on the page.
 * Includes authentication token in the request if available.
 */
async function fetchPlaces() {
  const token = getCookie('token');
  const headers = {
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${API_BASE_URL}/places`, {
      method: 'GET',
      headers: headers,
    });

    const data = await response.json();
    const errorBox = document.getElementById('errorBox');

    if (response.ok) {
      renderPlaces(data);
      if (errorBox) errorBox.style.display = 'none';
    } else {
      if (errorBox) {
        errorBox.textContent = data.error || 'Failed to load places. Please try again.';
        errorBox.style.display = 'block';
      }
    }
  } catch (error) {
    console.error('Error fetching places:', error);
    const errorBox = document.getElementById('errorBox');
    if (errorBox) {
      errorBox.textContent = 'A network error occurred. Please try again.';
      errorBox.style.display = 'block';
    }
  }
}

/**
 * Renders a list of places into the DOM.
 */
function renderPlaces(places) {
  const container = document.getElementById('places-list');
  if (!container) return;
  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);
    card.innerHTML = `
      <img src="${place.picture_url || 'https://via.placeholder.com/300x200'}" alt="${place.title}" class="place-image">
      <div class="place-details">
        <h3 class="place-title">${place.title}</h3>
        <div class="place-city">${place.city || 'N/A'}</div>
        <div class="place-price">$${place.price.toFixed(2)}</div>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      </div>
    `;
    container.appendChild(card);
  });
}

function handlePriceFilter(event) {
    const selectedPrice = event.target.value;

    const placeCards = document.querySelectorAll('.place-card');

    placeCards.forEach(card => {
        const price = parseFloat(card.getAttribute('data-price'));

        if (selectedPrice == 'all' || price <= parseFloat(selectedPrice)){
            card.style.display = 'block';
        }else{
            card.style.display = 'none';
        }
    });
}

document.addEventListener('DOMContentLoaded', () => {
  fetchPlaces();

  const priceFilter = document.getElementById('price-filter');
  if (priceFilter) {
    priceFilter.addEventListener('change', handlePriceFilter);
  }
});