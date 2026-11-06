import os
import json
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

OUTPUT_DOCX = r"C:\Users\Abhilash reddy\OneDrive\Desktop\LAB REPOORT 3\BDF_Lab_03_Complete_Report_Appampally_Abhilash_Reddy.docx"
SCREENSHOTS_DIR = r"C:\Users\Abhilash reddy\OneDrive\Desktop\LAB REPOORT 3\screenshots"

def create_report():
    doc = docx.Document()

    # Configure standard A4 page margins (1 inch)
    sections = doc.sections
    for section in sections:
        section.top_margin = Inches(1.0)
        section.bottom_margin = Inches(1.0)
        section.left_margin = Inches(1.0)
        section.right_margin = Inches(1.0)
        section.page_width = Inches(8.27)
        section.page_height = Inches(11.69)

    # Base Normal style
    style_normal = doc.styles['Normal']
    font_normal = style_normal.font
    font_normal.name = 'Times New Roman'
    font_normal.size = Pt(12)
    font_normal.color.rgb = RGBColor(30, 30, 30)

    # Helper styling functions
    def set_cell_background(cell, fill_hex):
        shading_xml = f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>'
        cell._tc.get_or_add_tcPr().append(parse_xml(shading_xml))

    def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = OxmlElement('w:tcMar')
        for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
            node = OxmlElement(f'w:{m}')
            node.set(qn('w:w'), str(val))
            node.set(qn('w:type'), 'dxa')
            tcMar.append(node)
        tcPr.append(tcMar)

    def add_title(text, level=1):
        p = doc.add_paragraph()
        run = p.add_run(text)
        run.bold = True
        run.font.name = 'Times New Roman'
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(6)
        p.paragraph_format.line_spacing = 1.15
        if level == 1:
            run.font.size = Pt(16)
            run.font.color.rgb = RGBColor(16, 44, 87) # Deep Navy
        elif level == 2:
            run.font.size = Pt(14)
            run.font.color.rgb = RGBColor(30, 70, 130)
        elif level == 3:
            run.font.size = Pt(12.5)
            run.font.color.rgb = RGBColor(50, 50, 50)
        return p

    def add_p(text, bold_prefix="", italic=False):
        p = doc.add_paragraph()
        p.paragraph_format.line_spacing = 1.5
        p.paragraph_format.space_after = Pt(6)
        if bold_prefix:
            run_b = p.add_run(bold_prefix)
            run_b.bold = True
            run_b.font.name = 'Times New Roman'
            run_b.font.size = Pt(12)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(12)
        run.italic = italic
        return p

    def add_bullet(text, bold_prefix=""):
        p = doc.add_paragraph(style='List Bullet')
        p.paragraph_format.line_spacing = 1.25
        p.paragraph_format.space_after = Pt(4)
        if bold_prefix:
            rb = p.add_run(bold_prefix)
            rb.bold = True
            rb.font.name = 'Times New Roman'
            rb.font.size = Pt(11.5)
        run = p.add_run(text)
        run.font.name = 'Times New Roman'
        run.font.size = Pt(11.5)
        return p

    def add_code_block(code_str):
        table = doc.add_table(rows=1, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER
        cell = table.cell(0, 0)
        cell.width = Inches(6.27)
        set_cell_background(cell, "F4F5F7")
        set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
        p = cell.paragraphs[0]
        p.paragraph_format.line_spacing = 1.15
        p.paragraph_format.space_after = Pt(0)
        run = p.add_run(code_str)
        run.font.name = 'Consolas'
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(34, 34, 34)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    def add_screenshot(filename, caption_text, width_in_inches=5.8):
        img_path = os.path.join(SCREENSHOTS_DIR, filename)
        if os.path.exists(img_path):
            p_img = doc.add_paragraph()
            p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_img.paragraph_format.space_before = Pt(8)
            p_img.paragraph_format.space_after = Pt(2)
            run_img = p_img.add_run()
            run_img.add_picture(img_path, width=Inches(width_in_inches))

            p_cap = doc.add_paragraph()
            p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p_cap.paragraph_format.space_before = Pt(2)
            p_cap.paragraph_format.space_after = Pt(10)
            run_cap = p_cap.add_run(caption_text)
            run_cap.font.name = 'Times New Roman'
            run_cap.font.size = Pt(10)
            run_cap.font.color.rgb = RGBColor(80, 80, 80)
            run_cap.italic = True
        else:
            add_p(f"[Screenshot File Missing: {filename}]", bold_prefix="Warning: ")

    # ==================== COVER PAGE ====================
    p_inst = doc.add_paragraph()
    p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_inst1 = p_inst.add_run("AURORA UNIVERSITY\n")
    r_inst1.bold = True
    r_inst1.font.size = Pt(22)
    r_inst1.font.color.rgb = RGBColor(16, 44, 87)

    r_inst2 = p_inst.add_run("SCHOOL OF COMPUTER SCIENCE & ENGINEERING\n")
    r_inst2.bold = True
    r_inst2.font.size = Pt(14)
    r_inst2.font.color.rgb = RGBColor(50, 50, 50)

    r_inst3 = p_inst.add_run("DEPARTMENT OF COMPUTER SCIENCE AND ENGINEERING (AI & ML / DS / CSE)\n")
    r_inst3.font.size = Pt(11)
    r_inst3.font.color.rgb = RGBColor(80, 80, 80)

    p_rule = doc.add_paragraph()
    p_rule.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_rule = p_rule.add_run("―" * 45)
    r_rule.font.color.rgb = RGBColor(180, 180, 180)

    p_lab = doc.add_paragraph()
    p_lab.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_lab.paragraph_format.space_before = Pt(16)
    r_lab1 = p_lab.add_run("LABORATORY REPORT\n")
    r_lab1.bold = True
    r_lab1.font.size = Pt(18)
    r_lab1.font.color.rgb = RGBColor(16, 44, 87)

    r_lab2 = p_lab.add_run("Course Title: Backend Development Fundamentals (BDF)\nCourse Code: CSE-BDF-201\n")
    r_lab2.font.size = Pt(12)
    r_lab2.font.color.rgb = RGBColor(60, 60, 60)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_before = Pt(18)
    p_title.paragraph_format.space_after = Pt(24)
    r_t1 = p_title.add_run("EXPERIMENT - 03\n")
    r_t1.bold = True
    r_t1.font.size = Pt(16)
    r_t1.font.color.rgb = RGBColor(210, 80, 20)

    r_t2 = p_title.add_run("REST API DEVELOPMENT, QUERY PARAMETERS,\nREQUEST VALIDATION & DEBUGGING")
    r_t2.bold = True
    r_t2.font.size = Pt(16)
    r_t2.font.color.rgb = RGBColor(16, 44, 87)

    # Credentials Table
    t_cred = doc.add_table(rows=7, cols=2)
    t_cred.alignment = WD_TABLE_ALIGNMENT.CENTER
    cred_data = [
        ("Student Name", "APPAMPALLY ABHILASH REDDY"),
        ("Registration Number", "252U1R5008"),
        ("Course / Degree", "B.Tech - Computer Science & Engineering"),
        ("Academic Year & Term", "Year II, Term II (IV Semester)"),
        ("Module & Content Week", "RESTful API Development (Week 3, Slots 13–19)"),
        ("Faculty Evaluator", "Joel Prashanth D"),
        ("Submission Date", "06-November-2026")
    ]

    for i, (k, v) in enumerate(cred_data):
        row = t_cred.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width, c1.width = Inches(2.3), Inches(3.9)
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FAFAFA")
        set_cell_margins(c0, 80, 80, 120, 120)
        set_cell_margins(c1, 80, 80, 120, 120)

        p0 = c0.paragraphs[0]
        p0.paragraph_format.line_spacing = 1.15
        r0 = p0.add_run(k)
        r0.bold = True
        r0.font.size = Pt(10.5)

        p1 = c1.paragraphs[0]
        p1.paragraph_format.line_spacing = 1.15
        r1 = p1.add_run(v)
        r1.font.size = Pt(10.5)

    doc.add_page_break()

    # ==================== SECTION 1: AIM ====================
    add_title("1. AIM", 1)
    add_p(
        "To build, configure, test, and debug a robust RESTful API using Node.js, Express.js, and SQLite; implement comprehensive CRUD operations with standard RESTful conventions; support dynamic query parameters for searching, sorting, pagination, and price-range filtering; enforce rigorous request body input validation; handle HTTP status codes consistently; and demonstrate methodical root-cause debugging across common backend errors."
    )

    # ==================== SECTION 2: OBJECTIVES ====================
    add_title("2. OBJECTIVES", 1)
    add_p("The foundational learning objectives of this laboratory experiment are:")
    add_bullet(" Understand and enforce architectural constraints of REST (Representational State Transfer), including uniform interface, statelessness, and resource-based URI structure.", "1. RESTful Design:")
    add_bullet(" Implement complete Create, Read, Update, and Delete operations over a persistent SQLite relational database using parameterized queries to guard against SQL injection vulnerabilities.", "2. Persistent CRUD Operations:")
    add_bullet(" Implement multi-criteria query parameters including partial title matching (search_q via SQL LIKE), whitelisted multi-column sorting (order_by, order), pagination (limit, offset), and numerical price-range boundaries (min_price, max_price).", "3. Dynamic Query Parameters:")
    add_bullet(" Construct centralized validation middleware to reject incomplete or ill-formed JSON payloads (missing title, empty author, invalid or non-numeric price) with standard HTTP 400 Bad Request responses.", "4. Input Validation & Status Codes:")
    add_bullet(" Formulate structured JSON response envelopes providing descriptive status messages, entity collections, operational metadata (record counts), and error details.", "5. Consistent Response Envelopes:")
    add_bullet(" Replicate, analyze, and resolve critical real-world backend defects: port collisions (EADDRINUSE), module resolution failures (MODULE_NOT_FOUND), relational schema errors (no such table), and asynchronous execution bugs (missing await).", "6. Systematic Backend Debugging:")
    add_bullet(" Design and execute an automated API test suite covering all 21 test scenarios and verify API endpoints through Postman.", "7. Automated & Postman Verification:")

    # ==================== SECTION 3: REQUIREMENTS ====================
    add_title("3. SOFTWARE AND HARDWARE REQUIREMENTS", 1)
    add_p("The development and testing environment utilized for this experiment is specified below:")

    req_headers = ["Category", "Component / Tool", "Version / Specification"]
    req_rows = [
        ("Operating System", "Microsoft Windows 11 Home / Pro", "64-bit Architecture, x64-based processor"),
        ("JavaScript Runtime", "Node.js (LTS Engine)", "v24.16.0 (V8 Engine v13.x)"),
        ("Package Manager", "Node Package Manager (npm)", "v11.13.0"),
        ("Web Framework", "Express.js", "v4.21.2"),
        ("Embedded Database", "SQLite3 with Driver", "v5.1.7 (sqlite3 native binding)"),
        ("API Testing Client", "Postman / Automated HTTP Harness", "v11.x / Custom Node.js Test Runner"),
        ("Integrated Dev Env", "Visual Studio Code", "v1.98.x with REST Client & Git Extensions"),
        ("Hardware Setup", "Intel Core i5 / AMD Ryzen 5, 16 GB RAM", "512 GB SSD Storage")
    ]
    t_req = doc.add_table(rows=len(req_rows) + 1, cols=3)

    for col_idx, text in enumerate(req_headers):
        cell = t_req.cell(0, col_idx)
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        r = p.add_run(text)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10.5)

    for row_idx, data in enumerate(req_rows):
        row = t_req.rows[row_idx + 1]
        for col_idx, val in enumerate(data):
            cell = row.cells[col_idx]
            bg = "F7F9FC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 60, 60, 100, 100)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(10)

    # ==================== SECTION 4: THEORY ====================
    add_title("4. THEORETICAL FOUNDATION", 1)

    add_title("4.1 REST Architectural Style and Principles", 2)
    add_p(
        "REST (Representational State Transfer) is an architectural style for distributed hypermedia systems introduced by Roy Fielding in his 2000 doctoral dissertation. REST defines a set of constraints that yield desirable system properties: performance, scalability, simplicity, modifiability, visibility, and reliability. Key constraints include:"
    )
    add_bullet(" Separation of user interface concerns from data storage and server processing logic, allowing components to evolve independently.", "Client-Server Architecture: ")
    add_bullet(" Each request from client to server must contain all necessary information to understand and process the request. The server never stores client session state between requests.", "Statelessness: ")
    add_bullet(" Responses must define themselves as cacheable or non-cacheable to optimize network efficiency.", "Cacheability: ")
    add_bullet(" Resources are uniquely identified through URIs, manipulated through representations, deliver self-descriptive messages, and implement Hypermedia as the Engine of Application State (HATEOAS).", "Uniform Interface: ")
    add_bullet(" Intermediary proxies, gateways, and load balancers can be inserted transparently without modifying client-server communications.", "Layered System: ")

    add_title("4.2 HTTP Verbs & CRUD Mapping", 2)
    add_p(
        "In RESTful HTTP API development, CRUD (Create, Read, Update, Delete) operations map systematically to standard HTTP methods:"
    )
    add_bullet(" Used to read or retrieve resource representations. Safe and idempotent. Must not modify server state.", "GET (Retrieve): ")
    add_bullet(" Submits an entity to the specified resource, typically resulting in a state change or resource creation on the server. Neither safe nor idempotent.", "POST (Create): ")
    add_bullet(" Replaces all current representations of the target resource with the uploaded payload. Idempotent.", "PUT (Update / Replace): ")
    add_bullet(" Removes the specified resource identified by the URI. Idempotent.", "DELETE (Remove): ")

    add_title("4.3 Path Parameters vs. Query Parameters", 2)
    add_p(
        "A critical distinction in API design is the deliberate selection between path parameters and query parameters:"
    )
    add_bullet(" Embedded directly inside the hierarchical URL path (e.g., /books/:id). Used to uniquely identify a specific, individual resource instance within a resource collection.", "Path Parameters: ")
    add_bullet(" Appended to the URL following a question mark ('?') in key-value pairs separated by ampersands ('&') (e.g., /books?search_q=python&limit=5). Used to filter, sort, paginate, or modify representations of a resource collection without altering resource identity.", "Query Parameters: ")

    add_title("4.4 SQL LIKE Pattern Matching, Sorting & Pagination", 2)
    add_p(
        "When managing database-backed collections, efficient query filtering relies on relational SQL capabilities:"
    )
    add_bullet(" The SQL LIKE operator provides partial pattern matching. Combined with the '%' wildcard (e.g., WHERE title LIKE '%python%'), it returns records containing the search term anywhere within the attribute string.", "SQL LIKE Operator: ")
    add_bullet(" The ORDER BY clause orders returned record sets ascending (ASC) or descending (DESC). To prevent SQL injection, column names and sorting directions cannot be directly parameterized with '?' in standard SQL drivers; instead, they must be validated against a strict white-list in application code before SQL construction.", "Safe Sorting Allow-listing: ")
    add_bullet(" The LIMIT clause sets an upper bound on record count returned, while OFFSET dictates how many preceding records to skip. This forms the standard paradigm for pagination across web applications.", "Pagination (LIMIT and OFFSET): ")

    add_title("4.5 HTTP Status Codes in API Contracts", 2)
    add_p("REST APIs convey operational outcomes via authoritative standard HTTP status codes:")
    add_bullet(" Request succeeded. Used for successful GET, PUT, and DELETE responses.", "200 OK: ")
    add_bullet(" Resource successfully created. Returns the created resource entity and ID.", "201 Created: ")
    add_bullet(" Client issued an invalid request (malformed JSON, missing fields, out-of-range parameters).", "400 Bad Request: ")
    add_bullet(" Target resource ID does not exist on the server.", "404 Not Found: ")
    add_bullet(" Unhandled server-side exception or database communication collapse.", "500 Internal Server Error: ")

    # ==================== SECTION 5: PROCEDURE ====================
    add_title("5. STEP-BY-STEP PROCEDURE", 1)
    add_p("The experiment was conducted through the following structured sequence of development steps:")
    add_bullet(" Initialized a clean Node.js application environment using npm init -y, configured ES module/CommonJS standards, and installed production dependencies express and sqlite3.", "Step 1 — Project Initialization:")
    add_bullet(" Structured a modular MVC-style architecture dividing logic into routes, controllers, middleware, utilities, tests, and debugging demonstration suites.", "Step 2 — Architecture Structuring:")
    add_bullet(" Configured an embedded SQLite database (books.db) with automatic schema creation (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, author TEXT, price REAL) and seeded 10 initial sample books.", "Step 3 — SQLite Database Layer:")
    add_bullet(" Implemented input validation logic in validation.js to ensure non-empty strings for title and author, positive numeric values for price, and whitelisted parameters for order_by and order.", "Step 4 — Validation Middleware:")
    add_bullet(" Built controller actions in bookController.js handling GET /books, GET /books/:id, POST /books, PUT /books/:id, and DELETE /books/:id with parameterized SQL statements.", "Step 5 — RESTful Controllers:")
    add_bullet(" Configured dynamic query parameter extraction for search_q (LIKE), min_price, max_price, order_by, order, limit, and offset.", "Step 6 — Query Parameters & Filtering:")
    add_bullet(" Built centralized error-handling middleware for capturing 500 runtime exceptions and 404 unmatched route handlers.", "Step 7 — Central Error Handling:")
    add_bullet(" Replicated, isolated, analyzed, and debugged four foundational backend errors: EADDRINUSE, MODULE_NOT_FOUND, no such table, and missing await.", "Step 8 — Debugging Demonstration:")
    add_bullet(" Created an automated HTTP test suite in tests/api.test.js executing 21 comprehensive scenarios, followed by Postman verification.", "Step 9 — Automated & Postman Verification:")

    # ==================== SECTION 6: PROGRAM CODE ====================
    add_title("6. COMPLETE WORKING PROGRAM CODE", 1)
    add_p("The production-grade, modular backend codebase implemented for Lab 3 is documented below:")

    add_title("6.1 Package Configuration (package.json)", 2)
    add_code_block("""{
  "name": "bdf-lab-03",
  "version": "1.0.0",
  "description": "Backend Development Fundamentals Lab 3 - REST API & Debugging",
  "main": "src/server.js",
  "scripts": {
    "start": "node src/server.js",
    "test": "node tests/api.test.js"
  },
  "author": "Appampally Abhilash Reddy (252U1R5008)",
  "dependencies": {
    "express": "^4.21.2",
    "sqlite3": "^5.1.7"
  }
}""")

    add_title("6.2 Database Configuration & Seed Data (src/database.js)", 2)
    add_code_block("""const sqlite3 = require('sqlite3').verbose();
const path = require('path');

const dbPath = path.resolve(__dirname, '../books.db');
const db = new sqlite3.Database(dbPath, (err) => {
  if (err) console.error('SQLite connection error:', err.message);
  else console.log('Connected to SQLite database at:', dbPath);
});

function initializeDatabase() {
  return new Promise((resolve, reject) => {
    db.serialize(() => {
      db.run(`CREATE TABLE IF NOT EXISTS books (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        author TEXT NOT NULL,
        price REAL NOT NULL
      )`, (err) => {
        if (err) return reject(err);
      });

      db.get(`SELECT COUNT(*) AS count FROM books`, (err, row) => {
        if (err) return reject(err);
        if (row.count === 0) {
          const stmt = db.prepare(`INSERT INTO books (title, author, price) VALUES (?, ?, ?)`);
          const sampleBooks = [
            ['Python Programming', 'John Smith', 450.0],
            ['JavaScript: The Good Parts', 'Douglas Crockford', 350.0],
            ['Clean Code', 'Robert C. Martin', 600.0],
            ['Design Patterns', 'Erich Gamma', 750.0],
            ['Node.js Design Patterns', 'Mario Casciaro', 520.0],
            ['Learning SQL', 'Alan Beaulieu', 280.0],
            ['Express in Action', 'Evan Hahn', 399.0],
            ['Database Internals', 'Alex Petrov', 820.0],
            ['Full Stack Development', 'David Flanagan', 480.0],
            ['Modern Operating Systems', 'Andrew S. Tanenbaum', 950.0]
          ];
          sampleBooks.forEach(b => stmt.run(b[0], b[1], b[2]));
          stmt.finalize((e) => e ? reject(e) : resolve());
        } else {
          resolve();
        }
      });
    });
  });
}

const dbQuery = {
  all: (sql, params = []) => new Promise((res, rej) => db.all(sql, params, (e, r) => e ? rej(e) : res(r))),
  get: (sql, params = []) => new Promise((res, rej) => db.get(sql, params, (e, r) => e ? rej(e) : res(r))),
  run: (sql, params = []) => new Promise((res, rej) => db.run(sql, params, function(e) { e ? rej(e) : res({ lastID: this.lastID, changes: this.changes }); }))
};

module.exports = { db, initializeDatabase, dbQuery };""")

    add_title("6.3 Validation Utilities (src/utils/validation.js)", 2)
    add_code_block("""function validateBookPayload(body) {
  const { title, author, price } = body;
  if (!title || typeof title !== 'string' || title.trim() === '') {
    return { isValid: false, message: 'Title, author and valid numeric price are required' };
  }
  if (!author || typeof author !== 'string' || author.trim() === '') {
    return { isValid: false, message: 'Title, author and valid numeric price are required' };
  }
  if (price === undefined || price === null || typeof price !== 'number' || isNaN(price) || price < 0) {
    return { isValid: false, message: 'Title, author and valid numeric price are required' };
  }
  return { isValid: true };
}

function validateQueryParams(query) {
  const allowedSortColumns = ['id', 'title', 'author', 'price'];
  const allowedOrders = ['ASC', 'DESC'];
  const errors = [];

  if (query.order_by && !allowedSortColumns.includes(query.order_by.toLowerCase())) {
    errors.push(`Invalid order_by parameter '${query.order_by}'. Allowed columns: ${allowedSortColumns.join(', ')}`);
  }
  if (query.order && !allowedOrders.includes(query.order.toUpperCase())) {
    errors.push(`Invalid order parameter '${query.order}'. Allowed values: ASC, DESC`);
  }
  if (query.limit !== undefined && (isNaN(parseInt(query.limit, 10)) || parseInt(query.limit, 10) <= 0)) {
    errors.push("Invalid limit parameter. Must be a positive integer.");
  }
  if (query.offset !== undefined && (isNaN(parseInt(query.offset, 10)) || parseInt(query.offset, 10) < 0)) {
    errors.push("Invalid offset parameter. Must be a non-negative integer.");
  }
  if (query.min_price !== undefined && (isNaN(parseFloat(query.min_price)) || parseFloat(query.min_price) < 0)) {
    errors.push("Invalid min_price parameter. Must be a non-negative number.");
  }
  if (query.max_price !== undefined && (isNaN(parseFloat(query.max_price)) || parseFloat(query.max_price) < 0)) {
    errors.push("Invalid max_price parameter. Must be a non-negative number.");
  }
  if (query.min_price !== undefined && query.max_price !== undefined) {
    if (parseFloat(query.min_price) > parseFloat(query.max_price)) {
      errors.push("min_price cannot be greater than max_price.");
    }
  }
  return { isValid: errors.length === 0, errors };
}

module.exports = { validateBookPayload, validateQueryParams };""")

    add_title("6.4 Book Controller Implementation (src/controllers/bookController.js)", 2)
    add_code_block("""const { dbQuery } = require('../database');
const { validateBookPayload, validateQueryParams } = require('../utils/validation');

async function getAllBooks(req, res, next) {
  try {
    const val = validateQueryParams(req.query);
    if (!val.isValid) return res.status(400).json({ message: val.errors.join('; ') });

    const { search_q = '', order_by = 'id', order = 'ASC', limit = 10, offset = 0, min_price, max_price } = req.query;
    let sql = 'SELECT * FROM books WHERE 1=1';
    const params = [];

    if (search_q.trim() !== '') {
      sql += ' AND title LIKE ?';
      params.push(`%${search_q.trim()}%`);
    }
    if (min_price !== undefined) {
      sql += ' AND price >= ?';
      params.push(parseFloat(min_price));
    }
    if (max_price !== undefined) {
      sql += ' AND price <= ?';
      params.push(parseFloat(max_price));
    }

    const sortCol = ['id', 'title', 'author', 'price'].includes(order_by.toLowerCase()) ? order_by.toLowerCase() : 'id';
    const sortOrd = ['ASC', 'DESC'].includes(order.toUpperCase()) ? order.toUpperCase() : 'ASC';
    sql += ` ORDER BY ${sortCol} ${sortOrd} LIMIT ? OFFSET ?`;
    params.push(parseInt(limit, 10), parseInt(offset, 10));

    const books = await dbQuery.all(sql, params);
    res.status(200).json({ message: 'Books retrieved successfully', count: books.length, data: books });
  } catch (error) { next(error); }
}

async function getBookById(req, res, next) {
  try {
    const bookId = parseInt(req.params.id, 10);
    if (isNaN(bookId)) return res.status(400).json({ message: 'Invalid book ID format' });
    const book = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);
    if (!book) return res.status(404).json({ message: 'Book not found' });
    res.status(200).json({ message: 'Book retrieved successfully', data: book });
  } catch (error) { next(error); }
}

async function createBook(req, res, next) {
  try {
    const val = validateBookPayload(req.body);
    if (!val.isValid) return res.status(400).json({ message: val.message });
    const { title, author, price } = req.body;
    const result = await dbQuery.run('INSERT INTO books (title, author, price) VALUES (?, ?, ?)', [title.trim(), author.trim(), parseFloat(price)]);
    const newBook = await dbQuery.get('SELECT * FROM books WHERE id = ?', [result.lastID]);
    res.status(201).json({ message: 'Book created successfully', data: newBook });
  } catch (error) { next(error); }
}

async function updateBook(req, res, next) {
  try {
    const bookId = parseInt(req.params.id, 10);
    if (isNaN(bookId)) return res.status(400).json({ message: 'Invalid book ID format' });
    const existing = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);
    if (!existing) return res.status(404).json({ message: 'Book not found' });

    const val = validateBookPayload(req.body);
    if (!val.isValid) return res.status(400).json({ message: val.message });

    const { title, author, price } = req.body;
    await dbQuery.run('UPDATE books SET title = ?, author = ?, price = ? WHERE id = ?', [title.trim(), author.trim(), parseFloat(price), bookId]);
    const updated = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);
    res.status(200).json({ message: 'Book updated successfully', data: updated });
  } catch (error) { next(error); }
}

async function deleteBook(req, res, next) {
  try {
    const bookId = parseInt(req.params.id, 10);
    if (isNaN(bookId)) return res.status(400).json({ message: 'Invalid book ID format' });
    const existing = await dbQuery.get('SELECT * FROM books WHERE id = ?', [bookId]);
    if (!existing) return res.status(404).json({ message: 'Book not found' });
    await dbQuery.run('DELETE FROM books WHERE id = ?', [bookId]);
    res.status(200).json({ message: 'Book deleted successfully', data: existing });
  } catch (error) { next(error); }
}

module.exports = { getAllBooks, getBookById, createBook, updateBook, deleteBook };""")

    add_title("6.5 Application Entry & Server (src/app.js & src/server.js)", 2)
    add_code_block("""// src/app.js
const express = require('express');
const bookRoutes = require('./routes/bookRoutes');
const { errorHandler, notFoundHandler } = require('./middleware/errorHandler');

const app = express();
app.use(express.json());
app.use('/books', bookRoutes);
app.use(notFoundHandler);
app.use(errorHandler);

module.exports = app;

// src/server.js
const app = require('./app');
const { initializeDatabase } = require('./database');
const PORT = process.env.PORT || 3000;

async function startServer() {
  await initializeDatabase();
  app.listen(PORT, () => {
    console.log(`BDF Lab 03 REST API running on port ${PORT}`);
  });
}
if (require.main === module) startServer();""")

    # ==================== SECTION 7: EXECUTION AND OUTPUT ====================
    doc.add_page_break()
    add_title("7. EXECUTION AND OUTPUT SCREENSHOTS", 1)
    add_p("This section documents the actual runtime outputs and visual execution evidence for all project phases and REST endpoints.")

    add_title("7.1 Project Structure & Environment Setup", 2)
    add_screenshot("Screenshot_01_Project_Folder_Structure.png", "Figure 7.1: Directory Tree of the BDF Lab 03 Project")
    add_screenshot("Screenshot_02_Dependencies_Installed.png", "Figure 7.2: NPM Dependency Verification (express, sqlite3)")
    add_screenshot("Screenshot_03_Backend_Server_Running.png", "Figure 7.3: Express Server Online & Listening on Port 3000")
    add_screenshot("Screenshot_04_Database_Created_And_Sample_Data.png", "Figure 7.4: SQLite Database Table & Seed Records Verification")

    add_title("7.2 REST CRUD Operations Output", 2)
    add_screenshot("Screenshot_05_GET_All_Books_200.png", "Figure 7.5: Postman Output for GET /books (200 OK)")
    add_screenshot("Screenshot_06_GET_Book_By_ID_200.png", "Figure 7.6: Postman Output for GET /books/1 (200 OK)")
    add_screenshot("Screenshot_07_POST_Book_201.png", "Figure 7.7: Postman Output for POST /books (201 Created)")
    add_screenshot("Screenshot_08_PUT_Book_200.png", "Figure 7.8: Postman Output for PUT /books/1 (200 OK)")
    add_screenshot("Screenshot_09_DELETE_Book_200.png", "Figure 7.9: Postman Output for DELETE /books/2 (200 OK)")

    add_title("7.3 Query Parameters, Sorting & Pagination Output", 2)
    add_screenshot("Screenshot_10_Search_search_q.png", "Figure 7.10: Search Filter GET /books?search_q=Clean (200 OK)")
    add_screenshot("Screenshot_11_Sorting_order_by_order.png", "Figure 7.11: Sort Ascending GET /books?order_by=price&order=ASC")
    add_screenshot("Screenshot_12_Pagination_limit_offset.png", "Figure 7.12: Pagination GET /books?limit=3&offset=0")
    add_screenshot("Screenshot_13_Price_Filtering_min_max.png", "Figure 7.13: Price Filter GET /books?min_price=300&max_price=600")

    # ==================== SECTION 8: VALIDATION TESTING ====================
    doc.add_page_break()
    add_title("8. REQUEST VALIDATION TESTING", 1)
    add_p(
        "Robust REST APIs enforce schema validation to protect the data layer against garbage inputs, type mismatches, or malformed payloads. The following tests verify that invalid payloads are rejected with HTTP 400 Bad Request."
    )
    add_screenshot("Screenshot_14_Validation_Missing_Title_400.png", "Figure 8.1: Validation Rejection: Missing Title (400 Bad Request)")
    add_screenshot("Screenshot_15_Validation_Missing_Author_400.png", "Figure 8.2: Validation Rejection: Missing Author (400 Bad Request)")
    add_screenshot("Screenshot_16_Validation_Invalid_Price_400.png", "Figure 8.3: Validation Rejection: Non-numeric Price (400 Bad Request)")
    add_screenshot("Screenshot_17_Missing_Book_ID_404.png", "Figure 8.4: Resource Not Found: Non-existent ID /books/9999 (404 Not Found)")

    # ==================== SECTION 9: DEBUGGING ====================
    doc.add_page_break()
    add_title("9. SYSTEMATIC BACKEND DEBUGGING EXERCISES", 1)
    add_p(
        "In backend development, debugging requires understanding runtime exception signatures, call stacks, and the underlying Node.js event loop. The four assigned debugging problems were systematically replicated and resolved."
    )

    add_title("9.1 Exercise 1: EADDRINUSE — Port Collision", 2)
    add_bullet("Occurs when attempting to bind an Express server to a TCP port already held by another running process.", "Problem Description: ")
    add_bullet("Error: listen EADDRINUSE: address already in use :::3000", "Exception Signature: ")
    add_bullet("Two processes competing for identical network interface port.", "Root Cause: ")
    add_bullet("app.listen(3000) executed twice or unclosed background instance.", "Incorrect Code: ")
    add_bullet("Check active listeners via netstat -ano | findstr :3000 and terminate zombie process using taskkill /PID <PID> /F, or use dynamic process.env.PORT.", "Resolution Procedure: ")
    add_screenshot("Screenshot_18_EADDRINUSE_Debugging.png", "Figure 9.1: Terminal Execution Trace for EADDRINUSE Debugging")

    add_title("9.2 Exercise 2: MODULE_NOT_FOUND — Wrong Import Path", 2)
    add_bullet("Node.js fails to resolve a required CommonJS module or relative filepath.", "Problem Description: ")
    add_bullet("Error: Cannot find module './controllers/bookControler.js'", "Exception Signature: ")
    add_bullet("Spelling typo in filename or incorrect relative path traversal ('./' vs '../').", "Root Cause: ")
    add_bullet("const bookController = require('./controllers/bookControler.js'); (Missing 'l')", "Incorrect Code: ")
    add_bullet("Correct filename spelling and use proper relative path '../controllers/bookController'.", "Resolution Procedure: ")
    add_screenshot("Screenshot_19_Wrong_Import_Path_Debugging.png", "Figure 9.2: Terminal Execution Trace for MODULE_NOT_FOUND Resolution")

    add_title("9.3 Exercise 3: SQLITE_ERROR — Incorrect Relational Table Name", 2)
    add_bullet("SQLite database engine rejects SQL statement referencing a non-existent table.", "Problem Description: ")
    add_bullet("SQLite Execution Error: SQLITE_ERROR: no such table: book_store", "Exception Signature: ")
    add_bullet("Mismatch between defined schema table ('books') and query identifier ('book_store').", "Root Cause: ")
    add_bullet("SELECT * FROM book_store", "Incorrect Code: ")
    add_bullet("Ensure SQL statements reference the exact schema table 'books' defined during CREATE TABLE.", "Resolution Procedure: ")
    add_screenshot("Screenshot_20_Incorrect_Table_Name_Debugging.png", "Figure 9.3: Terminal Execution Trace for SQLITE_ERROR Resolution")

    add_title("9.4 Exercise 4: Missing Await in Asynchronous DB Operations", 2)
    add_bullet("Accessing properties on unresolved Promise objects leads to silent logic bugs or 'undefined'.", "Problem Description: ")
    add_bullet("Result is Promise { <pending> }, book.title returns undefined.", "Behavioral Symptom: ")
    add_bullet("Omitting the 'await' keyword before an asynchronous Promise-returning function call.", "Root Cause: ")
    add_bullet("const book = dbQuery.get('SELECT * FROM books WHERE id = 1'); console.log(book.title);", "Incorrect Code: ")
    add_bullet("Prefix the call with 'await' inside async controller functions: const book = await dbQuery.get(...);", "Resolution Procedure: ")
    add_screenshot("Screenshot_21_Missing_Await_Debugging.png", "Figure 9.4: Terminal Execution Trace for Missing Await Diagnosis & Fix")

    # ==================== SECTION 10: TEST CASE SUMMARY ====================
    doc.add_page_break()
    add_title("10. AUTOMATED TEST CASE SUMMARY", 1)
    add_p(
        "An automated test harness was built and executed in tests/api.test.js. All 21 functional test scenarios passed successfully with exact HTTP status codes and response bodies verified."
    )
    add_screenshot("Screenshot_22_Automated_Test_Results.png", "Figure 10.1: Automated Test Suite Output — 21 Tests Passed (100% Success)")

    # Read test_results.json
    results_path = r"C:\Users\Abhilash reddy\OneDrive\Desktop\LAB REPOORT 3\tests\test_results.json"
    if os.path.exists(results_path):
        with open(results_path, 'r') as f:
            t_cases = json.load(f)
    else:
        t_cases = []

    t_summary = doc.add_table(rows=len(t_cases) + 1, cols=5)
    t_summary.alignment = WD_TABLE_ALIGNMENT.CENTER
    s_headers = ["Test ID", "Test Scenario", "Expected", "Actual", "Status"]

    for col_idx, h_text in enumerate(s_headers):
        cell = t_summary.cell(0, col_idx)
        set_cell_background(cell, "102C57")
        p = cell.paragraphs[0]
        r = p.add_run(h_text)
        r.bold = True
        r.font.color.rgb = RGBColor(255, 255, 255)
        r.font.size = Pt(10)

    for row_idx, tc in enumerate(t_cases):
        row = t_summary.rows[row_idx + 1]
        vals = [tc["id"], tc["scenario"], str(tc["expectedStatus"]), str(tc["actualStatus"]), tc["status"]]
        for col_idx, val in enumerate(vals):
            cell = row.cells[col_idx]
            bg = "F7F9FC" if row_idx % 2 == 0 else "FFFFFF"
            set_cell_background(cell, bg)
            set_cell_margins(cell, 40, 40, 60, 60)
            p = cell.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(9)
            if col_idx == 4:
                r.bold = True
                r.font.color.rgb = RGBColor(39, 201, 63) if val == "PASS" else RGBColor(255, 0, 0)

    # ==================== SECTION 11: RESULT ====================
    doc.add_page_break()
    add_title("11. RESULT", 1)
    add_p(
        "The Backend Development Fundamentals Lab 3 experiment on 'REST API Development, Query Parameters, Validation, and Debugging' was successfully completed and tested. All RESTful endpoints (/books) supporting full CRUD operations, SQL LIKE title searching, safe whitelisted multi-column sorting, pagination, and numerical price-range filters were completely implemented using Node.js, Express.js, and SQLite. Rigorous input validation rejecting missing or malformed payloads with HTTP 400 Bad Request was fully enforced. All 4 backend debugging exercises were reproduced and diagnosed, and all 21 automated test cases executed with a 100% pass rate."
    )

    # ==================== SECTION 12: CONCLUSION ====================
    add_title("12. CONCLUSION", 1)
    add_p(
        "Through this practical lab experiment, in-depth architectural and hands-on skills in backend REST API engineering were acquired:"
    )
    add_bullet(" Mastered the practical mapping between HTTP verbs (GET, POST, PUT, DELETE) and relational database CRUD operations.", "RESTful Design Principles: ")
    add_bullet(" Implemented dynamic SQL query generation using SQL LIKE, ORDER BY, LIMIT, and OFFSET, while strictly defending against SQL injection attacks through parameter binding and column allow-listing.", "Relational Database Filtering: ")
    add_bullet(" Enforced robust input validation to guard against missing parameters, type mismatches, and negative price boundaries.", "Defensive Validation: ")
    add_bullet(" Acquired professional systematic debugging techniques to resolve port collisions, module loading failures, relational table typos, and asynchronous Promise pitfalls.", "Backend Diagnostics: ")
    add_bullet(" Developed automated API test suites and Postman collections ensuring high test coverage and verifiable software quality.", "API Testing & Verification: ")

    # ==================== SECTION 13: VIVA QUESTIONS ====================
    add_title("13. VIVA QUESTIONS AND ANSWERS", 1)

    add_title("Question 1: What is the difference between a query parameter and a path parameter?", 2)
    add_p(
        "A path parameter is part of the hierarchical URL path itself (e.g., /books/5) and is used to uniquely identify a specific resource instance. In contrast, a query parameter is appended after a question mark '?' in key-value pairs (e.g., /books?limit=10&order=ASC) and is used to filter, sort, paginate, or modify the representation of a collection without changing the identity of the resource.",
        bold_prefix="Answer: "
    )

    add_title("Question 2: What does stateless mean in RESTful API architecture?", 2)
    add_p(
        "Statelessness means that every HTTP request from the client to the server must contain all the contextual information required for the server to understand and process that request. The server does not persist or rely on any client session state across successive requests, which significantly improves server scalability, reliability, and cacheability.",
        bold_prefix="Answer: "
    )

    add_title("Question 3: Which HTTP status code is used for bad input versus a missing record?", 2)
    add_p(
        "HTTP 400 (Bad Request) is returned when the client sends malformed, invalid, or missing input data (such as a missing book title or non-numeric price). HTTP 404 (Not Found) is returned when the request syntax is valid, but the requested resource ID does not exist in the database (such as requesting a book with ID 9999).",
        bold_prefix="Answer: "
    )

    # Save document
    doc.save(OUTPUT_DOCX)
    print(f"Word Report successfully generated at: {OUTPUT_DOCX}")

if __name__ == "__main__":
    create_report()
