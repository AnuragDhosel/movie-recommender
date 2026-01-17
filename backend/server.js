/**
 * Movie Recommendation Backend Server
 * 
 * Express.js API Gateway for the Movie Recommendation System
 */

import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import movieRoutes from './src/routes/movies.js';
import { errorHandler } from './src/utils/errorHandler.js';

// Load environment variables
dotenv.config();

// Initialize Express app
const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Request logging
app.use((req, res, next) => {
    console.log(`${new Date().toISOString()} - ${req.method} ${req.path}`);
    next();
});

// Routes
app.get('/', (req, res) => {
    res.json({
        message: '🎬 Movie Recommendation Backend API',
        version: '1.0.0',
        endpoints: {
            '/api/recommend': 'GET - Get movie recommendations (param: title)',
            '/api/search': 'GET - Search for movies (param: query)',
            '/api/health': 'GET - Health check'
        }
    });
});

app.use('/api', movieRoutes);

// 404 Handler
app.use((req, res) => {
    res.status(404).json({
        success: false,
        error: 'Endpoint not found'
    });
});

// Centralized Error Handler
app.use(errorHandler);

// Start server
app.listen(PORT, () => {
    console.log('='.repeat(60));
    console.log('🎬 Movie Recommendation Backend Server');
    console.log('='.repeat(60));
    console.log(`🌐 Server running on http://localhost:${PORT}`);
    console.log(`🔗 ML Service URL: ${process.env.ML_SERVICE_URL || 'http://localhost:5000'}`);
    console.log('='.repeat(60));
});
