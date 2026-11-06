/**
 * Global Error Handler Middleware
 */
function errorHandler(err, req, res, next) {
  console.error('Unhandled Application Error:', err);

  // If response has already started sending
  if (res.headersSent) {
    return next(err);
  }

  const statusCode = err.statusCode || 500;
  const message = err.message || 'Internal Server Error';

  res.status(statusCode).json({
    message
  });
}

/**
 * 404 Route Not Found Middleware
 */
function notFoundHandler(req, res, next) {
  res.status(404).json({
    message: `Resource not found on endpoint: ${req.method} ${req.originalUrl}`
  });
}

module.exports = {
  errorHandler,
  notFoundHandler
};
