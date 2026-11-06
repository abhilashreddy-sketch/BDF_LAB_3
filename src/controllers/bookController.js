const { dbQuery } = require('../database');
const { validateBookPayload, validateQueryParams } = require('../utils/validation');

// GET /books - Retrieve books with search, filter, sort, pagination
async function getAllBooks(req, res, next) {
  try {
    // Validate query parameters
    const paramValidation = validateQueryParams(req.query);
    if (!paramValidation.isValid) {
      return res.status(400).json({
        message: paramValidation.errors.join('; ')
      });
    }

    const {
      search_q = '',
      order_by = 'id',
      order = 'ASC',
      limit = 10,
      offset = 0,
      min_price,
      max_price
    } = req.query;

    let sql = 'SELECT * FROM books WHERE 1=1';
    const params = [];

    // Search query using SQL LIKE
    if (search_q.trim() !== '') {
      sql += ' AND title LIKE ?';
      params.push(`%${search_q.trim()}%`);
    }

    // Min price filter
    if (min_price !== undefined) {
      sql += ' AND price >= ?';
      params.push(parseFloat(min_price));
    }

    // Max price filter
    if (max_price !== undefined) {
      sql += ' AND price <= ?';
      params.push(parseFloat(max_price));
    }

    // Safe SQL order by using allowlist
    const validOrderBy = ['id', 'title', 'author', 'price'].includes(order_by.toLowerCase())
      ? order_by.toLowerCase()
      : 'id';
    const validOrder = ['ASC', 'DESC'].includes(order.toUpperCase())
      ? order.toUpperCase()
      : 'ASC';

    sql += ` ORDER BY ${validOrderBy} ${validOrder}`;

    // Pagination limit & offset
    sql += ' LIMIT ? OFFSET ?';
    params.push(parseInt(limit, 10));
    params.push(parseInt(offset, 10));

    const books = await dbQuery.all(sql, params);

    res.status(200).json({
      message: 'Books retrieved successfully',
      count: books.length,
      data: books
    });
  } catch (error) {
    next(error);
  }
}

// GET /books/:id - Retrieve single book by ID
async function getBookById(req, res, next) {
  try {
    const { id } = req.params;
    const bookId = parseInt(id, 10);

    if (isNaN(bookId)) {
      return res.status(400).json({
        message: 'Invalid book ID format'
      });
    }

    const book = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);

    if (!book) {
      return res.status(404).json({
        message: 'Book not found'
      });
    }

    res.status(200).json({
      message: 'Book retrieved successfully',
      data: book
    });
  } catch (error) {
    next(error);
  }
}

// POST /books - Create new book
async function createBook(req, res, next) {
  try {
    const validation = validateBookPayload(req.body);
    if (!validation.isValid) {
      return res.status(400).json({
        message: validation.message
      });
    }

    const { title, author, price } = req.body;
    const result = await dbQuery.run(
      'INSERT INTO books (title, author, price) VALUES (?, ?, ?)',
      [title.trim(), author.trim(), parseFloat(price)]
    );

    const newBook = await dbQuery.get('SELECT * FROM books WHERE id = ?', [result.lastID]);

    res.status(201).json({
      message: 'Book created successfully',
      data: newBook
    });
  } catch (error) {
    next(error);
  }
}

// PUT /books/:id - Update existing book
async function updateBook(req, res, next) {
  try {
    const { id } = req.params;
    const bookId = parseInt(id, 10);

    if (isNaN(bookId)) {
      return res.status(400).json({
        message: 'Invalid book ID format'
      });
    }

    // Check if book exists
    const existing = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);
    if (!existing) {
      return res.status(404).json({
        message: 'Book not found'
      });
    }

    const validation = validateBookPayload(req.body);
    if (!validation.isValid) {
      return res.status(400).json({
        message: validation.message
      });
    }

    const { title, author, price } = req.body;
    await dbQuery.run(
      'UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?',
      [title.trim(), author.trim(), parseFloat(price), bookId]
    );

    const updatedBook = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);

    res.status(200).json({
      message: 'Book updated successfully',
      data: updatedBook
    });
  } catch (error) {
    next(error);
  }
}

// DELETE /books/:id - Delete book
async function deleteBook(req, res, next) {
  try {
    const { id } = req.params;
    const bookId = parseInt(id, 10);

    if (isNaN(bookId)) {
      return res.status(400).json({
        message: 'Invalid book ID format'
      });
    }

    // Check if book exists
    const existing = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);
    if (!existing) {
      return res.status(404).json({
        message: 'Book not found'
      });
    }

    await dbQuery.run('DELETE FROM books WHERE id = ?', [bookId]);

    res.status(200).json({
      message: 'Book deleted successfully',
      data: existing
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  getAllBooks,
  getBookById,
  createBook,
  updateBook,
  deleteBook
};
