const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, '../books.db');
const db = new sqlite3.Database(dbPath);

console.log('Querying non-existent table "book_store"...');
db.all('SELECT * FROM book_store', [], (err, rows) => {
  if (err) {
    console.error('SQLite Execution Error:', err.message);
  } else {
    console.log('Rows:', rows);
  }
  db.close();
});
