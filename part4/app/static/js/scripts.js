const API_BASE_URL = window.location.origin + '/api/v1';

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            // Your code to handle form submission
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            loginUser(email,password);
        });
    }
});

async function loginUser(email, password) {
    const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ email, password })
    });
    // Handle the response
    const data = await response.json();
    if (response.ok) {
  
    document.cookie = `token=${data.access_token}; path=/`;
    window.location.href = 'index.html';
} else {
    errorBox.textContent = data.error || 'Login failed. Please try again.';
        errorBox.style.display = 'block';
}
}