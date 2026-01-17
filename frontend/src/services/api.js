import axios from 'axios';

const API_BASE_URL = 'http://localhost:3000/api';

const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 15000,
});

export const movieService = {
    getRecommendations: async (title) => {
        try {
            const response = await api.get('/recommend', { params: { title } });
            return response.data;
        } catch (error) {
            throw error.response?.data?.error || 'Failed to fetch recommendations';
        }
    },

    searchMovies: async (query) => {
        try {
            const response = await api.get('/search', { params: { query } });
            return response.data;
        } catch (error) {
            throw error.response?.data?.error || 'Search failed';
        }
    },

    checkHealth: async () => {
        try {
            const response = await api.get('/health');
            return response.data;
        } catch (error) {
            return { success: false, backend: 'down' };
        }
    }
};

export default api;
