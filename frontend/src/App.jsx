import React, { useState } from 'react';
import { Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { movieService } from './services/api';

// Components
import SearchBar from './components/SearchBar';
import MovieGrid from './components/MovieGrid';
import LoadingSpinner from './components/LoadingSpinner';

import './App.css';

function App() {
    const [results, setResults] = useState(null);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);
    const [inputMovie, setInputMovie] = useState('');

    const handleSearch = async (title) => {
        setLoading(true);
        setError(null);
        setInputMovie(title);

        try {
            const data = await movieService.getRecommendations(title);
            setResults(data);
        } catch (err) {
            setError(err);
            setResults(null);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="app">
            <header className="app-header container">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="logo-container"
                >
                    <Sparkles className="sparkle-icon" />
                    <h1 className="gradient-text">MovieMate</h1>
                </motion.div>
                <p className="subtitle">AI-powered movie recommendations based on content similarity</p>
            </header>

            <main className="container">
                <SearchBar onSearch={handleSearch} isLoading={loading} />

                <AnimatePresence mode="wait">
                    {loading ? (
                        <LoadingSpinner key="loading" />
                    ) : error ? (
                        <motion.div
                            key="error"
                            initial={{ opacity: 0, scale: 0.9 }}
                            animate={{ opacity: 1, scale: 1 }}
                            exit={{ opacity: 0 }}
                            className="error-box glass"
                        >
                            <p>⚠️ {error}</p>
                            <p className="tip">Try a different title or check for typos.</p>
                        </motion.div>
                    ) : results ? (
                        <motion.div
                            key="results"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="results-container"
                        >
                            <div className="results-header">
                                <h2>Movies similar to <span className="highlight">"{results.matched}"</span></h2>
                                <div className="stats">Found {results.recommendations.length} recommendations</div>
                            </div>

                            <MovieGrid movies={results.recommendations} />
                        </motion.div>
                    ) : (
                        <motion.div
                            key="empty"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="hero-section"
                        >
                            <div className="hero-content glass">
                                <h2>Find your next favorite movie</h2>
                                <p>We use PCA and K-Nearest Neighbors to find movies that share the same DNA as your favorites—genres, cast, keywords, and plot context.</p>
                                <div className="example-tags">
                                    <span>Inception</span>
                                    <span>Interstellar</span>
                                    <span>The Dark Knight</span>
                                    <span>Toy Story</span>
                                </div>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>

            <footer className="app-footer">
                <p>© 2026 MovieMate ML Engine. Powered by TMDB Data.</p>
            </footer>
        </div>
    );
}

export default App;
