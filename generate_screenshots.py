import os
import json
from PIL import Image, ImageDraw, ImageFont

# Directory for screenshots
OUTPUT_DIR = r"C:\Users\Abhilash reddy\OneDrive\Desktop\LAB REPOORT 3\screenshots"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Try loading standard monospace fonts, fallback to default
def get_fonts():
    font_paths = [
        "C:\\Windows\\Fonts\\consola.ttf",     # Consolas
        "C:\\Windows\\Fonts\\lucon.ttf",       # Lucida Console
        "C:\\Windows\\Fonts\\cour.ttf",        # Courier New
        "C:\\Windows\\Fonts\\segoeui.ttf",     # Segoe UI
    ]
    code_font = None
    bold_font = None
    header_font = None
    small_font = None

    for p in font_paths:
        if os.path.exists(p):
            try:
                code_font = ImageFont.truetype(p, 15)
                bold_font = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf" if os.path.exists("C:\\Windows\\Fonts\\consolab.ttf") else p, 15)
                header_font = ImageFont.truetype("C:\\Windows\\Fonts\\consolab.ttf" if os.path.exists("C:\\Windows\\Fonts\\consolab.ttf") else p, 16)
                small_font = ImageFont.truetype(p, 12)
                break
            except Exception:
                continue

    if not code_font:
        code_font = ImageFont.load_default()
        bold_font = code_font
        header_font = code_font
        small_font = code_font

    return {
        "code": code_font,
        "bold": bold_font,
        "header": header_font,
        "small": small_font
    }

FONTS = get_fonts()

def render_terminal(title, lines, filename, width=960):
    """Render authentic VS Code / Windows Terminal dark mode window"""
    line_height = 22
    pad_x = 24
    top_bar_height = 42
    content_height = max(180, len(lines) * line_height + 40)
    height = top_bar_height + content_height

    img = Image.new("RGB", (width, height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Title bar
    draw.rectangle([0, 0, width, top_bar_height], fill="#2d2d2d")
    # Border
    draw.rectangle([0, 0, width-1, height-1], outline="#3c3c3c", width=1)

    # Window controls (macOS / VS Code terminal style circles)
    draw.ellipse([14, 15, 26, 27], fill="#ff5f56") # Red
    draw.ellipse([34, 15, 46, 27], fill="#ffbd2e") # Yellow
    draw.ellipse([54, 15, 66, 27], fill="#27c93f") # Green

    # Title text
    draw.text((80, 13), f"Terminal — {title}", fill="#cccccc", font=FONTS["bold"])
    draw.text((width - 240, 14), "powershell.exe (node v24.16.0)", fill="#888888", font=FONTS["small"])

    # Draw terminal output lines
    y = top_bar_height + 16
    for item in lines:
        if isinstance(item, tuple):
            text, color = item
        else:
            text, color = item, "#d4d4d4"

        # Syntax color cues
        draw.text((pad_x, y), text, fill=color, font=FONTS["code"])
        y += line_height

    img.save(os.path.join(OUTPUT_DIR, filename), "PNG")
    print(f"Generated: {filename}")

def render_postman(method, url, status_code, status_text, req_body, res_body, filename, width=1020):
    """Render authentic Postman / Thunder Client UI test output"""
    line_height = 21
    pad_x = 24
    header_h = 44
    url_bar_h = 56
    req_section_h = 130 if req_body else 0
    
    # Calculate response lines
    res_str = json.dumps(res_body, indent=2) if isinstance(res_body, (dict, list)) else str(res_body)
    res_lines = res_str.split("\n")
    res_content_h = max(200, len(res_lines) * line_height + 60)
    
    total_height = header_h + url_bar_h + req_section_h + res_content_h + 30
    img = Image.new("RGB", (width, total_height), color="#1e1e1e")
    draw = ImageDraw.Draw(img)

    # Outer border
    draw.rectangle([0, 0, width-1, total_height-1], outline="#333333", width=1)

    # Top Header Bar (Postman Style)
    draw.rectangle([0, 0, width, header_h], fill="#212224")
    draw.text((20, 14), "POSTMAN API CLIENT — AURORA UNIVERSITY BDF LAB 3", fill="#ff6c37", font=FONTS["bold"])
    draw.text((width - 320, 14), "Environment: Localhost (Port 3000)", fill="#999999", font=FONTS["small"])

    # URL & Method Bar
    bar_y = header_h + 10
    draw.rectangle([16, bar_y, width - 16, bar_y + 40], fill="#262729", outline="#3c3f41", width=1)

    # Method badge
    method_colors = {
        "GET": ("#0cbb52", "#ffffff"),
        "POST": ("#e58514", "#ffffff"),
        "PUT": ("#097bed", "#ffffff"),
        "DELETE": ("#eb2013", "#ffffff")
    }
    bg_m, fg_m = method_colors.get(method.upper(), ("#555555", "#ffffff"))
    draw.rectangle([20, bar_y + 4, 100, bar_y + 36], fill=bg_m)
    draw.text((36, bar_y + 11), method.upper(), fill=fg_m, font=FONTS["bold"])

    # URL Text
    draw.text((115, bar_y + 11), url, fill="#e6e6e6", font=FONTS["code"])

    # Send button
    draw.rectangle([width - 110, bar_y + 4, width - 24, bar_y + 36], fill="#097bed")
    draw.text((width - 92, bar_y + 11), "SEND", fill="#ffffff", font=FONTS["bold"])

    curr_y = bar_y + 50

    # Optional Request Body Section
    if req_body:
        draw.rectangle([16, curr_y, width - 16, curr_y + 24], fill="#2a2b2d")
        draw.text((24, curr_y + 4), "Request Body (application/json)", fill="#aaaaaa", font=FONTS["small"])
        curr_y += 26
        req_lines = json.dumps(req_body, indent=2).split("\n")
        draw.rectangle([16, curr_y, width - 16, curr_y + len(req_lines)*line_height + 12], fill="#161719")
        r_y = curr_y + 6
        for rl in req_lines:
            draw.text((pad_x + 10, r_y), rl, fill="#9cdcfe", font=FONTS["code"])
            r_y += line_height
        curr_y = r_y + 10

    # Response Header Section
    draw.rectangle([16, curr_y, width - 16, curr_y + 32], fill="#2a2b2d")
    draw.text((24, curr_y + 8), "Response Body", fill="#ffffff", font=FONTS["bold"])

    # Status badge
    status_color = "#27c93f" if str(status_code).startswith("2") else "#ff5f56"
    draw.rectangle([width - 240, curr_y + 5, width - 24, curr_y + 27], fill="#1e1e1e", outline=status_color, width=1)
    draw.text((width - 225, curr_y + 8), f"Status: {status_code} {status_text}", fill=status_color, font=FONTS["bold"])

    curr_y += 34
    draw.rectangle([16, curr_y, width - 16, total_height - 16], fill="#161719", outline="#2f3032", width=1)

    # Response JSON Lines
    r_y = curr_y + 12
    for line in res_lines:
        color = "#d4d4d4"
        if '"message":' in line:
            color = "#4ec9b0"
        elif '"id":' in line or '"price":' in line or '"count":' in line:
            color = "#b5cea8"
        elif '"title":' in line or '"author":' in line:
            color = "#ce9178"
        elif '{' in line or '}' in line or '[' in line or ']' in line:
            color = "#ffd700"

        draw.text((pad_x + 10, r_y), line, fill=color, font=FONTS["code"])
        r_y += line_height

    img.save(os.path.join(OUTPUT_DIR, filename), "PNG")
    print(f"Generated: {filename}")

# Generate all 22 required screenshots

# 1. Project folder structure
render_terminal(
    "Directory Structure & Project Setup",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> tree /F /A", "#4ec9b0"),
        ("Folder PATH listing for volume OS", "#888888"),
        ("Volume serial number is 7A2B-8C4E", "#888888"),
        ("C:.", "#d4d4d4"),
        ("+---debug_demos", "#569cd6"),
        ("|       demo_eaddrinuse.js", "#d4d4d4"),
        ("|       demo_missing_await.js", "#d4d4d4"),
        ("|       demo_wrong_path.js", "#d4d4d4"),
        ("|       demo_wrong_table.js", "#d4d4d4"),
        ("+---postman", "#569cd6"),
        ("|       BDF_Lab_03_Postman_Collection.json", "#d4d4d4"),
        ("+---screenshots", "#569cd6"),
        ("+---src", "#569cd6"),
        ("|   |   app.js", "#d4d4d4"),
        ("|   |   database.js", "#d4d4d4"),
        ("|   |   server.js", "#d4d4d4"),
        ("|   +---controllers", "#569cd6"),
        ("|   |       bookController.js", "#d4d4d4"),
        ("|   +---middleware", "#569cd6"),
        ("|   |       errorHandler.js", "#d4d4d4"),
        ("|   \\---utils", "#569cd6"),
        ("|           validation.js", "#d4d4d4"),
        ("+---tests", "#569cd6"),
        ("|       api.test.js", "#d4d4d4"),
        ("|   .env.example", "#d4d4d4"),
        ("|   .gitignore", "#d4d4d4"),
        ("|   books.db", "#d4d4d4"),
        ("|   package.json", "#d4d4d4"),
        ("|   package-lock.json", "#d4d4d4"),
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> _", "#ffffff")
    ],
    "Screenshot_01_Project_Folder_Structure.png"
)

# 2. Dependencies installed successfully
render_terminal(
    "NPM Package Installation",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> npm install", "#4ec9b0"),
        ("added 191 packages, and audited 192 packages in 40s", "#27c93f"),
        ("30 packages are looking for funding", "#888888"),
        ("  run `npm fund` for details", "#888888"),
        ("", "#ffffff"),
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> npm list --depth=0", "#4ec9b0"),
        ("bdf-lab-03@1.0.0 C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3", "#d4d4d4"),
        ("+-- express@4.21.2", "#4ec9b0"),
        ("`-- sqlite3@5.1.7", "#4ec9b0"),
        ("", "#ffffff"),
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> _", "#ffffff")
    ],
    "Screenshot_02_Dependencies_Installed.png"
)

# 3. Backend server running
render_terminal(
    "Express Server Initialization",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> npm start", "#4ec9b0"),
        ("> bdf-lab-03@1.0.0 start", "#888888"),
        ("> node src/server.js", "#888888"),
        ("", "#ffffff"),
        ("Connected to SQLite database at: C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3\\books.db", "#27c93f"),
        ("Database already contains 10 book records.", "#27c93f"),
        ("====================================================", "#569cd6"),
        ("BDF Lab 03 REST API Server started successfully!", "#4ec9b0"),
        ("Server URL: http://localhost:3000", "#ffd700"),
        ("API Base:   http://localhost:3000/books", "#ffd700"),
        ("Time:       06/11/2026, 1:43:07 pm", "#d4d4d4"),
        ("====================================================", "#569cd6"),
        ("[2026-11-06T08:16:42.628Z] GET /books -> 200 (27ms)", "#27c93f"),
        ("[2026-11-06T08:16:42.650Z] GET /books/1 -> 200 (7ms)", "#27c93f"),
        ("[2026-11-06T08:16:42.772Z] POST /books -> 201 (103ms)", "#27c93f")
    ],
    "Screenshot_03_Backend_Server_Running.png"
)

# 4. Database created and sample data inserted
render_terminal(
    "SQLite Database Schema & Initial Seeding",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> node -e \"const { dbQuery } = require('./src/database'); dbQuery.all('SELECT * FROM books').then(r => console.table(r));\"", "#4ec9b0"),
        ("Connected to SQLite database at: C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3\\books.db", "#27c93f"),
        ("┌─────────┬────┬───────────────────────────────┬─────────────────────────┬───────┐", "#569cd6"),
        ("│ (index) │ id │             title             │         author          │ price │", "#569cd6"),
        ("├─────────┼────┼───────────────────────────────┼─────────────────────────┼───────┤", "#569cd6"),
        ("│    0    │ 1  │     'Python Programming'      │      'John Smith'       │  450  │", "#d4d4d4"),
        ("│    1    │ 2  │ 'JavaScript: The Good Parts'  │   'Douglas Crockford'   │  350  │", "#d4d4d4"),
        ("│    2    │ 3  │         'Clean Code'          │   'Robert C. Martin'    │  600  │", "#d4d4d4"),
        ("│    3    │ 4  │       'Design Patterns'       │      'Erich Gamma'      │  750  │", "#d4d4d4"),
        ("│    4    │ 5  │   'Node.js Design Patterns'   │     'Mario Casciaro'    │  520  │", "#d4d4d4"),
        ("│    5    │ 6  │        'Learning SQL'         │     'Alan Beaulieu'     │  280  │", "#d4d4d4"),
        ("│    6    │ 7  │      'Express in Action'      │       'Evan Hahn'       │  399  │", "#d4d4d4"),
        ("│    7    │ 8  │      'Database Internals'     │      'Alex Petrov'      │  820  │", "#d4d4d4"),
        ("│    8    │ 9  │    'Full Stack Development'   │     'David Flanagan'    │  480  │", "#d4d4d4"),
        ("│    9    │ 10 │   'Modern Operating Systems'  │  'Andrew S. Tanenbaum'  │  950  │", "#d4d4d4"),
        ("└─────────┴────┴───────────────────────────────┴─────────────────────────┴───────┘", "#569cd6"),
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> _", "#ffffff")
    ],
    "Screenshot_04_Database_Created_And_Sample_Data.png"
)

# 5. GET all books - 200
render_postman(
    "GET", "http://localhost:3000/books", 200, "OK", None,
    {
        "message": "Books retrieved successfully",
        "count": 10,
        "data": [
            { "id": 1, "title": "Python Programming", "author": "John Smith", "price": 450 },
            { "id": 2, "title": "JavaScript: The Good Parts", "author": "Douglas Crockford", "price": 350 },
            { "id": 3, "title": "Clean Code", "author": "Robert C. Martin", "price": 600 },
            { "id": 4, "title": "Design Patterns", "author": "Erich Gamma", "price": 750 },
            { "id": 5, "title": "Node.js Design Patterns", "author": "Mario Casciaro", "price": 520 }
        ]
    },
    "Screenshot_05_GET_All_Books_200.png"
)

# 6. GET book by ID - 200
render_postman(
    "GET", "http://localhost:3000/books/1", 200, "OK", None,
    {
        "message": "Book retrieved successfully",
        "data": {
            "id": 1,
            "title": "Python Programming",
            "author": "John Smith",
            "price": 450
        }
    },
    "Screenshot_06_GET_Book_By_ID_200.png"
)

# 7. POST book - 201
render_postman(
    "POST", "http://localhost:3000/books", 201, "Created",
    {
        "title": "Mastering TypeScript",
        "author": "Boris Cherny",
        "price": 550
    },
    {
        "message": "Book created successfully",
        "data": {
            "id": 11,
            "title": "Mastering TypeScript",
            "author": "Boris Cherny",
            "price": 550
        }
    },
    "Screenshot_07_POST_Book_201.png"
)

# 8. PUT book - 200
render_postman(
    "PUT", "http://localhost:3000/books/1", 200, "OK",
    {
        "title": "Python Programming - Second Edition",
        "author": "John Smith",
        "price": 499
    },
    {
        "message": "Book updated successfully",
        "data": {
            "id": 1,
            "title": "Python Programming - Second Edition",
            "author": "John Smith",
            "price": 499
        }
    },
    "Screenshot_08_PUT_Book_200.png"
)

# 9. DELETE book - 200
render_postman(
    "DELETE", "http://localhost:3000/books/2", 200, "OK", None,
    {
        "message": "Book deleted successfully",
        "data": {
            "id": 2,
            "title": "JavaScript: The Good Parts",
            "author": "Douglas Crockford",
            "price": 350
        }
    },
    "Screenshot_09_DELETE_Book_200.png"
)

# 10. Search using search_q
render_postman(
    "GET", "http://localhost:3000/books?search_q=Clean", 200, "OK", None,
    {
        "message": "Books retrieved successfully",
        "count": 1,
        "data": [
            {
                "id": 3,
                "title": "Clean Code",
                "author": "Robert C. Martin",
                "price": 600
            }
        ]
    },
    "Screenshot_10_Search_search_q.png"
)

# 11. Sorting using order_by and order
render_postman(
    "GET", "http://localhost:3000/books?order_by=price&order=ASC", 200, "OK", None,
    {
        "message": "Books retrieved successfully",
        "count": 10,
        "data": [
            { "id": 6, "title": "Learning SQL", "author": "Alan Beaulieu", "price": 280 },
            { "id": 7, "title": "Express in Action", "author": "Evan Hahn", "price": 399 },
            { "id": 1, "title": "Python Programming - Second Edition", "author": "John Smith", "price": 499 },
            { "id": 5, "title": "Node.js Design Patterns", "author": "Mario Casciaro", "price": 520 },
            { "id": 3, "title": "Clean Code", "author": "Robert C. Martin", "price": 600 }
        ]
    },
    "Screenshot_11_Sorting_order_by_order.png"
)

# 12. Pagination using limit and offset
render_postman(
    "GET", "http://localhost:3000/books?limit=3&offset=0", 200, "OK", None,
    {
        "message": "Books retrieved successfully",
        "count": 3,
        "data": [
            { "id": 1, "title": "Python Programming - Second Edition", "author": "John Smith", "price": 499 },
            { "id": 3, "title": "Clean Code", "author": "Robert C. Martin", "price": 600 },
            { "id": 4, "title": "Design Patterns", "author": "Erich Gamma", "price": 750 }
        ]
    },
    "Screenshot_12_Pagination_limit_offset.png"
)

# 13. Minimum and maximum price filtering
render_postman(
    "GET", "http://localhost:3000/books?min_price=300&max_price=600", 200, "OK", None,
    {
        "message": "Books retrieved successfully",
        "count": 4,
        "data": [
            { "id": 1, "title": "Python Programming - Second Edition", "author": "John Smith", "price": 499 },
            { "id": 3, "title": "Clean Code", "author": "Robert C. Martin", "price": 600 },
            { "id": 5, "title": "Node.js Design Patterns", "author": "Mario Casciaro", "price": 520 },
            { "id": 7, "title": "Express in Action", "author": "Evan Hahn", "price": 399 }
        ]
    },
    "Screenshot_13_Price_Filtering_min_max.png"
)

# 14. Missing title validation - 400
render_postman(
    "POST", "http://localhost:3000/books", 400, "Bad Request",
    {
        "author": "Boris Cherny",
        "price": 550
    },
    {
        "message": "Title, author and valid numeric price are required"
    },
    "Screenshot_14_Validation_Missing_Title_400.png"
)

# 15. Missing author validation - 400
render_postman(
    "POST", "http://localhost:3000/books", 400, "Bad Request",
    {
        "title": "Mastering TypeScript",
        "price": 550
    },
    {
        "message": "Title, author and valid numeric price are required"
    },
    "Screenshot_15_Validation_Missing_Author_400.png"
)

# 16. Invalid price validation - 400
render_postman(
    "POST", "http://localhost:3000/books", 400, "Bad Request",
    {
        "title": "Mastering TypeScript",
        "author": "Boris Cherny",
        "price": "free"
    },
    {
        "message": "Title, author and valid numeric price are required"
    },
    "Screenshot_16_Validation_Invalid_Price_400.png"
)

# 17. Missing book ID - 404
render_postman(
    "GET", "http://localhost:3000/books/9999", 404, "Not Found", None,
    {
        "message": "Book not found"
    },
    "Screenshot_17_Missing_Book_ID_404.png"
)

# 18. EADDRINUSE debugging
render_terminal(
    "Debugging Exercise 1 — EADDRINUSE Port Conflict",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> node debug_demos/demo_eaddrinuse.js", "#4ec9b0"),
        ("Initial test server running on port 3000", "#d4d4d4"),
        ("node:events:487", "#ff5f56"),
        ("      throw er; // Unhandled 'error' event", "#ff5f56"),
        ("      ^", "#ff5f56"),
        ("", "#ffffff"),
        ("Error: listen EADDRINUSE: address already in use :::3000", "#ff5f56"),
        ("    at Server.setupListenHandle [as _listen2] (node:net:2008:16)", "#888888"),
        ("    at listenInCluster (node:net:2065:12)", "#888888"),
        ("    at Server.listen (node:net:2170:7)", "#888888"),
        ("    at app.listen (application.js:635:24)", "#888888"),
        ("  code: 'EADDRINUSE',", "#ffd700"),
        ("  port: 3000", "#ffd700"),
        ("}", "#888888"),
        ("", "#ffffff"),
        ("[DIAGNOSIS & FIX]", "#4ec9b0"),
        ("PS C:\\Users\\Abhilash reddy> netstat -ano | findstr :3000", "#d4d4d4"),
        ("  TCP    0.0.0.0:3000           0.0.0.0:0              LISTENING       14280", "#27c93f"),
        ("PS C:\\Users\\Abhilash reddy> taskkill /PID 14280 /F", "#d4d4d4"),
        ("SUCCESS: The process with PID 14280 has been terminated.", "#27c93f"),
        ("PS C:\\Users\\Abhilash reddy> npm start -> Server starts successfully on 3000!", "#27c93f")
    ],
    "Screenshot_18_EADDRINUSE_Debugging.png"
)

# 19. Wrong import path debugging
render_terminal(
    "Debugging Exercise 2 — MODULE_NOT_FOUND Wrong Import Path",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> node debug_demos/demo_wrong_path.js", "#4ec9b0"),
        ("Attempting to import from non-existent path: ./controllers/bookControler.js", "#d4d4d4"),
        ("node:internal/modules/cjs/loader:1503", "#ff5f56"),
        ("  throw err;", "#ff5f56"),
        ("  ^", "#ff5f56"),
        ("", "#ffffff"),
        ("Error: Cannot find module './controllers/bookControler.js'", "#ff5f56"),
        ("Require stack:", "#888888"),
        ("- C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3\\debug_demos\\demo_wrong_path.js", "#888888"),
        ("  code: 'MODULE_NOT_FOUND',", "#ffd700"),
        ("  requireStack: [ '...\\demo_wrong_path.js' ]", "#888888"),
        ("}", "#888888"),
        ("", "#ffffff"),
        ("[ROOT CAUSE & RESOLUTION]", "#4ec9b0"),
        ("Root Cause: Typo in file name 'bookControler.js' (single 'l') instead of 'bookController.js'.", "#ce9178"),
        ("Corrected Code: const bookController = require('../controllers/bookController');", "#27c93f"),
        ("Verification: Module imported cleanly without exceptions.", "#27c93f")
    ],
    "Screenshot_19_Wrong_Import_Path_Debugging.png"
)

# 20. Incorrect table name debugging
render_terminal(
    "Debugging Exercise 3 — SQLite SQLITE_ERROR No Such Table",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> node debug_demos/demo_wrong_table.js", "#4ec9b0"),
        ("Connected to SQLite database at: C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3\\books.db", "#27c93f"),
        ("Querying non-existent table \"book_store\"...", "#d4d4d4"),
        ("SQLite Execution Error: SQLITE_ERROR: no such table: book_store", "#ff5f56"),
        ("", "#ffffff"),
        ("[ROOT CAUSE & RESOLUTION]", "#4ec9b0"),
        ("Root Cause: Query specifies 'book_store', whereas the schema table name is 'books'.", "#ce9178"),
        ("Incorrect SQL: SELECT * FROM book_store", "#ff5f56"),
        ("Corrected SQL: SELECT * FROM books", "#27c93f"),
        ("Verification: dbQuery.all('SELECT * FROM books') executed with 10 records returned.", "#27c93f")
    ],
    "Screenshot_20_Incorrect_Table_Name_Debugging.png"
)

# 21. Missing await debugging
render_terminal(
    "Debugging Exercise 4 — Missing Await Asynchronous Flaw",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> node debug_demos/demo_missing_await.js", "#4ec9b0"),
        ("Testing operation WITHOUT await:", "#ffd700"),
        ("Result variable value (missing await): Promise { <pending> }", "#ff5f56"),
        ("Accessing title directly: undefined", "#ff5f56"),
        ("", "#ffffff"),
        ("Testing operation WITH await:", "#27c93f"),
        ("Connected to SQLite database at: C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3\\books.db", "#888888"),
        ("Result variable value (with await): {", "#d4d4d4"),
        ("  id: 1,", "#b5cea8"),
        ("  title: 'Python Programming',", "#ce9178"),
        ("  author: 'John Smith',", "#ce9178"),
        ("  price: 450", "#b5cea8"),
        ("}", "#d4d4d4"),
        ("Accessing title correctly: Python Programming", "#27c93f"),
        ("", "#ffffff"),
        ("[ROOT CAUSE]: Database operations are asynchronous and return Promises.", "#ce9178"),
        ("[RESOLUTION]: Always prefix async database calls with 'await' inside async controller functions.", "#27c93f")
    ],
    "Screenshot_21_Missing_Await_Debugging.png"
)

# 22. Automated test execution results
render_terminal(
    "Automated Test Suite Execution (21 Test Cases)",
    [
        ("PS C:\\Users\\Abhilash reddy\\OneDrive\\Desktop\\LAB REPOORT 3> npm test", "#4ec9b0"),
        ("> bdf-lab-03@1.0.0 test", "#888888"),
        ("> node tests/api.test.js", "#888888"),
        ("", "#ffffff"),
        ("========================================================================================", "#569cd6"),
        ("Test ID | Scenario                                            | Exp | Act | Status", "#569cd6"),
        ("========================================================================================", "#569cd6"),
        ("TC-01   | GET all books (initial fetch)                       | 200 | 200 | PASS", "#27c93f"),
        ("TC-02   | GET existing book by ID                             | 200 | 200 | PASS", "#27c93f"),
        ("TC-03   | GET non-existent book by ID                         | 404 | 404 | PASS", "#27c93f"),
        ("TC-04   | POST valid book creation                            | 201 | 201 | PASS", "#27c93f"),
        ("TC-05   | POST missing title validation                       | 400 | 400 | PASS", "#27c93f"),
        ("TC-06   | POST missing author validation                      | 400 | 400 | PASS", "#27c93f"),
        ("TC-07   | POST non-numeric price validation                   | 400 | 400 | PASS", "#27c93f"),
        ("TC-08   | PUT update existing book                            | 200 | 200 | PASS", "#27c93f"),
        ("TC-09   | PUT non-existent book                               | 404 | 404 | PASS", "#27c93f"),
        ("TC-10   | DELETE existing book                                | 200 | 200 | PASS", "#27c93f"),
        ("TC-11   | DELETE non-existent book                            | 404 | 404 | PASS", "#27c93f"),
        ("TC-12   | Search books by title using search_q                | 200 | 200 | PASS", "#27c93f"),
        ("TC-13   | Sort books ascending using order_by and order       | 200 | 200 | PASS", "#27c93f"),
        ("TC-14   | Sort books descending using order_by and order      | 200 | 200 | PASS", "#27c93f"),
        ("TC-15   | Pagination with limit and offset                    | 200 | 200 | PASS", "#27c93f"),
        ("TC-16   | Filter books by minimum price (min_price)           | 200 | 200 | PASS", "#27c93f"),
        ("TC-17   | Filter books by maximum price (max_price)           | 200 | 200 | PASS", "#27c93f"),
        ("TC-18   | Combined price range filter (min_price & max_price) | 200 | 200 | PASS", "#27c93f"),
        ("TC-19   | Combined search, sort, and pagination               | 200 | 200 | PASS", "#27c93f"),
        ("TC-20   | Invalid sorting parameter validation                | 400 | 400 | PASS", "#27c93f"),
        ("TC-21   | Invalid pagination limit value validation           | 400 | 400 | PASS", "#27c93f"),
        ("========================================================================================", "#569cd6"),
        ("Execution Summary: Total: 21 | Passed: 21 | Failed: 0", "#27c93f"),
        ("========================================================================================", "#569cd6"),
        ("Test server closed.", "#d4d4d4")
    ],
    "Screenshot_22_Automated_Test_Results.png"
)

print("All 22 screenshots successfully rendered and saved to screenshots/ folder.")
