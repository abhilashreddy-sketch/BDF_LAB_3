const express = require('express');
const bookRoutes = require('./routes/bookRoutes');
const { errorHandler, notFoundHandler } = require('./middleware/errorHandler');

const app = express();

// Request logging middleware for console audit
app.use((req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    const duration = Date.now() - start;
    console.log(`[${new Date().toISOString()}] ${req.method} ${req.originalUrl} -> ${res.statusCode} (${duration}ms)`);
  });
  next();
});

// JSON body parser middleware
app.use(express.json());

// Root test route
app.get('/', (req, res) => {
  res.status(200).json({
    message: 'Welcome to BDF Lab 3 Book Management REST API',
    endpoints: {
      getBooks: 'GET /books',
      getBookById: 'GET /books/:id',
      createBook: 'POST /books',
      updateBook: 'PUT /books/:id',
      deleteBook: 'DELETE /books/:id'
    },
    student: 'Appampally Abhilash Reddy (252U1R5008)',
    status: 'Operational'
  });
});

// Mount books resource routes
app.use('/books', bookRoutes);

// Catch-all 404 handler for unknown routes
app.use(notFoundHandler);

// Centralized error handler
app.use(errorHandler);

module.exports = app;
