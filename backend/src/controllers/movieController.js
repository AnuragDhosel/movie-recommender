/**
 * Movie Controller
 * 
 * Handles movie recommendation requests
 */

import mlService from '../services/mlService.js';

class MovieController {
    /**
     * Get movie recommendations
     */
    async getRecommendations(req, res) {
        try {
            const { title } = req.query;

            // Validation
            if (!title || title.trim() === '') {
                return res.status(400).json({
                    success: false,
                    error: 'Please provide a movie title'
                });
            }

            // Call ML service
            const result = await mlService.getRecommendations(title);

            if (!result.success) {
                return res.status(result.status || 500).json({
                    success: false,
                    error: result.error
                });
            }

            // Return recommendations
            return res.status(200).json({
                success: true,
                ...result.data
            });

        } catch (error) {
            console.error('Controller Error:', error);
            return res.status(500).json({
                success: false,
                error: 'Internal server error'
            });
        }
    }

    /**
     * Search for movies
     */
    async searchMovies(req, res) {
        try {
            const { query } = req.query;

            if (!query || query.trim().length < 2) {
                return res.status(400).json({
                    success: false,
                    error: 'Search query must be at least 2 characters'
                });
            }

            const result = await mlService.searchMovies(query);

            if (!result.success) {
                return res.status(result.status || 500).json({
                    success: false,
                    error: result.error
                });
            }

            return res.status(200).json({
                success: true,
                ...result.data
            });

        } catch (error) {
            console.error('Search Controller Error:', error);
            return res.status(500).json({
                success: false,
                error: 'Internal server error'
            });
        }
    }

    /**
     * Health check
     */
    async healthCheck(req, res) {
        try {
            const mlHealth = await mlService.checkHealth();

            return res.status(200).json({
                success: true,
                backend: 'healthy',
                mlService: mlHealth.success ? 'healthy' : 'down',
                mlServiceDetails: mlHealth.data || null
            });

        } catch (error) {
            return res.status(500).json({
                success: false,
                backend: 'error',
                mlService: 'unknown'
            });
        }
    }
}

export default new MovieController();
