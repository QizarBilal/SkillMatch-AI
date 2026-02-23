const api = {
  request: async (endpoint, options = {}) => {
    const token = localStorage.getItem('token');
    
    // Rule 1: Always use relative paths
    // Rule 5: Automatically include Authorization header
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(endpoint, {
        ...options,
        headers,
      });

      // Rule 6: Handle backend responses properly
      if (response.status === 401) {
        localStorage.removeItem('token');
        localStorage.removeItem('user_id');
        localStorage.removeItem('user_email');
        localStorage.removeItem('skillmatch_result');
        window.dispatchEvent(new Event('auth-error'));
        return null;
      }

      if (response.status === 405) {
        throw new Error('Configuration error (405). Please check API method.');
      }

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Request failed with status ${response.status}`);
      }

      return await response.json();
    } catch (error) {
      if (error.message === 'Failed to fetch') {
        throw new Error('Network failure. Please check your connection.');
      }
      throw error;
    }
  },

  get: (endpoint, options = {}) => api.request(endpoint, { ...options, method: 'GET' }),
  post: (endpoint, body, options = {}) => 
    api.request(endpoint, { 
      ...options, 
      method: 'POST', 
      body: body instanceof FormData ? body : JSON.stringify(body),
      headers: body instanceof FormData ? { ...options.headers } : { ...options.headers, 'Content-Type': 'application/json' }
    }),
};

export default api;
