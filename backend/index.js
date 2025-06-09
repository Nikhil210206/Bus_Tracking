// index.js

const express = require('express');
const app = express();

// Basic route
app.get('/', (req, res) => {
  res.send('Bus Tracking Backend Running!');
});

// Start server
const PORT = 3000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
