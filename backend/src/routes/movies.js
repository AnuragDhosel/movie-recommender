/**
 * Movie Routes
 */

import express from 'express';
import movieController from '../controllers/movieController.js';

const router = express.Router();

// Get movie recommendations
router.get('/recommend', movieController.getRecommendations);

// Search for movies
router.get('/search', movieController.searchMovies);

// Health check
router.get('/health', movieController.healthCheck);

export default router;
