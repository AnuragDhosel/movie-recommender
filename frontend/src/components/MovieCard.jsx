import React from 'react';
import { motion } from 'framer-motion';
import { Film } from 'lucide-react';

const MovieCard = ({ movie, index }) => {
    return (
        <motion.div
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.3, delay: index * 0.1 }}
            className="movie-record glass"
        >
            <a
                href={movie.wiki_url || '#'}
                target="_blank"
                rel="noopener noreferrer"
                className="poster-link"
                title={`View ${movie.title} on Wikipedia`}
            >
                <div className="poster-container">
                    {movie.poster_url ? (
                        <img src={movie.poster_url} alt={movie.title} loading="lazy" />
                    ) : (
                        <div className="no-poster">
                            <Film size={48} />
                        </div>
                    )}
                    <div className="rating-badge">
                        {movie.vote_average ? movie.vote_average.toFixed(1) : 'N/A'}
                    </div>
                </div>
            </a>
            <div className="movie-info">
                <h3>{movie.title}</h3>
                {movie.distance !== undefined && (
                    <div className="match-score">
                        Similarity: {((1 - movie.distance) * 100).toFixed(0)}%
                    </div>
                )}
            </div>
        </motion.div>
    );
};

export default MovieCard;
