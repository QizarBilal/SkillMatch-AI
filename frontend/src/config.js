const API_BASE_URL = import.meta.env.MODE === 'production'
  ? window.location.origin
  : 'http://127.0.0.1:8000';

export default API_BASE_URL;
