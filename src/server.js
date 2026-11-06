const app = require('./app');
const { initializeDatabase } = require('./database');

const PORT = process.env.PORT || 3000;

async function startServer() {
  try {
    await initializeDatabase();
    const server = app.listen(PORT, () => {
      console.log(`====================================================`);
      console.log(`BDF Lab 03 REST API Server started successfully!`);
      console.log(`Server URL: http://localhost:${PORT}`);
      console.log(`API Base:   http://localhost:${PORT}/books`);
      console.log(`Time:       ${new Date().toLocaleString()}`);
      console.log(`====================================================`);
    });
    return server;
  } catch (err) {
    console.error('Failed to start server:', err);
    process.exit(1);
  }
}

if (require.main === module) {
  startServer();
}

module.exports = { startServer };
