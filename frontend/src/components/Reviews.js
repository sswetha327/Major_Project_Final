import React from 'react';
import './Reviews.css';

function Reviews({ reviews }) {
  if (!reviews) {
    return null;
  }

  return (
    <div className="reviews-container">
      <h3>Customer Reviews</h3>
      <div className="reviews-list">
        {reviews.map((review, index) => (
          <div key={index} className={`review-item ${review.sentiment.toLowerCase()}`}>
            <p className="review-text">{review.text}</p>
            <p className="review-sentiment">Sentiment: {review.sentiment}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Reviews;
