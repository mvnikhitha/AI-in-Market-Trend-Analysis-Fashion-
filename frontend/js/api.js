// Kalainayam API Integration Module
// Handles all communication with the backend server

const API = (function() {
  const BASE_URL = 'http://localhost:5000/api';

  // Helper function for making fetch requests
  async function fetchAPI(endpoint, options = {}) {
    const url = `${BASE_URL}${endpoint}`;
    const defaultOptions = {
      headers: {
        'Content-Type': 'application/json',
      },
    };

    const config = { ...defaultOptions, ...options };
    
    try {
      const response = await fetch(url, config);
      if (!response.ok) {
        throw new Error(`API Error: ${response.status} ${response.statusText}`);
      }
      return await response.json();
    } catch (error) {
      console.error('Fetch error:', error);
      throw error;
    }
  }

  return {
    // Trends API
    getTrends: async function(region = 'global', days = 28) {
      try {
        return await fetchAPI(`/trends?region=${region}&days=${days}`);
      } catch (error) {
        console.warn('Falling back to mock trends due to API error');
        return null; // Will use mock data as fallback
      }
    },

    // Collection Suggestions API
    generateCollectionSuggestions: async function(params) {
      try {
        return await fetchAPI('/suggestions', {
          method: 'POST',
          body: JSON.stringify(params),
        });
      } catch (error) {
        console.warn('Falling back to client-side suggestions');
        return null; // Will use client-side generation as fallback
      }
    },

    // Newsletter Signup
    subscribeNewsletter: async function(email) {
      try {
        return await fetchAPI('/subscribe', {
          method: 'POST',
          body: JSON.stringify({ email }),
        });
      } catch (error) {
        console.error('Newsletter subscription error:', error);
        throw error;
      }
    },

    // Report Request
    requestReport: async function(formData) {
      try {
        return await fetchAPI('/request-report', {
          method: 'POST',
          body: JSON.stringify(formData),
        });
      } catch (error) {
        console.error('Report request error:', error);
        throw error;
      }
    },

    // Download Report
    downloadReport: async function(template) {
      try {
        const response = await fetch(`${BASE_URL}/download-report/${template}`);
        if (!response.ok) {
          throw new Error(`Download failed: ${response.status}`);
        }
        // Create blob and trigger download
        const blob = await response.blob();
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `kalainayam-${template}-report.pdf`;
        document.body.appendChild(a);
        a.click();
        window.URL.revokeObjectURL(url);
        document.body.removeChild(a);
      } catch (error) {
        console.error('Report download error:', error);
        throw error;
      }
    },

    // Health check
    ping: async function() {
      try {
        return await fetchAPI('/health');
      } catch (error) {
        console.error('Health check failed:', error);
        return false;
      }
    },
  };
})();

// Export for use in modules if needed
if (typeof module !== 'undefined' && module.exports) {
  module.exports = API;
}
