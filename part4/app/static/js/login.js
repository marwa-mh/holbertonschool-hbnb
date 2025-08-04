const API_BASE_URL = window.location.origin + '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
  const loginForm = document.getElementById('login-form');
  const errorBox = document.getElementById('errorBox');
  const submitButton = loginForm ? loginForm.querySelector('button[type="submit"]') : null;

  if (loginForm && submitButton && errorBox) {
    loginForm.addEventListener('submit', async (event) => {
      event.preventDefault();
      errorBox.style.display = 'none';
      submitButton.disabled = true;
      submitButton.textContent = 'Logging in...';

      const email = document.getElementById('email').value.trim();
      const password = document.getElementById('password').value.trim();

      if (!email || !password) {
        errorBox.textContent = 'Please fill in both email and password.';
        errorBox.style.display = 'block';
        return;
      }
        
      try {
        const data = await loginUser(email, password);
        // For better security, SameSite=Strict and Secure attributes are recommended for cookies.
        document.cookie = `token=${data.access_token}; path=/; SameSite=Strict; Secure`;
        window.location.href = 'index.html';
      } catch (error) {
        errorBox.textContent = error.message;
        errorBox.style.display = 'block';
      } finally {
        submitButton.disabled = false;
        submitButton.textContent = 'Login';
      }
    });
  }
});

async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, password }),
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.error || 'Login failed. Please try again.');
    }

    return data;
  } catch (error) {
    // Re-throw network errors or other unexpected issues to be handled by the caller.
    throw new Error(error.message || 'A network error occurred. Please try again.');
  }
}
