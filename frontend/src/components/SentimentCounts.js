import React from 'react';
import './SentimentCounts.css';

function SentimentCounts({ summary }) {
  if (!summary) {
    return null;
  }

  return (
    <div className="sentiment-counts">
      <div className="count positive">
        <h3>Positive</h3>
        <p>{summary.Positive}</p>
      </div>
      <div className="count neutral">
        <h3>Neutral</h3>
        <p>{summary.Neutral}</p>
      </div>
      <div className="count negative">
        <h3>Negative</h3>
        <p>{summary.Negative}</p>
      </div>
    </div>
  );
}

export default SentimentCounts;
