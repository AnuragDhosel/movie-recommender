import React from 'react';
import MovieCard from './MovieCard';

const MovieGrid = ({ movies }) => {
    return (
        <div className="movie-grid">
            {movies.map((movie, idx) => (
                <MovieCard key={movie.tmdb_id || idx} movie={movie} index={idx} />
            ))}
        </div>
    );
};

export default MovieGrid;
