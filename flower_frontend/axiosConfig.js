// axiosConfig.js
import axios from 'axios';

// Fonction pour obtenir le token CSRF à partir des cookies
const getCookie = (name) => {
  let cookieValue = null;
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';');
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
};

// Ajouter le token CSRF aux en-têtes Axios
const csrfToken = getCookie('csrftoken');
axios.defaults.headers.common['X-CSRFToken'] = csrfToken;

// Optionnel : configurer d'autres paramètres Axios ici
// axios.defaults.baseURL = 'http://your-api-url/';

export default axios;
