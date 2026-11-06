const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const fs = require('fs');

const dbPath = process.env.DB_PATH ? path.resolve(process.env.DB_PATH) : path.resolve(__dirname, '../books.db');

// Ensure target directory exists if customized (e.g. /var/data on Render disk)
const dbDir = path.dirname(dbPath);
if (!fs.existsSync(dbDir)) {
  fs.mkdirSync(dbDir, { recursive: true });
}

const db = new sqlite3.Database(dbPath, (err) => {
  if (err) {
    console.error('Error connecting to SQLite database:', err.message);
  } else {
    console.log('Connected to SQLite database at:', dbPath);
  }
});

// Initialize database schema and default sample records
function initializeDatabase() {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run(
        `CREATE TABLE IF NOT EXISTS books (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          title TEXT NOT NULL,
          author TEXT NOT NULL,
          price REAL NOT NULL
        )`,
        (err) => {
          if (err) {
            console.error('Error creating books table:', err.message);
            return reject(err);
          }
        }
      );

      // Check if table has records, if not insert sample records
      db.get(`SELECT COUNT(*) AS count FROM books`, (err, row) => {
        if (err) {
          return reject(err);
        }
        if (row.count === 0) {
          console.log('Seeding initial sample book records...');
          seedSampleData().then(resolve).catch(reject);
        } else {
          console.log(`Database already contains ${row.count} book records.`);
          resolve();
        }
      });
    });
  });
}

function seedSampleData() {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run(`DELETE FROM books`);
      db.run(`DELETE FROM sqlite_sequence WHERE name = 'books'`);
      const insertStmt = db.prepare(
        `INSERT INTO books (id, title, author, price) VALUES (?, ?, ?, ?)`
      );
      const sampleBooks = [
        [1, 'Python Programming', 'John Smith', 450.0],
        [2, 'JavaScript: The Good Parts', 'Douglas Crockford', 350.0],
        [3, 'Clean Code', 'Robert C. Martin', 600.0],
        [4, 'Design Patterns', 'Erich Gamma', 750.0],
        [5, 'Node.js Design Patterns', 'Mario Casciaro', 520.0],
        [6, 'Learning SQL', 'Alan Beaulieu', 280.0],
        [7, 'Express in Action', 'Evan Hahn', 399.0],
        [8, 'Database Internals', 'Alex Petrov', 820.0],
        [9, 'Full Stack Development', 'David Flanagan', 480.0],
        [10, 'Modern Operating Systems', 'Andrew S. Tanenbaum', 950.0]
      ];

      sampleBooks.forEach((book) => {
        insertStmt.run(book[0], book[1], book[2], book[3]);
      });

      insertStmt.finalize((err) => {
        if (err) return reject(err);
        console.log('Database initialized and seeded with 10 sample books.');
        resolve();
      });
    });
  });
}

// Helper methods returning Promises for async/await clean controller code
const dbQuery = {
  all: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.all(sql, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });
  },
  get: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.get(sql, params, (err, row) => {
        if (err) reject(err);
        else resolve(row);
      });
    });
  },
  run: (sql, params = []) => {
    return new Promise((resolve, reject) => {
      db.run(sql, params, function (err) {
        if (err) reject(err);
        else resolve({ lastID: this.lastID, changes: this.changes });
      });
    });
  }
};

module.exports = {
  db,
  initializeDatabase,
  seedSampleData,
  dbQuery
};
