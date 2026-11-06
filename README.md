# BDF Lab 3 – REST API Development and Validation

**Course:** Backend Development Fundamentals (BDF)  
**Course Code:** CSE-BDF-201  
**Institution:** Aurora University  
**Student Name:** Appampally Abhilash Reddy  
**Registration Number:** 252U1R5008  
**Faculty Evaluator:** Joel Prashanth D  
**Academic Year:** Year II, Term II (IV Semester)  

---

## 1. Project Introduction
This repository contains the complete, production-grade implementation of **Laboratory 03: REST API, Query Parameters, Validation, and Debugging** for Backend Development Fundamentals.

The project builds upon basic server architectures to deliver a RESTful Book Management web service backed by an embedded SQLite relational database (`books.db`), featuring comprehensive CRUD endpoints, dynamic search and filter parameters, defensive request body validation, standardized HTTP status code contracts, structured JSON response wrappers, and systematic root-cause debugging suites.

---

## 2. Experiment Objectives
- **RESTful Resource Modeling:** Design and implement intuitive, noun-based REST endpoints mapped to standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
- **Dynamic Query Parameters:** Support partial matching (`search_q`), multi-column sorting (`order_by`, `order`), pagination (`limit`, `offset`), and price ranges (`min_price`, `max_price`).
- **SQL Injection Prevention:** Enforce strict parameterization with `sqlite3` and column/order allowlists.
- **Defensive Input Validation:** Enforce schema validation returning `400 Bad Request` with descriptive error messages when required payload fields are missing or invalid.
- **HTTP Status Codes & Consistent JSON Envelopes:** Standardize responses using `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, and `500 Internal Server Error`.
- **Systematic Debugging:** Replicate, diagnose, and resolve four real-world backend defects (`EADDRINUSE`, `MODULE_NOT_FOUND`, `SQLITE_ERROR: no such table`, and missing `await`).
- **Automated Testing & Postman Verification:** Build automated test runners validating all 21 test scenarios.

---

## 3. Technologies Used
- **Runtime Environment:** Node.js (v24.16.0 LTS)
- **Web Framework:** Express.js (v4.21.2)
- **Database Engine:** SQLite3 (v5.1.7)
- **API Testing Tools:** Postman Collection v2.1, Native Node.js HTTP Test Suite
- **Version Control:** Git & GitHub

---

## 4. Project Folder Structure
```
BDF_LAB_03/
├── .env.example                                       # Environment template
├── .gitignore                                         # Git ignore configuration
├── BDF_Lab_03_Appampally_Abhilash_Reddy.zip           # Submission package
├── BDF_Lab_03_Complete_Report_Appampally_Abhilash_Reddy.docx # Academic lab report
├── books.db                                           # SQLite database with sample seed books
├── package.json                                       # Project dependencies & scripts
├── package-lock.json                                  # Dependency lock file
├── README.md                                          # Documentation
├── generate_screenshots.py                            # Screenshot generator utility
├── generate_word_report.py                            # Word report builder
├── src/
│   ├── app.js                                         # Express application configuration
│   ├── server.js                                      # HTTP server launcher
│   ├── database.js                                    # Database initialization, schema & seeders
│   ├── controllers/
│   │   └── bookController.js                          # CRUD business logic & query builder
│   ├── middleware/
│   │   └── errorHandler.js                            # Centralized 500 error & 404 handler
│   ├── routes/
│   │   └── bookRoutes.js                              # REST route declarations
│   └── utils/
│       └── validation.js                              # Request payload & query param validators
├── tests/
│   ├── api.test.js                                    # Automated 21-case test runner
│   └── test_results.json                              # Detailed JSON execution log
├── postman/
│   └── BDF_Lab_03_Postman_Collection.json             # Postman Collection v2.1
├── screenshots/                                       # 22 execution & debugging screenshots
└── debug_demos/                                       # Isolated scripts reproducing 4 debug defects
    ├── demo_eaddrinuse.js
    ├── demo_missing_await.js
    ├── demo_wrong_path.js
    └── demo_wrong_table.js
```

---

## 5. API Endpoints Specification

| Method | Endpoint | Description | Request Body | Status Codes |
|---|---|---|---|---|
| `GET` | `/` | API status and root information | None | `200` |
| `GET` | `/books` | Retrieve books with filter/sort/pagination | None | `200`, `400` |
| `GET` | `/books/:id` | Retrieve single book by primary key ID | None | `200`, `400`, `404` |
| `POST` | `/books` | Create a new book record | JSON: `title`, `author`, `price` | `201`, `400` |
| `PUT` | `/books/:id` | Update an existing book record | JSON: `title`, `author`, `price` | `200`, `400`, `404` |
| `DELETE` | `/books/:id` | Delete a book record by ID | None | `200`, `400`, `404` |

---

## 6. Query Parameters Documentation

The `GET /books` endpoint accepts the following query parameters:

| Parameter | Type | Default | Description / Constraints |
|---|---|---|---|
| `search_q` | String | `""` | Case-insensitive partial title search using SQL `LIKE '%term%'` |
| `order_by` | String | `"id"` | Column name to sort by: `id`, `title`, `author`, `price` (Allowlist guarded) |
| `order` | String | `"ASC"` | Sorting direction: `ASC` or `DESC` |
| `limit` | Integer | `10` | Maximum number of records to return (must be positive integer) |
| `offset` | Integer | `0` | Number of records to skip (must be non-negative integer) |
| `min_price` | Number | `undefined` | Lower price boundary (must be non-negative number) |
| `max_price` | Number | `undefined` | Upper price boundary (must be $\ge$ `min_price`) |

### Example Queries
- **Search by Title:** `GET /books?search_q=Clean`
- **Sort by Price Ascending:** `GET /books?order_by=price&order=ASC`
- **Sort by Price Descending:** `GET /books?order_by=price&order=DESC`
- **Pagination:** `GET /books?limit=3&offset=0`
- **Price Range Filter:** `GET /books?min_price=300&max_price=600`
- **Combined Query:** `GET /books?search_q=Design&order_by=price&order=ASC&limit=5&offset=0`

---

## 7. Request Body Validation Rules

When issuing `POST /books` or `PUT /books/:id`, the request body must satisfy:
1. `title`: Must be present, a non-empty string after trimming whitespace.
2. `author`: Must be present, a non-empty string after trimming whitespace.
3. `price`: Must be provided, non-null, a finite number, and $\ge 0$.

If any field fails validation, the API returns **HTTP 400 Bad Request**:
```json
{
  "message": "Title, author and valid numeric price are required"
}
```

---

## 8. HTTP Status Codes & Response Envelopes

- `200 OK`: Successful resource retrieval, update, or deletion.
- `201 Created`: Successful resource creation via `POST /books`.
- `400 Bad Request`: Payload validation failures or invalid query parameters.
- `404 Not Found`: Resource ID does not exist in the database, or endpoint does not exist.
- `500 Internal Server Error`: Unexpected server exceptions handled cleanly by middleware.

### Consistent JSON Format
**Successful GET /books:**
```json
{
  "message": "Books retrieved successfully",
  "count": 10,
  "data": [
    { "id": 1, "title": "Python Programming", "author": "John Smith", "price": 450 }
  ]
}
```

**Successful POST /books:**
```json
{
  "message": "Book created successfully",
  "data": {
    "id": 11,
    "title": "Mastering TypeScript",
    "author": "Boris Cherny",
    "price": 550
  }
}
```

---

## 9. Database Information
The project uses SQLite3 stored in `books.db`. The table schema is:
```sql
CREATE TABLE IF NOT EXISTS books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  price REAL NOT NULL
);
```
On initial boot or test execution, 10 sample computer science books are automatically seeded if the table is empty.

---

## 10. Installation & Running Instructions

### Prerequisites
- Node.js (v18.x or v24.x LTS)
- npm (v9.x or v11.x)
- Git

### 1. Clone the Repository
```bash
git clone https://github.com/abhilashreddy-sketch/BDF_LAB_03.git
cd BDF_LAB_03
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start the Server
```bash
npm start
```
The server will start listening on `http://localhost:3000`.

---

## 11. Automated Test Execution
Run the automated test runner verifying all 21 test scenarios:
```bash
npm test
```

### Automated Test Coverage (21/21 PASS)
| Test ID | Scenario | Expected | Status |
|---|---|---|---|
| `TC-01` | GET all books (initial fetch) | 200 OK | **PASS** |
| `TC-02` | GET existing book by ID | 200 OK | **PASS** |
| `TC-03` | GET non-existent book by ID | 404 Not Found | **PASS** |
| `TC-04` | POST valid book creation | 201 Created | **PASS** |
| `TC-05` | POST missing title validation | 400 Bad Request | **PASS** |
| `TC-06` | POST missing author validation | 400 Bad Request | **PASS** |
| `TC-07` | POST non-numeric price validation | 400 Bad Request | **PASS** |
| `TC-08` | PUT update existing book | 200 OK | **PASS** |
| `TC-09` | PUT non-existent book | 404 Not Found | **PASS** |
| `TC-10` | DELETE existing book | 200 OK | **PASS** |
| `TC-11` | DELETE non-existent book | 404 Not Found | **PASS** |
| `TC-12` | Search books by title (`search_q=Clean`) | 200 OK | **PASS** |
| `TC-13` | Sort books ascending (`order_by=price&order=ASC`) | 200 OK | **PASS** |
| `TC-14` | Sort books descending (`order_by=price&order=DESC`) | 200 OK | **PASS** |
| `TC-15` | Pagination with limit and offset (`limit=3&offset=0`) | 200 OK | **PASS** |
| `TC-16` | Filter by minimum price (`min_price=500`) | 200 OK | **PASS** |
| `TC-17` | Filter by maximum price (`max_price=400`) | 200 OK | **PASS** |
| `TC-18` | Combined price filter (`min_price=300&max_price=600`) | 200 OK | **PASS** |
| `TC-19` | Combined search, sort, and pagination | 200 OK | **PASS** |
| `TC-20` | Invalid sorting parameter validation | 400 Bad Request | **PASS** |
| `TC-21` | Invalid pagination limit validation | 400 Bad Request | **PASS** |

---

## 12. Postman Collection
An importable Postman Collection is located at:
```
postman/BDF_Lab_03_Postman_Collection.json
```
1. Open Postman.
2. Click **Import** $\rightarrow$ choose `postman/BDF_Lab_03_Postman_Collection.json`.
3. Collection variable `baseUrl` is pre-configured to `http://localhost:3000`.
4. Run requests individually or run all 21 requests using the Postman Collection Runner.

---

## 13. Debugging Exercises
The directory `debug_demos/` contains isolated scripts demonstrating four essential backend bugs:

1. **`demo_eaddrinuse.js` (EADDRINUSE):** Replicates port collisions when two servers bind to port 3000 simultaneously. Resolved via `netstat -ano | findstr :3000` and process termination.
2. **`demo_wrong_path.js` (MODULE_NOT_FOUND):** Replicates module path typos (`bookControler.js` vs `bookController.js`). Resolved with path normalization.
3. **`demo_wrong_table.js` (SQLITE_ERROR):** Replicates schema name mismatches (`book_store` vs `books`). Resolved by correcting the SQL identifier.
4. **`demo_missing_await.js` (Missing Await):** Replicates reading unresolved Promises returning `undefined`. Resolved by prepending `await` inside async controller functions.

---

## 14. Student Credentials
- **Student Name:** Appampally Abhilash Reddy
- **Registration Number:** 252U1R5008
- **Department:** Computer Science and Engineering
- **University:** Aurora University
- **Course:** Backend Development Fundamentals (CSE-BDF-201)
- **Academic Year:** 2025–2026
