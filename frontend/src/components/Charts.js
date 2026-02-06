import React from 'react';
import { Pie } from 'react-chartjs-2';
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js';
import './Charts.css';

ChartJS.register(ArcElement, Tooltip, Legend);

function Charts({ summary }) {
  if (!summary) {
    return null;
  }

  const data = {
    labels: ['Positive', 'Neutral', 'Negative'],
    datasets: [
      {
        data: [summary.Positive, summary.Neutral, summary.Negative],
        backgroundColor: ['#28a745', '#ffc107', '#dc3545'],
        hoverBackgroundColor: ['#218838', '#e0a800', '#c82333'],
      },
    ],
  };

  return (
    <div className="charts-container">
      <div className="chart">
        <h3>Sentiment Distribution</h3>
        <Pie data={data} />
      </div>
    </div>
  );
}

export default Charts;
