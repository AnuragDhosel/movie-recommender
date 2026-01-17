/**
 * ML Service Integration
 * 
 * This service communicates with the Flask ML service
 */

import axios from 'axios';

const ML_SERVICE_URL = process.env.ML_SERVICE_URL || 'http://localhost:5000';

class MLService {
  /**
   * Get movie recommendations
   */
  async getRecommendations(movieTitle) {
    try {
      const response = await axios.get(`${ML_SERVICE_URL}/api/recommend`, {
        params: { title: movieTitle },
        timeout: 10000 // 10 second timeout
      });
      
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('ML Service Error:', error.message);
      
      if (error.response) {
        // The request was made and the server responded with a status code
        // that falls out of the range of 2xx
        return {
          success: false,
          error: error.response.data.error || 'Failed to get recommendations',
          status: error.response.status
        };
      } else if (error.request) {
        // The request was made but no response was received
        return {
          success: false,
          error: 'ML service is not responding. Please ensure Flask server is running.',
          status: 503
        };
      } else {
        // Something happened in setting up the request
        return {
          success: false,
          error: error.message,
          status: 500
        };
      }
    }
  }

  /**
   * Search for movies
   */
  async searchMovies(query) {
    try {
      const response = await axios.get(`${ML_SERVICE_URL}/api/search`, {
        params: { query },
        timeout: 5000
      });
      
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      console.error('ML Service Search Error:', error.message);
      
      if (error.response) {
        return {
          success: false,
          error: error.response.data.error || 'Search failed',
          status: error.response.status
        };
      } else {
        return {
          success: false,
          error: 'ML service is not responding',
          status: 503
        };
      }
    }
  }

  /**
   * Check ML service health
   */
  async checkHealth() {
    try {
      const response = await axios.get(`${ML_SERVICE_URL}/api/health`, {
        timeout: 3000
      });
      
      return {
        success: true,
        data: response.data
      };
    } catch (error) {
      return {
        success: false,
        error: 'ML service is down'
      };
    }
  }
}

export default new MLService();
