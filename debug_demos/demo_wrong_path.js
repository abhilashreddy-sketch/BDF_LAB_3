// Demonstrating Module Not Found error with misspelled import path
console.log('Attempting to import from non-existent path: ./controllers/bookControler.js');
const bookController = require('./controllers/bookControler.js');
