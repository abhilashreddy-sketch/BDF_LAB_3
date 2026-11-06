# BDF Lab 3 – REST API Development, Validation and Deployment

**Course:** Backend Development Fundamentals (BDF)  
**Course Code:** CSE-BDF-201  
**Institution:** Aurora University  
**Student Name:** Appampally Abhilash Reddy  
**Registration Number:** 252U1R5008  
**Faculty Evaluator:** Joel Prashanth D  
**Academic Year:** Year II, Term II (IV Semester)  
**GitHub Repository:** [https://github.com/abhilashreddy-sketch/BDF_LAB_3](https://github.com/abhilashreddy-sketch/BDF_LAB_3)  
**Live Production API URL (Render):** [https://bdf-lab-3-1.onrender.com](https://bdf-lab-3-1.onrender.com)  

---

## 1. Project Introduction
This repository contains the complete, production-grade implementation of **Laboratory 03: REST API, Query Parameters, Validation, and Debugging** for Backend Development Fundamentals.

The project delivers a RESTful Book Management web service backed by SQLite relational database storage, deployed publicly on Render's cloud infrastructure. It implements full CRUD operations, multi-parameter search and filter controls, defensive request body validation, standardized HTTP status code contracts, structured JSON responses, and isolated backend debugging demonstration suites.

---

## 2. Experiment Objectives
- **RESTful Resource Modeling:** Construct intuitive, noun-based REST endpoints mapped to standard HTTP verbs (`GET`, `POST`, `PUT`, `DELETE`).
- **Dynamic Query Parameters:** Support partial matching (`search_q`), multi-column sorting (`order_by`, `order`), pagination (`limit`, `offset`), and price ranges (`min_price`, `max_price`).
- **SQL Injection Prevention:** Enforce parameterization with `sqlite3` and column/order allowlists.
- **Defensive Input Validation:** Enforce schema validation returning `400 Bad Request` with descriptive error messages when required payload fields are missing or invalid.
- **HTTP Status Codes & Consistent JSON Envelopes:** Standardize responses using `200 OK`, `201 Created`, `400 Bad Request`, `404 Not Found`, and `500 Internal Server Error`.
- **Systematic Debugging:** Replicate, diagnose, and resolve four real-world backend defects (`EADDRINUSE`, `MODULE_NOT_FOUND`, `SQLITE_ERROR: no such table`, and missing `await`).
- **Automated Testing & Postman Verification:** Build automated test runners validating all 21 test scenarios.
- **Production Deployment:** Host the web service live on Render with `0.0.0.0` network binding and dynamic port configuration.

---

## 3. Technologies Used
- **Runtime Environment:** Node.js (v24.16.0 LTS)
- **Web Framework:** Express.js (v4.21.2)
- **Database Engine:** SQLite3 (v5.1.7)
- **Cloud Hosting Platform:** Render (Web Service: `BDF_LAB_3-1`)
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
├── screenshots/                                       # Execution, Postman, and actual user screenshots
└── debug_demos/                                       # Isolated scripts reproducing 4 debug defects
    ├── demo_eaddrinuse.js
    ├── demo_missing_await.js
    ├── demo_wrong_path.js
    └── demo_wrong_table.js
```

---

## 5. Live Production API Endpoints (Render)

**Base URL:** `https://bdf-lab-3-1.onrender.com`

| Method | Endpoint | Description | Request Body | Status Codes |
|---|---|---|---|---|
| `GET` | `/books` | Retrieve books with filter/sort/pagination | None | `200`, `400` |
| `GET` | `/books/:id` | Retrieve single book by primary key ID | None | `200`, `400`, `404` |
| `POST` | `/books` | Create a new book record | JSON: `title`, `author`, `price`, `pages` | `201`, `400` |
| `PUT` | `/books/:id` | Update an existing book record | JSON: `title`, `author`, `price`, `pages` | `200`, `400`, `404` |
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

### Example Live Queries
- **GET All Books:** [https://bdf-lab-3-1.onrender.com/books](https://bdf-lab-3-1.onrender.com/books)
- **Search by Title:** [https://bdf-lab-3-1.onrender.com/books?search_q=Clean](https://bdf-lab-3-1.onrender.com/books?search_q=Clean)
- **Sort by Price Ascending:** [https://bdf-lab-3-1.onrender.com/books?order_by=price&order=ASC](https://bdf-lab-3-1.onrender.com/books?order_by=price&order=ASC)
- **Sort by Price Descending:** [https://bdf-lab-3-1.onrender.com/books?order_by=price&order=DESC](https://bdf-lab-3-1.onrender.com/books?order_by=price&order=DESC)
- **Pagination (Limit 3, Offset 0):** [https://bdf-lab-3-1.onrender.com/books?limit=3&offset=0](https://bdf-lab-3-1.onrender.com/books?limit=3&offset=0)
- **Price Range Filter (₹100 to ₹300):** [https://bdf-lab-3-1.onrender.com/books?min_price=100&max_price=300](https://bdf-lab-3-1.onrender.com/books?min_price=100&max_price=300)

---

## 7. Request Body Validation Rules

When issuing `POST /books` or `PUT /books/:id`, the request body must satisfy:
1. `title`: Must be present, a non-empty string after trimming whitespace.
2. `author`: Must be present, a non-empty string after trimming whitespace.
3. `price`: Must be provided, non-null, a finite number, and $\ge 0$.

If any required field is missing or invalid, the API returns **HTTP 400 Bad Request**:
```json
{
  "message": "Title, author and valid numeric price are required"
}
```

---

## 8. HTTP Status Codes
- `200 OK`: Successful resource retrieval, update, or deletion.
- `201 Created`: Successful resource creation via `POST /books`.
- `400 Bad Request`: Payload validation failures or invalid query parameters.
- `404 Not Found`: Resource ID does not exist in the database, or endpoint does not exist.
- `500 Internal Server Error`: Unexpected server exceptions handled cleanly by middleware.

---

## 9. Database Information & Persistence
The project uses SQLite3. On Render:
- The free tier filesystem is ephemeral; records reset to the initial seed dataset on cold restarts or redeployments.
- For permanent cloud persistence across container restarts, Render supports mounting a Persistent Disk (`/var/data`), configured seamlessly via the `DB_PATH=/var/data/books.db` environment variable.

---

## 10. Local Installation & Testing Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/abhilashreddy-sketch/BDF_LAB_3.git
cd BDF_LAB_3
```

### 2. Install Dependencies
```bash
npm install
```

### 3. Start the Server Locally
```bash
npm start
```
The server will start listening on `http://localhost:3000`.

### 4. Run Automated Test Suite
```bash
npm test
```
Executes all 21 test scenarios with 100% pass verification.

---

## 11. Postman Collection
An importable Postman Collection is located at:
```
postman/BDF_Lab_03_Postman_Collection.json
```
1. Open Postman.
2. Click **Import** $\rightarrow$ choose `postman/BDF_Lab_03_Postman_Collection.json`.
3. Set the collection variable `baseUrl` to `https://bdf-lab-3-1.onrender.com` (for live testing) or `http://localhost:3000` (for local testing).
4. Run requests individually or run all 21 requests using the Postman Collection Runner.

---

## 12. Screenshot Documentation
The `screenshots/` directory contains complete visual evidence:
- **Project Setup & Server:** Folder structure, npm dependencies, Express server startup, SQLite database creation.
- **REST CRUD Operations:** Postman outputs for GET all, GET by ID, POST, PUT, DELETE with exact HTTP status codes.
- **Query Parameters:** Title search (`search_q`), sorting (`order_by`, `order`), pagination (`limit`, `offset`), price range filtering (`min_price`, `max_price`).
- **Validation Rejection:** HTTP 400 rejections for missing title, missing author, non-numeric price.
- **Resource 404:** Non-existent ID handling.
- **Debugging Suites:** Terminal outputs for `EADDRINUSE`, `MODULE_NOT_FOUND`, `SQLITE_ERROR: no such table`, and missing `await`.
- **Actual User Screenshots:** Actual execution captures from development and testing.

---

## 13. Student Credentials
- **Student Name:** Appampally Abhilash Reddy
- **Registration Number:** 252U1R5008
- **Department:** Computer Science and Engineering
- **University:** Aurora University
- **Course:** Backend Development Fundamentals (CSE-BDF-201)
- **Academic Year:** 2025–2026
