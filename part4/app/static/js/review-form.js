document.addEventListener('DOMContentLoaded', () => {
  const reviewForm = document.getElementById('review-form');
  const token = getCookie('token');
  const placeId = getQueryParam('id');
  const errorBox = document.getElementById('errorBox');

  if (reviewForm && token && placeId && errorBox) {
    reviewForm.addEventListener('submit', async (event) => {
      event.preventDefault();

      const submitButton = reviewForm.querySelector('button[type="submit"]');
      const reviewText = document.getElementById('review-text').value.trim();
      const rating = document.getElementById('rating').value;

      if (!reviewText || !rating) {
        errorBox.textContent = 'Please provide both a rating and a review text.';
        errorBox.style.display = 'block';
        return;
      }

      submitButton.disabled = true;
      submitButton.textContent = 'Submitting...';
      errorBox.style.display = 'none';

      try {
        const response = await fetch(`${API_BASE_URL}/places/${placeId}/reviews`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({ text: reviewText, rating: parseInt(rating, 10) }),
        });

        const result = await response.json();
        if (!response.ok) {
          throw new Error(result.error || 'Failed to submit review.');
        }

        reviewForm.reset();

        // Dispatch a custom event to notify other parts of the page (i.e., place.js)
        document.dispatchEvent(new CustomEvent('reviewSubmitted'));
      } catch (error) {
        errorBox.textContent = error.message;
        errorBox.style.display = 'block';
      } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Submit';
      }
    });
  }
});