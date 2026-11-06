const express = require('express');
const app = express();
const PORT = 3000;

app.get('/test', (req, res) => res.send('OK'));

const server = app.listen(PORT, () => {
  console.log(`Initial test server running on port ${PORT}`);
  // Attempting to listen again on the exact same port to trigger EADDRINUSE
  const conflictingApp = express();
  conflictingApp.listen(PORT, () => {
    console.log('Conflicting server opened unexpectedly.');
  });
});
