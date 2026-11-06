/**
 * Request validation utilities for BDF Lab 03
 */

function validateBookPayload(body) {
  const { title, author, price } = body;

  // Title must be present, a string, and non-empty after trim
  if (!title || typeof title !== 'string' || title.trim() === '') {
    return {
      isValid: false,
      message: 'Title, author and valid numeric price are required'
    };
  }

  // Author must be present, a string, and non-empty after trim
  if (!author || typeof author !== 'string' || author.trim() === '') {
    return {
      isValid: false,
      message: 'Title, author and valid numeric price are required'
    };
  }

  // Price must be provided, non-null, and a valid finite number >= 0
  if (
    price === undefined ||
    price === null ||
    typeof price !== 'number' ||
    isNaN(price) ||
    price < 0
  ) {
    return {
      isValid: false,
      message: 'Title, author and valid numeric price are required'
    };
  }

  return { isValid: true };
}

function validateQueryParams(query) {
  const allowedSortColumns = ['id', 'title', 'author', 'price'];
  const allowedOrders = ['ASC', 'DESC'];

  const errors = [];

  // Validate order_by if supplied
  if (query.order_by) {
    const col = query.order_by.toLowerCase();
    if (!allowedSortColumns.includes(col)) {
      errors.push(`Invalid order_by parameter '${query.order_by}'. Allowed columns: ${allowedSortColumns.join(', ')}`);
    }
  }

  // Validate order if supplied
  if (query.order) {
    const ord = query.order.toUpperCase();
    if (!allowedOrders.includes(ord)) {
      errors.push(`Invalid order parameter '${query.order}'. Allowed values: ASC, DESC`);
    }
  }

  // Validate limit if supplied
  if (query.limit !== undefined) {
    const limitNum = parseInt(query.limit, 10);
    if (isNaN(limitNum) || limitNum <= 0) {
      errors.push("Invalid limit parameter. Must be a positive integer.");
    }
  }

  // Validate offset if supplied
  if (query.offset !== undefined) {
    const offsetNum = parseInt(query.offset, 10);
    if (isNaN(offsetNum) || offsetNum < 0) {
      errors.push("Invalid offset parameter. Must be a non-negative integer.");
    }
  }

  // Validate min_price if supplied
  if (query.min_price !== undefined) {
    const minP = parseFloat(query.min_price);
    if (isNaN(minP) || minP < 0) {
      errors.push("Invalid min_price parameter. Must be a non-negative number.");
    }
  }

  // Validate max_price if supplied
  if (query.max_price !== undefined) {
    const maxP = parseFloat(query.max_price);
    if (isNaN(maxP) || maxP < 0) {
      errors.push("Invalid max_price parameter. Must be a non-negative number.");
    }
  }

  if (query.min_price !== undefined && query.max_price !== undefined) {
    const minP = parseFloat(query.min_price);
    const maxP = parseFloat(query.max_price);
    if (!isNaN(minP) && !isNaN(maxP) && minP > maxP) {
      errors.push("min_price cannot be greater than max_price.");
    }
  }

  return {
    isValid: errors.length === 0,
    errors
  };
}

module.exports = {
  validateBookPayload,
  validateQueryParams
};
