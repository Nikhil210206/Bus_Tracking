// index.js
const express = require('express');
const cors = require('cors');
const app = express();
const PORT = 3000;

app.use(cors());
app.use(express.json()); // to read JSON body

// Temporary in-memory object to store locations
const busLocations = {};

// POST endpoint: Driver sends location
app.post('/location', (req, res) => {
  const { busNumber, lat, lng } = req.body;
  if (!busNumber || !lat || !lng) {
    return res.status(400).json({ error: 'Missing data' });
  }
  busLocations[busNumber] = { lat, lng };
  res.json({ message: 'Location updated successfully' });
});

// GET endpoint: Student requests location
app.get('/location/:busNumber', (req, res) => {
  const busNumber = req.params.busNumber;
  const location = busLocations[busNumber];
  if (!location) {
    return res.status(404).json({ error: 'Bus not found' });
  }
  res.json(location);
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
