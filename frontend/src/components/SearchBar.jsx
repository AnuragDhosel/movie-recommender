import React, { useState } from 'react';
import { Search, Loader2 } from 'lucide-react';

const SearchBar = ({ onSearch, isLoading }) => {
    const [query, setQuery] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (query.trim()) onSearch(query);
    };

    return (
        <form onSubmit={handleSubmit} className="search-container animate-fade-in">
            <div className="search-wrapper glass">
                <Search className="search-icon" size={20} />
                <input
                    type="text"
                    placeholder="Enter a movie title (e.g., Inception)..."
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    disabled={isLoading}
                />
                <button type="submit" disabled={isLoading || !query.trim()}>
                    {isLoading ? <Loader2 className="animate-spin" size={20} /> : 'Recommend'}
                </button>
            </div>
        </form>
    );
};

export default SearchBar;
