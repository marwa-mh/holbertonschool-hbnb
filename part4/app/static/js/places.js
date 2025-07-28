const API_BASE_URL = window.location.origin + '/api/v1';
function renderAmenityIcon(name) {
    const icons = {
        'WiFi': '<i class="fa fa-wifi" title="WiFi"></i>',
        'Air Conditioning': '<i class="fa fa-snowflake" title="Air Conditioning"></i>',
        'Parking': '<i class="fa fa-car" title="Parking"></i>',
        // Add more mappings
    };
    return icons[name] || `<span>${name}</span>`;
}

document.addEventListener('DOMContentLoaded', () => {
    
        fetchPlaces()

});

async function fetchPlaces() {
    const response = await fetch(`${API_BASE_URL}/places`, {
        method: 'GET',
        headers: {
            'Content-Type': 'application/json'
        }
    });
    // Handle the response
    const data = await response.json();
    
    const errorBox = document.getElementById('errorBox');

    if (response.ok) {
        
            renderPlaces(data);
        
        errorBox.style.display ='none'
} else {
    errorBox.textContent = data.error || 'Failed to load places. Please try again.';
        errorBox.style.display = 'block';
}
}

function renderPlaces(places) {
  const container = document.getElementById('places-list');
  container.innerHTML = '';

  places.forEach(place => {
    const card = document.createElement('div');
    card.className = 'place-card';
    card.setAttribute('data-price', place.price);
    card.innerHTML = `
      <img src="${place.picture_url}" alt="Place Image" class="place-image">
      <div class="place-details">
        <h3 class="place-title">${place.title}</h3>
        <div class="place-city">${place.city}</div>
        <div class="place-price">$${place.price.toFixed(2)}</div>
        <a href="place.html?id=${place.id}" class="details-button">View Details</a>
      </div>
    `;

    container.appendChild(card);
  });
}

document.getElementById('price-filter').addEventListener('change', (event) => {

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
});