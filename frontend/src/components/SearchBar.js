import React, { useState } from 'react';
import './SearchBar.css';

function SearchBar({ onSearch, loading }) {
  const [url, setUrl] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (url) {
      onSearch(url);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="search-bar">
      <input
        type="text"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        placeholder="Enter product review URL"
        disabled={loading}
      />
      <button type="submit" disabled={loading}>
        {loading ? 'Analyzing...' : 'Search'}
      </button>
    </form>
  );
}

export default SearchBar;
