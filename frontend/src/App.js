import React, { useState } from 'react';
import axios from 'axios';
import './App.css';
import SearchBar from './components/SearchBar';
import SentimentCounts from './components/SentimentCounts';
import Charts from './components/Charts';
import Reviews from './components/Reviews';

function App() {
  const [analysis, setAnalysis] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSearch = async (url) => {
    setLoading(true);
    setAnalysis(null);
    
    // Validate URL
    if (!url || !url.startsWith('http')) {
      alert('Please enter a valid URL starting with http:// or https://');
      setLoading(false);
      return;
    }
    
    try {
      const response = await axios.post('http://127.0.0.1:5001/analyze-product', { url });
      setAnalysis(response.data);
      
      // Check if we got mock data
      if (response.data.reviews && response.data.reviews.length > 0) {
        const firstReview = response.data.reviews[0].text;
        if (firstReview.includes("This product is absolutely amazing!") || 
            firstReview.includes("I'm quite disappointed")) {
          console.log('Note: Using demo data as real reviews could not be scraped');
        }
      }
    } catch (error) {
      console.error('Error analyzing product:', error);
      alert('Failed to analyze product. Please check:\n1. The URL is correct\n2. Backend is running on port 5001\n3. No CORS errors in console');
    }
    setLoading(false);
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>Product Sentiment Analyzer</h1>
      </header>
      <main>
        <SearchBar onSearch={handleSearch} loading={loading} />
        {loading && <p>Analyzing... Please wait.</p>}
        {analysis && (
          <>
            <SentimentCounts summary={analysis.summary} />
            <Charts summary={analysis.summary} />
            <Reviews reviews={analysis.reviews} />
            {analysis.reviews && analysis.reviews.length > 0 && 
             analysis.reviews[0].text.includes("This product is absolutely amazing") && (
              <div style={{marginTop: '20px', padding: '10px', backgroundColor: '#fff3cd', border: '1px solid #ffeaa7', borderRadius: '4px'}}>
                <p style={{margin: 0, color: '#856404'}}>
                  <strong>Note:</strong> Real reviews could not be scraped from the URL. 
                  Showing demo data for demonstration purposes.
                </p>
              </div>
            )}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
