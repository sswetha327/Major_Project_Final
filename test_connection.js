const axios = require('axios');

async function testConnection() {
  try {
    console.log('Testing connection to backend...');
    const response = await axios.post('http://127.0.0.1:5000/analyze-product', { 
      url: 'https://example.com' 
    });
    console.log('Success! Response:', response.data.summary);
    console.log('Number of reviews:', response.data.reviews.length);
  } catch (error) {
    console.error('Error:', error.message);
    if (error.response) {
      console.error('Status:', error.response.status);
      console.error('Data:', error.response.data);
    }
  }
}

testConnection();
