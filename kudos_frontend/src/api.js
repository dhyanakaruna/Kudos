const API_BASE_URL = 'http://localhost:8000/api';

class ApiService {
  constructor() {
    this.currentUserId = localStorage.getItem('currentUserId') || null;
  }

  setCurrentUser(userId) {
    this.currentUserId = userId;
    localStorage.setItem('currentUserId', userId);
  }

  getCurrentUserId() {
    return this.currentUserId;
  }

  async makeRequest(url, options = {}) {
    const headers = {
      'Content-Type': 'application/json',
      ...options.headers,
    };

    if (this.currentUserId) {
      headers['X-User-ID'] = this.currentUserId;
    }

    try {
      const response = await fetch(`${API_BASE_URL}${url}`, {
        ...options,
        headers,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        const errorMessage = errorData.error || `HTTP error! status: ${response.status}`;
        
        // Handle specific error cases
        if (response.status === 404 && url.includes('/users/me/')) {
          throw new Error('Invalid user ID');
        }
        
        throw new Error(errorMessage);
      }

      return response.json();
    } catch (error) {
      if (error.name === 'TypeError' && error.message.includes('Failed to fetch')) {
        throw new Error('Unable to connect to the server. Please make sure the backend is running on http://localhost:8000');
      }
      throw error;
    }
  }

  // User endpoints
  async getCurrentUser() {
    return this.makeRequest('/users/me/');
  }

  async getUsers() {
    return this.makeRequest('/users/');
  }

  async getOrganizations() {
    return this.makeRequest('/organizations/');
  }

  async getUsersByOrganization(orgId) {
    return this.makeRequest(`/organizations/${orgId}/users/`);
  }

  // Kudo endpoints
  async giveKudo(receiverId, message) {
    return this.makeRequest('/kudos/', {
      method: 'POST',
      body: JSON.stringify({
        receiver: receiverId,
        message: message,
      }),
    });
  }

  async getReceivedKudos() {
    return this.makeRequest('/kudos/received/');
  }
}

export default new ApiService();
