const API_BASE_URL = window.location.origin + '/api/v1';

/**
 * Retrieves a cookie by its name.
 * @param {string} name The name of the cookie to retrieve.
 * @returns {string|null} The cookie value or null if not found.
 */
function getCookie(name) {
  const cookieStr = document.cookie;
  const cookies = cookieStr.split(';');
  for (let cookie of cookies) {
    const [key, value] = cookie.trim().split('=');
    if (key === name) return decodeURIComponent(value);
  }
  return null;
}

/**
 * Extracts a query parameter from the URL by its name.
 * @param {string} paramName - The name of the query parameter.
 * @returns {string|null} The parameter value or null if not found.
 */
function getQueryParam(paramName) {
  const params = new URLSearchParams(window.location.search);
  return params.get(paramName);
}

/**
 * Logs the user out by clearing the token cookie and redirecting.
 * @param {Event} event The click event.
 */
function logoutUser(event) {
  event.preventDefault();
  // To delete a cookie, set its Max-Age to 0.
  document.cookie = 'token=; path=/; Max-Age=0; SameSite=Strict';
  // Redirect to login page for a cleaner logout experience.
  window.location.href = 'login.html';
}

/**
 * Checks user authentication status and updates the UI accordingly.
 * This should be called *after* the header has been loaded.
 */
function handleAuthUI() {
  const token = getCookie('token');
  const loginLink = document.querySelector('header nav a.login-button');
  const logoutLink = document.querySelector('header nav a.logout-button');
  // Also handle the review form on the place details page
  const reviewForm = document.getElementById('review-form');

  if (loginLink) {
    loginLink.style.display = token ? 'none' : 'block';
  }
  if (logoutLink) {
    logoutLink.style.display = token ? 'block' : 'none';
    if (token) {
      logoutLink.addEventListener('click', logoutUser);
    }
  }
  if (reviewForm) {
    reviewForm.style.display = token ? 'block' : 'none';
  }
}

/**
 * Fetches and injects a component into a placeholder element.
 * @param {string} componentPath - The path to the HTML component file.
 * @param {string} placeholderSelector - The CSS selector for the placeholder element.
 * @param {() => void} [callback] - Optional callback to run after injection.
 */
async function loadComponent(componentPath, placeholderSelector, callback) {
  const placeholder = document.querySelector(placeholderSelector);
  if (!placeholder) return;

  try {
    const response = await fetch(componentPath);
    if (!response.ok) throw new Error(`Failed to load ${componentPath}`);
    const html = await response.text();
    placeholder.innerHTML = html;
    if (callback) {
      callback();
    }
  } catch (error) {
    console.error(`Error loading component: ${componentPath}`, error);
    placeholder.innerHTML = `<p style="color: red; text-align: center;">Error loading content.</p>`;
  }
}

// Load components when the DOM is ready
document.addEventListener('DOMContentLoaded', () => {
  // The header component requires a callback to handle auth UI after it's loaded.
  loadComponent('../static/components/_header.html', 'header', handleAuthUI);
  loadComponent('../static/components/_footer.html', 'footer');
});